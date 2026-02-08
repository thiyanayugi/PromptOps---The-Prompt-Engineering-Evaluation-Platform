"""
Execution runner module for PromptOps.

Coordinates the execution of prompts against datasets including
compilation, LLM invocation, and result collection.
"""
import time
import datetime
from typing import List, Dict, Any
from .prompt_compiler import PromptCompiler
from .storage import Storage # We'll implement this next, but referencing it now
from ..llm.client import LLMClient

class Runner:
    """Executes prompts against datasets."""
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        
    def run_batch(self, prompt_version: Dict, dataset: List[Dict], dataset_name: str) -> Dict[str, Any]:
        """
        Runs a batch of inputs from a dataset against a prompt.
        """
        # Generate unique run ID using ISO timestamp
        run_id = datetime.datetime.now().isoformat()
        results = []
        
        # Process each test case in the dataset
        for case in dataset:
            # 1. Compile
            compiled = PromptCompiler.compile(prompt_version, case)
            
            # Measure execution time for latency tracking
            # 2. Execute
            start_time = time.time()
            try:
                output = self.llm_client.generate(
                    system_prompt=compiled["system_prompt"],
                    user_prompt=compiled["user_message"]
                )
            except Exception as e:
                output = f"Error generating response: {e}"
            end_time = time.time()
            latency = end_time - start_time
            
            # Collect run results for this test case
            # 3. Record Result
            results.append({
                "case_id": case.get("id", "unknown"),
                "input_variables": case,
                "prompt_text": compiled["user_message"],
                "output": output,
                "latency": latency,
                # Evaluation will happen in a separate step or here? 
                # The requirements say "Automatically evaluate outputs". 
                # We'll attach raw results first, then evaluator can run on them.
                "evaluation": {} # Placeholder
            })
        
        # Create comprehensive run summary with metadata
        run_summary = {
            "run_id": run_id,
            "timestamp": run_id,
            "prompt_version": prompt_version.get("version", "unknown"),
             "prompt_name": prompt_version.get("name", "unknown"),
            "dataset_id": dataset_name,
            "results": results,
            "metrics": {} # To be filled by evaluator
        }
        
        return run_summary
