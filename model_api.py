import os
import httpx
from dotenv import load_dotenv
from openai import AsyncOpenAI
from functools import lru_cache
import asyncio
import json

# Load environment variables
load_dotenv()
OPEN_ROUTER_KEY = os.getenv("OPEN_ROUTER_KEY")
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

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
    
    OLLAMA = {
        "base_url": "http://localhost:11434/api/generate"
    }
    
    GEMINI = {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/models",
        "api_key": GOOGLE_API_KEY
    }
    
    @staticmethod
    def is_valid_provider(provider: str) -> bool:
        return provider in ["open-router", "llama-cpp", "ollama", "gemini"]


async def generate_ollama_response(prompt: str, model: str, **kwargs) -> str:
    """
    Simple async function to get response from local Ollama API.
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        **kwargs
    }
    
    async with httpx.AsyncClient(timeout=1200.0) as client:
        response = await client.post(ProviderConfig.OLLAMA["base_url"], json=payload)
        response.raise_for_status()
        return response.json()['response']

async def generate_gemini_response(prompt: str, model: str, **kwargs) -> str:
    """
    Generate response using Google's Gemini API via REST.
    """
    config = ProviderConfig.GEMINI
    
    # Convert parameters to Gemini format
    generation_config = {}
    if 'temperature' in kwargs:
        generation_config['temperature'] = kwargs['temperature']
    if 'max_tokens' in kwargs:
        generation_config['maxOutputTokens'] = kwargs['max_tokens']
    
    # Prepare the request payload
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": generation_config
    }

    url = f"{config['base_url']}/{model}:generateContent?key={config['api_key']}"
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        
        data = response.json()
        
        # Check for blocked content
        if 'promptFeedback' in data and data['promptFeedback'].get('blockReason'):
            raise ValueError(f"Response was blocked: {data['promptFeedback']['blockReason']}")
        
        # Extract the generated text
        if 'candidates' in data and len(data['candidates']) > 0:
            content = data['candidates'][0]['content']
            if 'parts' in content and len(content['parts']) > 0:
                return content['parts'][0]['text']
        
        raise ValueError("No valid response content found in the API response")

@lru_cache(maxsize=1)
def get_client(provider: str) -> AsyncOpenAI:
    """
    Get or create a singleton client instance based on the provider.
    Uses lru_cache to ensure only one client instance is created per provider.
    
    Args:
        provider: API provider ("open-router", "llama-cpp", "ollama", or "gemini")
    
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
    elif provider == "llama-cpp":
        config = ProviderConfig.LLAMA_CPP
    elif provider in ["gemini", "ollama"]:
        return None  # These providers don't use OpenAI client
    
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
    if provider == "ollama":
        return await generate_ollama_response(prompt, model, **kwargs)
    elif provider == "gemini":
        return await generate_gemini_response(prompt, model, **kwargs)
    
    client = get_client(provider)
    
    if provider == "llama-cpp":
        completion = await client.completions.create(
            model=model,
            prompt=prompt,
            **kwargs
        )
        return completion.content
    else:  # provider == "open-router"
        completion = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return completion.choices[0].message.content


if __name__ == "__main__":
    async def main():
        prompt = "Write 'Hello, World!' in D programming language."
        provider = "gemini"
        model = "gemini-pro"  # or "gemini-pro-vision" for image capabilities
        model = "gemini-1.5-pro"
        model = "gemini-2.0-flash-exp"
        model = "gemini-exp-1206"
        model = "gemini-2.0-flash-exp"
        #model = "gemini-2.0-flash-thinking-exp-01-21"
        
        try:
            response = await make_completion_call(prompt, provider, model)
            print("Generated completion:", response)
        except Exception as e:
            print("Error during completion call:", str(e))

    asyncio.run(main())