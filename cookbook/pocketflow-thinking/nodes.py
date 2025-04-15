# cookbook/pocketflow-thinking/nodes.py
from pocketflow import Node
import yaml
from utils import call_llm

class ChainOfThoughtNode(Node):
    def prep(self, shared):
        # Gather problem and previous thoughts
        problem = shared.get("problem", "")
        thoughts = shared.get("thoughts", [])
        current_thought_number = shared.get("current_thought_number", 0)
        
        # Increment the current thought number for the next step
        shared["current_thought_number"] = current_thought_number + 1
        
        # Format previous thoughts simply
        thoughts_text = "\n".join([
            f"Thought {t['thought_number']}: {t['current_thinking']}" + 
            (f"\n  (Plan: {t.get('next_thought_planning', 'N/A')})" if t.get('next_thought_needed') else "")
            for t in thoughts
        ])
        
        return {
            "problem": problem,
            "thoughts_text": thoughts_text,
            "current_thought_number": current_thought_number + 1, 
        }
    
    def exec(self, prep_res):
        problem = prep_res["problem"]
        thoughts_text = prep_res["thoughts_text"]
        current_thought_number = prep_res["current_thought_number"] 
        
        # Create the simplified prompt for the LLM
        prompt = f"""
You are solving a complex problem step-by-step. Focus on generating the next logical thought in the sequence.

Problem: {problem}

Previous thoughts:
{thoughts_text if thoughts_text else "No previous thoughts yet."}

Your task is to generate the next thought (Thought {current_thought_number}). Think about the current step required to move closer to the solution.

Format your response ONLY as a YAML structure enclosed in ```yaml ... ```:
```yaml
current_thinking: |
  # Your detailed thinking for this step. 
  # If this step provides the final answer, state the final answer clearly here.
next_thought_needed: true # Set to false ONLY when 'current_thinking' contains the complete final answer.
next_thought_planning: |
  # Optional: Briefly describe what the *next* thought should focus on. Leave empty if none or if finished.
```"""
        
        response = call_llm(prompt)
        
        # Simple YAML extraction
        yaml_str = response.split("```yaml")[1].split("```")[0].strip()
        thought_data = yaml.safe_load(yaml_str)

        # --- Validation ---
        # Ensure required keys are present after parsing
        assert "current_thinking" in thought_data, "LLM response missing 'current_thinking'"
        assert "next_thought_needed" in thought_data, "LLM response missing 'next_thought_needed'"
        # 'next_thought_planning' is optional, so no assert needed, but we can ensure it exists
        thought_data.setdefault("next_thought_planning", "") 
        # --- End Validation ---
        
        # Add thought number
        thought_data["thought_number"] = current_thought_number
        return thought_data

    
    def post(self, shared, prep_res, exec_res):
        # Add the new thought to the list
        if "thoughts" not in shared:
            shared["thoughts"] = []
        shared["thoughts"].append(exec_res)
        
        # If we're done, extract the solution from the last thought's thinking
        if exec_res.get("next_thought_needed") == False:
            shared["solution"] = exec_res["current_thinking"]
            print("\n=== FINAL SOLUTION ===")
            print(exec_res["current_thinking"])
            print("======================\n")
            return "end"
        
        # Otherwise, continue the chain
        print(f"\nThought {exec_res['thought_number']}:")
        print(exec_res['current_thinking'])
        if exec_res.get('next_thought_planning'):
            print(f"\nNext step planned: {exec_res['next_thought_planning']}")
        # print(f"Next thought needed: {exec_res.get('next_thought_needed')}") # Redundant if planning shown
        print("-" * 50)
        
        return "continue"  # Continue the chain