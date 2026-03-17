from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, init_db
import models
from routes import workers, jobs

init_db()
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Velai Vandi API",
    description="AI powered local job matching system",
    version="1.0"
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
