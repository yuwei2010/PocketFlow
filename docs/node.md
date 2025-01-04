---
layout: default
title: "Node"
parent: "Core Abstraction"
nav_order: 1
---

# Node

A **Node** is the smallest building block of Mini LLM Flow. Each Node has 3 steps:

1. `prep(shared)`
   - A reliable step for preprocessing data from the `shared` store. 
   - Examples: *query DB, read files, or serialize data into a string*.
   - Returns `prep_res`, which is used by `exec()` and `post()`.

2. `exec(prep_res)`
   - The **main execution** step, with optional retries and error handling (below).
   - Examples: *primarily for LLMs, but can also for remote APIs*。 
   - ⚠️ If retries enabled, ensure idempotent implementation.
   - Returns `exec_res`, which is passed to `post()`.

3.`post(shared, prep_res, exec_res)`
   - A reliable postprocessing step to write results back to the `shared` store and decide the next Action. 
   - Examples: *update DB, change states, log results, decide next Action*.
   - Returns a **string** specifying the next Action (`"default"` if none).

> All 3 steps are optional. You could run only `prep` if you just need to prepare data without calling the LLM.
{: .note }


## Fault Tolerance & Retries

Nodes in Mini LLM Flow can **retry** execution if `exec()` raises an exception. You control this via two parameters when you create the Node:

- `max_retries` (int): How many times to try running `exec()`. The default is `1`, which means **no** retry.
- `wait` (int): The time to wait (in **seconds**) before each retry attempt. By default, `wait=0` (i.e., no waiting). Increasing this is helpful when you encounter rate-limits or quota errors from your LLM provider and need to back off.

```python 
my_node = SummarizeFile(max_retries=3, wait=10)
```

When an exception occurs in `exec()`, the Node automatically retries until:

- It either succeeds, or
- The Node has retried `max_retries - 1` times already and fails on the last attempt.

### Graceful Fallback

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

