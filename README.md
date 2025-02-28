
<div align="center">
  <img src="./assets/title.png" width="600"/>
</div>


![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://the-pocket.github.io/PocketFlow/)


A [100-line](pocketflow/__init__.py) minimalist LLM framework for ([Multi-](https://the-pocket.github.io/PocketFlow/multi_agent.html))[Agents](https://the-pocket.github.io/PocketFlow/agent.html), [Workflow](https://the-pocket.github.io/PocketFlow/decomp.html), [RAG](https://the-pocket.github.io/PocketFlow/rag.html), etc.

- Install via  ```pip install pocketflow```, or just copy the [source code](pocketflow/__init__.py) (only 100 lines).
- To learn more, check out the [documentation](https://the-pocket.github.io/PocketFlow/). For an in-depth design dive, read the [essay](https://github.com/The-Pocket/.github/blob/main/profile/pocketflow.md).

## Why Pocket Flow?

For a new development paradigmn: **Build LLM Apps by Chatting with LLM agents, Not Coding**!

- 🧑 Human **describe LLM App requirements** in a design doc.
- 🤖 The agent (like Cursor AI) **implements App** your code automatically.


<br>
<div align="center">
  <a href="https://youtu.be/0Pv5HVoVBYE" target="_blank">
    <img src="./assets/youtube.png" width="500" alt="IMAGE ALT TEXT" style="cursor: pointer;">
  </a>
</div>
<br>


**How does Pocket Flow compare to other frameworks?** Pocket Flow is *purpose-built for LLM Agents* (e.g., Cursor AI):

1. **🫠 LangChain-like frameworks** overwhelm Cursor AI with *complex and outdated* abstractions.
2. 😐  **Without a framework**, code is *ad hoc*—suitable only for immediate tasks, *not modular or maintainable*.
3. **🥰 With Pocket Flow**: (1) Minimal and expressive—easy for Cursor AI to pick up. (2) *Nodes and Flows* keep everything *modular*. (3) A *Shared Store* decouples your data structure from compute logic.

In short, the **100 lines** ensures LLM Agents follows *solid coding practices* without sacrificing *flexibility*. 

**How to set up Pocket Flow for LLM agents?**

  - **For quick questions**: Use  the [GPT assistant](https://chatgpt.com/g/g-677464af36588191b9eba4901946557b-pocket-flow-assistant) (note: it uses older models not ideal for coding).
  - **For one-time LLM task**:  Create a [ChatGPT](https://help.openai.com/en/articles/10169521-using-projects-in-chatgpt) or [Claude](https://www.anthropic.com/news/projects) project; upload the [docs](docs) to project knowledge.
  - **For LLM App development**: Use [Cursor AI](https://www.cursor.com/). Copy [.cursorrules](assets/.cursorrules) nto your project root as **[Cursor Rules](https://docs.cursor.com/context/rules-for-ai)**.


## What can Pocket Flow build?

Below are examples LLM Apps and tutorials

<div align="center">
  
| App Name  | Difficulty    |  Learning Objectives  |
| :------------- | :------------- | :--------------------- |
| [Youtube ELI5 Summarizer](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple)  | ★☆☆  *Beginner*   | [Map Reduce](https://the-pocket.github.io/PocketFlow/mapreduce.html) | 
| [AI Paul Graham](https://github.com/The-Pocket/Tutorial-YC-Partner)  | ★☆☆  *Beginner*   | [RAG](https://the-pocket.github.io/PocketFlow/rag.html) | 

</div>

- Do you want to create your own Python project? Start with  [this template](https://github.com/The-Pocket/PocketFlow-Template-Python)
  

## How does Pocket Flow work?

The [100 lines](pocketflow/__init__.py) capture what we believe to be the core abstraction of LLM frameworks:
 - **Computation**: A *graph* that breaks down tasks into nodes, with *branching, looping,  and nesting*.
 - **Communication**: A *shared store* that all nodes can read and write to.

<br>
<div align="center">
  <img src="./assets/abstraction.png" width="600"/>
</div>
<br>

From there, it’s easy to implement popular design patterns like ([Multi-](https://the-pocket.github.io/PocketFlow/multi_agent.html))[Agents](https://the-pocket.github.io/PocketFlow/agent.html), [Workflow](https://the-pocket.github.io/PocketFlow/decomp.html), [RAG](https://the-pocket.github.io/PocketFlow/rag.html), etc.

<br>
<div align="center">
  <img src="./assets/design.png" width="600"/>
</div>
<br>


