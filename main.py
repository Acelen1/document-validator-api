from fastapi import FastAPI, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from uuid import uuid4
import yaml

from models import Document, DocumentCreate, DocumentUpdateRequest
from database import SessionLocal, engine, Base

# crea tabelle se non esistono
Base.metadata.create_all(bind=engine)

app = FastAPI()
validated_documents = []

# dependency per sessione DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# root
@app.get("/")
async def root():
    return {"Hello": "World"}

# fetch tutti i documenti
@app.get("/api/v1/documents")
def fetch_documents(db: Session = Depends(get_db)):
    return db.query(Document).all()

# ✅ QUESTA PRIMA (IMPORTANTE)
@app.get("/api/v1/documents/results")
def get_validated_documents():
    return validated_documents

# register document
@app.post("/api/v1/documents")
def register_document(document: DocumentCreate, db: Session = Depends(get_db)):
    new_doc = Document(
        id=str(uuid4()),
        worker_name=document.worker_name,
        training_completed=document.training_completed,
        medical_certificate=document.medical_certificate,
        middle_name=document.middle_name,
        status="pending",
        errors=[]
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return {"id": new_doc.id}

# ❌ QUESTA DOPO
@app.get("/api/v1/documents/{document_id}")
def get_document(document_id: str, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail=f"document with id {document_id} not found")
    return doc

# delete document
@app.delete("/api/v1/documents/{document_id}")
def delete_document(document_id: str, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail=f"document with id {document_id} does not exist")
    db.delete(doc)
    db.commit()
    return {"detail": f"document {document_id} deleted"}

# update document
@app.put("/api/v1/documents/{document_id}")
def update_document(document_update: DocumentUpdateRequest, document_id: str, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail=f"document with id {document_id} does not exist")
    
    if document_update.worker_name is not None:
        doc.worker_name = document_update.worker_name
    if document_update.training_completed is not None:
        doc.training_completed = document_update.training_completed
    if document_update.medical_certificate is not None:
        doc.medical_certificate = document_update.medical_certificate
    if document_update.middle_name is not None:
        doc.middle_name = document_update.middle_name
    
    db.commit()
    db.refresh(doc)
    return doc

# validate document
@app.post("/api/v1/documents/validate")
def validate_document(document: DocumentCreate = Body(...), db: Session = Depends(get_db)):
    try:
        with open("rules.yaml") as f:
            rules = yaml.safe_load(f) or {}
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="rules.yaml non trovato")

    errors = []

    if rules.get("training_completed") and not document.training_completed:
        errors.append("training_completed is missing or False")
    if rules.get("medical_certificate") and not document.medical_certificate:
        errors.append("medical_certificate is missing or False")

    status = "valid" if not errors else "invalid"

    db_doc = Document(
        id=str(uuid4()),
        worker_name=document.worker_name,
        training_completed=document.training_completed,
        medical_certificate=document.medical_certificate,
        middle_name=document.middle_name,
        status=status,
        errors=errors
    )
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)

    validated_documents.append({
        "document_id": db_doc.id,
        "worker_name": db_doc.worker_name,
        "status": db_doc.status,
        "errors": db_doc.errors
    })

    return {
        "document_id": db_doc.id,
        "worker_name": db_doc.worker_name,
        "status": db_doc.status,
        "errors": db_doc.errors
    }