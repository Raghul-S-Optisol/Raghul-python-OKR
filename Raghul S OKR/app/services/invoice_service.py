import re
from pdfminer.high_level import extract_text
import io
from app.config.database import db
from app.models.invoice_model import InvoiceUpdate
from fastapi import HTTPException
from datetime import datetime
from bson import ObjectId

invoices_collection = db['invoices']

# Extract data from PDF content
async def extract_invoice_data(pdf_content: bytes):
    try:
        text = extract_text(io.BytesIO(pdf_content))

        # Define a regex pattern for invoice number (e.g., "INV123", "Invoice #12345", etc.)
        invoice_number_pattern = r'(?:INV|Invoice #)?(\d+)'

        # Search for the invoice number in the extracted text
        match = re.search(invoice_number_pattern, text)
        if match:
            invoice_number = match.group(0)  # Get the full match (e.g., "INV123")
        else:
            raise HTTPException(status_code=400, detail="Invoice number not found in the PDF.")

        date = str(datetime.now().date())  # You can modify this to extract the actual date if needed
        amount = 123.45  # Placeholder; you can also extract this from the PDF if required

        return {
            "invoice_number": invoice_number,
            "date": date,
            "amount": amount
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error extracting data: {str(e)}")

# Process and store the invoice
async def process_and_store_invoice(pdf_content: bytes):
    invoice_data = await extract_invoice_data(pdf_content)
    inserted_result = await invoices_collection.insert_one(invoice_data)  # Await the insertion
    inserted_id = invoice_data.invoice_number
    return {"message": "Invoice uploaded and data extracted", "invoice_id": str(inserted_id)}

# Fetch invoice by number
async def get_invoice_by_number(invoice_number: str):
    invoice = await invoices_collection.find_one({"invoice_number": invoice_number})
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    # Convert ObjectId to string for JSON serialization
    invoice["_id"] = str(invoice["_id"])

    return invoice

# Update invoice data
async def update_invoice_data(invoice_number: str, update_data: InvoiceUpdate):
    updated_invoice = await invoices_collection.update_one(
        {"invoice_number": invoice_number},
        {"$set": update_data.dict()}
    )
    if updated_invoice.matched_count == 0:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {"message": "Invoice updated successfully"}

# Delete invoice by number
async def delete_invoice_by_number(invoice_number: str):
    result = await invoices_collection.delete_one({"invoice_number": invoice_number})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {"message": "Invoice deleted successfully"}
