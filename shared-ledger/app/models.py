from sqlalchemy import Column, Integer, String, DateTime, Enum
import enum
from datetime import UTC, datetime
from app.database import Base 

class LedgerOperation(enum.Enum):
    DAILY_REWARD = "DAILY_REWARD"
    SIGNUP_CREDIT = "SIGNUP_CREDIT"
    CREDIT_SPEND = "CREDIT_SPEND"
    CREDIT_ADD = "CREDIT_ADD"
    CONTENT_CREATION = "CONTENT_CREATION"
    CONTENT_ACCESS = "CONTENT_ACCESS"

class LedgerEntry(Base):
    __tablename__ = "ledger_entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    operation = Column(Enum(LedgerOperation), nullable=False)
    amount = Column(Integer, nullable=False)
    nonce = Column(String, unique=True, nullable=False)
    owner_id = Column(String, nullable=False)
    created_on = Column(DateTime, default=lambda: datetime.now(UTC))