import os
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Optional, Literal
import aiohttp
import json

load_dotenv()

# Load credentials once at module import
CLIENT_ID = os.getenv("JDOODLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("JDOODLE_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("JDoodle credentials are required. Set JDOODLE_CLIENT_ID and JDOODLE_CLIENT_SECRET environment variables.")

@dataclass
class CreditResponse:
    """Response from JDoodle API credit check."""
    status: str
    used: Optional[int] = None
    error_message: Optional[str] = None

    @classmethod
    def from_api_response(cls, response_data: dict) -> 'CreditResponse':
        """Create a CreditResponse instance from API response data."""
        if "used" in response_data:
            return cls(
                status="success",
                used=response_data.get("used")
            )
        return cls(
            status="failed",
            error_message=response_data.get("error", "Unknown error occurred")
        )

    @classmethod
    def error(cls, message: str) -> 'CreditResponse':
        """Create an error response."""
        return cls(status="failed", error_message=message)

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
        "ada": ("ada", "5"),
        "cpp": ("cpp17", "1"),
        "cobol": ("cobol", "4"),
        "julia": ("julia", "0"),
        "fortran": ("fortran", "5"),
        "d": ("d", "3"),
        "groovy": ("groovy", "5"),
    }
    return version_mapping.get(language, (language, "0"))[1]

def _get_language_name(language: str) -> str:
    """Get the standardized language name for the API."""
    version_mapping = {
        "python": "python3",
        "cpp": "cpp17"
    }
    return version_mapping.get(language, language)

async def get_credits_spent() -> CreditResponse:
    """
    Asynchronously check the number of credits spent using the JDoodle API.
    
    Returns:
        CreditResponse containing credit usage details or error information
    """
    headers = {"Content-Type": "application/json"}
    payload = {
        "clientId": CLIENT_ID,
        "clientSecret": CLIENT_SECRET
    }
    
    CREDITS_URL = "https://api.jdoodle.com/v1/credit-spent"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                CREDITS_URL,
                headers=headers,
                json=payload
            ) as response:
                response_text = await response.text()
                if response.status != 200:
                    return CreditResponse.error(f"HTTP {response.status}: {response_text}")
                
                result = json.loads(response_text)
                return CreditResponse.from_api_response(result)
                
    except aiohttp.ClientError as http_err:
        return CreditResponse.error(f"HTTP error occurred: {str(http_err)}")
    except Exception as err:
        return CreditResponse.error(f"An unexpected error occurred: {str(err)}")

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
    print(f"Execute code, in jdoodle_executor.py")
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

async def main():
    """Example usage of both endpoints"""
    # Check credits spent
    credits_response = await get_credits_spent()
    if credits_response.status == "success":
        print(f"Credits used: {credits_response.used}")
    else:
        print(f"Error checking credits: {credits_response.error_message}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())