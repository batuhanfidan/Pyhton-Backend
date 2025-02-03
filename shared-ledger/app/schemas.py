from pydantic import BaseModel, ConfigDict
from app.models import LedgerOperation
from pydantic import field_validator

class LedgerCreate(BaseModel):
    owner_id: str
    operation: LedgerOperation
    amount: int
    nonce: str
    
    model_config = ConfigDict(from_attributes=True)
    
    @field_validator('amount')
    def validate_amount_for_operation(cls, v, values):
        if 'operation' in values:
            op = values['operation']
            if op in [LedgerOperation.CREDIT_SPEND, LedgerOperation.CONTENT_ACCESS] and v > 0:
                raise ValueError(f"{op.value} operation amount must be negative")
            if op in [LedgerOperation.DAILY_REWARD, LedgerOperation.SIGNUP_CREDIT, LedgerOperation.CONTENT_CREATION] and v < 0:
                raise ValueError(f"{op.value} operation amount must be positive")
        return v