from typing import List, Dict, Any

class Metrics:
    """Computes aggregated metrics for a run."""
    
    @staticmethod
    def compute(evaluated_results: List[Dict]) -> Dict[str, Any]:
        """
        Aggregates metrics from a list of evaluated results.
        """
        total = len(evaluated_results)
        if total == 0:
            return {}
            
        total_clarity = 0
        total_latency = 0
        total_words = 0
        
        for res in evaluated_results:
            evals = res.get("evaluation", {})
            total_clarity += evals.get("clarity_score", 0)
            total_words += evals.get("word_count", 0)
            total_latency += res.get("latency", 0)
            
        return {
            "total_runs": total,
            "avg_clarity_score": round(total_clarity / total, 2),
            "avg_latency_seconds": round(total_latency / total, 4),
            "avg_word_count": round(total_words / total, 1)
        }
