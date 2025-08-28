from google import genai
from google.genai import types
from .config import GEMINI_API_KEY, MODEL_NAME, SYSTEM_INSTRUCTION
from .cache import get_cached_response, cache_response

# Initialize client
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

def generate_response(prompt: str) -> str:
    """
    Generate a response using Gemini AI or return cached result.
    
    Args:
        prompt: The user's input prompt
        
    Returns:
        str: The AI-generated response or error message
    """
    # Check cache first
    if cached := get_cached_response(prompt):
        return cached
    
    # Validate client configuration
    if not client:
        return "Error: Gemini API not configured"
    
    try:
        # Generate response from Gemini
        response = client.models.generate_content(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                max_output_tokens=100,
                temperature=0.7,
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            ),
            contents=prompt
        )
        
        response_text = response.text if response.text is not None else ""
        cache_response(prompt, response_text)
        return response_text
        
    except Exception as e:
        error_msg = f"Error: {type(e).__name__}"
        return error_msg