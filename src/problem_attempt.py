from src.model_api import make_completion_call
from src.prompt_manager import get_prompt
from src.jdoodle_executor import execute_code
from src.code_extractor import extract_code
from src.simple_agent import agent_attempt_solution
from src.problem_attempt_result import ProblemAttemptResult
from src.problem_loader import Problem


async def attempt_problem(
    model: str, programming_language: str, problem: Problem, provider: str, **kwargs
) -> ProblemAttemptResult:
    """
    Attempt to solve a problem using a given model and programming language.

    Args:
        model: The model to use
        programming_language: The programming language to use
        problem: The problem to solve
        provider: OpenRouter or Llama.cpp
    """

    if model.startswith("agent"):
        return await agent_attempt_solution(
            model=model,
            programming_language=programming_language,
            problem=problem,
            provider=provider,
            **kwargs,
        )
    else:
        return await attempt_zero_shot_solution(
            model=model,
            problem=problem,
            programming_language=programming_language,
            provider=provider,
            **kwargs,
        )


async def attempt_zero_shot_solution(
    model: str, problem: Problem, programming_language: str, provider: str, **kwargs
) -> ProblemAttemptResult:
    """
    Attempt to solve a problem using a zero-shot approach.

    Args:
        model: The model to use
        problem: The problem to solve
        programming_language: The programming language to use

    Returns:
        A ProblemAttemptResult instance representing the result of the attempt
    """

    try:
        prompt = get_prompt(programming_language, problem)
        content = await make_completion_call(prompt, provider, model=model)

        code = extract_code(content, programming_language)
        if code is None:
            return ProblemAttemptResult.from_exception(
                error_message="No code could be extracted from the completion",
                problem_id=problem.problem_id,
                model=model,
                programming_language=programming_language,
            )

        problem_input = problem.input
        api_response = await execute_code(code, programming_language, problem_input)
        if api_response.status == "failed":
            return ProblemAttemptResult.from_exception(
                error_message=api_response.error_message or "",
                problem_id=problem.problem_id,
                model=model,
                programming_language=programming_language,
                code=code,
            )
        else:
            return ProblemAttemptResult.build_from_api_response(
                problem=problem,
                model=model,
                programming_language=programming_language,
                api_response=api_response,
                code=code,
            )

    except Exception as e:
        print(f"Exception, model {model}, programming_language {programming_language}")
        print(f"Exception: {e}")
        return ProblemAttemptResult.from_exception(
            error_message=str(e),
            problem_id=problem.problem_id,
            model=model,
            programming_language=programming_language,
        )

