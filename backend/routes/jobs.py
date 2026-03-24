from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models import Job, Worker
from ai.extractor import extract_skills
from ai.embedder import embed
from ai.location import haversine
from ai.ranker import compute_score
from sqlalchemy import text

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
    # AI Pipeline: Extract keywords -> Embed -> pgvector
    skills_text = " ".join(extract_skills(job.skills_required))
    vector = embed(skills_text)

    db_job = Job(
        employer_name=job.employer_name,
        skills_required=job.skills_required,
        skill_vector=vector,
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

    if job.skill_vector is None:
        # Fallback if no vector
        skills_text = " ".join(extract_skills(job.skills_required))
        vector_list = embed(skills_text)
        vector_str = str([float(x) for x in vector_list])
    else:
        # pgvector Vector object needs list/str conversion appropriately
        vector_str = str([float(x) for x in job.skill_vector])

    # pgvector cosine similarity - query top candidates
    # Using explicit type cast in bindparam as per pgvector docs when querying dynamically
    candidates = db.execute(
        text("""
            SELECT worker_id, name, skills, experience, lat, lon,
                   1 - (skill_vector <=> CAST(:vec AS vector)) AS skill_sim
            FROM workers
            WHERE availability = true AND skill_vector IS NOT NULL
            ORDER BY skill_vector <=> CAST(:vec AS vector)
            LIMIT 20
        """),
        {"vec": vector_str}
    ).fetchall()

    results = []
    for c in candidates:
        dist = haversine(c.lat, c.lon, job.lat, job.lon)
        # Avoid penalizing too much if skill sim is slightly negative
        sim = max(0.0, c.skill_sim)
        score = compute_score(sim, dist, c.experience)
        results.append({
            "worker_id": c.worker_id,
            "name": c.name,
            "skills": c.skills,
            "score": score,
            "distance_km": round(dist, 1),
            "lat": c.lat,
            "lon": c.lon,
            "experience": c.experience
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)[:5]

@router.get("/match_jobs/{worker_id}")
def match_jobs(worker_id: int, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.worker_id == worker_id).first()
    if not worker:
        return {"error": "Worker not found"}

    if worker.skill_vector is None:
        skills_text = " ".join(extract_skills(worker.skills))
        vector_list = embed(skills_text)
        vector_str = str([float(x) for x in vector_list])
    else:
        # pgvector Vector object needs list/str conversion appropriately
        vector_str = str([float(x) for x in worker.skill_vector])

    # pgvector cosine similarity - query top candidates
    candidates = db.execute(
        text("""
            SELECT job_id, employer_name, skills_required, salary, lat, lon,
                   1 - (skill_vector <=> CAST(:vec AS vector)) AS skill_sim
            FROM jobs
            WHERE skill_vector IS NOT NULL
            ORDER BY skill_vector <=> CAST(:vec AS vector)
            LIMIT 20
        """),
        {"vec": vector_str}
    ).fetchall()

    results = []
    for c in candidates:
        dist = haversine(c.lat, c.lon, worker.lat, worker.lon)
        sim = max(0.0, c.skill_sim)
        # We don't have job experience requirement, default to 0 for job scoring
        score = compute_score(sim, dist, 0)
        results.append({
            "job_id": c.job_id,
            "employer_name": c.employer_name,
            "skills_required": c.skills_required,
            "salary": c.salary,
            "score": score,
            "distance_km": round(dist, 1),
            "lat": c.lat,
            "lon": c.lon
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)[:5]
