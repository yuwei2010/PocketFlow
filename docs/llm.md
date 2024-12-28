---
layout: default
title: "LLM Integration"
nav_order: 3
---

# Call LLM 

For your LLM application, implement a function to call LLMs yourself. 
You can ask an assistant like ChatGPT or Claude to generate an example. 
For instance, asking ChatGPT to "implement a `call_llm` function that takes a prompt and returns the LLM response" gives:

```python
def call_llm(prompt):
    from openai import OpenAI
    # Set the OpenAI API key (use environment variables, etc.)
    client = OpenAI(api_key="YOUR_API_KEY_HERE")
    r = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content

# Example usage
call_llm("How are you?")
```

## Improvements
You can enhance the function as needed. Examples:

1. Handle chat history:

```python
def call_llm(messages):
    from openai import OpenAI
    client = OpenAI(api_key="YOUR_API_KEY_HERE")
    r = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    return r.choices[0].message.content
```

2. Add in-memory caching:

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def call_llm(prompt):
    # Your implementation here
    pass
```

3. Enable logging:

```python
def call_llm(prompt):
    import logging
    logging.info(f"Prompt: {prompt}")
    response = ...
    logging.info(f"Response: {response}")
    return response
```

You can also try libraries like `litellm`

## Why not provide an LLM call function?
I believe it is a bad practice to provide LLM-specific implementations in a general framework:
- LLM APIs change frequently. Hardcoding them makes maintenance difficult.
- You may need flexibility to switch vendors, use fine-tuned models, or deploy local LLMs.
- Custom optimizations like prompt caching, request batching, or response streaming may be required.


