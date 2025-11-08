import streamlit as st
import requests

# 🌟 Page setup
st.set_page_config(page_title="Invoice vs PO Reconciliation", page_icon="📄")

# 🌟 Title
st.title("📄 Invoice vs Purchase Order Reconciliation Agent")

# Backend URL (FastAPI)
BACKEND_URL = "http://127.0.0.1:8000/api/compare"


# 🧾 File uploaders
invoice = st.file_uploader("Upload Invoice PDF", type=["pdf"])
po = st.file_uploader("Upload Purchase Order PDF", type=["pdf"])

# 🖱️ Compare button
if st.button("Compare"):
    if not invoice or not po:
        st.warning("⚠️ Please upload both the Invoice and Purchase Order files!")
    else:
        # Prepare files for POST request
        files = {
            "invoice": (invoice.name, invoice.getvalue(), "application/pdf"),
            "po": (po.name, po.getvalue(), "application/pdf")
        }

        # Send request to backend
        with st.spinner("🔍 Analyzing files and comparing using Gemini..."):
            try:
                response = requests.post(BACKEND_URL, files=files)

                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Comparison complete!")
                    st.json(result)
                else:
                    st.error(f"❌ Error: {response.status_code}")
                    st.text(response.text)

            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Could not connect to backend: {e}")
