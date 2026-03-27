"""
Evaluation orchestration module for PromptOps.

Coordinates the evaluation process including rule-based and LLM-based
assessment of generated outputs.
"""
from typing import Dict, Any, List
from .judge import Judge

class Evaluator:
    """Orchestrates evaluation of run results."""
    
    
    # Initialize with a judge instance for quality assessment
    def __init__(self, judge: Judge):
        self.judge = judge
        
    def evaluate_run(self, run_results: List[Dict]) -> List[Dict]:
        """
        Takes a list of raw run results and adds evaluation scores.
        """
        # Collect evaluated results to return
        evaluated_results = []
        # Iterate through each run result to apply evaluation metrics
        for result in run_results:
            # Extract the generated text output for evaluation
            output = result.get("output", "")
            
            # Calculate basic word count metric
            # 1. Rule-based checks
            # Calculate simple word count metric (integer)
            word_count = len(output.split())
            
            # Invoke LLM judge for quality assessment
            # 2. LLM Judge
            # Expects a tuple of (score, reasoning_string) from judge
            clarity_score, reasoning = self.judge.evaluate(output, criteria="clarity")
            
            # Build evaluation results dictionary
            # Update result with evals
            result["evaluation"] = {
                "word_count": word_count,
                "clarity_score": clarity_score,
                "reasoning": reasoning
            }
            # Append enriched result to output list
            evaluated_results.append(result)
            
        # Return the fully evaluated list of results
        return evaluated_results
