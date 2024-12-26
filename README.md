<h1 align="center">miniLLMFlow</h1>

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Minimalist LLM framework in [100 lines](minillmflow/__init__.py). Express popular paradigms like agents, task decomposition, RAG, and more.

- Install via  ```pip install minillmflow```. Or just copy the [source codes](minillmflow/__init__.py) (it's only 100 lines)
- We  **strongly recommened** using LLMs (e.g., Claude, ChatGPT, Cursor) to develop LLM applications with [this prompt](minillmflow/docs/prompt)

## Why miniLLMFlow?

The future of programming will be heavily LLM-assited, and LLMs:

1. **😀 Shine at Feature Implementation**: 
With proper docs, LLMs can handle APIs, tools, chunking, prompt wrapping, etc. 
These are hard to maintain and optimize, so they don’t belong in the framework.

2. **☹️ Struggle with Paradigm Design**:
Paradigms like MapReduce, task decomposition, and agents are powerful, even for LLMs.
However, designing these elegantly remains challenging for LLMs.

To enable LLMs to develop LLM applications, a framework should
(1) remove redunant feature implementations but
(2) keep core paradigms to build on.
It turns out that such a framework only needs 100 lines of code.

<div align="center">
  <img src="./docs/minillmflow.jpg" width="400"/>
</div>

