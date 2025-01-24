import os
from dataclasses import dataclass
from typing import Optional, Literal
import aiohttp
import json

# Load credentials once at module import
CLIENT_ID = os.getenv("JDOODLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("JDOODLE_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("JDoodle credentials are required. Set JDOODLE_CLIENT_ID and JDOODLE_CLIENT_SECRET environment variables.")


@dataclass
class ExecuteCodeResponse:
    """Response from JDoodle API execution."""
    status: str
    output: Optional[str] = None
    statusCode: Optional[str] = None
    memory: Optional[str] = None
    cpuTime: Optional[str] = None
    compilationStatus: Optional[str] = None
    isCompiled: Optional[bool] = None
    isExecutionSuccess: Optional[bool] = None
    error_message: Optional[str] = None
    
    @classmethod
    def from_api_response(cls, response_data: dict) -> 'ExecuteCodeResponse':
        """Create an ExecuteCodeResponse instance from API response data."""
        if "output" in response_data:
            return cls(
                status="success",
                output=response_data.get("output"),
                statusCode=response_data.get("statusCode"),
                memory=response_data.get("memory"),
                cpuTime=response_data.get("cpuTime"),
                isCompiled=response_data.get("isCompiled"),
                isExecutionSuccess=response_data.get("isExecutionSuccess"),
            )
        return cls(
            status="failed",
            error_message=response_data.get("error", "Unknown error occurred")
        )

    @classmethod
    def error(cls, message: str) -> 'ExecuteCodeResponse':
        """Create an error response."""
        return cls(status="failed", error_message=message)

def _get_version_index(language: str) -> str:
    """Get the version index for a given programming language."""
    version_mapping = {
        "python": ("python3", "4"),
        "go": ("go", "5"),
        "haskell": ("haskell", "5"),
        "rust": ("rust", "5"),
        "ocaml": ("ocaml", "2"),
        "prolog": ("prolog", "2"),
        "ada": ("ada", "2"),
        "cpp": ("cpp17", "1"),
    }
    return version_mapping.get(language, (language, "0"))[1]

def _get_language_name(language: str) -> str:
    """Get the standardized language name for the API."""
    version_mapping = {
        "python": "python3",
        "cpp": "cpp17"
    }
    return version_mapping.get(language, language)

async def execute_code(
    code: str,
    programming_language: str,
    input_data: str = "",
    version_index: Optional[str] = None,
    compile_only: bool = False
) -> ExecuteCodeResponse:
    """
    Asynchronously executes code using the JDoodle API.
    
    Args:
        code: The source code to execute
        programming_language: The programming language (e.g., 'python3', 'java')
        input_data: The input to provide via standard input
        version_index: Version of the language to use
        compile_only: If True, only compile the code without executing
        
    Returns:
        ExecuteCodeResponse containing execution details or error information
    """
    if not version_index:
        version_index = _get_version_index(programming_language)
        
    language = _get_language_name(programming_language)
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "clientId": CLIENT_ID,
        "clientSecret": CLIENT_SECRET,
        "script": code,
        "stdin": input_data,
        "language": language,
        "versionIndex": version_index,
        "compileOnly": compile_only
    }
    
    EXECUTE_URL = "https://api.jdoodle.com/v1/execute"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                EXECUTE_URL,
                headers=headers,
                json=payload
            ) as response:
                response_text = await response.text()
                if response.status != 200:
                    return ExecuteCodeResponse.error(f"HTTP {response.status}: {response_text}")
                
                result = json.loads(response_text)
                return ExecuteCodeResponse.from_api_response(result)
                
    except aiohttp.ClientError as http_err:
        return ExecuteCodeResponse.error(f"HTTP error occurred: {str(http_err)}")
    except Exception as err:
        return ExecuteCodeResponse.error(f"An unexpected error occurred: {str(err)}")
