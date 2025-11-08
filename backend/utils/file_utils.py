import tempfile
from fastapi import UploadFile

def save_temp_file(uploaded_file: UploadFile) -> str:
    """
    Save uploaded file temporarily and return the path.
    """
    suffix = uploaded_file.filename.split(".")[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
        tmp.write(uploaded_file.file.read())
        tmp.flush()
        return tmp.name
