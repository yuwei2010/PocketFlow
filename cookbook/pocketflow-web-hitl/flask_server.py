import asyncio
import uuid
import json
import os
from flask import Flask, request, jsonify, render_template, send_from_directory, Response
from flow import create_feedback_flow

# --- Configuration ---
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# --- State Management (In-Memory - NOT FOR PRODUCTION) ---
tasks = {} # task_id -> {"shared": dict, "status": str, "task_obj": asyncio.Task}

# --- Background Flow Runner ---
async def run_flow_background(task_id, flow, shared):
    """Runs the flow in background, uses queue in shared for SSE."""
    if task_id not in tasks: return # Should not happen
    queue = shared.get("sse_queue")
    if not queue:
        print(f"ERROR: Task {task_id} missing sse_queue in shared store!")
        tasks[task_id]["status"] = "failed"
        # Cannot easily report via SSE if queue is missing
        return

    tasks[task_id]["status"] = "running"
    await queue.put({"status": "running"})
    print(f"Task {task_id}: Flow starting.")

    final_status = "unknown"
    error_message = None
    try:
        await flow.run_async(shared)
        # Check final state
        if shared.get("final_result") is not None:
            final_status = "completed"
        else:
            # If flow ends without setting final_result (e.g., error before ResultNode)
            final_status = "finished_incomplete"
        print(f"Task {task_id}: Flow finished with status: {final_status}")

    except Exception as e:
        final_status = "failed"
        error_message = str(e)
        print(f"Task {task_id}: Flow failed: {e}")
    finally:
        if task_id in tasks:
            tasks[task_id]["status"] = final_status
            final_update = {"status": final_status}
            if final_status == "completed":
                final_update["final_result"] = shared.get("final_result")
            elif error_message:
                final_update["error"] = error_message
            await queue.put(final_update)
        # Signal end of stream
        await queue.put(None)
        print(f"Task {task_id}: Background task ended. Final update put on queue.")

# --- Flask Routes ---
@app.route('/')
async def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
async def static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/submit', methods=['POST'])
async def submit_task():
    if not request.is_json or 'data' not in request.json:
        return jsonify({"error": "Requires JSON with 'data' field"}), 400

    task_id = str(uuid.uuid4())
    feedback_event = asyncio.Event()
    status_queue = asyncio.Queue() # Queue for SSE

    # Initial shared state for the flow
    shared = {
        "task_input": request.json['data'],
        "processed_output": None,
        "feedback": None,
        "review_event": feedback_event,
        "sse_queue": status_queue, # Make queue accessible to nodes
        "final_result": None,
        "task_id": task_id
    }

    flow = create_feedback_flow()

    # Store task state
    tasks[task_id] = {
        "shared": shared,
        "status": "pending",
        # "flow": flow, # Not strictly needed if we don't re-use it
        "task_obj": None # Will hold the background task
    }

    await status_queue.put({"status": "pending", "task_id": task_id})

    # Start flow execution in background
    task_obj = asyncio.create_task(run_flow_background(task_id, flow, shared))
    tasks[task_id]["task_obj"] = task_obj

    print(f"Task {task_id}: Submitted.")
    return jsonify({"message": "Task submitted", "task_id": task_id}), 202

@app.route('/feedback/<task_id>', methods=['POST'])
async def provide_feedback(task_id):
    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404

    task_info = tasks[task_id]
    shared = task_info["shared"]
    queue = shared.get("sse_queue")

    async def report_error(message, status_code=400):
        print(f"Task {task_id}: Feedback error - {message}")
        if queue: await queue.put({"status": "feedback_error", "error": message})
        return jsonify({"error": message}), status_code

    if not request.is_json or 'feedback' not in request.json:
        return await report_error("Requires JSON with 'feedback' field")
    feedback = request.json.get('feedback')
    if feedback not in ["approved", "rejected"]:
        return await report_error("Invalid feedback value")

    review_event = shared.get("review_event")
    if not review_event or review_event.is_set():
        return await report_error("Task not awaiting feedback or feedback already sent", 409)

    print(f"Task {task_id}: Received feedback: {feedback}")
    if queue: await queue.put({"status": "processing_feedback"})
    tasks[task_id]["status"] = "processing_feedback"

    shared["feedback"] = feedback
    review_event.set() # Signal the waiting ReviewNode

    return jsonify({"message": f"Feedback '{feedback}' received"}), 200

# --- SSE Endpoint ---
@app.route('/stream/<task_id>')
async def stream(task_id):
    if task_id not in tasks or "sse_queue" not in tasks[task_id]["shared"]:
        return Response("data: {\"status\": \"error\", \"error\": \"Task or queue not found\"}\n\n",
                        mimetype='text/event-stream', status=404)

    queue = tasks[task_id]["shared"]["sse_queue"]

    async def event_generator():
        print(f"SSE Stream: Client connected for {task_id}")
        try:
            while True:
                update = await queue.get()
                if update is None: # Sentinel for end of stream
                    print(f"SSE Stream: Sentinel received for {task_id}, closing.")
                    yield f"data: {json.dumps({'status': 'stream_closed'})}\n\n"
                    break
                sse_data = json.dumps(update)
                print(f"SSE Stream: Sending for {task_id}: {sse_data}")
                yield f"data: {sse_data}\n\n"
                queue.task_done()
        except asyncio.CancelledError:
            print(f"SSE Stream: Client disconnected for {task_id}.")
        finally:
            print(f"SSE Stream: Generator finished for {task_id}.")
            # Optional: Cleanup task entry after stream ends?
            # if task_id in tasks: del tasks[task_id] # Careful if task state needed elsewhere

    headers = {'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache'}
    return Response(event_generator(), mimetype='text/event-stream', headers=headers)

# --- Main ---
# Use an ASGI server like Hypercorn: `hypercorn server:app`
if __name__ == '__main__':
    print("Run using an ASGI server, e.g., 'hypercorn flask_server:app'")