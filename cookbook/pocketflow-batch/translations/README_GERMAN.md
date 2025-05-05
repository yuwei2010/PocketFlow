<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/title.png" alt="Pocket Flow – 100-Zeilen minimalistisches LLM-Framework" width="600"/>
</div>

[English](https://github.com/The-Pocket/PocketFlow/blob/main/README.md) | [中文](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_CHINESE.md) | [Español](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_SPANISH.md) | [日本語](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_JAPANESE.md) | Deutsch | [Русский](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_RUSSIAN.md) | [Português](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_PORTUGUESE.md) | [Français](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_FRENCH.md) | [한국어](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_KOREAN.md)

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://the-pocket.github.io/PocketFlow/)
 <a href="https://discord.gg/hUHHE9Sa6T">
    <img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat">
</a>

Pocket Flow ist ein [100-Zeilen](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py) minimalistisches LLM-Framework

- **Leichtgewichtig**: Nur 100 Zeilen. Kein überflüssiger Code, keine Abhängigkeiten, keine Herstellerbindung.
  
- **Ausdrucksstark**: Alles was du liebst—([Multi-](https://the-pocket.github.io/PocketFlow/design_pattern/multi_agent.html))[Agents](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html), [Workflow](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html), [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html), und mehr.

- **[Agentenbasiertes Programmieren](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)**: Lass KI-Agenten (z.B. Cursor AI) Agenten bauen—10-fache Produktivitätssteigerung!

Starte mit Pocket Flow:
- Installation via ```pip install pocketflow``` oder kopiere einfach den [Quellcode](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py) (nur 100 Zeilen).
- Erfahre mehr in der [Dokumentation](https://the-pocket.github.io/PocketFlow/). Um die Motivation zu verstehen, lies die [Geschichte](https://zacharyhuang.substack.com/p/i-built-an-llm-framework-in-just).
- Fragen? Nutze diesen [KI-Assistenten](https://chatgpt.com/g/g-677464af36588191b9eba4901946557b-pocket-flow-assistant) oder [erstelle ein Issue!](https://github.com/The-Pocket/PocketFlow/issues/new)
- 🎉 Tritt unserem [Discord](https://discord.gg/hUHHE9Sa6T) bei, um dich mit anderen Entwicklern zu vernetzen, die mit Pocket Flow arbeiten!
- 🎉 Pocket Flow war ursprünglich in Python, aber wir haben jetzt auch [Typescript](https://github.com/The-Pocket/PocketFlow-Typescript), [Java](https://github.com/The-Pocket/PocketFlow-Java), [C++](https://github.com/The-Pocket/PocketFlow-CPP) und [Go](https://github.com/The-Pocket/PocketFlow-Go) Versionen!

## Warum Pocket Flow?

Aktuelle LLM-Frameworks sind überladen... Du brauchst nur 100 Zeilen für ein LLM-Framework!

<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/meme.jpg" width="400"/>


  |                | **Abstraktion**          | **App-spezifische Wrapper**                                      | **Anbieter-spezifische Wrapper**                                    | **Zeilen**       | **Größe**    |
|----------------|:-----------------------------: |:-----------------------------------------------------------:|:------------------------------------------------------------:|:---------------:|:----------------------------:|
| LangChain  | Agent, Chain               | Viele <br><sup><sub>(z.B. QA, Zusammenfassung)</sub></sup>              | Viele <br><sup><sub>(z.B. OpenAI, Pinecone, etc.)</sub></sup>                   | 405K          | +166MB                     |
| CrewAI     | Agent, Chain            | Viele <br><sup><sub>(z.B. FileReadTool, SerperDevTool)</sub></sup>         | Viele <br><sup><sub>(z.B. OpenAI, Anthropic, Pinecone, etc.)</sub></sup>        | 18K           | +173MB                     |
| SmolAgent   | Agent                      | Einige <br><sup><sub>(z.B. CodeAgent, VisitWebTool)</sub></sup>         | Einige <br><sup><sub>(z.B. DuckDuckGo, Hugging Face, etc.)</sub></sup>           | 8K            | +198MB                     |
| LangGraph   | Agent, Graph           | Einige <br><sup><sub>(z.B. Semantic Search)</sub></sup>                     | Einige <br><sup><sub>(z.B. PostgresStore, SqliteSaver, etc.) </sub></sup>        | 37K           | +51MB                      |
| AutoGen    | Agent                | Einige <br><sup><sub>(z.B. Tool Agent, Chat Agent)</sub></sup>              | Viele <sup><sub>[Optional]<br> (z.B. OpenAI, Pinecone, etc.)</sub></sup>        | 7K <br><sup><sub>(nur Kern)</sub></sup>    | +26MB <br><sup><sub>(nur Kern)</sub></sup>          |
| **PocketFlow** | **Graph**                    | **Keine**                                                 | **Keine**                                                  | **100**       | **+56KB**                  |

</div>

## Wie funktioniert Pocket Flow?

Die [100 Zeilen](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py) erfassen die Kernabstraktion von LLM-Frameworks: Graph!
<br>
<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/abstraction.png" width="900"/>
</div>
<br>

Von dort aus ist es einfach, beliebte Designmuster wie ([Multi-](https://the-pocket.github.io/PocketFlow/design_pattern/multi_agent.html))[Agents](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html), [Workflow](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html), [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html) usw. zu implementieren.
<br>
<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/design.png" width="900"/>
</div>
<br>
✨ Nachfolgend sind grundlegende Tutorials:

<div align="center">
  
|  Name  | Schwierigkeit    |  Beschreibung  |  
| :-------------:  | :-------------: | :--------------------- |  
| [Chat](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat) | ☆☆☆ <br> *Sehr einfach*   | Ein einfacher Chatbot mit Gesprächsverlauf |
| [Strukturierte Ausgabe](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-structured-output) | ☆☆☆ <br> *Sehr einfach* | Extrahieren strukturierter Daten aus Lebensläufen durch Prompting |
| [Workflow](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-workflow) | ☆☆☆ <br> *Sehr einfach*   | Ein Schreibworkflow, der Gliederung erstellt, Inhalte verfasst und Formatierung anwendet |
| [Agent](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-agent) | ☆☆☆ <br> *Sehr einfach*   | Ein Recherche-Agent, der im Web suchen und Fragen beantworten kann |
| [RAG](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-rag) | ☆☆☆ <br> *Sehr einfach*   | Ein einfacher Retrieval-augmented Generation Prozess |
| [Batch](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-batch) | ☆☆☆ <br> *Sehr einfach* | Ein Batch-Prozessor, der Markdown-Inhalte in mehrere Sprachen übersetzt |
| [Streaming](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-llm-streaming) | ☆☆☆ <br> *Sehr einfach*   | Eine Echtzeit-LLM-Streaming-Demo mit Nutzer-Unterbrechungsfunktion |
| [Chat-Leitplanke](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat-guardrail) | ☆☆☆ <br> *Sehr einfach*  | Ein Reiseberater-Chatbot, der nur reisebezogene Anfragen verarbeitet |
| [Map-Reduce](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-map-reduce) | ★☆☆ <br> *Anfänger* | Ein Lebenslauf-Qualifikationsprozessor mit Map-Reduce-Muster für Batch-Auswertung |
| [Multi-Agent](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-multi-agent) | ★☆☆ <br> *Anfänger* | Ein Tabu-Wortspiel für asynchrone Kommunikation zwischen zwei Agenten |
| [Supervisor](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-supervisor) | ★☆☆ <br> *Anfänger* | Der Recherche-Agent wird unzuverlässig... Lass uns einen Überwachungsprozess bauen |
| [Parallel](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-parallel-batch) | ★☆☆ <br> *Anfänger*   | Eine Demonstration paralleler Ausführung mit 3-facher Beschleunigung |
| [Paralleler Flow](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-parallel-batch-flow) | ★☆☆ <br> *Anfänger*   | Eine parallele Bildverarbeitungsdemo mit 8-facher Beschleunigung durch mehrere Filter |
| [Mehrheitsentscheidung](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-majority-vote) | ★☆☆ <br> *Anfänger* | Verbessere die Genauigkeit durch Aggregation mehrerer Lösungsversuche |
| [Denkprozess](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-thinking) | ★☆☆ <br> *Anfänger*   | Löse komplexe Probleme durch Chain-of-Thought |
| [Gedächtnis](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat-memory) | ★☆☆ <br> *Anfänger* | Ein Chatbot mit Kurz- und Langzeitgedächtnis |
| [Text2SQL](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-text2sql) | ★☆☆ <br> *Anfänger* | Konvertiere natürliche Sprache in SQL-Abfragen mit automatischer Debugging-Schleife |
| [MCP](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-mcp) | ★☆☆ <br> *Anfänger* | Agent, der das Model Context Protocol für numerische Operationen verwendet |
| [A2A](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-a2a) | ★☆☆ <br> *Anfänger* | Agent mit Agent-to-Agent-Protokoll für Agent-übergreifende Kommunikation |
| [Web HITL](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-web-hitl) | ★☆☆ <br> *Anfänger* | Ein minimaler Webdienst für eine menschliche Überprüfungsschleife mit SSE-Updates |

</div>

👀 Möchtest du weitere einfache Tutorials sehen? [Erstelle ein Issue!](https://github.com/The-Pocket/PocketFlow/issues/new)

## Wie nutzt man Pocket Flow?

🚀 Durch **Agentenbasiertes Programmieren** – das schnellste LLM-App-Entwicklungsparadigma, bei dem *Menschen designen* und *Agenten programmieren*!

<br>
<div align="center">
  <a href="https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to" target="_blank">
    <img src="https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F423a39af-49e8-483b-bc5a-88cc764350c6_1050x588.png" width="700" alt="IMAGE ALT TEXT" style="cursor: pointer;">
  </a>
</div>
<br>

✨ Nachfolgend sind Beispiele für komplexere LLM-Apps:

<div align="center">
  
|  App-Name     |  Schwierigkeit    | Themen  | Mensch-Design | Agent-Code |
| :-------------:  | :-------------: | :---------------------: |  :---: |  :---: |
| [Cursor mit Cursor erstellen](https://github.com/The-Pocket/Tutorial-Cursor) <br> <sup><sub>Wir werden die Singularität bald erreichen ...</sup></sub> | ★★★ <br> *Fortgeschritten*   | [Agent](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html) | [Design-Dokument](https://github.com/The-Pocket/Tutorial-Cursor/blob/main/docs/design.md) | [Flow-Code](https://github.com/The-Pocket/Tutorial-Cursor/blob/main/flow.py)
| [Codebase-Wissenserstellung](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge) <br> <sup><sub>Das Leben ist zu kurz, um verwirrt auf fremden Code zu starren</sup></sub> |  ★★☆ <br> *Mittel* | [Workflow](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html) | [Design-Dokument](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge/blob/main/docs/design.md) | [Flow-Code](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge/blob/main/flow.py)
| [Ask AI Paul Graham](https://github.com/The-Pocket/Tutorial-YC-Partner) <br> <sup><sub>Frage AI Paul Graham, falls du nicht aufgenommen wirst</sup></sub> | ★★☆ <br> *Mittel*  | [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html) <br> [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) <br> [TTS](https://the-pocket.github.io/PocketFlow/utility_function/text_to_speech.html) | [Design-Dokument](https://github.com/The-Pocket/Tutorial-AI-Paul-Graham/blob/main/docs/design.md) | [Flow-Code](https://github.com/The-Pocket/Tutorial-AI-Paul-Graham/blob/main/flow.py)
| [Youtube-Zusammenfassung](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple)  <br> <sup><sub>Erklärt dir YouTube-Videos, als wärst du 5</sup></sub> | ★☆☆ <br> *Anfänger*   | [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) |  [Design-Dokument](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple/blob/main/docs/design.md) | [Flow-Code](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple/blob/main/flow.py)
| [Kaltakquise-Generator](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization)  <br> <sup><sub>Sofortige Eisbrecher, die kalte Leads zu heißen machen</sup></sub> | ★☆☆ <br> *Anfänger*   | [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) <br> [Web-Suche](https://the-pocket.github.io/PocketFlow/utility_function/websearch.html) |  [Design-Dokument](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization/blob/master/docs/design.md) | [Flow-Code](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization/blob/master/flow.py)

</div>

- Möchtest du **Agentenbasiertes Programmieren** lernen?

  - Schau dir [meinen YouTube-Kanal](https://www.youtube.com/@ZacharyLLM?sub_confirmation=1) für Video-Tutorials an, wie einige der oben genannten Apps erstellt wurden!

  - Willst du deine eigene LLM-App bauen? Lies diesen [Beitrag](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)! Beginne mit [dieser Vorlage](https://github.com/The-Pocket/PocketFlow-Template-Python)!