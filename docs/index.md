---
layout: default
title: "Home"
nav_order: 1
---

# Pocket Flow

> If you are an AI assistant reading this document, please read all the non-optional and non-advanced parts. If you are helping a human build an LLM app, please carefully review the [Development Playbook](./guide.md).
{: .warning }

A [100-line](https://github.com/the-pocket/PocketFlow/blob/main/pocketflow/__init__.py) minimalist LLM framework for *Agents, Task Decomposition, RAG, etc*.


We model the LLM workflow as a **Graph + Shared Store**:
- **Nodes** handle simple (LLM) tasks.
- Nodes connect through **Actions** (labeled edges) for *Agents*.  
- **Flows** orchestrate a directed graph of Nodes for *Task Decomposition*.
- Nodes within Flows communicate through a **Shared Store**.
- A Flow can be used as a Node (for **Nesting**).
- **Batch** Nodes/Flows for data-intensive tasks.
- **Async** Nodes/Flows allow waits for asynchronous tasks.


<div align="center">
  <img src="https://github.com/the-pocket/PocketFlow/raw/main/assets/meme.jpg?raw=true" width="400"/>
</div>



> Have questions? Chat with [AI Assistant](https://chatgpt.com/g/g-677464af36588191b9eba4901946557b-mini-llm-flow-assistant)
{: .note }


## Core Abstraction

- [Node](./core_abstraction/node.md)
- [Flow](./core_abstraction/flow.md)
- [Communication](./core_abstraction/communication.md)
- [Batch](./core_abstraction/batch.md)
- [(Advanced) Async](./core_abstraction/async.md)
- [(Advanced) Parallel](./core_abstraction/parallel.md)

## Utility Function

- [LLM Wrapper](./utility_function/llm.md)
- [Tool](./utility_function/tool.md)
- [(Optional) Viz and Debug](./utility_function/viz.md)
- Chunking

> We do not provide built-in utility functions. Example implementations are provided as reference.
{: .warning }


## Design Pattern

- [Structured Output](./design_pattern/structure.md)
- [Workflow](./design_pattern/workflow.md)
- [Map Reduce](./design_pattern/mapreduce.md)
- [RAG](./design_pattern/rag.md)
- [Agent](./design_pattern/agent.md)
- [(Optional) Chat Memory](./design_pattern/memory.md)
- [(Advanced) Multi-Agents](./design_pattern/multi_agent.md)
- Evaluation

## [Develop your LLM Apps](./guide.md)