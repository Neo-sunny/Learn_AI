import os
import sys
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError, InvalidArgument, ResourceExhausted
from dotenv import load_dotenv

# 1. Load environment variables from the root .env file
# This loads GEMINI_API_KEY into os.environ
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

def initialize_client():
    """Initializes and verifies the Gemini API Client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or "your_gemini_api_key" in api_key:
        print("[ERROR] GEMINI_API_KEY is missing or not set in the .env file.")
        print("Please copy .env.template to .env and configure your key from Google AI Studio.")
        sys.exit(1)
        
    # Configure the global genai client
    genai.configure(api_key=api_key)
    print("[SUCCESS] Gemini Client configured.")

def generate_text_response(prompt: str, system_instruction: str = None, temperature: float = 0.0):
    """
    Calls the Gemini model to generate a text response with optional system instructions and temperature.
    
    Args:
        prompt: The user prompt to send to the model.
        system_instruction: Guidelines or persona that govern the model's behavior.
        temperature: Controls randomness (0.0 = deterministic, 1.0 = creative/random).
    """
    # Using 'gemini-2.5-flash' as the standard, fast, and cost-effective model
    model_name = "gemini-2.5-flash"
    
    # Define generation parameters
    generation_config = genai.types.GenerationConfig(
        temperature=temperature,
        max_output_tokens=1000,
    )
    
    try:
        # Create the model instance
        # You can pass system_instruction directly during model creation
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
            system_instruction=system_instruction
        )
        
        print(f"\n--- Sending Prompt to {model_name} (Temp: {temperature}) ---")
        if system_instruction:
            print(f"System Instruction: \"{system_instruction}\"")
        print(f"Prompt: \"{prompt}\"")
        print("----------------------------------------------------------")
        
        # Call the API to generate content
        response = model.generate_content(prompt)
        
        # Check if the prompt or response was blocked by safety filters
        if response.prompt_feedback.block_reason:
            print(f"[WARNING] Prompt blocked by safety filters: {response.prompt_feedback.block_reason}")
            return
            
        print("\n[Gemini Response]:")
        print(response.text)
        print("----------------------------------------------------------\n")
        
    except InvalidArgument as e:
        print(f"[API ERROR] Invalid configuration or model argument. Check parameter bounds. Details: {e}")
    except ResourceExhausted as e:
        print(f"[API ERROR] Rate limit exceeded or quota exhausted. Details: {e}")
    except GoogleAPIError as e:
        print(f"[API ERROR] A Google API error occurred. Details: {e}")
    except Exception as e:
        print(f"[UNKNOWN ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Initialize the client
    initialize_client()
    
    # Test 1: Simple Prompt
    simple_prompt = "Explain in three bullet points what an API key is and why it must be kept secret."
    generate_text_response(simple_prompt)
    
    # Test 2: Prompt with a specific System Instruction and lower temperature
    # (Low temperature makes the output structure more reliable, great for backend logic)
    system_rules = "You are a  GCP Cloud Architect. Answer technical questions very briefly and with a focus on production safety."
    technical_prompt = "What is the best way to handle temporary database connection losses in a microservice API?"
    
    generate_text_response(
        prompt=technical_prompt,
        system_instruction=system_rules,
        temperature=0.0 # Lower temperature for SRE technical advice
    )
