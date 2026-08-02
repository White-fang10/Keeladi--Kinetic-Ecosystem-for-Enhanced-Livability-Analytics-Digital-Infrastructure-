import google.generativeai as genai
from app.core.config import settings

def get_gemini_model(model_name: str = "gemini-1.5-flash"):
    """
    Initializes and returns a Gemini model instance.
    Defaults to gemini-1.5-flash for speed and multi-modal support.
    """
    if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "your_gemini_api_key_here":
        # Return a mock or raise an error in production, but for MVP we configure it if available
        pass
        
    genai.configure(api_key=settings.GEMINI_API_KEY)
    
    # Configure the model to return JSON structure where required
    generation_config = {
        "temperature": 0.2,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 1024,
        "response_mime_type": "application/json",
    }
    
    return genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config,
    )
