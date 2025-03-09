
<div align="center">
  <img src="./assets/title.png" width="600"/>
</div>


![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://the-pocket.github.io/PocketFlow/)
 <a href="https://discord.gg/hUHHE9Sa6T">
    <img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat">
</a>

Pocket Flow is a [100-line](pocketflow/__init__.py) minimalist LLM framework

- **Expressive**: Everything you love from larger frameworks—([Multi-](https://the-pocket.github.io/PocketFlow/design_pattern/multi_agent.html))[Agents](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html), [Workflow](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html), [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html), and more.
  
- **Lightweight**: Just the core graph abstraction in 100 lines. Zero bloat, zero dependencies, zero vendor lock-in.
  
- **Principled**: Built with modularity and clear separation of concerns at its heart for maintainable codes.

- **AI-Friendly**: Intuitive enough for AI agents (e.g., Cursor AI) to assist humans in [Vibe Coding](https://x.com/karpathy/status/1886192184808149383).
  
- To install, ```pip install pocketflow```or just copy the [source code](pocketflow/__init__.py) (only 100 lines).
  
- To learn more, check out the [documentation](https://the-pocket.github.io/PocketFlow/). For an in-depth design dive, read the [essay](https://github.com/The-Pocket/.github/blob/main/profile/pocketflow.md).
  
- 🎉 We now have a [discord](https://discord.gg/hUHHE9Sa6T)


## What can Pocket Flow build?

✨ Below are examples of LLM Apps:

<div align="center">
  
| Formal App Name  | Informal One-Liner |Difficulty    |  Learning Objectives  |
| :------------- | :-------------  | :------------- | :--------------------- |
| [Ask AI Paul Graham](https://github.com/The-Pocket/Tutorial-YC-Partner)  | Ask AI Paul Graham, in case you don't get in | ★★☆ <br> *Medium*   | [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html) <br> [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) <br> [Text-to-Speech](https://the-pocket.github.io/PocketFlow/utility_function/text_to_speech.html) |
| [Youtube Summarizer](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple)  | Explain YouTube Videos to you like you're 5 | ★☆☆ <br> *Beginner*   | [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) | 
| [Cold Opener Generator](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization)  | Instant icebreakers that turn cold leads hot | ★☆☆ <br> *Beginner*   | [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) <br> [Web Search](https://the-pocket.github.io/PocketFlow/utility_function/websearch.html) | 

</div>

- Want to learn how I vibe code these LLM Apps? Check out [my YouTube](https://www.youtube.com/@ZacharyLLM?sub_confirmation=1)
- Want to create your own Python project? Start with  [this template](https://github.com/The-Pocket/PocketFlow-Template-Python)

## Why Pocket Flow?

For **[Vibe Coding](https://x.com/karpathy/status/1886192184808149383)**, the fastest development paradigmn!

- 🧑 Human **describe LLM App requirements** in a design doc.
- 🤖 The agent (like Cursor AI) **implements App** your code automatically.

<br>
<div align="center">
  <a href="https://youtu.be/Cf38Bi8U0Js" target="_blank">
    <img src="./assets/tutorial.png" width="500" alt="IMAGE ALT TEXT" style="cursor: pointer;">
  </a>
</div>
<br>


Compare to other frameworks, Pocket Flow is <i>purpose-built for LLM Agents</i>

1. **🫠 LangChain-like frameworks** overwhelm Cursor AI with *complex* abstractions, *deprecated* functions and *irritating* dependency issues.
   
3. 😐  **Without a framework**, code is *ad hoc*—suitable only for immediate tasks, *not modular or maintainable*.
   
5. **🥰 With Pocket Flow**: (1) Minimal and expressive—easy for Cursor AI to pick up. (2) *Nodes and Flows* keep everything *modular*. (3) A *Shared Store* decouples your data structure from compute logic.

In short, the **100 lines** ensures LLM Agents follows *solid coding practices* without sacrificing *simplicity* or *flexibility*. 




## How does Pocket Flow work?

The [100 lines](pocketflow/__init__.py) capture what we believe to be the core abstraction of LLM frameworks:
 - **Computation**: A *graph* that breaks down tasks into nodes, with *branching, looping,  and nesting*.
 - **Communication**: A *shared store* that all nodes can read and write to.

<br>
<div align="center">
  <img src="./assets/abstraction.png" width="600"/>
</div>
<br>

From there, it’s easy to implement popular design patterns like ([Multi-](https://the-pocket.github.io/PocketFlow/design_pattern/multi_agent.html))[Agents](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html), [Workflow](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html), [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html), etc.

<br>
<div align="center">
  <img src="./assets/design.png" width="600"/>
</div>
<br>


## How to start Vibe Coding with Pocket Flow?

    
- **For quick questions**: Use  the [GPT assistant](https://chatgpt.com/g/g-677464af36588191b9eba4901946557b-pocket-flow-assistant) (note: it uses older models not ideal for coding).
  
- **For one-time LLM task**:  Create a [ChatGPT](https://help.openai.com/en/articles/10169521-using-projects-in-chatgpt) or [Claude](https://www.anthropic.com/news/projects) project; upload the [docs](docs) to project knowledge.
  
- **For LLM App development**: Use [Cursor AI](https://www.cursor.com/).
  
    - If you want to start a new project, check out the [project template](https://github.com/The-Pocket/PocketFlow-Template-Python).
      
    - If you already have a project, copy [.cursorrules](.cursorrules) to your project root as [Cursor Rules](https://docs.cursor.com/context/rules-for-ai).


