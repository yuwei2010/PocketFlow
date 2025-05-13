import os
from openai import OpenAI

def call_llm(prompt, history=None):
    """
    Calls the OpenAI API to get a response from an LLM.

    Args:
        prompt: The user's current prompt.
        history: A list of previous messages in the conversation, where each message
                 is a dict with "role" and "content" keys. E.g.,
                 [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi there!"}]

    Returns:
        The LLM's response content as a string.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your-api-key")) # Default if not set

    messages = []
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": prompt})

    r = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    return r.choices[0].message.content

if __name__ == "__main__":
    # Ensure you have OPENAI_API_KEY set in your environment for this test to work
    print("Testing LLM call...")
    
    # Test with a simple prompt
    response = call_llm("Tell me a short joke")
    print(f"LLM (Simple Joke): {response}")

    # Test with history
    chat_history = [
        {"role": "user", "content": "What is the capital of France?"},
        {"role": "assistant", "content": "The capital of France is Paris."}
    ]
    follow_up_prompt = "And what is a famous landmark there?"
    response_with_history = call_llm(follow_up_prompt, history=chat_history)
    print(f"LLM (Follow-up with History): {response_with_history}") 