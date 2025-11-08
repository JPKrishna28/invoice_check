import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_from_pdf(pdf_path: str):
    """
    Send PDF to Gemini to extract structured data (invoice/PO).
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    with open(pdf_path, "rb") as f:
        pdf_content = f.read()

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
        {"role": "user", "parts": [prompt, {"mime_type": "application/pdf", "data": pdf_content}]}
    ])

    return response.text  # JSON string
