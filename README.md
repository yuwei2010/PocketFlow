
<div align="center">
  <img src="./assets/title.png" width="600"/>
</div>


![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://the-pocket.github.io/PocketFlow/)
 <a href="https://discord.gg/hUHHE9Sa6T">
    <img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat">
</a>

Pocket Flow is a [100-line](pocketflow/__init__.py) minimalist LLM framework

- **Lightweight**: Just 100 lines. Zero bloat, zero dependencies, zero vendor lock-in.
  
- **Expressive**: Everything you love from large frameworks—([Multi-](https://the-pocket.github.io/PocketFlow/design_pattern/multi_agent.html))[Agents](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html), [Workflow](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html), [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html), and more.

- **AI-Friendly**: Let AI Agents (e.g., Cursor AI) build Agents—10x productivity boost!

- To install, ```pip install pocketflow```or just copy the [source code](pocketflow/__init__.py) (only 100 lines).
  
- To learn more, check out the [documentation](https://the-pocket.github.io/PocketFlow/). For an in-depth design dive, read the [essay](https://github.com/The-Pocket/.github/blob/main/profile/pocketflow.md).
  
- 🎉 We now have a [discord](https://discord.gg/hUHHE9Sa6T)!

## Why Pocket Flow?

Current LLM frameworks are bloated. You only need 100 lines for LLM Framework!

<div align="center">
  <img src="./assets/meme.jpg" width="400"/>


  |                | **Abstraction**          | **App-Specific Wrappers**                                      | **Vendor-Specific Wrappers**                                    | **Lines**       | **Size**    |
|----------------|:-----------------------------: |:-----------------------------------------------------------:|:------------------------------------------------------------:|:---------------:|:----------------------------:|
| LangChain  | Agent, Chain               | Many <br><sup><sub>(e.g., QA, Summarization)</sub></sup>              | Many <br><sup><sub>(e.g., OpenAI, Pinecone, etc.)</sub></sup>                   | 405K          | +166MB                     |
| LlamaIndex | Agent, Graph      | Native <sup><sub>for RAG <br>(Summarization, KG Indexing)</sub></sup>          | Many <sup><sub>[Optional] <br>(e.g., OpenAI, Pinecone, etc.)</sub></sup>        | 77K <br><sup><sub>(core-only)</sub></sup>   | +189MB <br><sup><sub>(core-only)</sub></sup>         |
| CrewAI     | Agent, Chain            | Many <br><sup><sub>(e.g., FileReadTool, SerperDevTool)</sub></sup>         | Many <br><sup><sub>(e.g., OpenAI, Anthropic, Pinecone, etc.)</sub></sup>        | 18K           | +173MB                     |
| Haystack   | Agent, Graph         | Many <br><sup><sub>(e.g., QA, Summarization)</sub></sup>                   | Many <br><sup><sub>(e.g., OpenAI, Anthropic, Pinecone, etc.)</sub></sup>        | 31K           | +195MB                     |
| SmolAgent   | Agent                      | Some <br><sup><sub>(e.g., CodeAgent, VisitWebTool)</sub></sup>         | Some <br><sup><sub>(e.g., DuckDuckGo, Hugging Face, etc.)</sub></sup>           | 8K            | +198MB                     |
| LangGraph   | Agent, Graph           | Some <br><sup><sub>(e.g., Semantic Search)</sub></sup>                     | Some <br><sup><sub>(e.g., PostgresStore, SqliteSaver, etc.) </sub></sup>        | 37K           | +51MB                      |
| AutoGen    | Agent                | Some <br><sup><sub>(e.g., Tool Agent, Chat Agent)</sub></sup>              | Many <sup><sub>[Optional]<br> (e.g., OpenAI, Pinecone, etc.)</sub></sup>        | 7K <br><sup><sub>(core-only)</sub></sup>    | +26MB <br><sup><sub>(core-only)</sub></sup>          |
| **PocketFlow** | **Graph**                    | **None**                                                 | **None**                                                  | **100**       | **+56KB**                  |

</div>

Pocket Flow also makes an excellent educational resource by revealing exactly how an LLM framework works under the hood—without the heavy abstractions of larger libraries.

## How does Pocket Flow work?

The [100 lines](pocketflow/__init__.py) capture the core abstraction of LLM frameworks: Graph!

<div align="center">
  <img src="./assets/abstraction.png" width="500"/>
</div>

From there, it’s easy to implement popular design patterns like ([Multi-](https://the-pocket.github.io/PocketFlow/design_pattern/multi_agent.html))[Agents](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html), [Workflow](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html), [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html), etc.

<div align="center">
  <img src="./assets/design.png" width="500"/>
</div>




## How to Use Pocket Flow?


🚀 It's highly recommended to **build Agents with Agents**—the fastest development paradigm!

- 😎 **Humans** craft the **high-level requirements and system design**.

- 🤖 **AI agents** (e.g., Cursor AI) handle the **low-level implementation**.

Check out the video to see the process in action!

<br>
<div align="center">
  <a href="https://youtu.be/Cf38Bi8U0Js" target="_blank">
    <img src="./assets/tutorial.png" width="500" alt="IMAGE ALT TEXT" style="cursor: pointer;">
  </a>
</div>
<br>


## What can Pocket Flow build?

✨ Below are examples of LLM Apps:

<div align="center">
  
| Formal App Name  | Informal One-Liner |Difficulty    |  Learning Objectives  |
| :------------- | :-------------  | :-------------: | :--------------------- |
| [Ask AI Paul Graham](https://github.com/The-Pocket/Tutorial-YC-Partner)  | Ask AI Paul Graham, in case you don't get in | ★★☆ <br> *Medium*   | [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html) <br> [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) <br> [Text-to-Speech](https://the-pocket.github.io/PocketFlow/utility_function/text_to_speech.html) |
| [Youtube Summarizer](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple)  | Explain YouTube Videos to you like you're 5 | ★☆☆ <br> *Beginner*   | [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) | 
| [Cold Opener Generator](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization)  | Instant icebreakers that turn cold leads hot | ★☆☆ <br> *Beginner*   | [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) <br> [Web Search](https://the-pocket.github.io/PocketFlow/utility_function/websearch.html) | 

</div>

- Want to learn how I built these LLM Apps? Check out [my YouTube](https://www.youtube.com/@ZacharyLLM?sub_confirmation=1)!
  
- Want to create your own Python project? Start with  [this template](https://github.com/The-Pocket/PocketFlow-Template-Python)!





