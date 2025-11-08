from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tempfile
from backend.services.gemini_service import extract_from_pdf
from backend.services.comparer import compare_invoice_po
from backend.routes import compare

app = FastAPI(title="Invoice vs PO Agent using Gemini")

# ✅ Allow Streamlit access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include router
app.include_router(compare.router)

@app.get("/")
def home():
    return {"message": "Backend is running with Gemini API 🚀"}

@app.post("/compare")
async def compare_files(invoice: UploadFile = File(...), po: UploadFile = File(...)):
    """Send both PDFs to Gemini for extraction + intelligent comparison"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_invoice, \
         tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_po:
        
        temp_invoice.write(await invoice.read())
        temp_po.write(await po.read())

        invoice_data = extract_from_pdf(temp_invoice.name)
        po_data = extract_from_pdf(temp_po.name)

        result = compare_invoice_po(invoice_data, po_data)

    return {"comparison_result": result}
