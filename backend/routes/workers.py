from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models import Worker
from ai.extractor import extract_skills
from ai.embedder import embed

router = APIRouter(prefix="/workers", tags=["workers"])

class WorkerSchema(BaseModel):
    name: str
    skills: str
    experience: int
    lat: float
    lon: float

@router.post("/register")
def register_worker(worker: WorkerSchema, db: Session = Depends(get_db)):
    # AI Pipeline: Extract keywords -> Embed -> pgvector
    skills_text = " ".join(extract_skills(worker.skills))
    vector = embed(skills_text)

    db_worker = Worker(
        name=worker.name,
        skills=worker.skills,
        skill_vector=vector,
        experience=worker.experience,
        lat=worker.lat,
        lon=worker.lon
    )
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return {"status": "registered", "worker_id": db_worker.worker_id}

@router.get("/")
def get_workers(db: Session = Depends(get_db)):
    workers = db.query(Worker).all()
    return [{"worker_id": w.worker_id, "name": w.name, "skills": w.skills, "experience": w.experience, "lat": w.lat, "lon": w.lon} for w in workers]