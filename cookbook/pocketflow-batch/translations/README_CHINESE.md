<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/title.png" alt="Pocket Flow – 100行代码的极简LLM框架" width="600"/>
</div>

[English](https://github.com/The-Pocket/PocketFlow/blob/main/README.md) | 中文 | [Español](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_SPANISH.md) | [日本語](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_JAPANESE.md) | [Deutsch](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_GERMAN.md) | [Русский](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_RUSSIAN.md) | [Português](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_PORTUGUESE.md) | [Français](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_FRENCH.md) | [한국어](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_KOREAN.md)

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://the-pocket.github.io/PocketFlow/)
 <a href="https://discord.gg/hUHHE9Sa6T">
    <img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat">
</a>

Pocket Flow 是一个[仅100行代码](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py)的极简主义LLM框架

- **轻量级**：仅100行代码。零臃肿，零依赖，零供应商锁定。
  
- **表达力强**：包含你喜爱的所有功能—([多](https://the-pocket.github.io/PocketFlow/design_pattern/multi_agent.html))[智能体](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html)、[工作流](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html)、[RAG检索增强生成](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html)等等。

- **[智能体编程](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)**：让AI智能体（例如Cursor AI）构建智能体—生产力提升10倍！

开始使用Pocket Flow：
- 安装方式：```pip install pocketflow```，或者直接复制[源代码](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py)（仅100行）。
- 了解更多，请查看[文档](https://the-pocket.github.io/PocketFlow/)。想了解开发动机，请阅读这个[故事](https://zacharyhuang.substack.com/p/i-built-an-llm-framework-in-just)。
- 有问题？试试这个[AI助手](https://chatgpt.com/g/g-677464af36588191b9eba4901946557b-pocket-flow-assistant)，或者[创建一个issue！](https://github.com/The-Pocket/PocketFlow/issues/new)
- 🎉 加入我们的[Discord](https://discord.gg/hUHHE9Sa6T)，与其他使用Pocket Flow构建应用的开发者交流！
- 🎉 Pocket Flow最初是用Python开发的，但现在我们也有[Typescript](https://github.com/The-Pocket/PocketFlow-Typescript)、[Java](https://github.com/The-Pocket/PocketFlow-Java)、[C++](https://github.com/The-Pocket/PocketFlow-CPP)和[Go](https://github.com/The-Pocket/PocketFlow-Go)版本！

## 为什么选择Pocket Flow？

当前的LLM框架都过于臃肿... 而LLM框架其实只需要100行代码！

<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/meme.jpg" width="400"/>


  |                | **抽象**          | **应用特定包装器**                                      | **供应商特定包装器**                                    | **代码行数**       | **大小**    |
|----------------|:-----------------------------: |:-----------------------------------------------------------:|:------------------------------------------------------------:|:---------------:|:----------------------------:|
| LangChain  | Agent, Chain               | 众多 <br><sup><sub>(例如，问答，摘要)</sub></sup>              | 众多 <br><sup><sub>(例如，OpenAI, Pinecone等)</sub></sup>                   | 405K          | +166MB                     |
| CrewAI     | Agent, Chain            | 众多 <br><sup><sub>(例如，FileReadTool, SerperDevTool)</sub></sup>         | 众多 <br><sup><sub>(例如，OpenAI, Anthropic, Pinecone等)</sub></sup>        | 18K           | +173MB                     |
| SmolAgent   | Agent                      | 一些 <br><sup><sub>(例如，CodeAgent, VisitWebTool)</sub></sup>         | 一些 <br><sup><sub>(例如，DuckDuckGo, Hugging Face等)</sub></sup>           | 8K            | +198MB                     |
| LangGraph   | Agent, Graph           | 一些 <br><sup><sub>(例如，语义搜索)</sub></sup>                     | 一些 <br><sup><sub>(例如，PostgresStore, SqliteSaver等) </sub></sup>        | 37K           | +51MB                      |
| AutoGen    | Agent                | 一些 <br><sup><sub>(例如，Tool Agent, Chat Agent)</sub></sup>              | 众多 <sup><sub>[可选]<br> (例如，OpenAI, Pinecone等)</sub></sup>        | 7K <br><sup><sub>(仅核心)</sub></sup>    | +26MB <br><sup><sub>(仅核心)</sub></sup>          |
| **PocketFlow** | **Graph**                    | **无**                                                 | **无**                                                  | **100**       | **+56KB**                  |

</div>

## Pocket Flow如何工作？

这[100行代码](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py)捕捉了LLM框架的核心抽象：图（Graph）！
<br>
<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/abstraction.png" width="900"/>
</div>
<br>

有了这个基础，就可以轻松实现流行的设计模式，如([多](https://the-pocket.github.io/PocketFlow/design_pattern/multi_agent.html))[智能体](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html)、[工作流](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html)、[RAG检索增强生成](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html)等。
<br>
<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/design.png" width="900"/>
</div>
<br>
✨ 以下是基础教程：

<div align="center">
  
|  名称  | 难度    |  描述  |  
| :-------------:  | :-------------: | :--------------------- |  
| [聊天](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat) | ☆☆☆ <br> *入门*   | 带有对话历史的基础聊天机器人 |
| [结构化输出](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-structured-output) | ☆☆☆ <br> *入门* | 通过提示从简历中提取结构化数据 |
| [工作流](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-workflow) | ☆☆☆ <br> *入门*   | 一个写作工作流程，包括大纲、内容编写和样式应用 |
| [智能体](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-agent) | ☆☆☆