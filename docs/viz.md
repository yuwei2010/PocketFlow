---
layout: default
title: "Visualization"
parent: "Details"
nav_order: 3
---

# Visualization

Visualizing the nested graph can help understanding. While we **don’t** include built-in visualization tools, we provide an example using **Mermaid**.

### Example: Visualization of Node with Mermaid

This code recursively traverses the nested graph, assigns unique IDs to each node, and treats Flow nodes as subgraphs to generate Mermaid syntax for a hierarchical visualization.

{% raw %}
```python
def build_mermaid(start):
    ids, visited, lines = {}, set(), ["graph LR"]
    ctr = 1
    def get_id(n):
        nonlocal ctr
        return ids[n] if n in ids else (ids.setdefault(n, f"N{ctr}"), (ctr := ctr + 1))[0]
    def link(a, b):
        lines.append(f"    {a} --> {b}")
    def walk(node, parent=None):
        if node in visited:
            return parent and link(parent, get_id(node))
        visited.add(node)
        if isinstance(node, Flow):
            node.start and parent and link(parent, get_id(node.start))
            lines.append(f"\n    subgraph sub_flow_{get_id(node)}[{type(node).__name__}]")
            node.start and walk(node.start)
            for nxt in node.successors.values():
                node.start and walk(nxt, get_id(node.start)) or (parent and link(parent, get_id(nxt))) or walk(nxt)
            lines.append("    end\n")
        else:
            lines.append(f"    {(nid := get_id(node))}['{type(node).__name__}']")
            parent and link(parent, nid)
            [walk(nxt, nid) for nxt in node.successors.values()]
    walk(start)
    return "\n".join(lines)
```
{% endraw %}

### Usage Example

Here, we define some example Nodes and Flows:

```python
class DataPrepBatchNode(BatchNode): pass
class ValidateDataNode(Node): pass
class FeatureExtractionNode(Node): pass
class TrainModelNode(Node): pass
class EvaluateModelNode(Node): pass
class ModelFlow(Flow): pass

feature_node = FeatureExtractionNode()
train_node = TrainModelNode()
evaluate_node = EvaluateModelNode()
feature_node >> train_node >> evaluate_node
model_flow = ModelFlow(start=feature_node)
data_prep_node = DataPrepBatchNode()
validate_node = ValidateDataNode()
data_prep_node >> validate_node >> model_flow
build_mermaid(start=data_prep_node)
```

The code generates a Mermaid diagram:

```mermaid
graph LR
    N1["DataPrepBatchNode"]
    N2["ValidateDataNode"]
    N1 --> N2
    N2 --> N3

    subgraph sub_flow_N4[ModelFlow]
    N3["FeatureExtractionNode"]
    N5["TrainModelNode"]
    N3 --> N5
    N6["EvaluateModelNode"]
    N5 --> N6
    end
```
