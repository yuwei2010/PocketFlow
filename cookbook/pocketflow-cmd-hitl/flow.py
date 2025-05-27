from pocketflow import Flow
from .nodes import GetTopicNode, GenerateJokeNode, GetFeedbackNode

def create_joke_flow() -> Flow:
    """Creates and returns the joke generation flow."""
    # Create nodes
    get_topic_node = GetTopicNode()
    generate_joke_node = GenerateJokeNode()
    get_feedback_node = GetFeedbackNode()

    # Connect nodes
    # GetTopicNode -> GenerateJokeNode (default action)
    get_topic_node >> generate_joke_node
    
    # GenerateJokeNode -> GetFeedbackNode (default action)
    generate_joke_node >> get_feedback_node

    # GetFeedbackNode actions:
    # "Approve" -> Ends the flow (no further connection)
    # "Disapprove" -> GenerateJokeNode
    # get_feedback_node.connect_to(generate_joke_node, action="Disapprove")
    get_feedback_node - "Disapprove" >> generate_joke_node # Alternative syntax

    # Create flow starting with the input node
    joke_flow = Flow(start=get_topic_node)
    return joke_flow 