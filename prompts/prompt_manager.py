from pathlib import Path
from typing import Dict, List, Optional, Any

from problem_loader import Problem
from jdoodle_executor import ExecuteCodeResponse


def _read_prompts(prompt_dir: str, prompt_names: List[str]) -> Dict[str, str]:
    dir_path = Path(prompt_dir)

    if not dir_path.exists():
        raise FileNotFoundError(f"Directory not found: {prompt_dir}")
    if not dir_path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {prompt_dir}")

    prompts: Dict[str, str] = {}

    for prompt_name in prompt_names:
        file_path = dir_path / f"{prompt_name}.txt"
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                prompts[prompt_name] = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file not found: {file_path}")
        except IOError as e:
            raise IOError(f"Error reading {file_path}: {str(e)}")

    return prompts


_prompt_dir = "prompts"

_prompt_list = [
    "rust_prompt",
    "python_prompt",
    "cpp_prompt",
    "haskell_prompt",
    "ocaml_prompt",
    "rust_aoc_prompt",
    "python_aoc_prompt",
    "cpp_aoc_prompt",
    "haskell_aoc_prompt",
    "ocaml_aoc_prompt",
    "go_prompt",
    "go_aoc_prompt",
    "ada_aoc_prompt",
    "ada_prompt",
    "julia_prompt",
    "cobol_prompt",
    "d_prompt",
    "fortran_prompt",
    "groovy_prompt",
]

prompts = _read_prompts(_prompt_dir, _prompt_list)

base_prompt = """
{language_prompt}

Problem statement:
{problem_statement}

Example input (via stdin):
{example_input}

Example output:
{example_output}
"""

correction_prompt = """
To solve this problem:

{problem_statement}

You provided the following code in {programming_language}:

{code}

The code produced the following output:

{output}

And the following error:

{error}

Please correct the code and try again.
Your response should only contain a single code block containing the whole corrected code.
Do not write only the changes, write the whole code block.
The code should compile and run successfully.
"""


def get_prompt(programming_language: str, problem: Problem) -> str:
    if "aoc" in problem.problem_id:
        return get_prompt_aoc(programming_language, problem)
    else:
        return get_prompt_misc(programming_language, problem)


def get_prompt_misc(programming_language: str, problem: Problem) -> str:
    problem_statement = problem.problem_statement
    example_input = problem.example_input
    example_output = problem.example_output

    if programming_language == "rust":
        language_prompt = prompts["rust_prompt"]
    elif programming_language == "python":
        language_prompt = prompts["python_prompt"]
    elif programming_language == "haskell":
        language_prompt = prompts["haskell_prompt"]
    elif programming_language == "cpp":
        language_prompt = prompts["cpp_prompt"]
    elif programming_language == "go":
        language_prompt = prompts["go_prompt"]
    elif programming_language == "ocaml":
        language_prompt = prompts["ocaml_prompt"]
    elif programming_language == "ada":
        language_prompt = prompts["ada_prompt"]
    elif programming_language == "julia":
        language_prompt = prompts["julia_prompt"]
    elif programming_language == "cobol":
        language_prompt = prompts["cobol_prompt"]
    elif programming_language == "d":
        language_prompt = prompts["d_prompt"]
    elif programming_language == "fortran":
        language_prompt = prompts["fortran_prompt"]
    elif programming_language == "groovy":
        language_prompt = prompts["groovy_prompt"]
    else:
        raise ValueError(
            f"Unsupported prompt for programming language: {programming_language}"
        )

    return base_prompt.format(
        language_prompt=language_prompt,
        problem_statement=problem_statement,
        example_input=example_input,
        example_output=example_output,
    )


def get_prompt_aoc(programming_language: str, problem: Problem) -> str:
    problem_statement = problem.problem_statement

    if programming_language == "rust":
        language_prompt = prompts["rust_aoc_prompt"]
    elif programming_language == "python":
        language_prompt = prompts["python_aoc_prompt"]
    elif programming_language == "haskell":
        language_prompt = prompts["haskell_aoc_prompt"]
    elif programming_language == "cpp":
        language_prompt = prompts["cpp_aoc_prompt"]
    elif programming_language == "go":
        language_prompt = prompts["go_aoc_prompt"]
    elif programming_language == "ocaml":
        language_prompt = prompts["ocaml_aoc_prompt"]
    elif programming_language == "ada":
        language_prompt = prompts["ada_aoc_prompt"]
    else:
        raise ValueError(
            f"Unsupported prompt for programming language: {programming_language}"
        )

    return language_prompt + "\n" + problem_statement


def get_correction_prompt(
    programming_language: str,
    problem: Problem,
    code: str,
    api_response: ExecuteCodeResponse,
) -> str:
    output = api_response.output or ""
    error = api_response.error_message or ""

    problem_statement = problem.problem_statement

    return correction_prompt.format(
        problem_statement=problem_statement,
        programming_language=programming_language,
        code=code,
        output=output,
        error=error,
    )
