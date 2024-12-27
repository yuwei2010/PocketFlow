---
layout: default
title: "Home"
---

# Mini LLM Flow

A 100-line minimalist LLM framework for agents, task decomposition, RAG, etc.

![Alt text](/docs/assets/minillmflow.jpg)

## Core Abstraction

We model the LLM workflow as a **Nested Flow**:

- Each **Node** handles a simple LLM task (e.g., text summarization, structure extraction, or question answering).
- Nodes are chained together to form a **Flow** for more complex tasks. One Node can be chained to multiple Nodes based on **Actions**, e.g., for agentic steps.
- A Flow can be treated as a Node for **Nested Flows**.
- Both Nodes and Flows can be **Batched** for data-intensive tasks (e.g., processing one file at a time in a directory of files).
- Nodes and Flows can be **Async**, e.g., for user feedback before proceeding.

- [Node](./node.md)
- [Flow](./flow.md)
- [Communication](./communication.md)
- [Batch](./batch.md)
- [Async](./async.md)

## Paradigm Implementation

- Task Decomposition
- Agent
- Map Reduce
- RAG
- Structured Output

## Example Use Cases

TODO
