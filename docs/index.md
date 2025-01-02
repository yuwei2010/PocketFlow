---
layout: default
title: "Home"
nav_order: 1
---

# Mini LLM Flow

A [100-line](https://github.com/zachary62/miniLLMFlow/blob/main/minillmflow/__init__.py) minimalist LLM framework for *Agents, Task Decomposition, RAG, etc*.


We model the LLM workflow as a **Nested Directed Graph**:
- **Nodes** handle simple (LLM) tasks.
- Nodes connect through **Actions** (labeled edges) for *Agents*.  
- **Flows** orchestrate a directed graph of Nodes for *Task Decomposition*.
- A Flow can be used as a Node (for **Nesting**).
- **Batch** Nodes/Flows for data-intensive tasks.
- **Async** Nodes/Flows allow waits or **Parallel** execution

Have questions? Chat with [AI Assistant](https://chatgpt.com/g/g-677464af36588191b9eba4901946557b-mini-llm-flow-assistant)

<div align="center">
  <img src="https://github.com/zachary62/miniLLMFlow/blob/main/assets/minillmflow.jpg?raw=true" width="400"/>
</div>

## Core Abstraction

- [Node](./node.md)
- [Flow](./flow.md)
- [Communication](./communication.md)
- [Batch](./batch.md)
- [(Advanced) Async](./async.md)
- [(Advanced) Parallel](./parallel.md)

## Low-Level Details

> **Note:** We do not provide implementation.
{: .note }

- [LLM Wrapper](./llm.md)
- [Tool](./tool.md)

## High-Level Paradigm

- [Structured Output](./structure.md)
- Task Decomposition
- Map Reduce
- RAG
- Chat Memory
- Agent
- Multi-Agent
- Evaluation

## Example Projects

- Coming soon ... 
