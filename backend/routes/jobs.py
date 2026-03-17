from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models import Job, Worker

router = APIRouter(prefix="/jobs", tags=["jobs"])

class JobSchema(BaseModel):
    employer_name: str
    skills_required: str
    salary: int
    lat: float
    lon: float
    urgency: int = 1

def basic_match(worker_skills: str, job_skills: str) -> float:
    w = set(worker_skills.lower().split(","))
    j = set(job_skills.lower().split(","))
    w = {x.strip() for x in w}
    j = {x.strip() for x in j}
    if not j:
        return 0.0
    return len(w & j) / max(len(j), 1)

@router.post("/post")
def post_job(job: JobSchema, db: Session = Depends(get_db)):
    db_job = Job(
        employer_name=job.employer_name,
        skills_required=job.skills_required,
        salary=job.salary,
        lat=job.lat,
        lon=job.lon,
        urgency=job.urgency
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return {"status": "posted", "job_id": db_job.job_id}

@router.get("/")
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    return [{"job_id": j.job_id, "employer_name": j.employer_name, "skills_required": j.skills_required, "salary": j.salary, "lat": j.lat, "lon": j.lon} for j in jobs]

@router.get("/match_workers/{job_id}")
def match_workers(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.job_id == job_id).first()
    if not job:
        return {"error": "Job not found"}

    workers = db.query(Worker).filter(Worker.availability == True).all()
    results = []

    for w in workers:
        score = basic_match(w.skills, job.skills_required)
        # Pre-AI fallback distance calculation: Euclidean distance
        # To make it simple, we just penalize large differences in lat/lon slightly
        lat_diff = abs(w.lat - job.lat)
        lon_diff = abs(w.lon - job.lon)
        dist_penalty = (lat_diff + lon_diff) * 10

        final_score = max(0.0, score - dist_penalty)
        if final_score > 0:
            results.append({
                "worker_id": w.worker_id,
                "name": w.name,
                "skills": w.skills,
                "score": round(final_score, 2),
                "lat": w.lat,
                "lon": w.lon,
                "experience": w.experience
            })

    return sorted(results, key=lambda x: x["score"], reverse=True)[:5]

@router.get("/match_jobs/{worker_id}")
def match_jobs(worker_id: int, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.worker_id == worker_id).first()
    if not worker:
        return {"error": "Worker not found"}

    jobs = db.query(Job).all()
    results = []

    for j in jobs:
        score = basic_match(worker.skills, j.skills_required)
        lat_diff = abs(worker.lat - j.lat)
        lon_diff = abs(worker.lon - j.lon)
        dist_penalty = (lat_diff + lon_diff) * 10

        final_score = max(0.0, score - dist_penalty)
        if final_score > 0:
            results.append({
                "job_id": j.job_id,
                "employer_name": j.employer_name,
                "skills_required": j.skills_required,
                "salary": j.salary,
                "score": round(final_score, 2),
                "lat": j.lat,
                "lon": j.lon
            })

    return sorted(results, key=lambda x: x["score"], reverse=True)[:5]
