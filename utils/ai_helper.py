import google.generativeai as genai
import os

# Configure Gemini AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "your-default-key")
genai.configure(api_key=GOOGLE_API_KEY)

def get_ai_response(query):
    """
    Get response from Gemini AI for financial queries
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        # Add financial context to the prompt
        prompt = f"""As a financial expert, please answer the following question:
        {query}
        
        Please provide a clear and concise response with any relevant financial insights."""
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise Exception(f"Error with Gemini AI: {str(e)}")
