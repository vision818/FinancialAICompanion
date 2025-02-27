import google.generativeai as genai
import os

# Configure Gemini AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

genai.configure(api_key=GOOGLE_API_KEY)

def get_ai_response(query):
    """
    Get response from Gemini AI for financial queries
    """
    try:
        model = genai.GenerativeModel('gemini-pro')

        # Add financial context to the prompt
        prompt = f"""As a financial expert AI assistant, please provide a detailed response to the following question:

        Question: {query}

        Please include:
        - Clear explanations of financial concepts
        - Relevant market insights if applicable
        - Practical advice or recommendations
        - Data-driven analysis where relevant

        Keep the response professional but easy to understand."""

        response = model.generate_content(prompt)
        if not response.text:
            raise Exception("Empty response received from AI")
        return response.text
    except Exception as e:
        error_msg = str(e)
        if "API_KEY_INVALID" in error_msg:
            raise Exception("Invalid API key. Please check your Google API key configuration.")
        raise Exception(f"Error with Gemini AI: {error_msg}")