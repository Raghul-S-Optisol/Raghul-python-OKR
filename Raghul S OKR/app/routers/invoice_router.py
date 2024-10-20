from fastapi import APIRouter, UploadFile, File
from app.controllers import invoice_controller
from app.models.invoice_model import InvoiceUpdate

router = APIRouter()

@router.post("/upload-invoice/")
async def upload_invoice(file: UploadFile = File(...)):
    return await invoice_controller.upload_invoice(file)

@router.get("/fetch-invoice/{invoice_number}")
async def fetch_invoice(invoice_number: str):
    return await invoice_controller.fetch_invoice(invoice_number)

@router.put("/update-invoice/{invoice_number}")
async def update_invoice(invoice_number: str, update_data: InvoiceUpdate):
    return await invoice_controller.update_invoice(invoice_number, update_data)

@router.delete("/delete-invoice/{invoice_number}")
async def delete_invoice(invoice_number: str):
    return await invoice_controller.delete_invoice(invoice_number)
