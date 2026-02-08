"""
Evaluation orchestration module for PromptOps.

Coordinates the evaluation process including rule-based and LLM-based
assessment of generated outputs.
"""
from typing import Dict, Any, List
from .judge import Judge

class Evaluator:
    """Orchestrates evaluation of run results."""
    
    def __init__(self, judge: Judge):
        self.judge = judge
        
    def evaluate_run(self, run_results: List[Dict]) -> List[Dict]:
        """
        Takes a list of raw run results and adds evaluation scores.
        """
        evaluated_results = []
        for result in run_results:
            output = result.get("output", "")
            
            # Calculate basic word count metric
            # 1. Rule-based checks
            word_count = len(output.split())
            
            # Invoke LLM judge for quality assessment
            # 2. LLM Judge
            clarity_score, reasoning = self.judge.evaluate(output, criteria="clarity")
            
            # Build evaluation results dictionary
            # Update result with evals
            result["evaluation"] = {
                "word_count": word_count,
                "clarity_score": clarity_score,
                "reasoning": reasoning
            }
            evaluated_results.append(result)
            
        return evaluated_results
