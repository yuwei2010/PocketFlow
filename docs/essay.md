---
layout: default
title: "Essay"
parent: "Apps"
nav_order: 2
---

# Summarization + QA agent for Paul Graham Essay

```python
from pocketflow import *
import openai, os, yaml

# Minimal LLM wrapper
def call_llm(prompt):
    openai.api_key = "YOUR_API_KEY_HERE"
    r = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content

shared = {"data": {}, "summary": {}}

# Load data into shared['data']
class LoadData(Node):
    def prep(self, shared):
        path = "./PocketFlow/data/PaulGrahamEssaysLarge"
        for fn in os.listdir(path):
            with open(os.path.join(path, fn), 'r') as f:
                shared['data'][fn] = f.read()
    def exec(self, res): pass
    def post(self, s, pr, er): pass

LoadData().run(shared)

# Summarize one file
class SummarizeFile(Node):
    def prep(self, s): return s['data'][self.params['filename']]
    def exec(self, content): return call_llm(f"{content} Summarize in 10 words.")
    def post(self, s, pr, sr): s["summary"][self.params['filename']] = sr

node_summ = SummarizeFile()
node_summ.set_params({"filename":"addiction.txt"})
node_summ.run(shared)

# Map-Reduce summarization
class MapSummaries(BatchNode):
    def prep(self, s):
        text = s['data'][self.params['filename']]
        return [text[i:i+10000] for i in range(0, len(text), 10000)]
    def exec(self, chunk):
        return call_llm(f"{chunk} Summarize in 10 words.")
    def post(self, s, pr, er):
        s["summary"][self.params['filename']] = [f"{i}. {r}" for i,r in enumerate(er)]

class ReduceSummaries(Node):
    def prep(self, s): return s["summary"][self.params['filename']]
    def exec(self, chunks): return call_llm(f"{chunks} Combine into 10 words summary.")
    def post(self, s, pr, sr): s["summary"][self.params['filename']] = sr

map_summ = MapSummaries()
reduce_summ = ReduceSummaries()
map_summ >> reduce_summ

flow = Flow(start=map_summ)
flow.set_params({"filename":"before.txt"})
flow.run(shared)

# Summarize all files
class SummarizeAllFiles(BatchFlow):
    def prep(self, s): return [{"filename":fn} for fn in s['data']]

SummarizeAllFiles(start=flow).run(shared)

# QA agent
class FindRelevantFile(Node):
    def prep(self, s):
        q = input("Enter a question: ")
        filenames = list(s['summary'].keys())
        file_summaries = [f"- '{fn}': {s['summary'][fn]}" for fn in filenames]
        return q, filenames, file_summaries

    def exec(self, p):
        q, filenames, file_summaries = p
        if not q:
            return {"think":"no question", "has_relevant":False}
        
        resp = call_llm(f"""
Question: {q} 
Find the most relevant file from: {file_summaries}
If none, explain why

Output in code fence:
```yaml
think: >
    reasoning about relevance
has_relevant: true/false
most_relevant: filename if relevant
```""")
        yaml_str = resp.split("```yaml")[1].split("```")[0].strip()
        result = yaml.safe_load(yaml_str)
        
        # Validate response
        assert isinstance(result, dict)
        assert "think" in result
        assert "has_relevant" in result
        assert isinstance(result["has_relevant"], bool)
        
        if result["has_relevant"]:
            assert "most_relevant" in result
            assert result["most_relevant"] in filenames
            
        return result

    def exec_fallback(self, p, exc): return {"think":"error","has_relevant":False}
    def post(self, s, pr, res):
        q, _ = pr
        if not q:
            print("No question asked"); return "end"
        if res["has_relevant"]:
            s["question"], s["relevant_file"] = q, res["most_relevant"]
            print("Relevant file:", res["most_relevant"])
            return "answer"
        else:
            print("No relevant file:", res["think"])
            return "retry"

class AnswerQuestion(Node):
    def prep(self, s):
        return s['question'], s['data'][s['relevant_file']]
    def exec(self, p):
        q, txt = p
        return call_llm(f"Question: {q}\nText: {txt}\nAnswer in 50 words.")
    def post(self, s, pr, ex):
        print("Answer:", ex)

class NoOp(Node): pass

frf = FindRelevantFile(max_retries=3)
aq = AnswerQuestion()
noop = NoOp()

frf - "answer" >> aq >> frf
frf - "retry"  >> frf
frf - "end"    >> noop

qa = Flow(start=frf)
qa.run(shared)
```