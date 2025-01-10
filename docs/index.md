---
layout: default
title: "Home"
nav_order: 1
---

# Pocket Flow

A [100-line](https://github.com/miniLLMFlow/PocketFlow/blob/main/pocketflow/__init__.py) minimalist LLM framework for *Agents, Task Decomposition, RAG, etc*.


We model the LLM workflow as a **Nested Directed Graph**:
- **Nodes** handle simple (LLM) tasks.
- Nodes connect through **Actions** (labeled edges) for *Agents*.  
- **Flows** orchestrate a directed graph of Nodes for *Task Decomposition*.
- A Flow can be used as a Node (for **Nesting**).
- **Batch** Nodes/Flows for data-intensive tasks.
- **Async** Nodes/Flows allow waits or **Parallel** execution


<div align="center">
  <img src="https://github.com/miniLLMFlow/PocketFlow/raw/main/assets/minillmflow.jpg?raw=true" width="400"/>
</div>



> Have questions? Chat with [AI Assistant](https://chatgpt.com/g/g-677464af36588191b9eba4901946557b-mini-llm-flow-assistant)
{: .note }


## Core Abstraction

- [Node](./node.md)
- [Flow](./flow.md)
- [Communication](./communication.md)
- [Batch](./batch.md)
- [(Advanced) Async](./async.md)
- [(Advanced) Parallel](./parallel.md)

## Low-Level Details

- [LLM Wrapper](./llm.md)
- [Tool](./tool.md)
- [Visualization](./viz.md)
- Chunking

> We do not provide built-in implementations. 
> Example implementations are provided as reference.
{: .warning }


## High-Level Paradigm

- [Structured Output](./structure.md)
- [Task Decomposition](./decomp.md)
- [Map Reduce](./mapreduce.md)
- [RAG](./rag.md)
- [Chat Memory](./memory.md)
- [Agent](./agent.md)
- [(Advanced) Multi-Agents](./multi_agent.md)
- Evaluation

## Example Projects

- [Summarization + QA agent for Paul Graham Essay](./essay.md)
- More coming soon...
