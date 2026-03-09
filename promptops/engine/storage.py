"""
Data persistence module for PromptOps.

Handles saving and loading run results to/from the filesystem.
"""
import json
import os
from typing import Dict, List, Optional
import glob

class Storage:
    """Handles persistence of results and other data."""
    
    def __init__(self, results_dir: str = "promptops/results"):
        self.results_dir = results_dir
        # Ensure results directory exists on initialization
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)
            
    def save_run(self, run_data: Dict) -> str:
        """Saves a run result to a JSON file. Returns the filename."""
        # Sanitize timestamp for safe filename
        timestamp = run_data.get("timestamp", "").replace(":", "-").replace(".", "-")
        filename = f"run_{timestamp}.json"
        # Build full path for writing
        path = os.path.join(self.results_dir, filename)
        
        try:
            with open(path, "w", encoding="utf-8") as f:
                # Use indent=2 for human-readable output
                json.dump(run_data, f, indent=2)
            return filename
        except Exception as e:
            print(f"Error saving run: {e}")
            return ""

    def load_run(self, filename: str) -> Optional[Dict]:
        """Loads a run result from a JSON file."""
        path = os.path.join(self.results_dir, filename)
        # Return None early if file does not exist
        if not os.path.exists(path):
            return None
            
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading run {filename}: {e}")
            return None

    def list_runs(self) -> List[str]:
        """Lists all run files."""
        # Find all JSON result files in directory
        # Simple glob to find json files
        files = glob.glob(os.path.join(self.results_dir, "*.json"))
        # Return filenames sorted by newest first
        # Return just filenames, sorted by modification time (newest first)
        files.sort(key=os.path.getmtime, reverse=True)
        return [os.path.basename(f) for f in files]
