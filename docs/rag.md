---
layout: default
title: "RAG"
parent: "Paradigm" 
nav_order: 4
---

# RAG (Retrieval Augmented Generation)

For certain LLM tasks like answering questions, providing context is essential.
Use [vector search](./tool.md) to find relevant context for LLM responses.

### Example: Question Answering

```python
class PrepareEmbeddings(Node):
    def prep(self, shared):
        texts = shared["texts"]
        embeddings = [get_embedding(text) for text in texts]
        shared["search_index"] = create_index(embeddings)

class AnswerQuestion(Node):
    def prep(self, shared):
        question = input("Enter question: ")
        query_embedding = get_embedding(question)
        indices, _ = search_index(shared["search_index"], query_embedding, top_k=1)
        relevant_text = shared["texts"][indices[0][0]]
        return question, relevant_text

    def exec(self, inputs):
        question, context = inputs
        prompt = f"Question: {question}\nContext: {context}\nAnswer: "
        return call_llm(prompt)

    def post(self, shared, prep_res, exec_res):
        print(f"Answer: {exec_res}")

# Connect nodes
prep = PrepareEmbeddings()
qa = AnswerQuestion()

prep >> qa

# Create flow
qa_flow = Flow(start=prep)
qa_flow.run(shared)
```