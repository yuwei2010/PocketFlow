---
layout: default
title: "Batch"
nav_order: 6
---

# Batch

**Batch** functionality in Mini LLM Flow makes it easier to handle a **list** of items in one Node or **rerun** a Flow multiple times. This is particularly useful for:

- **Chunk-based processing** (e.g., summarizing large texts in parts).  
- **Multi-file** processing.  
- **Iterating** over lists of parameters (e.g., user queries, documents, or URLs).

## 1. BatchNode

A **BatchNode** extends `Node` but changes how `prep()` and `exec()` behave:

- **`prep(shared)`**: Should return an **iterable** (list, generator, etc.) of items. 
- **`exec(shared, item)`**: Is called **once per item** in that iterable. 
- **`post(shared, prep_res, exec_res_list)`**: Receives a **list** of results from all the `exec()` calls. You can combine or store them.

### Example: Map Summaries

```python
class MapSummaries(BatchNode):
    def prep(self, shared):
        # Suppose we have a big file; we want to chunk it
        content = shared["data"].get("large_text.txt", "")
        chunk_size = 10000
        chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
        # Return this list. The exec() method will be called once per chunk
        return chunks

    def exec(self, shared, chunk):
        prompt = f"Summarize this chunk in 10 words: {chunk}"
        summary = call_llm(prompt)
        return summary

    def post(self, shared, prep_res, exec_res_list):
        # prep_res is the list of chunks
        # exec_res_list is the list of summaries from each chunk
        combined = "\n".join(exec_res_list)
        shared["summary"]["large_text.txt"] = combined
        return "default"
```

**Flow** usage:
```python
map_summaries = MapSummaries()
flow = Flow(start=map_summaries)
flow.run(shared)
```

- After `prep()` returns multiple chunks, `exec()` is called for each chunk. 
- The aggregated `exec_res_list` is passed to `post()`, where you can do final processing.

### Key Differences from a Normal Node

1. **`exec()`** is called once per item returned by `prep()`.  
2. The final **output** of `exec()` calls is collected into a list and given to `post()`.  
3. `post()` still returns an **action**—just like a regular Node.

---

## 2. BatchFlow

A **BatchFlow** runs a **Flow** multiple times, each time with a different set of `params`. You can think of it as a loop that replays the Flow for each parameter set.

### Example: Summarize Many Files

```python
class SummarizeAllFiles(BatchFlow):
    def prep(self, shared):
        # Return a list of parameter dicts (one per file)
        filenames = list(shared["data"].keys())  # e.g., ["file1.txt", "file2.txt", ...]
        params_list = [{"filename": fn} for fn in filenames]
        return params_list

    # No custom exec() or post(), so we rely on BatchFlow’s default
```

Then define a **Flow** that handles **one** file. Suppose we have `Flow(start=summarize_file)`.  

```python
# Example "per-file" flow (just one node):
summarize_file = SummarizeFile()

# Or possibly something more elaborate:
# load_file >> summarize >> reduce etc.

# Then we wrap it into a BatchFlow:
summarize_all_files = SummarizeAllFiles(start=summarize_file)

# Running it:
summarize_all_files.run(shared)
```

**Under the hood**:
1. `prep(shared)` in `SummarizeAllFiles` returns a list of param dicts, e.g., `[{filename: "file1.txt"}, {filename: "file2.txt"}, ...]`.
2. The BatchFlow **iterates** over these param dicts. For each one, it sets the params on the sub-Flow (in this case, `summarize_file` or a bigger flow) and calls `flow.run(shared)`.
3. Once done, you have run the same Flow for each item.

### Nested or Multi-level Batches

You could nest a BatchFlow inside another BatchFlow. For instance, if you wanted to:

- Outer batch: iterate over directories (Flow that enumerates files in each directory).  
- Inner batch: summarize each file in that directory.

This can be done by making the **outer** BatchFlow’s `exec()` return a list of files, which triggers the **inner** BatchFlow each time. For most simpler use cases, a single BatchFlow is enough.

---

## 3. Best Practices & Tips

1. **Plan your Input**: For a BatchNode, design `prep()` to yield only the minimal necessary data (e.g., text chunks).  
2. **Aggregating Results**: `post()` is the place to combine partial results from `exec_res_list`.  
3. **Large Batches**: If you have **thousands of items**, consider processing in chunks (e.g., yield 100 items at a time) or using an **Async** approach for concurrency.  
4. **Hierarchy**:
   - **BatchNode** is good for a single-step repeated operation (e.g., chunk-based summarization).
   - **BatchFlow** is good if you have a **multi-step** process you want to repeat for a list of parameters.

---

## 4. Putting It All Together

```python
# We'll combine the ideas:
class MapSummaries(BatchNode):
    def prep(self, shared):
        content = shared["data"].get("bigfile.txt", "")
        chunk_size = 10000
        return [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]

    def exec(self, shared, chunk):
        return call_llm(f"Summarize chunk: {chunk}")

    def post(self, shared, prep_res, exec_res_list):
        combined = "\n".join(exec_res_list)
        shared["summary"]["bigfile.txt"] = combined
        return "default"

map_summaries_node = MapSummaries()
map_flow = Flow(start=map_summaries_node)

# If we want to do the above for multiple big files in shared['data']:
class SummarizeAllFiles(BatchFlow):
    def prep(self, shared):
        # Generate param dicts, each specifying a file
        return [{"filename": fn} for fn in shared["data"]]

# But to handle chunking inside the Flow, we might do:
# 1) A node that sets a param "filename" in a shared place 
# 2) Or combine logic differently.

# For now, let's just show usage:
summarize_all = SummarizeAllFiles(start=map_flow)
summarize_all.run(shared)
```

In this snippet:

- `MapSummaries` is a `BatchNode` that chunk-summarizes one file.  
- `map_flow` is a `Flow` with that single BatchNode.  
- `SummarizeAllFiles` is a `BatchFlow` that runs `map_flow` for every file in `shared["data"]`.

**Result**: Each file is chunked by `MapSummaries`, and you get a summary for each.

---

## Summary

- **BatchNode**: Single-step repetition. `prep()` returns a list, `exec()` is called once per item, `post()` aggregates results.  
- **BatchFlow**: Repeatedly runs a Flow with different params. Great for multi-step or nested processes.  

By mixing these two patterns, you can easily handle **large data** or **multiple inputs** in a streamlined, scalable way. 
