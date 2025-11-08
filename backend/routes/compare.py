from fastapi import APIRouter, UploadFile, File
import tempfile
import os
from ..services.gemini_service import extract_from_pdf
from ..services.comparer import compare_invoice_po

router = APIRouter()

@router.post("/compare")
async def compare_files(invoice: UploadFile = File(...), po: UploadFile = File(...)):
    temp_invoice_path = None
    temp_po_path = None
    
    try:
        # Create temporary files
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_invoice:
            temp_invoice.write(await invoice.read())
            temp_invoice_path = temp_invoice.name
            
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_po:
            temp_po.write(await po.read())
            temp_po_path = temp_po.name

        # Extract data from PDFs
        invoice_data = extract_from_pdf(temp_invoice_path)
        po_data = extract_from_pdf(temp_po_path)

        # Compare the data
        result = compare_invoice_po(invoice_data, po_data)

        return {"comparison_result": result}
    
    except Exception as e:
        return {"error": f"Failed to process files: {str(e)}"}
    
    finally:
        # Clean up temporary files
        if temp_invoice_path and os.path.exists(temp_invoice_path):
            os.unlink(temp_invoice_path)
        if temp_po_path and os.path.exists(temp_po_path):
            os.unlink(temp_po_path)

