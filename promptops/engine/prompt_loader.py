"""
Module for loading and managing prompt versions from the filesystem.

This module provides the PromptLoader class which handles reading
and parsing JSON-based prompt configuration files.
"""
import json
import os
from typing import List, Dict, Optional

class PromptLoader:
    """Loads prompt versions from the filesystem."""
    
    def __init__(self, prompts_dir: str = "promptops/prompts"):
        self.prompts_dir = prompts_dir
        
    def list_prompts(self) -> List[str]:
        """Returns a list of available prompt filenames."""
        # Check if prompts directory exists before listing
        if not os.path.exists(self.prompts_dir):
            return []
        return [f for f in os.listdir(self.prompts_dir) if f.endswith(".json")]

    def load_prompt(self, filename: str) -> Optional[Dict]:
        """Loads a specific prompt file."""
        path = os.path.join(self.prompts_dir, filename)
        if not os.path.exists(path):
            return None
            
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading prompt {filename}: {e}")
            return None
