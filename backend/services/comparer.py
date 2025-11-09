import google.generativeai as genai
import os
from dotenv import load_dotenv
from pathlib import Path
from .parser import parse_gemini_json_response

# Load environment variables from multiple possible locations
env_path = Path(__file__).parent.parent / '.env'  # backend/.env
load_dotenv(env_path)
root_env_path = Path(__file__).parent.parent.parent / '.env'  # root/.env
load_dotenv(root_env_path)

# Configure Gemini with API key
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("No API key found. Please set GOOGLE_API_KEY or GEMINI_API_KEY in your .env file")

genai.configure(api_key=api_key)

def compare_invoice_po(invoice_text: str, po_text: str) -> dict:
    """
    Use Gemini to intelligently compare extracted invoice and PO data.
    """
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
    You are an expert document reconciliation agent.
    Compare the following Invoice and Purchase Order content.
    Highlight:
    - Matching fields (like Invoice Number, Date, Amount, Vendor)
    - Differences or mismatches
    - Missing information in either file

    Output the result as structured JSON with keys:
    {{
        "matches": [...],
        "mismatches": [...],
        "summary": "..."
    }}

    --- INVOICE CONTENT ---
    {invoice_text}

    --- PURCHASE ORDER CONTENT ---
    {po_text}
    """

    try:
        response = model.generate_content(prompt)
        return {"comparison": response.text}
    except Exception as e:
        return {"error": str(e)}
def extract_text_from_gemini_response(response_text: str) -> str:
    """
    Extract plain text content from Gemini response.
    """
    # Assuming the response is plain text for simplicity
    return response_text