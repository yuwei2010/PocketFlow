---
layout: default
title: "Design Guidance"
parent: "Apps"
nav_order: 1
---

# LLM System Design Guidance


## Example LLM Project File Structure

```
my_project/
├── main.py
├── flow.py
├── utils/
│   ├── __init__.py
│   ├── call_llm.py
│   └── search_web.py
├── tests/
│   ├── __init__.py
│   ├── test_flow.py
│   └── test_nodes.py
├── requirements.txt
└── docs/
    └── design.md
```


### `docs/`

Store the documentation of the project.

It should include a `design.md` file, which describes 
- Project requirements
- Required utility functions
- High-level flow with a mermaid diagram
- Shared memory data structure
- For each node, discuss
  - Node purpose and design (e.g., should it be a batch or async node?)
  - How the data shall be read (for `prep`) and written (for `post`)
  - How the data shall be processed (for `exec`)

### `utils/`

Houses functions for external API calls (e.g., LLMs, web searches, etc.). 

It’s recommended to dedicate one Python file per API call, with names like `call_llm.py` or `search_web.py`. Each file should include:

- The function to call the API
- A main function to run that API call

For instance, here’s a simplified `call_llm.py` example:

```python
from openai import OpenAI

def call_llm(prompt):
    client = OpenAI(api_key="YOUR_API_KEY_HERE")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def main():
    prompt = "Hello, how are you?"
    print(call_llm(prompt))

if __name__ == "__main__":
    main()
```

### `main.py`

Serves as the project’s entry point.

### `flow.py`

Implements the application’s flow, starting with node followed by the flow structure.


### `tests/`

Optionally contains all tests. Use `pytest` for testing flows, nodes, and utility functions.
For example, `test_call_llm.py` might look like:

```python
from utils.call_llm import call_llm

def test_call_llm():
    prompt = "Hello, how are you?"
    assert call_llm(prompt) is not None
```

## System Design Steps:

1. **Understand Requirements**  
   - Clarify application objectives.
   - Determine and implement the necessary utility functions (e.g., for LLMs, web searches, file handling).

2. **High-Level Flow Design**  
   - Design the flow on how to use the utility functions to achieve the objectives.
   - Identify possible branching for *Node Action* and data-heavy steps for *Batch*.

3. **Shared Memory Structure**  
   - For small apps, in-memory data is sufficient.  
   - For larger or persistent needs, use a database.  
   - Define data schemas or structures and how states are stored or updated.

4. **Implementation**  
   - Start with minimal, straightforward code (e.g., avoid heavy type checking initially).
   - For each node, specify data access (for `prep` and `post`) and data processing (for `exec`).

5. **Optimization**  
   - *Prompt Engineering:* Provide clear instructions and examples to reduce ambiguity.  
   - *Task Decomposition:* Break complex tasks into manageable steps.

6. **Reliability**  
   - *Structured Output:* Verify outputs match the desired format, and increase `max_retries`.
   - *Test Cases:* Create tests for parts of the flow with clear inputs/outputs.  
   - *Self-Evaluation:* For unclear areas, add another Node for LLMs to review the results.
