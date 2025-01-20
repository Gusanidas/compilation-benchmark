import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from functools import lru_cache

# Load environment variables
load_dotenv()
OPEN_ROUTER_KEY = os.getenv("OPEN_ROUTER_KEY")

# Track the first provider used
_INITIALIZED_PROVIDER = None

class ProviderConfig:
    OPEN_ROUTER = {
        "base_url": "https://openrouter.ai/api/v1",
        "api_key": OPEN_ROUTER_KEY
    }
    
    LLAMA_CPP = {
        "base_url": "http://localhost:8080/v1",
        "api_key": "sk-no-key-required"
    }

    @staticmethod
    def is_valid_provider(provider: str) -> bool:
        return provider in ["open-router", "llama-cpp"]

@lru_cache(maxsize=1)
def get_client(provider: str) -> AsyncOpenAI:
    """
    Get or create a singleton client instance based on the provider.
    Uses lru_cache to ensure only one client instance is created per provider.
    
    Args:
        provider: API provider ("open-router" or "llama-cpp")
    
    Returns:
        AsyncOpenAI: The client instance
        
    Raises:
        ValueError: If provider is not supported or different from first initialization
    """
    if not ProviderConfig.is_valid_provider(provider):
        raise ValueError(f"Unsupported provider: {provider}")
    
    global _INITIALIZED_PROVIDER
    if _INITIALIZED_PROVIDER is None:
        _INITIALIZED_PROVIDER = provider
    elif _INITIALIZED_PROVIDER != provider:
        raise ValueError(
            f"Cannot switch providers during runtime. "
            f"First call was made with '{_INITIALIZED_PROVIDER}', "
            f"but attempting to use '{provider}'"
        )
    
    if provider == "open-router":
        config = ProviderConfig.OPEN_ROUTER
    else:  # provider == "llama-cpp"
        config = ProviderConfig.LLAMA_CPP
    
    return AsyncOpenAI(
        base_url=config["base_url"],
        api_key=config["api_key"],
    )

async def make_completion_call(
    prompt: str,
    provider: str,
    model: str,
    **kwargs
) -> str:
    """
    Asynchronously makes a completion call to a specified provider's model.
    Args:
        prompt (str): The input prompt to generate a completion for.
        provider (str): The name of the provider to use for the completion.
        model (str): The model identifier to use for the completion.
        **kwargs: Additional keyword arguments to pass to the completion request.
    Returns:
        str: The generated completion text.
    Raises:
        Exception: If the completion call fails or the response is invalid.
    """
    client = get_client(provider)
    
    completion = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
    return completion.choices[0].message.content