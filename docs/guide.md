---
layout: default
title: "Design Guidance"
parent: "Apps"
nav_order: 1
---

# LLM System Design Guidance


## System Design Steps

1. **Project Requirements**  
   - Identify the project's core entities, and provide a step-by-step user story.  
   - Define a list of both functional and non-functional requirements.

2. **Utility Functions**  
   - Determine the utility functions on which this project depends (e.g., for LLM calls, web searches, file handling).  
   - Implement these functions and write basic tests to confirm they work correctly.

> After this step, don't jump straight into building an LLM system.  
>
> First, make sure you clearly understand the problem by manually solving it using some example inputs.  
>
> It's always easier to first build a solid intuition about the problem and its solution, then focus on automating the process.  
{: .warning }

3. **Flow Design**  
   - Build a high-level design of the flow of nodes (for example, using a Mermaid diagram) to automate the solution.  
   - For each node in your flow, specify:  
     - **prep**: How data is accessed or retrieved.  
     - **exec**: The specific utility function to use (ideally one function per node).  
     - **post**: How data is updated or persisted.  
   - Identify potential design patterns, such as Batch, Agent, or RAG.

4. **Data Structure**  
   - Decide how you will store and update state (in memory for smaller applications or in a database for larger, persistent needs).  
   - If it isn’t straightforward, define data schemas or models detailing how information is stored, accessed, and updated.  
   - As you finalize your data structure, you may need to refine your flow design.

5. **Implementation**  
   - For each node, implement the **prep**, **exec**, and **post** functions based on the flow design.  
   - Start coding with a simple, direct approach (avoid over-engineering at first).  
   - Add logging throughout the code to facilitate debugging.

6. **Optimization**  
   - **Prompt Engineering**: Use clear, specific instructions with illustrative examples to reduce ambiguity.  
   - **Task Decomposition**: Break large or complex tasks into manageable, logical steps.

7. **Reliability**  
   - **Structured Output**: Ensure outputs conform to the required format. Consider increasing `max_retries` if needed.  
   - **Test Cases**: Develop clear, reproducible tests for each part of the flow.  
   - **Self-Evaluation**: Introduce an additional node (powered by LLMs) to review outputs when results are uncertain.


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
