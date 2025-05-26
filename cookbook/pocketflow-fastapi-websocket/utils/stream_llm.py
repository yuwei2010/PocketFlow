import os
from openai import OpenAI

def stream_llm(messages):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your-api-key"))
    
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True,
        temperature=0.7
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content

if __name__ == "__main__":
    messages = [{"role": "user", "content": "Hello!"}]
    for chunk in stream_llm(messages):
        print(chunk, end="", flush=True)
    print() 