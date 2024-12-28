---
layout: default
title: "Communication"
nav_order: 4
---

# Communication

In **Mini LLM Flow**, Nodes and Flows **communicate** with each other in two ways:

1. **Shared Store** – A global data structure (often a Python dict) that every Node can read from and write to.
2. **Params** – Small pieces of metadata or configuration, set on each Node or Flow, typically used to identify items or tweak behavior.

This design avoids complex message-passing or data routing. It also lets you **nest** Flows easily without having to manage multiple channels.

---

## 1. Shared Store

### Overview

A shared store is typically a Python dictionary, like:
`` 
shared = {"data": {}, "summary": {}, "config": { ... }, ...}
``

Every Node’s `prep()`, `exec()`, and `post()` methods receive the **same** `shared` object. This makes it easy to:
- Read data that another Node loaded, such as a text file or database record.
- Write results for later Nodes to consume.
- Maintain consistent state across the entire Flow.

### Example

`` 
class LoadData(Node):
    def prep(self, shared):
        # Suppose we read from disk or an API
        shared["data"]["my_file.txt"] = "Some text content"
        return None

    def exec(self, shared, prep_res):
        # Not doing anything special here
        return None

    def post(self, shared, prep_res, exec_res):
        return "default"

class Summarize(Node):
    def prep(self, shared):
        # We can read what LoadData wrote
        content = shared["data"].get("my_file.txt", "")
        return content

    def exec(self, shared, prep_res):
        prompt = f"Summarize: {prep_res}"
        summary = call_llm(prompt)
        return summary

    def post(self, shared, prep_res, exec_res):
        shared["summary"]["my_file.txt"] = exec_res
        return "default"
``

Here,
- `LoadData` writes to `shared["data"]`.
- `Summarize` reads from the same location.  
No special data-passing code—just the same `shared` object.

### Why Not Message Passing?

**Message-passing** can be great for simple DAGs, but with **nested graphs** (Flows containing Flows, repeated or cyclic calls), routing messages can become complicated. A shared store keeps the design simpler and easier to debug.

---

## 2. Params

**Params** let you store **per-Node** or **per-Flow** configuration that does **not** need to be in the global store. They are:
- **Immutable** during a Node’s run cycle (i.e., don’t change mid-run).
- **Set** via `set_params()`.
- **Cleared** or updated each time you call the Flow or Node again.

Common examples:
- **File names** to process.
- **Model hyperparameters** for an LLM call.
- **API credentials** or specialized flags.

### Example

`` 
# 1) Create a Node that uses params
class SummarizeFile(Node):
    def prep(self, shared):
        # Access the node's param
        filename = self.params["filename"]
        return shared["data"].get(filename, "")

    def exec(self, shared, prep_res):
        prompt = f"Summarize: {prep_res}"
        return call_llm(prompt)

    def post(self, shared, prep_res, exec_res):
        filename = self.params["filename"]
        shared["summary"][filename] = exec_res
        return "default"

# 2) Set params
node = SummarizeFile()
node.set_params({"filename": "doc1.txt"})

# 3) Run
node.run(shared)
``

Because **params** are only for that Node, you don’t pollute the global `shared` with fields that might only matter to one operation.

---

## 3. Shared Store vs. Params

- **Shared Store**: 
  - Public, global. 
  - Great for data results, large content, or anything multiple nodes need.
  - Must be carefully structured (like designing a mini schema).

- **Params**:
  - Local, ephemeral config for a single node or flow execution.
  - Perfect for small values such as filenames or numeric IDs.
  - Does **not** persist across different nodes unless specifically copied into `shared`.

---

## 4. Best Practices

1. **Design a Clear `shared` Schema**  
   - Decide on keys upfront. Example: `shared["data"]` for raw data, `shared["summary"]` for results, etc.

2. **Use Params for Identifiers / Config**  
   - If you need to pass a single ID or filename to a Node, **params** are usually best.

3. **Don’t Overuse the Shared Store**  
   - Keep it tidy. If a piece of data only matters to one Node, consider using `params` or discarding it after usage.

4. **Ensure `shared` Is Accessible**  
   - If you switch from an in-memory dict to a database or file-based approach, the Node code can remain the same as long as your `shared` interface is consistent.

---

## Putting It All Together

`` 
# Suppose you have a flow:
load_data >> summarize_file
my_flow = Flow(start=load_data)

# Example usage:
load_data.set_params({"path": "path/to/data/folder"})  # local param for load_data
summarize_file.set_params({"filename": "my_text.txt"})  # local param for summarize_file

# shared store
shared = {
    "data": {},
    "summary": {}
}

my_flow.run(shared)
# After run, shared["summary"]["my_text.txt"] might have the LLM summary
``

- `load_data` uses its param (`"path"`) to load some data into `shared["data"]`.
- `summarize_file` uses its param (`"filename"`) to pick which file from `shared["data"]` to summarize.
- They share results via `shared["summary"]`.

That’s the **Mini LLM Flow** approach to communication:  
- **A single shared store** to handle large data or results for multiple Nodes.  
- **Per-node params** for minimal configuration and identification.

Use these patterns to build powerful, modular LLM pipelines with minimal overhead.
