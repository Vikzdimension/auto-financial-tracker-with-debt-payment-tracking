from sqlalchemy.orm import Session
from app.models import Transaction
from datetime import datetime
from email.utils import parsedate_to_datetime

def save_transaction(db: Session, user_id: int, message: dict):
    existing = db.query(Transaction).filter(Transaction.email_id == message['email_id']).first()
    if existing:
        return existing
    
    # Parse date using email.utils which handles various email date formats
    try:
        parsed_date = parsedate_to_datetime(message['date']) if message['date'] else datetime.utcnow()
    except (ValueError, TypeError):
        parsed_date = datetime.utcnow()
    
    txn = Transaction(
        user_id=user_id,
        vendor=message['vendor'],
        subject=message['subject'],
        amount=message.get('amount', 0),
        category=None,
        email_id=message['email_id'],
        date=parsed_date
    )
    db.add(txn)
    db.commit()
    db.refresh(txn)
    return txn