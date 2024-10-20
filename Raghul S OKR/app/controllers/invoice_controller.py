from fastapi import UploadFile, HTTPException
from app.services import invoice_service
from app.models.invoice_model import InvoiceUpdate

async def upload_invoice(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    pdf_content = await file.read()
    return await invoice_service.process_and_store_invoice(pdf_content)

async def fetch_invoice(invoice_number: str):
    return await invoice_service.get_invoice_by_number(invoice_number)

async def update_invoice(invoice_number: str, update_data: InvoiceUpdate):
    return await invoice_service.update_invoice_data(invoice_number, update_data)

async def delete_invoice(invoice_number: str):
    return await invoice_service.delete_invoice_by_number(invoice_number)
