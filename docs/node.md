---
layout: default
title: "Node"
---

# Node

A **Node** is the smallest building block of Mini LLM Flow. Each Node has three lifecycle methods:

1. **`prep(shared)`**  
   - Optionally preprocess data before calling your LLM or doing heavy computation.
   - Often used for tasks like reading files, chunking text, or validation.
   - Returns `prep_res`, which will be passed to both `exec()` and `post()`.

2. **`exec(shared, prep_res)`**  
   - The main execution step, typically where you call your LLM or any external APIs.
   - Returns `exec_res`, which is passed to `post()`.

3. **`post(shared, prep_res, exec_res)`**  
   - Optionally perform post-processing, such as writing results back to the `shared` store or deciding the next action.  
   - Often used to finalize outputs, trigger next steps, or log results.  
   - Returns a **string** to specify the next action (`"default"` if nothing or `None` is returned).


## Fault Tolerance & Retries

Nodes in Mini LLM Flow can **retry** execution if `exec()` raises an exception. You control this via a `max_retries` parameter when you create the Node. By default, `max_retries = 1` (meaning no retry).

```
# Example usage:
my_node = SummarizeFile(max_retries=3)
```

When an exception occurs in `exec()`, the Node automatically retries until:

- It either succeeds, **or**
- The Node has retried `max_retries - 1` times already and fails on the last attempt.

If you want to **gracefully handle** the error rather than raising it, you can override:

``  
def process_after_fail(self, shared, prep_res, exc):
    raise exc
``  

By **default**, it just re-raises `exc`. But you can return a fallback result instead. That fallback result becomes the `exec_res` passed to `post()`.

## Minimal Example

``  
class SummarizeFile(Node):
    def prep(self, shared):
        filename = self.params["filename"]
        return shared["data"][filename]

    def exec(self, shared, prep_res):
        if not prep_res:
            raise ValueError("Empty file content!")
        prompt = f"Summarize this text in 10 words: {prep_res}"
        summary = call_llm(prompt)  # might fail
        return summary

    def process_after_fail(self, shared, prep_res, exc):
        # Provide a simple fallback instead of crashing
        return "There was an error processing your request."

    def post(self, shared, prep_res, exec_res):
        filename = self.params["filename"]
        shared["summary"][filename] = exec_res
        # Return "default" by not returning anything
``  

