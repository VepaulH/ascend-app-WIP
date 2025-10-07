
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine
from .openai_parser import parse_text_to_entry
from .settings import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Wellness AI Speedrun")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/health")
def health():
    return {"status": "ok", "use_pytorch": settings.USE_PYTORCH}

@app.get("/api/entries", response_model=list[schemas.EntryOut])
def list_entries(db: Session = Depends(get_db)):
    return crud.list_entries(db)

@app.post("/api/entries", response_model=schemas.EntryOut)
def create_entry(payload: schemas.EntryIn, db: Session = Depends(get_db)):
    return crud.create_entry(db, payload)

@app.post("/api/chat", response_model=schemas.EntryOut)
def chat_parse(payload: schemas.ChatIn, db: Session = Depends(get_db)):
    try:
        parsed = parse_text_to_entry(payload.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return crud.create_entry(db, schemas.EntryIn(**parsed))
