
from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

def list_entries(db: Session):
    return db.query(models.Entry).order_by(models.Entry.timestamp.desc()).limit(200).all()

def create_entry(db: Session, payload: schemas.EntryIn):
    entry = models.Entry(
        mood=payload.mood,
        habit=payload.habit,
        duration=payload.duration,
        notes=payload.notes,
        timestamp=payload.timestamp or datetime.utcnow(),
        user_id=payload.user_id or 1,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
