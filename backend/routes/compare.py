from fastapi import APIRouter, UploadFile, File
import tempfile
from backend.services.gemini_service import extract_from_pdf
from backend.services.comparer import compare_invoice_po

router = APIRouter()

@router.post("/compare")
async def compare_files(invoice: UploadFile = File(...), po: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_invoice, \
         tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_po:
        temp_invoice.write(await invoice.read())
        temp_po.write(await po.read())

        invoice_data = extract_from_pdf(temp_invoice.name)
        po_data = extract_from_pdf(temp_po.name)

        result = compare_invoice_po(invoice_data, po_data)

    return {"comparison_result": result}

