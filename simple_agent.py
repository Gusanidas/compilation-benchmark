from typing import Optional, Any, Dict, Tuple, List
import asyncio
from jdoodle_executor import ExecuteCodeResponse, execute_code
from code_extractor import extract_code
from problem_attempt_result import ProblemAttemptResult
from prompts.prompt_manager import get_correction_prompt, get_prompt
from model_api import make_completion_call
from problem_loader import Problem

# Default configuration values
DEFAULT_MAX_ATTEMPTS = 5
DEFAULT_MIN_CORRECT = 1
DEFAULT_INITIAL_ATTEMPTS = 3

async def agent_attempt_solution(
    model: str,
    programming_language: str,
    problem: Problem,
    provider: str,
    max_attempts: int = DEFAULT_MAX_ATTEMPTS,
    min_correct: int = DEFAULT_MIN_CORRECT,
    initial_attempts: int = DEFAULT_INITIAL_ATTEMPTS,
    **kwargs
) -> ProblemAttemptResult:
    """
    Attempt to solve a programming problem using an LLM API.
    
    Args:
        client: The API client instance
        model: The model identifier string
        programming_language: Target programming language
        problem: Dictionary containing problem details
        max_attempts: Maximum number of retry attempts
        min_correct: Minimum number of successful evaluations needed
        initial_attempts: Number of initial attempts to generate code
        **kwargs: Additional keyword arguments for API calls
    
    Returns:
        ProblemAttemptResult: Object containing the attempt results
    """
    if model.startswith("agent") and "_" in model:
        _, model = model.split("_")

    total = 0
    successful_attempts = []
    code_error_attempts = []
    
    while total < max_attempts:
        tasks = []
        for i in range(max(1, initial_attempts - len(code_error_attempts))):
            prompt = get_prompt(programming_language, problem)
            tasks.append(_single_attempt(
                model,
                prompt,
                programming_language,
                problem,
                provider,
                **kwargs
            ))

        for i in range(min(len(code_error_attempts), initial_attempts)):
            code, api_response = code_error_attempts[i]
            prompt = get_correction_prompt(programming_language, problem, code, api_response)
            tasks.append(_single_attempt(
                model,
                prompt,
                programming_language,
                problem,
                provider,
                **kwargs
            ))

        results = await asyncio.gather(*tasks)
        new_successful_attempts, new_code_error_attempts = _classify_attempts(results)
        successful_attempts.extend(new_successful_attempts)
        code_error_attempts.extend(new_code_error_attempts)

        total += len(results)

        if len(successful_attempts) >= min_correct:
            break
    
    return _get_final_result(successful_attempts, code_error_attempts, problem, "agent_"+model, programming_language)

async def _single_attempt(
    model: str,
    prompt: str,
    programming_language: str,
    problem: Problem,
    provider: str,
    **kwargs
) -> Tuple[bool, Optional[str], Optional[ExecuteCodeResponse]]:
    """
    Make a single attempt at generating and executing code for the problem.
    
    Returns:
        Tuple containing success status, generated code, and API response
    """
    try:
        content = await make_completion_call(prompt, provider, model, **kwargs)
        code = extract_code(content, programming_language)
        
        if code is None:
            return False, None, None

        api_response = await execute_code(
            code,
            programming_language,
            problem.input,
        )
        
        return True, code, api_response
    except Exception as e:
        print(f"Error during code generation and evaluation: {e}")
        return False, None, ExecuteCodeResponse.error(str(e))

def _classify_attempts(
    attempts: List[Tuple[bool, Optional[str], ExecuteCodeResponse]]
) -> Tuple[List[Tuple[str, Dict[str, Any]]], List[Tuple[str, Dict[str, Any]]]]:
    """
    Classify attempts into successful and failed attempts.
    
    Returns:
        Tuple of (successful_attempts, code_error_attempts)
    """
    successful_attempts = []
    code_error_attempts = []
    for success, code, api_response in attempts:
        if not success:
            continue
        compilation_success = api_response.isCompiled
        runtime_success = api_response.isExecutionSuccess
        if compilation_success and runtime_success:
            successful_attempts.append((code, api_response))
        else:
            code_error_attempts.append((code, api_response))
    return successful_attempts, code_error_attempts

def _get_final_result(
    successful_attempts: List[Tuple[str, ExecuteCodeResponse]],
    code_error_attempts: List[Tuple[str, ExecuteCodeResponse]],
    problem: Problem,
    model: str,
    programming_language: str
) -> ProblemAttemptResult:
    """
    Determine the final result based on all attempts.
    
    Returns:
        ProblemAttemptResult: The final attempt result
    """
    if len(successful_attempts) < 1 and len(code_error_attempts) > 0:
        code, api_response = code_error_attempts[0]
        return ProblemAttemptResult.build_from_api_response(
            api_response=api_response,
            problem=problem,
            model=model,
            programming_language=programming_language,
            code=code
        )
    elif len(successful_attempts) > 0:
        votes_by_output = {}
        for code, api_response in successful_attempts:
            output = api_response.output
            output = "" if output is None else output
            output = output.strip()
            votes_by_output[output] = votes_by_output.get(output, 0) + 1
        best_output = max(votes_by_output, key=lambda k: votes_by_output.get(k, 0))
        for code, api_response in successful_attempts:
            output = api_response.output
            output = "" if output is None else output
            output = output.strip()
            if output == best_output:
                return ProblemAttemptResult.build_from_api_response(
                    api_response=api_response,
                    problem=problem,
                    model=model,
                    programming_language=programming_language
                )
    return ProblemAttemptResult.from_exception(
        "No successful attempts",
        problem_id=problem.problem_id,
        model=model,
        programming_language=programming_language
    )