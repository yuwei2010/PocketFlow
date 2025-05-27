import os
from openai import OpenAI

def call_llm(prompt: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your-api-key"))
    r = client.chat.completions.create(
        model="gpt-4o", 
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content

if __name__ == "__main__":
    print("Testing real LLM call:")
    joke_prompt = "Tell me a short joke about a programmer."
    print(f"Prompt: {joke_prompt}")
    response = call_llm(joke_prompt)
    print(f"Response: {response}")