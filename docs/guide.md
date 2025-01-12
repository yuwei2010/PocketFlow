---
layout: default
title: "Design Guidance"
parent: "Apps"
nav_order: 1
---

# LLM System Design Guidance

{: .important }
> Use LLMs to help with system design and implementation wherever possible.

1. **Understand Requirements**  
   - Clarify the app’s needs and workflow.  
   - Determine data access (e.g., from files or databases).

2. **High-Level Flow Design**  
   - Represent the process as a *Nested Directed Graph*.  
   - Identify possible branching for *Node Action*.  
   - Identify data-heavy steps for *Batch*.

3. **Shared Memory Structure**  
   - For small apps, in-memory data is sufficient.  
   - For larger or persistent needs, use a database.  
   - Define schemas or data structures and plan how states will be stored and updated.

4. **Implementation**  
   - Rely on LLMs for coding tasks.  
   - Start with minimal, straightforward code (e.g., avoid heavy type checking initially).

5. **Optimization**  
   - *Prompt Engineering:* Provide clear instructions and examples to reduce ambiguity.  
   - *Task Decomposition:* Break complex tasks into manageable steps.

6. **Reliability**  
   - *Structured Output:* Verify outputs match the desired format, and increase `max_retries`.
   - *Test Cases:* Create tests for parts of the flow with clear inputs/outputs.  
   - *Self-Evaluation:* For unclear areas, add another Node for LLMs to review the results.
