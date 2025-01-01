---
layout: default
title: "Node"
parent: "Core Abstraction"
nav_order: 1
---

# Node

A **Node** is the smallest building block of Mini LLM Flow. Each Node has 3 steps:

1. **`prep(shared)`**  
   - Reads and preprocesses data from the `shared` store for LLMs.
   - Examples: query DB, read files, or serialize data into a string.
   - Returns `prep_res`, which will be passed to both `exec()` and `post()`.

2. **`exec(prep_res)`**  
   - The main execution step where the LLM is called.
   - Optionally has built-in retry and error handling (below).
   - ⚠️ If retry enabled, ensure implementation is idempotent.
   - Returns `exec_res`, which is passed to `post()`.

3. **`post(shared, prep_res, exec_res)`**  
   - Writes results back to the `shared` store or decides the next action.  
   - Examples: finalize outputs, trigger next steps, or log results.
   - Returns a **string** to specify the next action (`"default"` if nothing or `None` is returned).

All 3 steps are optional. For example, you might only need to run the Prep without calling the LLM.

## Fault Tolerance & Retries

Nodes in Mini LLM Flow can **retry** execution if `exec()` raises an exception. You control this via a `max_retries` parameter when you create the Node. By default, `max_retries = 1` (meaning no retry).

```python 
my_node = SummarizeFile(max_retries=3)
```

When an exception occurs in `exec()`, the Node automatically retries until:

- It either succeeds, or
- The Node has retried `max_retries - 1` times already and fails on the last attempt.

If you want to **gracefully handle** the error rather than raising it, you can override:

```python 
def exec_fallback(self, shared, prep_res, exc):
    raise exc
```

By default, it just re-raises `exc`. But you can return a fallback result instead. 
That fallback result becomes the `exec_res` passed to `post()`.

## Example

```python 
class SummarizeFile(Node):
    def prep(self, shared):
        filename = self.params["filename"]
        return shared["data"][filename]

    def exec(self, prep_res):
        if not prep_res:
            raise ValueError("Empty file content!")
        prompt = f"Summarize this text in 10 words: {prep_res}"
        summary = call_llm(prompt)  # might fail
        return summary

    def exec_fallback(self, shared, prep_res, exc):
        # Provide a simple fallback instead of crashing
        return "There was an error processing your request."

    def post(self, shared, prep_res, exec_res):
        filename = self.params["filename"]
        shared["summary"][filename] = exec_res
        # Return "default" by not returning anything

summarize_node = SummarizeFile(max_retries=3)

# Run the node standalone for testing (calls prep->exec->post).
# If exec() fails, it retries up to 3 times before calling exec_fallback().
summarize_node.set_params({"filename": "test_file.txt"})
action_result = summarize_node.run(shared)

print("Action returned:", action_result)  # Usually "default"
print("Summary stored:", shared["summary"].get("test_file.txt"))
```  

