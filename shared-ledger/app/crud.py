from sqlalchemy.orm import Session
from app.models import LedgerEntry
from app.schemas import LedgerCreate
import uuid

def create_ledger_entry(db: Session, entry: LedgerCreate):
    new_entry = LedgerEntry(
        owner_id=entry.owner_id,
        operation=entry.operation,
        amount=entry.amount,
        nonce=str(uuid.uuid4()),
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

def get_ledger_balance(db: Session, owner_id: str):
    entries = db.query(LedgerEntry).filter(LedgerEntry.owner_id == owner_id).all()
    return sum(entry.amount for entry in entries)