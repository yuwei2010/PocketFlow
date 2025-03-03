---
layout: default
title: "Development Playbook"
---

# LLM Application Development Playbook

> If you are an AI assistant involved in building LLM Apps, read this guide **VERY, VERY** carefully! This is the most important chapter in the entire document. Throughout development, you should always (1) start with a small and simple solution, (2) design at a high level (`docs/design.md`) before implementation, and (3) frequently ask humans for feedback and clarification.
{: .warning }




## System Design Steps


These system designs should be a collaboration between humans and AI assistants:

| Stage                  | Human      | AI        | Comment                                                                 |
|:-----------------------|:----------:|:---------:|:------------------------------------------------------------------------|
| 1. Project Requirements | ★★★ High  | ★☆☆ Low   | Humans understand the requirements and context best.                    |
| 2. Utility Functions   | ★★☆ Medium | ★★☆ Medium | The human is familiar with external APIs and integrations, and the AI assists with implementation. |
| 3. Flow Design         | ★★☆ Medium | ★★☆ Medium | The human identifies complex and ambiguous parts, and the AI helps with redesign. |
| 4. Data Schema         | ★☆☆ Low   | ★★★ High  | The AI assists in designing the data schema based on the flow.          |
| 5. Implementation      | ★☆☆ Low   | ★★★ High  | The human identifies complex and ambiguous parts, and the AI helps with redesign. |
| 6. Optimization        | ★★☆ Medium | ★★☆ Medium | The human reviews the code and evaluates the results, while the AI helps optimize. |
| 7. Reliability         | ★☆☆ Low   | ★★★ High  | The AI helps write test cases and address corner cases.                 |

1. **Project Requirements**: Clearify the requirements for your project.

2. **Utility Functions**: Although the AI system is the decision-maker, it relies on **external utility functions**:

   <div align="center"><img src="https://github.com/the-pocket/PocketFlow/raw/main/assets/utility.png?raw=true" width="400"/></div>

   - Reading inputs (e.g., retrieving Slack messages, reading emails)
   - Writing outputs (e.g., generating reports, sending emails)
   - External tool usage (e.g., calling LLMs, searching the web)
   - **LLM-based tasks** (e.g., summarizing text, analyzing sentiment) are **not** utility functions. Instead, they are *internal core functions* within the AI system—designed in step 3—and are built on top of the utility functions.
   -  > **Start small!** Only include the most important ones to begin with!
      {: .best-practice }

3. **Flow Design (Compute)**: Create a high-level design for the application’s flow.
   - Identify potential design patterns, such as Batch, Agent, or RAG.
   - For each node, specify:
     - **Purpose**: The high-level compute logic
     - `exec`: The specific utility function to call (ideally, one function per node)
   - > **If a human can’t solve it, an LLM can’t automate it!** Before building an LLM system, thoroughly understand the problem by manually solving example inputs to develop intuition.
     {: .best-practice }

4. **Data Schema (Data)**: Plan how data will be stored and updated.
   - For simple apps, use an in-memory dictionary.
   - For more complex apps or when persistence is required, use a database.
   - For each node, specify:
     - `prep`: How the node reads data
     - `post`: How the node writes data

5. **Implementation**: Implement nodes and flows based on the design.
   - Start with a simple, direct approach (avoid over-engineering and full-scale type checking or testing). Let it fail fast to identify weaknesses.
   - Add logging throughout the code to facilitate debugging.

6. **Optimization**:
   - **Use Intuition**: For a quick initial evaluation, human intuition is often a good start.
   - **Redesign Flow (Back to Step 3)**: Consider breaking down tasks further, introducing agentic decisions, or better managing input contexts.
   - If your flow design is already solid, move on to micro-optimizations:
     - **Prompt Engineering**: Use clear, specific instructions with examples to reduce ambiguity.
     - **In-Context Learning**: Provide robust examples for tasks that are difficult to specify with instructions alone.

   - > **You’ll likely iterate a lot!** Expect to repeat Steps 3–6 hundreds of times.
     >
     > <div align="center"><img src="https://github.com/the-pocket/PocketFlow/raw/main/assets/success.png?raw=true" width="400"/></div>
     {: .best-practice }

7. **Reliability**  
   - **Node Retries**: Add checks in the node `exec` to ensure outputs meet requirements, and consider increasing `max_retries` and `wait` times.
   - **Logging and Visualization**: Maintain logs of all attempts and visualize node results for easier debugging.
   - **Self-Evaluation**: Add a separate node (powered by an LLM) to review outputs when results are uncertain.

## Example LLM Project File Structure

```
my_project/
├── main.py
├── flow.py
├── utils/
│   ├── __init__.py
│   ├── call_llm.py
│   └── search_web.py
├── requirements.txt
└── docs/
    └── design.md
```

- **`docs/design.md`**: Contains project documentation for each step above. This should be high-level and no-code.
- **`utils/`**: Contains all utility functions.
  - It’s recommended to dedicate one Python file to each API call, for example `call_llm.py` or `search_web.py`.
  - Each file should also include a `main()` function to try that API call
- **`flow.py`**: Implements the application’s flow, starting with node definitions followed by the overall structure.
- **`main.py`**: Serves as the project’s entry point.