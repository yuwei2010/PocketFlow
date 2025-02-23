<h1 align="center">Pocket Flow - LLM Framework in 100 Lines</h1>



![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://the-pocket.github.io/PocketFlow/)

<div align="center">
  <img src="./assets/minillmflow.jpg" width="400"/>
</div>

<br>

A [100-line](pocketflow/__init__.py) minimalist LLM framework for ([Multi-](https://the-pocket.github.io/PocketFlow/multi_agent.html))[Agents](https://the-pocket.github.io/PocketFlow/agent.html), [Prompt Chaining](https://the-pocket.github.io/PocketFlow/decomp.html), [RAG](https://the-pocket.github.io/PocketFlow/rag.html), etc.

- Install via  ```pip install pocketflow```, or just copy the [source code](pocketflow/__init__.py) (only 100 lines)

- If the 100 lines are terse, check out a [friendlier intro](https://chatgpt.com/share/678564bd-1ba4-8000-98e4-a6ffe363c1b8)

- Documentation: https://the-pocket.github.io/PocketFlow/

## Why Pocket Flow? Let LLM Agents Build LLM Agents for you!

Pocket Flow is designed to be **the framework used by LLM Agents**: 

- 🧑 Human users only need to specify LLM project requirements

- 🤖 LLM Agents build the LLM project for you, using *Pocket Flow*

To build LLM projects with LLM Agents (Cursor, ChatGPT, Claude, etc.):


  - **[Cursor Rules](https://docs.cursor.com/context/rules-for-ai)**: Copy and paste the [.cursorrule](https://github.com/The-Pocket/PocketFlow/blob/main/assets/.cursorrules) (created from [docs](docs)) into the root of your project.

  - **[ChatGPT Project](https://help.openai.com/en/articles/10169521-using-projects-in-chatgpt)**: Create a project and upload the [docs](docs) to project knowledge
  
  - **[Claude Project](https://www.anthropic.com/news/projects)**: Create a project and upload the [docs](docs) to project knowledge
    
  - **GPT Store**: Try this [GPT assistant](https://chatgpt.com/g/g-677464af36588191b9eba4901946557b-mini-llm-flow-assistant). However, it uses older models and is not good at coding.





## What's Pocket Flow? Graph + Shared Store

The [100 lines](pocketflow/__init__.py) capture what we believe to be the core abstraction of LLM projects: 
 - **Computation Model**: *Graph* that breaks down tasks into multiple nodes, with *branching, recursion and nesting*
 - **Communication Model**: *Shared Store* that all graph nodes can read and write to

<br>
<div align="center">
  <img src="./assets/abstraction.png" width="600"/>
</div>
<br>

From there, it’s easy to implement popular design patterns like ([Multi-](https://the-pocket.github.io/PocketFlow/multi_agent.html))[Agents](https://the-pocket.github.io/PocketFlow/agent.html), [Prompt Chaining](https://the-pocket.github.io/PocketFlow/decomp.html), [RAG](https://the-pocket.github.io/PocketFlow/rag.html), etc.

<br>
<div align="center">
  <img src="./assets/paradigm.png" width="600"/>
</div>
<br>

- To learn about how Pocket Flow works, check out the [documentation](https://the-pocket.github.io/PocketFlow/)
- For an in-depth dive on the design, check out the [essay](https://github.com/The-Pocket/.github/blob/main/profile/pocketflow.md)



