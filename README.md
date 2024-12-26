<h1 align="center">miniLLMFlow</h1>

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Minimalist LLM framework in [100 lines](minillmflow/__init__.py). Express popular LLM paradigms like agents, task decomposition, chain of thought, RAG, and more.

- Install via  ```pip install minillmflow```. Or just copy the [source codes](minillmflow/__init__.py) (it's only 100 lines)
- We  **strongly recommened** using LLMs (e.g., Claude, ChatGPT, Cursor) to build LLM applications with [this prompt](minillmflow/docs/prompt)

## Why miniLLMFlow?

The future of programming will be heavily LLM-assited, and LLMs:

1. **👍 Excel at Feature Implementation**: 
Give proper context/docs, they know how to use APIs, tools, text chunking, prompt wrapping, etc. 
These shouldn't be part of an LLM framework, as they're hard to maintain, update, and optimize.

2. **👎 Suck at Paradigm Design**:
Paradigms like MapReduce, DAG workflows, and recent agents are powerful for reasoning about problems.
However, designing elegant paradigms is challenging, and LLMs tend to write redundant code.

Can we build a framework that: 
(1) removes redunant feature implementations, 
(2) but keep core paradigms for LLMs to program against?

Turns out that we just need 100 lines of codes.

<div align="center">
  <img src="./docs/minillmflow.jpg" width="400"/>
</div>

