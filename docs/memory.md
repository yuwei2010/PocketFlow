---
layout: default
title: "Chat Memory"
parent: "Paradigm"
nav_order: 5
---

# Chat Memory

Multi-turn conversations require memory management to maintain context while avoiding overwhelming the LLM.

### 1. Naive Approach: Full History

Sending the full chat history may overwhelm LLMs.

```python
class ChatNode(Node):
    def prep(self, shared):
        if "history" not in shared:
            shared["history"] = []
        user_input = input("You: ")
        return shared["history"], user_input

    def exec(self, inputs):
        history, user_input = inputs
        messages = [{"role": "system", "content": "You are a helpful assistant"}]
        for h in history:
            messages.append(h)
        messages.append({"role": "user", "content": user_input})
        response = call_llm(messages)
        return response

    def post(self, shared, prep_res, exec_res):
        shared["history"].append({"role": "user", "content": prep_res[1]})
        shared["history"].append({"role": "assistant", "content": exec_res})
        return "continue"

chat = ChatNode()
chat - "continue" >> chat
flow = Flow(start=chat)
```

### 2. Improved Memory Management

We can:
1. Recursively summarize conversations for overview.
2. Use [vector search](./tool.md) to retrieve relevant past exchanges for details

```python
class HandleInput(Node):
    def prep(self, shared):
        if "history" not in shared:
            shared["history"] = []
            shared["summary"] = ""
            shared["memory_index"] = None
            shared["memories"] = []
        
        user_input = input("You: ")
        query_embedding = get_embedding(user_input)
        
        relevant_memories = []
        if shared["memory_index"] is not None:
            indices, _ = search_index(shared["memory_index"], query_embedding, top_k=2)
            relevant_memories = [shared["memories"][i[0]] for i in indices]
        
        shared["current_input"] = {
            "summary": shared["summary"],
            "relevant": relevant_memories,
            "input": user_input
        }

class GenerateResponse(Node):
    def prep(self, shared):
        return shared["current_input"]

    def exec(self, context):
        prompt = f"""Context:
Summary: {context['summary']}
Relevant past: {context['relevant']}
User: {context['input']}

Response:"""
        return call_llm(prompt)
        
    def post(self, shared, prep_res, exec_res):
        shared["history"].append({"role": "user", "content": prep_res["input"]})
        shared["history"].append({"role": "assistant", "content": exec_res})

class UpdateMemory(Node):
    def prep(self, shared):
        return shared["current_input"]["input"]

    def exec(self, user_input):
        return get_embedding(user_input)
        
    def post(self, shared, prep_res, exec_res):
        shared["memories"].append(prep_res)
        if shared["memory_index"] is None:
            shared["memory_index"] = create_index([exec_res])
        else:
            shared["memory_index"].add(np.array([exec_res]))

class UpdateSummary(Node):
    def prep(self, shared):
        if shared["history"]:
            return shared["history"][-10:]
        return None

    def exec(self, recent_history):
        if recent_history:
            return call_llm(f"Summarize this conversation:\n{recent_history}")
        return ""

    def post(self, shared, prep_res, exec_res):
        if exec_res:
            shared["summary"] = exec_res

# Connect nodes
input_node = HandleInput()
response_node = GenerateResponse() 
memory_node = UpdateMemory()
summary_node = UpdateSummary()

input_node >> response_node >> memory_node >> summary_node >> input_node

chat_flow = Flow(start=input_node)
```
