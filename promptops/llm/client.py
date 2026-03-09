"""
LLM client abstraction and mock implementation.

Provides abstract interface for LLM interactions and a mock client for testing.
"""
import abc
import time
import random

class LLMClient(abc.ABC):
    """Abstract base class for LLM clients."""
    
    @abc.abstractmethod
    def generate(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """Generates a response from the LLM."""
        # Subclasses must implement this method
        pass

class MockLLMClient(LLMClient):
    """Mock LLM client for testing and development."""
    
    def generate(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """Simulates an LLM response."""
        # kwargs accepted for API compatibility but not used in mock
        # Simulate realistic API latency
        time.sleep(0.5) # Simulate latency
        
        # Generate contextual responses based on prompts
        # Simple heuristic to return something relevant based on the user prompt
        # This is just for the demo to look somewhat realistic without an API key
        if "science" in system_prompt.lower() or "science" in user_prompt.lower():
            if "gravity" in user_prompt.lower():
                return "Gravity is like an invisible glue that pulls everything towards the center of the Earth. It keeps us on the ground!"
            elif "photosynthesis" in user_prompt.lower():
                return "Photosynthesis is how plants eat sunlight to grow. They turn light and water into food!"
            
        return f"Mock response to: {user_prompt[:20]}..."
