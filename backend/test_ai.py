import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_db, SessionLocal
from models import Worker, Job

client = TestClient(app)

def test_api_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Velai Vandi backend running"}

def test_register_worker():
    payload = {
        "name": "Test Worker",
        "skills": "python, fastapi, postgres",
        "experience": 3,
        "lat": 11.0,
        "lon": 76.9
    }
    with client: # Triggers startup/lifespan events
        response = client.post("/workers/register", json=payload)
        assert response.status_code == 200
        assert response.json()["status"] == "registered"
        worker_id = response.json()["worker_id"]

        # Verify vector was generated
        db = SessionLocal()
        worker = db.query(Worker).filter(Worker.worker_id == worker_id).first()
        assert worker is not None
        assert worker.skill_vector is not None
        assert len(worker.skill_vector) == 128
        db.close()

def test_post_job():
    payload = {
        "employer_name": "Tech Corp",
        "skills_required": "python, fastapi",
        "salary": 50000,
        "lat": 11.01,
        "lon": 76.91,
        "urgency": 2
    }
    with client:
        response = client.post("/jobs/post", json=payload)
        assert response.status_code == 200
        assert response.json()["status"] == "posted"
        job_id = response.json()["job_id"]

        # Verify vector was generated
        db = SessionLocal()
        job = db.query(Job).filter(Job.job_id == job_id).first()
        assert job is not None
        assert job.skill_vector is not None
        assert len(job.skill_vector) == 128
        db.close()

def test_match_workers():
    with client:
        # First create a job to match against
        job_payload = {
            "employer_name": "Match Test Corp",
            "skills_required": "python, postgres, docker",
            "salary": 60000,
            "lat": 11.05,
            "lon": 76.95,
            "urgency": 1
        }
        res = client.post("/jobs/post", json=job_payload)
        job_id = res.json()["job_id"]

        # Register a matching worker
        worker_payload = {
            "name": "Match Test Worker",
            "skills": "python, postgres, docker, aws",
            "experience": 5,
            "lat": 11.06,
            "lon": 76.96
        }
        client.post("/workers/register", json=worker_payload)

        response = client.get(f"/jobs/match_workers/{job_id}")
        assert response.status_code == 200
        matches = response.json()
        assert len(matches) <= 5
        assert len(matches) > 0
        assert "score" in matches[0]
        assert "distance_km" in matches[0]

        # Check sorting
        if len(matches) > 1:
            assert matches[0]["score"] >= matches[1]["score"]

def test_match_jobs():
    with client:
        # Register a worker to match jobs for
        worker_payload = {
            "name": "Job Match Test Worker",
            "skills": "plumbing, welding",
            "experience": 2,
            "lat": 11.02,
            "lon": 76.92
        }
        res = client.post("/workers/register", json=worker_payload)
        worker_id = res.json()["worker_id"]

        # Create a matching job
        job_payload = {
            "employer_name": "Job Match Test Corp",
            "skills_required": "plumbing",
            "salary": 10000,
            "lat": 11.03,
            "lon": 76.93,
            "urgency": 3
        }
        client.post("/jobs/post", json=job_payload)

        response = client.get(f"/jobs/match_jobs/{worker_id}")
        assert response.status_code == 200
        matches = response.json()
        assert len(matches) <= 5
        assert len(matches) > 0
        assert "score" in matches[0]
        assert "distance_km" in matches[0]

        # Check sorting
        if len(matches) > 1:
            assert matches[0]["score"] >= matches[1]["score"]
