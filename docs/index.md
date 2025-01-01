---
layout: default
title: "Home"
nav_order: 1
---

# Mini LLM Flow

A [100-line](https://github.com/zachary62/miniLLMFlow/blob/main/minillmflow/__init__.py) minimalist LLM framework for *Agents, Task Decomposition, RAG, etc*.

<div align="center">
  <img src="https://github.com/zachary62/miniLLMFlow/blob/main/assets/minillmflow.jpg?raw=true" width="400"/>
</div>

## Core Abstraction

We model the LLM workflow as a **Nested Directed Graph**:
- **Nodes** handle simple (LLM) tasks.
- Nodes connect through **Actions** (labeled edges) for *Agents*.  
- **Flows** orchestrate a directed graph of Nodes for *Task Decomposition*.
- A Flow can be used as a Node (for **Nesting**).
- **Batch** Nodes/Flows for data-intensive tasks.
- **Async** Nodes/Flows allow waits or **Parallel** execution

To learn more:
- [Node](./node.md)
- [Flow](./flow.md)
- [Communication](./communication.md)
- [Batch](./batch.md)
- [(Advanced) Async](./async.md)
- [(Advanced) Parallel](./parallel.md)

## LLM Wrapper & Tools

**We DO NOT provide built-in LLM wrappers and tools!**

I believe it is a *bad practice* to provide low-level implementations in a general framework:
- **APIs change frequently.** Hardcoding them makes maintenance a nightmare.
- You may need **flexibility.** E.g., using fine-tunined LLMs or deploying local ones.
- You may need **optimizations.** E.g., prompt caching, request batching, response streaming...

We provide some simple example implementations:
- [LLM Wrapper](./llm.md)
- [Tool](./tool.md)

## Paradigm

Based on the core abstraction, we implement common high-level paradigms:

- [Structured Output](./structure.md)
- Task Decomposition
- RAG
- Chat Memory
- Map Reduce
- Agent
- Multi-Agent
- Evaluation

## Example Projects

- Coming soon ... 
