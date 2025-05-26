from pocketflow import Flow
from nodes import StreamingChatNode

def create_streaming_chat_flow():
    chat_node = StreamingChatNode()
    return Flow(start=chat_node) 