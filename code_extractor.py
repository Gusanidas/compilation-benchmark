import re
from typing import Optional


def extract_code(text, language) -> Optional[str]:
    pattern = rf"```{language}\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    
    if matches:
        return matches[-1].strip()
    
    return None