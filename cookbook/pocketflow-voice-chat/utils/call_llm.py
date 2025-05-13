import os
from openai import OpenAI

def call_llm(prompt, history=None):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your-api-key"))

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
    print("Testing LLM call...")
    
    response = call_llm("Tell me a short joke")
    print(f"LLM (Simple Joke): {response}")

    chat_history = [
        {"role": "user", "content": "What is the capital of France?"},
        {"role": "assistant", "content": "The capital of France is Paris."}
    ]
    follow_up_prompt = "And what is a famous landmark there?"
    response_with_history = call_llm(follow_up_prompt, history=chat_history)
    print(f"LLM (Follow-up with History): {response_with_history}") 