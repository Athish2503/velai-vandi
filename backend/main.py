from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, init_db
import models
from routes import workers, jobs
from database import SessionLocal
from ai.embedder import fit
from contextlib import asynccontextmanager

init_db()
models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Train the embedder with initial corpus on startup
    db = SessionLocal()
    # Fetch all skills to create the TF-IDF vocabulary
    workers_skills = [w.skills for w in db.query(models.Worker.skills).all()]
    jobs_skills = [j.skills_required for j in db.query(models.Job.skills_required).all()]
    corpus = workers_skills + jobs_skills

    # Add some base corpus in case DB is completely empty to prevent SVD failures
    base_corpus = [
        "mechanic repair engine electrical wiring",
        "driver transport truck delivery car",
        "plumber pipe water leak fitting",
        "carpenter wood furniture assembly building",
        "electrician wiring socket circuit power",
        "welder iron steel metal fabricate",
        "painter color wall paint brush",
        "mason concrete brick cement block",
        "cleaner sweep wash dust house",
        "cook food kitchen chef recipe"
    ]

    fit(corpus + base_corpus)
    db.close()
    yield

app = FastAPI(
    title="Velai Vandi API",
    description="AI powered local job matching system",
    version="1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workers.router)
app.include_router(jobs.router)

@app.get("/")
def root():
    return {"message": "Velai Vandi backend running"}
