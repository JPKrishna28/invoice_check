import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def compare_invoice_po(invoice_text: str, po_text: str) -> dict:
    """
    Use Gemini to intelligently compare extracted invoice and PO data.
    """
    model = genai.GenerativeModel("gemini-1.5-pro")

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