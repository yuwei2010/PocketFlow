import asyncio
import logging
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from flow import create_streaming_chat_flow
from nodes import StreamingChatNode

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PocketFlow Chat Interface", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Store active connections (in production, use Redis or similar)
active_connections: dict = {}

@app.get("/")
async def get_chat_interface():
    return FileResponse("static/index.html")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for chat functionality
    """
    await websocket.accept()
    connection_id = id(websocket)
    
    # Initialize shared store for this connection
    shared_store = {
        "websocket": websocket,
        "user_message": "",
        "conversation_history": []
    }
    
    active_connections[connection_id] = shared_store
    logger.info(f"New WebSocket connection: {connection_id}")
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            logger.info(f"Received message: {data}")
            
            # Parse the message
            try:
                parsed_message = json.loads(data)
                message_type = parsed_message.get("type", "message")
                content = parsed_message.get("content", "")
            except json.JSONDecodeError:
                # If not JSON, treat as plain text message
                message_type = "message"
                content = data
            
            if message_type == "message":
                # Store user message in shared store
                shared_store["user_message"] = content
                
                # Process message through PocketFlow
                try:
                    flow = create_streaming_chat_flow()
                    action = flow.run(shared_store)
                    
                    # Handle streaming if chunks are available
                    if "response_chunks" in shared_store:
                        chunks = shared_store["response_chunks"]
                        chat_node = StreamingChatNode()
                        full_response = await chat_node.stream_response(chunks, websocket)
                        
                        # Add AI response to conversation history
                        shared_store["conversation_history"].append({
                            "role": "assistant",
                            "content": full_response
                        })
                        
                        logger.info(f"Processed message, response length: {len(full_response)}")
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "content": f"Processing error: {str(e)}"
                    }))
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {connection_id}")
        if connection_id in active_connections:
            del active_connections[connection_id]
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        if connection_id in active_connections:
            del active_connections[connection_id]

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting PocketFlow Chat Interface...")
    print("📱 Open http://localhost:8000 in your browser")
    uvicorn.run(app, host="0.0.0.0", port=8000) 