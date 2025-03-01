---
layout: default
title: "Map Reduce"
parent: "Design Pattern"
nav_order: 3
---

# Map Reduce

MapReduce is a design pattern suitable when you have either:
- Large input data (e.g., multiple files to process), or
- Large output data (e.g., multiple forms to fill)

and there is a logical way to break the task into smaller, ideally independent parts. 
You first break down the task using [BatchNode](./batch.md) in the map phase, followed by aggregation in the reduce phase.


### Example: Document Summarization

```python
class MapSummaries(BatchNode):
    def prep(self, shared): return [shared["text"][i:i+10000] for i in range(0, len(shared["text"]), 10000)]
    def exec(self, chunk): return call_llm(f"Summarize this chunk: {chunk}")
    def post(self, shared, prep_res, exec_res_list): shared["summaries"] = exec_res_list

class ReduceSummaries(Node):
    def prep(self, shared): return shared["summaries"]
    def exec(self, summaries): return call_llm(f"Combine these summaries: {summaries}")
    def post(self, shared, prep_res, exec_res): shared["final_summary"] = exec_res

# Connect nodes
map_node = MapSummaries()
reduce_node = ReduceSummaries()
map_node >> reduce_node

# Create flow 
summarize_flow = Flow(start=map_node)
summarize_flow.run(shared)
```
