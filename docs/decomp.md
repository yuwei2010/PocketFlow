---
layout: default
title: "Task Decomposition"
parent: "Paradigm"
nav_order: 2
---

# Task Decomposition

Many real-world tasks are too complex for one LLM call. The solution is to decompose them into multiple calls as a [Flow](./flow.md) of Nodes.

### Example: Article Writing

```python
class GenerateOutline(Node):
    def exec(self, topic):
        prompt = f"Create a detailed outline for an article about {topic}"
        return call_llm(prompt)

class WriteSection(Node):
    def exec(self, section):
        prompt = f"Write content for this section: {section}"
        return call_llm(prompt)

class ReviewAndRefine(Node):
    def exec(self, draft):
        prompt = f"Review and improve this draft: {draft}"
        return call_llm(prompt)

# Connect nodes  
outline = GenerateOutline()
write = WriteSection()
review = ReviewAndRefine()

outline >> write >> review

# Create flow
writing_flow = Flow(start=outline)
writing_flow.run({"topic": "AI Safety"})
```
