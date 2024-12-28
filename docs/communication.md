---
layout: default
title: "Communication"
parent: "Core Abstraction"
nav_order: 3
---

# Communication

Nodes and Flows **communicate** in two ways:

1. **Shared Store** – A global data structure (often an in-mem dict) that all nodes can read from and write to. Every Node’s `prep()`, `exec()`, and `post()` methods receive the **same** `shared` store.  
2. **Params** – Each node and Flow has a `params` dict assigned by the **parent Flow**. Params mostly serve as identifiers, letting each node/flow know what task it’s assigned.

If you know memory management, **Shared Store** is like a **heap** shared across function calls, while **Params** is like a **stack** assigned by parent function calls.


### Why Not Message Passing?

**Message passing** can work for simple DAGs (e.g., for data pipelines), but with **nested graphs** (Flows containing Flows, repeated or cyclic calls), routing messages becomes hard to maintain. A shared store keeps the design simpler and easier.

---

## 1. Shared Store

### Overview

A shared store is typically an in-mem dictionary, like:
```python
shared = {"data": {}, "summary": {}, "config": {...}, ...}
```python

It can also contain local file handlers, DB connections, or a combination for persistence.  
We recommend deciding the data structure or DB schema in advance based on your app requirements.

### Example

```python
class LoadData(Node):
    def prep(self, shared):
        # Suppose we read from disk or an API
        shared["data"]["my_file.txt"] = "Some text content"
        return None

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

load_data = LoadData()
summarize = Summarize()
load_data >> summarize
flow = Flow(start=load_data)

shared = {}
flow.run(shared)
```

Here:
- `LoadData` writes to `shared["data"]`.
- `Summarize` reads from the same location.  
No special data-passing—just the same `shared` object.

---

## 2. Params

**Params** let you store **per-Node** or **per-Flow** config that doesn’t need to live in the global store. They are:
- **Immutable** during a Node’s run cycle (i.e., they don’t change mid-`prep`, `exec`, `post`).
- **Set** via `set_params()`.  
  ⚠️ Only set the uppermost Flow params because others will be overwritten by the parent Flow. If you need to set child node params, see [Batch](./batch.md).
- **Cleared** and updated each time a parent Flow calls it.

Typically, **Params** are identifiers (e.g., file name, page number). Use them to fetch the task you assigned or write to a specific part of the shared store.

### Example

```python
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

# 3) Set Node params directly (for testing)
node.set_params({"filename": "doc1.txt"})
node.run(shared)

# 4) Create Flow
flow = Flow(start=node)

# 5) Set Flow params (overwrites node params)
flow.set_params({"filename": "doc2.txt"})
flow.run(shared)  # The node summarizes doc2, not doc1
```

---

## 3. Shared Store vs. Params

Think of the **Shared Store** like a heap and **Params** like a stack.

- **Shared Store**:
  - Public, global.
  - You can design and populate ahead, e.g., for the input to process.
  - Great for data results, large content, or anything multiple nodes need.
  - Keep it tidy—structure it carefully (like a mini schema).

- **Params**:
  - Local, ephemeral.
  - Passed in by parent Flows. You should only set it for the uppermost flow.
  - Perfect for small values like filenames or numeric IDs.
  - Do **not** persist across different nodes and are reset.