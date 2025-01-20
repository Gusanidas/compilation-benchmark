from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
from jdoodle_executor import  ExecuteCodeResponse
from problem_loader import Problem

@dataclass
class ProblemAttemptResult:
    problem_id: str
    programming_language: str
    model: str
    compilation_success: bool
    runtime_success: bool
    problem_correct: bool
    success: bool
    output: Optional[str]
    code_errors: Optional[str]
    attempt_error: Optional[str]
    code: Optional[str]

    @classmethod
    def build_from_api_response(
        cls,
        problem: Problem,
        model: str,
        programming_language: str,
        api_response: ExecuteCodeResponse,
        code: Optional[str] = None,
    ) -> "ProblemAttemptResult":
        """
        Builds a ProblemAttemptResult instance from the new API response format.
        Args:
            problem: Dictionary containing problem details including ID and expected output
            model: The model used for execution
            programming_language: The programming language used
            api_response: The API response dictionary containing execution results
            code: Optional code that was executed
        Returns:
            A ProblemAttemptResult instance populated with the API response data
        """
        problem_id, expected_output = problem.problem_id, problem.output

        # Extract status information
        if api_response.isCompiled is not None and api_response.isCompiled:
            compilation_success = True
        else:
            compilation_success = api_response.compilationStatus == 0
        if api_response.isExecutionSuccess is not None and api_response.isExecutionSuccess:
            runtime_success = True
        else:
            runtime_success = api_response.error_message is None or len(api_response.error_message) < 1

        if not compilation_success:
            runtime_success = False

        # Get output and errors
        output = api_response.output
        output = "" if output is None else output
        output = clean_output(output)
        attempt_error = api_response.error_message

        # Check if the output matches expected result
        # Only check if execution was successful
        problem_correct = False
        if runtime_success:
            problem_correct = compare_outputs(output, expected_output)

        success = True

        # Code errors are now contained in the output field when execution fails
        code_errors = output if not runtime_success else None

        return cls(
            problem_id=problem_id,
            programming_language=programming_language,
            model=model,
            compilation_success=compilation_success,
            runtime_success=runtime_success,
            problem_correct=problem_correct,
            success=success,
            output=output if runtime_success else None,
            code_errors=code_errors,
            attempt_error=attempt_error,
            code=code,
        )

    @classmethod
    def from_exception(
        cls,
        error_message: str,
        problem_id: str,
        model: str,
        programming_language: str,
        code: Optional[str] = None,
    ) -> "ProblemAttemptResult":
        """
        Creates a ProblemAttemptResult instance from an error message.

        Args:
            error_message: The error message to be stored
            problem_id: The ID of the problem
            model: The model used
            programming_language: The programming language used
            code: Optional code that was attempted

        Returns:
            A ProblemAttemptResult instance representing a failed attempt
        """
        return cls(
            problem_id=problem_id,
            programming_language=programming_language,
            model=model,
            compilation_success=False,
            problem_correct=False,
            runtime_success=False,
            success=False,
            output=None,
            code_errors=None,
            attempt_error=error_message,
            code=code,
        )

    def to_writable_dict(self) -> Dict[str, Any]:
        """
        Converts the instance to a dictionary that can be written to a JSONL file.

        Args:
            filename: The path to the JSONL file to write to
        """
        # Convert instance to dictionary and remove excluded fields
        data = asdict(self)
        data.pop("attempt_error")
        data.pop("success")
        return data


def compare_outputs(output: str, expected_output: str) -> bool:
    if output is None or expected_output is None or len(output) < 1:
        return False
    output_lines = [line for line in output.splitlines() if line.strip()]
    expected_lines = [line for line in expected_output.splitlines() if line.strip()]

    output_iter = iter(output_lines)
    
    for expected_line in expected_lines:
        try:
            output_line = next(output_iter)
        except StopIteration:
            return False

        if output_line.strip() != expected_line.strip():
            return False

    for remaining_line in output_iter:
        if remaining_line.strip():  
            return False

    return True


def clean_output(output: str) -> str:
    cleaned_lines = []
    for line in output.splitlines():
        if "jdoodle" not in line.lower():
            cleaned_lines.append(line)
    return "\n".join(cleaned_lines)