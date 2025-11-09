import google.generativeai as genai
import os
import base64
from dotenv import load_dotenv
from pathlib import Path

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

def extract_from_pdf(pdf_path: str):
    """
    Send PDF to Gemini to extract structured data (invoice/PO).
    """
    try:
        # Debug: Check if API key is available
        current_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        print(f"DEBUG: API key available: {'Yes' if current_api_key else 'No'}")
        if current_api_key:
            print(f"DEBUG: API key starts with: {current_api_key[:10]}...")
        
        model = genai.GenerativeModel("gemini-2.0-flash")
        with open(pdf_path, "rb") as f:
            pdf_content = f.read()

        # Encode PDF content to base64
        pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')

        prompt = """
        You are a data extraction assistant.
        Extract structured key information from this PDF.
        Return JSON with fields:
        - DocumentType (Invoice or PurchaseOrder)
        - VendorName
        - InvoiceNumber or PONumber
        - Date
        - TotalAmount
        - LineItems: [ {Description, Quantity, UnitPrice, Total} ]
        """

        response = model.generate_content([
            prompt,
            {
                "mime_type": "application/pdf",
                "data": pdf_base64
            }
        ])

        return response.text  # JSON string
    
    except Exception as e:
        print(f"DEBUG: Error in extract_from_pdf: {str(e)}")
        return f"Error extracting data from PDF: {str(e)}"
