<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/title.png" alt="Pocket Flow – 100-строчный минималистичный LLM фреймворк" width="600"/>
</div>

[English](https://github.com/The-Pocket/PocketFlow/blob/main/README.md) | [中文](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_CHINESE.md) | [Español](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_SPANISH.md) | [日本語](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_JAPANESE.md) | [Deutsch](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_GERMAN.md) | Русский | [Português](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_PORTUGUESE.md) | [Français](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_FRENCH.md) | [한국어](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_KOREAN.md)

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://the-pocket.github.io/PocketFlow/)
 <a href="https://discord.gg/hUHHE9Sa6T">
    <img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat">
</a>

Pocket Flow — это [100-строчный](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py) минималистичный LLM фреймворк

- **Легкий**: Всего 100 строк. Никакого избыточного кода, никаких зависимостей, никакой привязки к поставщикам.
  
- **Выразительный**: Всё, что вы любите—([Мульти-](https://the-pocket.github.io/PocketFlow/design_pattern/multi_agent.html))[Агенты](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html), [Рабочие процессы](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html), [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html) и многое другое.

- **[Агентное программирование](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)**: Позвольте ИИ-агентам (например, Cursor AI) создавать агентов — повышение продуктивности в 10 раз!

Начало работы с Pocket Flow:
- Для установки используйте ```pip install pocketflow``` или просто скопируйте [исходный код](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py) (всего 100 строк).
- Чтобы узнать больше, ознакомьтесь с [документацией](https://the-pocket.github.io/PocketFlow/). Чтобы понять мотивацию, прочитайте [историю](https://zacharyhuang.substack.com/p/i-built-an-llm-framework-in-just).
- Есть вопросы? Воспользуйтесь этим [ИИ-ассистентом](https://chatgpt.com/g/g-677464af36588191b9eba4901946557b-pocket-flow-assistant), или [создайте задачу!](https://github.com/The-Pocket/PocketFlow/issues/new)
- 🎉 Присоединяйтесь к нашему [Discord](https://discord.gg/hUHHE9Sa6T), чтобы связаться с другими разработчиками, использующими Pocket Flow!
- 🎉 Pocket Flow изначально написан на Python, но теперь у нас есть версии на [Typescript](https://github.com/The-Pocket/PocketFlow-Typescript), [Java](https://github.com/The-Pocket/PocketFlow-Java), [C++](https://github.com/The-Pocket/PocketFlow-CPP) и [Go](https://github.com/The-Pocket/PocketFlow-Go)!

## Почему Pocket Flow?

Текущие LLM фреймворки слишком громоздки... Для LLM фреймворка достаточно всего 100 строк!

<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/meme.jpg" width="400"/>


  |                | **Абстракция**          | **Обертки для приложений**                                      | **Обертки для поставщиков**                                    | **Строк**       | **Размер**    |
|----------------|:-----------------------------: |:-----------------------------------------------------------:|:------------------------------------------------------------:|:---------------:|:----------------------------:|
| LangChain  | Агент, Цепочка               | Много <br><sup><sub>(например, вопросы-ответы, суммаризация)</sub></sup>              | Много <br><sup><sub>(например, OpenAI, Pinecone и т.д.)</sub></sup>                   | 405K          | +166MB                     |
| CrewAI     | Агент, Цепочка            | Много <br><sup><sub>(например, FileReadTool, SerperDevTool)</sub></sup>         | Много <br><sup><sub>(например, OpenAI, Anthropic, Pinecone и т.д.)</sub></sup>        | 18K           | +173MB                     |
| SmolAgent   | Агент                      | Некоторые <br><sup><sub>(например, CodeAgent, VisitWebTool)</sub></sup>         | Некоторые <br><sup><sub>(например, DuckDuckGo, Hugging Face и т.д.)</sub></sup>           | 8K            | +198MB                     |
| LangGraph   | Агент, Граф           | Некоторые <br><sup><sub>(например, Semantic Search)</sub></sup>                     | Некоторые <br><sup><sub>(например, PostgresStore, SqliteSaver и т.д.) </sub></sup>        | 37K           | +51MB                      |
| AutoGen    | Агент                | Некоторые <br><sup><sub>(например, Tool Agent, Chat Agent)</sub></sup>              | Много <sup><sub>[Опционально]<br> (например, OpenAI, Pinecone и т.д.)</sub></sup>        | 7K <br><sup><sub>(только ядро)</sub></sup>    | +26MB <br><sup><sub>(только ядро)</sub></sup>          |
| **PocketFlow** | **Граф**                    | **Нет**                                                 | **Нет**                                                  | **100**       | **+56KB**                  |

</div>

## Как работает Pocket Flow?

[100 строк](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py) охватывают основную абстракцию LLM фреймворков: Граф!
<br>
<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/abstraction.png" width="900"/>
</div>
<br>

Отсюда легко реализовать популярные шаблоны проектирования, такие как ([Мульти-](https://the-pocket.github.io/PocketFlow/design_pattern/multi_agent.html))[Агенты](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html), [Рабочие процессы](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html), [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html) и т.д.
<br>
<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/design.png" width="900"/>
</div>
<br>
✨ Ниже приведены базовые руководства:

<div align="center">
  
|  Название  | Сложность    |  Описание  |  
| :-------------:  | :-------------: | :--------------------- |  
| [Чат](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat) | ☆☆☆ <br> *Элементарно*   | Базовый чат-бот с историей разговора |
| [Структурированный вывод](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-structured-output) | ☆☆☆ <br> *Элементарно* | Извлечение структурированных данных из резюме с помощью промптов |
| [Рабочий процесс](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-workflow) | ☆☆☆ <br> *Элементарно*   | Процесс написания, включающий структурирование, создание контента и стилизацию |
| [Агент](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-agent) | ☆☆☆ <br> *Элементарно*   | Исследовательский агент, который может искать в интернете и отвечать на вопросы |
| [RAG](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-rag) | ☆☆☆ <br> *Элементарно*   | Простой процесс генерации с извлечением информации |
| [Пакетная обработка](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-batch) | ☆☆☆ <br> *Элементарно* | Пакетный обработчик, который переводит markdown-контент на несколько языков |
| [Потоковая передача](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-llm-streaming) | ☆☆☆ <br> *Элементарно*   | Демонстрация потоковой передачи LLM в реальном времени с возможностью прерывания пользователем |
| [Защита чата](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat-guardrail) | ☆☆☆ <br> *Элементарно*  | Чат-бот туристического консультанта, обрабатывающий только запросы, связанные с путешествиями |
| [Map-Reduce](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-map-reduce) | ★☆☆ <br> *Начальный* | Обработчик квалификаций резюме с использованием шаблона map-reduce для пакетной оценки |
| [Мульти-агент](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-multi-agent) | ★☆☆ <br> *Начальный* | Игра в Табу для асинхронного общения между двумя агентами |
| [Наблюдатель](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-supervisor) | ★☆☆ <br> *Начальный* | Исследовательский агент становится ненадежным... Давайте создадим процесс наблюдения|
| [Параллельная обработка](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-parallel-batch) | ★☆☆ <br> *Начальный*   | Демонстрация параллельного выполнения, показывающая ускорение в 3 раза |
| [Параллельный поток](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-parallel-batch-flow) | ★☆☆ <br> *Начальный*   | Демонстрация параллельной обработки изображений, показывающая ускорение в 8 раз с несколькими фильтрами |
| [Голосование большинства](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-majority-vote) | ★☆☆ <br> *Начальный* | Повышение точности рассуждений путем объединения нескольких попыток решения |
| [Размышление](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-thinking) | ★☆☆ <br> *Начальный*   | Решение сложных задач рассуждения с помощью цепочки размышлений |
| [Память](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat-memory) | ★☆☆ <br> *Начальный* | Чат-бот с краткосрочной и долгосрочной памятью |
| [Text2SQL](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-text2sql) | ★☆☆ <br> *Начальный* | Преобразование естественного языка в SQL-запросы с автоматическим циклом отладки |
| [MCP](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-mcp) | ★☆☆ <br> *Начальный* |  Агент, использующий протокол модельного контекста для числовых операций |
| [A2A](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-a2a) | ★☆☆ <br> *Начальный* | Агент, обернутый протоколом Agent-to-Agent для межагентной коммуникации |
| [Web HITL](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-web-hitl) | ★☆☆ <br> *Начальный* | Минимальный веб-сервис для цикла человеческой проверки с обновлениями SSE |

</div>