import google.generativeai as genai
import os
import base64
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_from_pdf(pdf_path: str):
    """
    Send PDF to Gemini to extract structured data (invoice/PO).
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
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
        return f"Error extracting data from PDF: {str(e)}"
