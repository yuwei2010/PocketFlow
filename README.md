<h1 align="center">Mini LLM Flow</h1>

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A 100-line minimalist LLM framework for agents, task decomposition, RAG, etc.

- Install via  ```pip install minillmflow```, or just copy the [source](minillmflow/__init__.py) (only 100 lines)

- **Pro tip:** Build LLM apps with LLMs assistants (ChatGPT, Claude, etc.) via [this prompt](docs/prompt)

## Why Mini LLM Flow?

In the future, **LLM apps will be developed by LLMs**: users specify requirements, and LLMs design, build, and maintain on their own. Current LLMs:

1. **😀 Shine at Low-level Implementation**: 
With proper docs, LLMs can handle APIs, tools, chunking, prompt wrapping, etc. 
These are hard to maintain and optimize for a general-purpose framework.

2. **☹️ Struggle with High-level Paradigms**:
Paradigms like MapReduce, task decomposition, and agents are powerful for development.
However, designing these elegantly remains challenging for LLMs.

To enable LLMs to develop LLM app, a framework should
(1) remove specialized low-level implementations, and
(2) keep high-level paradigms to program against.
Hence, I built this framework that lets LLMs focus on what matters. It turns out 100 lines is all you need.


<div align="center">
  <img src="./docs/minillmflow.jpg" width="400"/>
</div>

