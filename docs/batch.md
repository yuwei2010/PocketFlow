---
layout: default
title: "Batch"
parent: "Core Abstraction"
nav_order: 4
---

# Batch

**Batch** makes it easier to handle large inputs in one Node or **rerun** a Flow multiple times. Useful for:
- **Chunk-based** processing (e.g., large texts in parts).  
- **Multi-file** processing.  
- **Iterating** over lists of params (e.g., user queries, documents, URLs).

## 1. BatchNode

A **BatchNode** extends `Node` but changes `prep()` and `exec()`:

- **`prep(shared)`**: returns an **iterable** (list, generator, etc.).
- **`exec(shared, item)`**: called **once** per item in that iterable.
- **`post(shared, prep_res, exec_res_list)`**: receives a **list** of all `exec()` results, can combine or store them, and returns an **Action**.


### Example: Summarize a Large File

```python
class MapSummaries(BatchNode):
    def prep(self, shared):
        # Suppose we have a big file; chunk it
        content = shared["data"].get("large_text.txt", "")
        chunk_size = 10000
        chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
        return chunks

    def exec(self, shared, chunk):
        prompt = f"Summarize this chunk in 10 words: {chunk}"
        summary = call_llm(prompt)
        return summary

    def post(self, shared, prep_res, exec_res_list):
        combined = "\n".join(exec_res_list)
        shared["summary"]["large_text.txt"] = combined
        return "default"

map_summaries = MapSummaries()
flow = Flow(start=map_summaries)
flow.run(shared)
```

---

## 2. BatchFlow

A **BatchFlow** runs a **Flow** multiple times, each with different `params`. Think of it as a loop that replays the Flow for each param set.


### Example: Summarize Many Files

```python
class SummarizeAllFiles(BatchFlow):
    def prep(self, shared):
        filenames = list(shared["data"].keys())  # e.g., ["file1.txt", "file2.txt", ...]
        return [{"filename": fn} for fn in filenames]

# Suppose we have a per-file flow:
# load_file >> summarize >> reduce etc.
summarize_file = SummarizeFile(start=load_file)

summarize_all_files = SummarizeAllFiles(start=summarize_file)
summarize_all_files.run(shared)
```

**Under the hood**:
1. `prep(shared)` returns a list of param dicts (e.g., `[{filename: "file1.txt"}, {filename: "file2.txt"}, ...]`).
2. The BatchFlow **iterates** over them, sets params on the sub-Flow, and calls `flow.run(shared)` each time.
3. The Flow is run repeatedly, once per item.

### Nested or Multi-level Batches

You can nest a BatchFlow in another BatchFlow. For example:
- Outer batch: iterate over directories.
- Inner batch: summarize each file in a directory.

The **outer** BatchFlow’s `exec()` can return a list of directories; the **inner** BatchFlow then processes each file in those dirs.