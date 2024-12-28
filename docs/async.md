---
layout: default
title: "Async"
nav_order: 7
---

# Async

**Mini LLM Flow** supports **async/await** paradigms for concurrency or parallel workloads. This is particularly useful for:
- Making **concurrent LLM calls** (e.g., if your LLM client library supports async).
- Handling **network I/O** or **external APIs** in an event loop.
- Minimizing **idle** time while waiting for responses, especially in batch operations.

## 1. AsyncNode

An **AsyncNode** is like a normal `Node`, except `exec()` (and optionally `prep()`) can be declared **async**. You can `await` inside these methods. For example:

```python
class AsyncSummarizeFile(AsyncNode):
    async def prep(self, shared):
        # Possibly do async file reads or small concurrency tasks
        filename = self.params["filename"]
        return shared["data"].get(filename, "")

    async def exec(self, shared, prep_res):
        # Use an async LLM client or other I/O
        if not prep_res:
            raise ValueError("File content is empty (async).")

        prompt = f"Summarize asynchronously: {prep_res}"
        # Suppose call_llm_async is an async function
        summary = await call_llm_async(prompt)
        return summary

    def post(self, shared, prep_res, exec_res):
        # post can remain sync
        filename = self.params["filename"]
        shared["summary"][filename] = exec_res
        return "default"
```

- **`prep(shared)`** can be `async def` if you want to do asynchronous pre-processing.
- **`exec(shared, prep_res)`** is typically the main place for async logic.
- **`post`** can stay sync or be async; it’s optional to mark it `async`.

## 2. AsyncFlow

An **AsyncFlow** is a Flow where nodes can be **AsyncNode**s or normal `Node`s. You run it in an event loop with `await async_flow.run(shared)`.

### Minimal Example

```python
class MyAsyncFlow(AsyncFlow):
    pass  # Usually, you just instantiate AsyncFlow with a start node

# Build your nodes
load_data_node = LoadData()  # normal Node is OK, too
async_summarize = AsyncSummarizeFile()

# Connect them
load_data_node >> async_summarize

my_flow = MyAsyncFlow(start=load_data_node)

# Running the flow (in an async context):
import asyncio

async def main():
    shared = {"data": {}, "summary": {}}
    await my_flow.run(shared)

asyncio.run(main())
```

- If the start node or any subsequent node is an `AsyncNode`, the Flow automatically calls its `prep()`, `exec()`, `post()` as async functions.
- You can mix normal `Node`s and `AsyncNode`s in the same flow. **AsyncFlow** will handle the difference seamlessly.

## 3. BatchAsyncFlow

If you want to run a batch of flows **concurrently**, you can use `BatchAsyncFlow`. Like `BatchFlow`, it generates a list of parameter sets in `prep()`, but each iteration runs the sub-flow asynchronously.

```python
class SummarizeAllFilesAsync(BatchAsyncFlow):
    async def prep(self, shared):
        # Return a list of param dicts (like in BatchFlow),
        # but you can do async logic here if needed.
        filenames = list(shared["data"].keys())
        return [{"filename": fn} for fn in filenames]

# Usage:
# Suppose async_summarize_flow is an AsyncFlow that processes a single file.

all_files_flow = SummarizeAllFilesAsync(start=async_summarize_flow)

# Then in your async context:
await all_files_flow.run(shared)
```

Under the hood:
1. `prep()` returns a list of param sets.  
2. `BatchAsyncFlow` processes each **in sequence** by default, but each iteration is still an async run of the sub-flow.  
3. If you want **true concurrency** (e.g., launch sub-flows in parallel), you can override methods or manage concurrency at a higher level.

## 4. Combining Async with Retries & Fault Tolerance

Just like normal Nodes, an `AsyncNode` can have `max_retries` and a `process_after_fail(...)` method:

```python
class RetryAsyncNode(AsyncNode):
    def __init__(self, max_retries=3):
        super().__init__(max_retries=max_retries)

    async def exec(self, shared, prep_res):
        # Potentially failing async call
        response = await async_api_call(...)
        return response

    def process_after_fail(self, shared, prep_res, exc):
        # Provide fallback response
        return "Unable to complete async call due to error."
```

## 5. Best Practices

1. **Ensure Your LLM Client or I/O Library is Async-Aware**  
   - For truly concurrent calls, your LLM or HTTP client must support async. Otherwise, you gain little from using `AsyncNode`.
2. **Manage Rate Limits**  
   - Parallelizing many calls can hit LLM rate limits. Consider adding semaphores or concurrency checks.
3. **Use `asyncio.gather` If Needed**  
   - If you want multiple async calls in the same node, you can await them concurrently with `asyncio.gather`.
4. **Check Exceptions**  
   - If one call fails, how does it affect your flow? Decide if you want to retry or fallback.

## 6. Summary

- **AsyncNode**: A Node that supports `async def prep()/exec()/post()`.
- **AsyncFlow**: Orchestrates normal + async nodes. Run via `await flow.run(shared)`.
- **BatchAsyncFlow**: Repeats an AsyncFlow for multiple parameter sets, each iteration in an async manner.

By taking advantage of Python’s `asyncio` and the same minimal design, you can scale up your LLM or I/O tasks without blocking, making **Mini LLM Flow** suitable for high-throughput or high-latency scenarios.
