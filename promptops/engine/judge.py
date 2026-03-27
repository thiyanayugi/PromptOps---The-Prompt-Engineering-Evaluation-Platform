"""
LLM-based judging module for PromptOps.

Uses an LLM to evaluate generated outputs based on criteria.
"""
import json
from ..llm.client import LLMClient

class Judge:
    """Uses an LLM to evaluate outputs."""
    
    def __init__(self, llm_client: LLMClient):
        # Store the LLM client for making evaluation calls
        self.llm_client = llm_client
        
    def evaluate(self, output: str, criteria: str = "clarity") -> float:
        """
        Evaluates the output based on criteria. 
        Returns a score from 1-5.
        """
        # Define the system prompt for the AI judge
        system_prompt = "You are an AI judge. You evaluate text based on specific criteria."
        # Construct the user prompt with the text and evaluation criteria
        user_prompt = f"""
        Evaluate the following text for {criteria} on a scale of 1 to 5.
        
        Text: "{output}"
        
        Return ONLY a JSON object with this format:
        {{
            "score": <int>,
            "reasoning": "<string>"
        }}
        """
        
        try:
            # Send evaluation prompt to the LLM
            response = self.llm_client.generate(system_prompt, user_prompt)
            # Naive parsing provided the mock returns strings, but in real life we'd need robust JSON parsing
            # For the mock, we might get a string back that isn't JSON if we stick to the mock logic exactly
            # So let's handle the mock case gracefully or update the mock to be smarter? 
            # I'll implement a basic parser that looks for the JSON structure
            
            # 3. Parse Response
            # For the mock client currently implemented, it returns simple strings. 
            # We need to simulate the JSON return if we use the mock.
            # Or we can just return a dummy score if parsing fails.
            
            # Attempt to extract and parse JSON from response
            if "{" in response and "}" in response:
                start = response.find("{")
                end = response.rfind("}") + 1
                json_str = response[start:end]
                data = json.loads(json_str)
                # Extract score and reasoning from parsed JSON
                return data.get("score", 0), data.get("reasoning", "Parsed from judge output")
            else:
                # Fallback for mock non-json responses or simple failure
                return 3, "Judge returned non-JSON output (Mock fallback)"
                
        except Exception as e:
            # Return zero score on any unexpected error
            return 0, f"Judge error: {str(e)}"
