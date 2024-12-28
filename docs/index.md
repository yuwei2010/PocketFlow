---
layout: default
title: "Home"
nav_order: 1
---

# Mini LLM Flow

A [100-line](https://github.com/zachary62/miniLLMFlow/blob/main/minillmflow/__init__.py) minimalist LLM framework for agents, task decomposition, RAG, etc.

We model the LLM workflow as a **Nested Flow**:
- Each **Node** handles a simple LLM task.
- Nodes are chained together to form a **Flow** for compute-intensive tasks.
- One Node can be chained to multiple Nodes through **Actions** as an agent.
- A Flow can be treated as a Node for **Nested Flows**.
- Both Nodes and Flows can be **Batched** for data-intensive tasks.
- Nodes and Flows can be **Async** for user inputs.

<div align="center">
  <img src="https://github.com/zachary62/miniLLMFlow/blob/main/assets/minillmflow.jpg?raw=true" width="400"/>
</div>

## Preparation

- [LLM Integration](./llm.md)

## Core Abstraction

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
- Evaluation

## Example Use Cases

TODO
