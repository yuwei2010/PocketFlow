import asyncio
import json
from pocketflow import Node
from utils.stream_llm import stream_llm

class StreamingChatNode(Node):
    """
    Single node that processes user message and streams LLM response via WebSocket
    """
    def prep(self, shared):
        user_message = shared.get("user_message", "")
        conversation_history = shared.get("conversation_history", [])
        websocket = shared.get("websocket")
        
        # Build messages for OpenAI format
        messages = []
        
        # Add system message
        messages.append({
            "role": "system", 
            "content": "You are a helpful AI assistant. Please respond naturally and helpfully to user queries."
        })
        
        # Add conversation history (keep last 10 messages)
        for msg in conversation_history[-10:]:
            messages.append(msg)
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        return messages, websocket, user_message
    
    def exec(self, prep_res):
        messages, websocket, user_message = prep_res
        
        # Get streaming response from LLM
        response_chunks = stream_llm(messages)
        
        return response_chunks, websocket, user_message
    
    async def stream_response(self, chunks, websocket):
        """
        Stream LLM response chunks to WebSocket
        """
        full_response = ""
        
        try:
            # Send start indicator
            await websocket.send_text(json.dumps({"type": "start", "content": ""}))
            
            # Stream each chunk
            for chunk_content in chunks:
                full_response += chunk_content
                
                # Send chunk via WebSocket
                await websocket.send_text(json.dumps({
                    "type": "chunk",
                    "content": chunk_content
                }))
                
                # Add small delay to simulate real streaming
                await asyncio.sleep(0.05)
            
            # Send end indicator
            await websocket.send_text(json.dumps({"type": "end", "content": ""}))
            
        except Exception as e:
            await websocket.send_text(json.dumps({
                "type": "error",
                "content": f"Streaming error: {str(e)}"
            }))
            print(f"Streaming error: {e}")
        
        return full_response
    
    def post(self, shared, prep_res, exec_res):
        chunks, websocket, user_message = exec_res
        
        # Store the chunks and websocket for async processing
        shared["response_chunks"] = chunks
        shared["websocket"] = websocket
        
        # Add user message to conversation history
        shared["conversation_history"].append({
            "role": "user",
            "content": user_message
        })
        
        return "stream" 