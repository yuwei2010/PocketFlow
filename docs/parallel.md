---
layout: default
title: "(Advanced) Parallel"
parent: "Core Abstraction"
nav_order: 6
---

# (Advanced) Parallel

**Parallel** Nodes and Flows let you run multiple tasks **concurrently**—for example, summarizing multiple texts at once. Unlike a regular **BatchNode**, which processes items sequentially, **AsyncParallelBatchNode** and **AsyncParallelBatchFlow** can fire off tasks in parallel. This can improve performance by overlapping I/O and compute. 

## AsyncParallelBatchNode

Like **AsyncBatchNode**, but uses `prep_async()`, `exec_async()`, and `post_async()` in **parallel**:

```python
class ParallelSummaries(AsyncParallelBatchNode):
    async def prep_async(self, shared):
        # e.g., multiple texts
        return shared["texts"]

    async def exec_async(self, text):
        prompt = f"Summarize: {text}"
        return await call_llm_async(prompt)

    async def post_async(self, shared, prep_res, exec_res_list):
        shared["summary"] = "\n\n".join(exec_res_list)
        return "default"

node = ParallelSummaries()
flow = AsyncFlow(start=node)
```

## AsyncParallelBatchFlow

Parallel version of **BatchFlow**. Each iteration of the sub-flow runs **concurrently** using different parameters:

```python
class SummarizeMultipleFiles(AsyncParallelBatchFlow):
    async def prep_async(self, shared):
        return [{"filename": f} for f in shared["files"]]

sub_flow = AsyncFlow(start=LoadAndSummarizeFile())
parallel_flow = SummarizeMultipleFiles(start=sub_flow)
await parallel_flow.run_async(shared)
```

## Best Practices

- **Ensure Tasks Are Independent**  
  If each item depends on the output of a previous item, **don’t** parallelize. Parallelizing dependent tasks can lead to inconsistencies or race conditions.

- **Beware Rate Limits**  
  Parallel calls can **quickly** trigger rate limits on LLM services. You may need a **throttling** mechanism (e.g., semaphores or sleep intervals) to avoid hitting vendor limits.

- **Consider Single-Node Batch APIs**  
  Some LLMs offer a **batch inference** API where you can send multiple prompts in a single call. This is more complex to implement but can be more efficient than launching many parallel requests. Conceptually, it can look similar to an **AsyncBatchNode** or **BatchNode**, but the underlying call bundles multiple items into **one** request.