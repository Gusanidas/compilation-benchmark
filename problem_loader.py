from dataclasses import dataclass
from pathlib import Path
import asyncio
import aiofiles
from typing import Optional, List, Set

@dataclass
class Problem:
    problem_id: str
    problem_statement: str
    input: str
    output: str
    example_input: Optional[str] = None
    example_output: Optional[str] = None

async def read_file_content(file_path) -> Optional[str]:
    try:
        async with aiofiles.open(file_path, 'r') as f:
            return await f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}")
        return None

async def load_problem_from_directory(problem_dir: Path, required_fields: Set[str]) -> Optional[Problem]:
    """
    Common functionality to load a problem from a directory.
    Returns None if required files are missing.
    
    Args:
        problem_dir: Path to the directory containing problem files
        required_fields: Set of required field names (without .txt extension)
    """
    # Check if required files exist
    if not all((problem_dir / f"{field}.txt").exists() 
              for field in required_fields):
        print(f"Directory {problem_dir.name} is missing required files")
        return None
    
    # Create tasks for reading all possible field files
    all_fields = {'problem_statement', 'input', 'output', 'example_input', 'example_output'}
    file_read_tasks = {}
    
    for field in all_fields:
        file_path = problem_dir / f"{field}.txt"
        if file_path.exists():
            file_read_tasks[field] = read_file_content(file_path)
    
    # Wait for all files to be read
    results = await asyncio.gather(*file_read_tasks.values())
    result_dict = dict(zip(file_read_tasks.keys(), results))
    
    # Check if all required fields are present and not None
    if not all(field in result_dict and result_dict[field] is not None 
              for field in required_fields):
        print(f"Failed to read one or more required files in {problem_dir.name}")
        return None
    
    # Add problem_id
    result_dict['problem_id'] = problem_dir.name
    
    # Check if all fields in result_dict match Problem class fields
    valid_fields = set(Problem.__annotations__.keys())
    if not all(field in valid_fields for field in result_dict):
        print(f"Invalid fields found in {problem_dir.name}")
        return None
    
    return Problem(**result_dict)

async def load_aoc_problems() -> List[Problem]:
    """
    Load Advent of Code problems from a directory structure where each subdirectory
    contains the problem files.
    """
    required_fields = {'problem_statement', 'input', 'output'}
    
    dir_path = Path('problems/aoc_problems')
    subdirectories = [d for d in dir_path.iterdir() if d.is_dir()]
    
    problems = []
    for problem_dir in subdirectories:
        if problem := await load_problem_from_directory(problem_dir, required_fields):
            problems.append(problem)
    
    return problems

async def load_problems() -> List[Problem]:
    """
    Load problems from the misc_problems directory.
    """
    required_fields = {'problem_statement', 'input', 'output', 'example_input', 'example_output'}
    
    misc_problems_path = Path('problems/misc_problems')
    if not misc_problems_path.exists():
        print("misc_problems directory does not exist")
        return []
    
    subdirectories = [d for d in misc_problems_path.iterdir() if d.is_dir()]
    subdirectories.sort(key=lambda x: int(x.name) if x.name.isdigit() else float('inf'))
    
    problems = []
    for problem_dir in subdirectories:
        if problem := await load_problem_from_directory(problem_dir, required_fields):
            problems.append(problem)
    
    return problems