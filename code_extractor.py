import re
from typing import Optional


def extract_code(text, language) -> Optional[str]:
    """
    Extracts code blocks for a specific programming language from text.
    Only looks for code blocks marked with ```language and ```.
    
    Args:
        text (str): Text containing code blocks
        language (str): Programming language to look for (e.g., 'python', 'rust', 'ocaml')
        
    Returns:
        str: First matching code block found, or None if no code block is found
    """

    pattern = rf"```{language}\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    
    return None