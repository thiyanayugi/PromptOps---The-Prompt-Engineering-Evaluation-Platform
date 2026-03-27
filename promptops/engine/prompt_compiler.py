"""
Prompt compilation module for PromptOps.

Handles template variable substitution to generate final prompts.
"""
from typing import Dict, Any

class PromptCompiler:
    """Compiles prompts by substituting variables in templates."""
    
    # Stateless utility: no class state needed
    @staticmethod
    def compile(prompt_template: Dict[str, Any], dataset_row: Dict[str, Any]) -> Dict[str, str]:
        """
        Substitutes variables from the dataset row into the prompt user_template.
        
        Args:
            prompt_template: The prompt definition (must contain 'system_prompt' and 'user_template').
            dataset_row: A dictionary containing values to substitute into the template.
            
        Returns:
            A dictionary with 'system_prompt' and compiled 'user_message'.
        """
        # Extract system and user templates from prompt definition
        # Use .get() to avoid KeyError if system_prompt is missing
        system_prompt = prompt_template.get("system_prompt", "")
        # Use .get() to avoid KeyError if user_template is missing
        user_template = prompt_template.get("user_template", "")
        
        # Use Python str.format() for template variable substitution
        # Basic python string formatting
        try:
            compiled_user_message = user_template.format(**dataset_row)
        except KeyError as e:
            # Dataset row is missing a variable required by the template
            compiled_user_message = f"Error: Missing variable {e} in dataset for template."
        except Exception as e:
            # Catch any other unexpected formatting errors
            compiled_user_message = f"Error compiling prompt: {str(e)}"
        
        # Return compiled prompt with system and user components
        return {
            "system_prompt": system_prompt,
            "user_message": compiled_user_message
        }
