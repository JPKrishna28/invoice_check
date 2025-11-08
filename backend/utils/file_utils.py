import tempfile
from fastapi import UploadFile

async def save_temp_file(uploaded_file: UploadFile) -> str:
    """
    Save uploaded file temporarily and return the path.
    """
    suffix = uploaded_file.filename.split(".")[-1] if uploaded_file.filename else "tmp"
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
        content = await uploaded_file.read()
        tmp.write(content)
        tmp.flush()
        return tmp.name
