<h1 align="center">Pocket Flow - LLM Framework in 100 Lines</h1>



![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://the-pocket.github.io/PocketFlow/)

<div align="center">
  <img src="./assets/minillmflow.jpg" width="400"/>
</div>

<br>

A [100-line](pocketflow/__init__.py) minimalist LLM framework for ([Multi-](https://the-pocket.github.io/PocketFlow/multi_agent.html))[Agents](https://the-pocket.github.io/PocketFlow/agent.html), [Prompt Chaining](https://the-pocket.github.io/PocketFlow/decomp.html), [RAG](https://the-pocket.github.io/PocketFlow/rag.html), etc.

- ⚙️ Install via  ```pip install pocketflow```, or just copy the [source code](pocketflow/__init__.py) (only 100 lines)

- 😊 If the 100 lines feel terse and you’d prefer a friendlier intro, [check this out](https://chatgpt.com/share/678564bd-1ba4-8000-98e4-a6ffe363c1b8)

- 📖 Documentation: https://the-pocket.github.io/PocketFlow/

## Why Pocket Flow? Let LLM Agents Build LLM Agents for you!

Pocket Flow is designed to be **the framework used by LLM Agents**: 

- 🧑 Human users specify project requirements and provide high-level guidance

- 🤖 LLM Agents build and maintain LLM projects for you, using *Pocket Flow*

To build LLM projects with LLMs Agents (ChatGPT, Claude, Cursor.ai, etc.):

<details>
  <summary><b>(🫵 Click to expand) Use Claude to build LLM apps</b></summary>

  - Create a [project](https://www.anthropic.com/news/projects) and upload the [docs](docs) to project knowledge

  - Set project custom instructions. For example:
    ```
    1. check "tool.md" and "llm.md" for the required functions.
    2. design the high-level (batch) flow and nodes in artifact using mermaid
    3. design the shared memory structure: define its fields, data structures, and how they will be updated.
    Think out aloud for above first and ask users if your design makes sense.
    4. Finally, implement. Start with simple, minimalistic codes without, for example, typing. Write the codes in artifact.
    ```
  - Ask it to build LLM apps (Sonnet 3.5 strongly recommended)!
    ```
    Help me build a chatbot based on a directory of PDFs.
    ```

    <div align="center">
      <img src="./assets/claude_project.gif"/>
    </div>
</details>

<details>
  <summary><b>(🫵 Click to expand) Use ChatGPT to build LLM apps</b></summary>

  - Try the [GPT assistant](https://chatgpt.com/g/g-677464af36588191b9eba4901946557b-mini-llm-flow-assistant). However, it uses older models, which are good for explaining but not that good at coding.

    <div align="center">
      <img src="./assets/gpt_store.gif"/>
    </div>

  - For stronger coding capabilities, consider sending the [docs](docs) to more advanced models like O1.

      - Paste the docs link (https://github.com/the-pocket/PocketFlow/tree/main/docs) to [Gitingest](https://gitingest.com/).

      - Then, paste the generated contents into your O1 prompt, and ask it to build LLM apps.
   
  
</details>




## What's Pocket Flow? Graph + Shared Store

The [100 lines](pocketflow/__init__.py) capture what what we believe to be the core abstraction of LLM projects: 
 - **Graph** as the *Computation Model* that breaks down tasks into multiple-step LLM chains, with branching, recursion and nesting for agent-like decision-making
 - **Shared Store** as the *Communication Model* that all graph nodes can read and write to

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

- 📖 To learn about how Pocket Flow works, please check out the [documentation](https://the-pocket.github.io/PocketFlow/)
- 🤓 For a more in-depth dive on the design choices, check out the [essay](https://github.com/The-Pocket/.github/blob/main/profile/pocketflow.md)



