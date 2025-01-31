from pydantic import BaseModel
from app.models import LedgerOperation

class LedgerCreate(BaseModel):
    owner_id: str
    operation: LedgerOperation
    amount: int
    nonce: str
