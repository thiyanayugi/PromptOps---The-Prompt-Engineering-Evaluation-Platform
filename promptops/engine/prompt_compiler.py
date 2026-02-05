from typing import Dict, Any

class PromptCompiler:
    """Compiles prompts by substituting variables in templates."""
    
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
        system_prompt = prompt_template.get("system_prompt", "")
        user_template = prompt_template.get("user_template", "")
        
        # Basic python string formatting
        try:
            compiled_user_message = user_template.format(**dataset_row)
        except KeyError as e:
            compiled_user_message = f"Error: Missing variable {e} in dataset for template."
        except Exception as e:
            compiled_user_message = f"Error compiling prompt: {str(e)}"
            
        return {
            "system_prompt": system_prompt,
            "user_message": compiled_user_message
        }
