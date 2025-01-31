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
    temperature: Optional[float] = None

    @classmethod
    def build_from_api_response(
        cls,
        problem: Problem,
        model: str,
        programming_language: str,
        api_response: ExecuteCodeResponse,
        code: Optional[str] = None,
        **kwargs,
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

        # Check for temperature in kwargs
        temperature = kwargs.get("temperature")

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
            temperature=temperature,
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
        if self.temperature is None:
            data.pop("temperature")
        return data


def compare_outputs(output: str, expected_output: str) -> bool:
    if output is None or expected_output is None or len(output) < 1:
        return False
    
    # Get non-empty lines and convert to lowercase
    output_lines = [line.lower().strip() for line in output.splitlines() if line.strip()]
    expected_lines = [line.lower().strip() for line in expected_output.splitlines() if line.strip()]
    
    output_iter = iter(output_lines)
    
    def normalize_number_list(line: str) -> str:
        # Check if the line appears to be a list of numbers
        # First, try splitting by comma and/or spaces
        potential_numbers = line.replace(',', ' ').split()
        
        # Check if all elements are numbers
        try:
            numbers = [float(num) for num in potential_numbers]
            # If successful, return space-separated numbers
            return ' '.join(str(num) for num in numbers)
        except ValueError:
            # If not all elements are numbers, return the original line
            return line
    
    for expected_line in expected_lines:
        try:
            output_line = next(output_iter)
        except StopIteration:
            return False
            
        # Normalize both lines
        expected_normalized = normalize_number_list(expected_line)
        output_normalized = normalize_number_list(output_line)
        
        if output_normalized != expected_normalized:
            return False
            
    # Check for any remaining non-empty lines
    #for remaining_line in output_iter:
    #    if remaining_line.strip():
    #        return False
            
    return True


def clean_output(output: str, programming_language: str = "") -> str:
    """
    Cleans the output string by removing unwanted lines based on the programming language.
    
    Args:
        output: The raw output string to clean
        programming_language: The programming language of the executed code (case insensitive)
        
    Returns:
        A cleaned string with unwanted lines removed
    """
    # Convert programming_language to lowercase for case-insensitive comparison
    programming_language = programming_language.lower()
    
    cleaned_lines = []
    
    # Split the output into lines for processing
    lines = output.splitlines()
    
    for line in lines:
        # Skip any line containing 'jdoodle' (case insensitive)
        if "jdoodle" in line.lower():
            continue
            
        # For ADA specifically, skip compilation and linking messages
        if programming_language == "ada":
            # Skip gcc compilation messages
            if line.startswith("gcc -c"):
                continue
            # Skip warning about file name
            if "warning: file name does not match" in line:
                continue
            # Skip gnatbind and gnatlink messages
            if line.startswith("gnatbind") or line.startswith("gnatlink"):
                continue
                
        # If we haven't skipped the line, add it to our cleaned lines
        cleaned_lines.append(line)
    
    # Join the remaining lines back together
    return "\n".join(cleaned_lines)