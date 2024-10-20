from pydantic import BaseModel

class InvoiceUpdate(BaseModel):
    date: str
    amount: float
