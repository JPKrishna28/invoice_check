import json
import re
from typing import Dict, Any

def parse_gemini_json_response(response_text: str) -> Dict[Any, Any]:
    """
    Parse JSON response from Gemini, handling potential formatting issues.
    """
    try:
        # Try to parse as direct JSON
        return json.loads(response_text)
    except json.JSONDecodeError:
        try:
            # Try to extract JSON from markdown code blocks
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            
            # Try to find JSON-like content
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
                
            # If no JSON found, return the text as is
            return {"raw_text": response_text}
            
        except json.JSONDecodeError:
            return {"error": "Failed to parse response", "raw_text": response_text}

def extract_key_fields(data: Dict[Any, Any]) -> Dict[str, Any]:
    """
    Extract key fields from parsed document data.
    """
    if isinstance(data, dict):
        return {
            "document_type": data.get("DocumentType", "Unknown"),
            "vendor_name": data.get("VendorName", "Unknown"),
            "number": data.get("InvoiceNumber") or data.get("PONumber", "Unknown"),
            "date": data.get("Date", "Unknown"),
            "total_amount": data.get("TotalAmount", "Unknown"),
            "line_items": data.get("LineItems", [])
        }
    return {"error": "Invalid data format"}