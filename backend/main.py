from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import compare

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
