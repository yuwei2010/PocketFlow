---
layout: default
title: "Agentic Coding"
---

# Agentic Coding: Humans Design, Agents code!

> If you are an AI agents involved in building LLM Systems, read this guide **VERY, VERY** carefully! This is the most important chapter in the entire document. Throughout development, you should always (1) start with a small and simple solution, (2) design at a high level (`docs/design.md`) before implementation, and (3) frequently ask humans for feedback and clarification.
{: .warning }

## System Design Steps

These system designs should be a collaboration between humans and AI assistants:

| Stage                  | Human      | AI        | Comment                                                                 |
|:-----------------------|:----------:|:---------:|:------------------------------------------------------------------------|
| 1. Requirements | ★★★ High  | ★☆☆ Low   | Humans understand the requirements and context.                    |
| 2. Flow          | ★★☆ Medium | ★★☆ Medium |  Humans specify the high-level design, and the AI fills in the details. |
| 3. Utilities   | ★★☆ Medium | ★★☆ Medium | Humans provide available external APIs and integrations, and the AI helps with implementation. |
| 4. Node          | ★☆☆ Low   | ★★★ High  | The AI helps design the node types and data handling based on the flow.          |
| 5. Implementation      | ★☆☆ Low   | ★★★ High  |  The AI implements the flow based on the design. |
| 6. Optimization        | ★★☆ Medium | ★★☆ Medium | Humans evaluate the results, and the AI helps optimize. |
| 7. Reliability         | ★☆☆ Low   | ★★★ High  |  The AI writes test cases and addresses corner cases.     |

1. **Requirements**: Clarify the requirements for your project, and evaluate whether an AI system is a good fit. AI systems are:
    - suitable for routine tasks that require common sense (e.g., filling out forms, replying to emails).
    - suitable for creative tasks where all inputs are provided (e.g., building slides, writing SQL).
    - **NOT** suitable for tasks that are highly ambiguous and require complex info (e.g., building a startup).
    - > **If a human can’t solve it, an LLM can’t automate it!** Before building an LLM system, thoroughly understand the problem by manually solving example inputs to develop intuition.  
      {: .best-practice }


2. **Flow Design**: Outline at a high level, describe how your AI system orchestrates nodes.
    - Identify applicable design patterns (e.g., [Map Reduce](./design_pattern/mapreduce.md), [Agent](./design_pattern/agent.md), [RAG](./design_pattern/rag.md)).
    - Outline the flow and draw it in a mermaid diagram. For example:
      ```mermaid
      flowchart LR
          firstNode[First Node] --> secondNode[Second Node]
          secondNode --> thirdNode[Third Node]
      ```

3. **Utilities**: Based on the Flow Design, identify and implement necessary utility functions.
    - Think of your AI system as the brain. It needs a body—these *external utility functions*—to interact with the real world:
        <div align="center"><img src="https://github.com/the-pocket/PocketFlow/raw/main/assets/utility.png?raw=true" width="400"/></div>

        - Reading inputs (e.g., retrieving Slack messages, reading emails)
        - Writing outputs (e.g., generating reports, sending emails)
        - Using external tools (e.g., calling LLMs, searching the web)
        - **NOTE**: *LLM-based tasks* (e.g., summarizing text, analyzing sentiment) are **NOT** utility functions; rather, they are *core functions* internal in the AI system.
    - For each utility function, implement it and write a simple test.
    - Document their input/output, as well as why they are necessary. For example:
      - *Name*: Embedding (`utils/get_embedding.py`)
      - *Input*: `str`
      - *Output*: a vector of 3072 floats
      - *Necessity:* Used by the second node to embed text


4. **Node Design**: Plan how each node will read and write data, and use utility functions.
   - Start with the shared data design
      - For simple systems, use an in-memory dictionary.
      - For more complex systems or when persistence is required, use a database.
      - **Don't Repeat Yourself"**: Use in-memory references or foreign keys.
   - For each node, describe its type, how it reads and writes data, and which utility function it uses. Keep it specific but high-level without codes. For example:
     - `type`: Regular (or Batch, or Async)
     - `prep`: Read "text" from the shared store
     - `exec`: Call the embedding utility function
     - `post`: Write "embedding" to the shared store


5. **Implementation**: Implement the initial nodes and flows based on the design.
   - **“Keep it simple, stupid!”** Avoid complex features and full-scale type checking.
   - **FAIL FAST**! Avoid `try` logic so you can quickly identify any weak points in the system.
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
- **`flow.py`**: Implements the system's flow, starting with node definitions followed by the overall structure.
- **`main.py`**: Serves as the project’s entry point.