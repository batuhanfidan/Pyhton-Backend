from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import LedgerEntry, LedgerOperation
from app.schemas import LedgerCreate
import uuid

app = FastAPI()

@app.get("/ledger/{owner_id}")
def get_ledger_balance(owner_id: str, db: Session = Depends(get_db)):
    entries = db.query(LedgerEntry).filter(LedgerEntry.owner_id == owner_id).all()
    balance = sum(entry.amount for entry in entries)
    return {"owner_id": owner_id, "balance": balance}

@app.post("/ledger")
def add_ledger_entry(entry: LedgerCreate, db: Session = Depends(get_db)):
    existing_entry = db.query(LedgerEntry).filter(LedgerEntry.nonce == entry.nonce).first()
    if existing_entry:
        raise HTTPException(status_code=400, detail="Duplicate transaction detected")

    new_entry = LedgerEntry(
        operation=entry.operation,
        amount=entry.amount,
        nonce=str(uuid.uuid4()),
        owner_id=entry.owner_id
    )
    db.add(new_entry)
    db.commit()
    return {"message": "Transaction added successfully"}
