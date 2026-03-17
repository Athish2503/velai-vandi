# Implementation Plan — Velai Vandi

---

## Folder Structure

```
velai-vandi/
├── backend/
│   ├── main.py                  # FastAPI app entry
│   ├── models.py                # SQLAlchemy models (pgvector columns)
│   ├── database.py              # PostgreSQL connection
│   ├── routes/
│   │   ├── workers.py
│   │   └── jobs.py
│   └── ai/
│       ├── extractor.py         # spaCy skill extraction
│       ├── embedder.py          # text → vector (TF-IDF fit or sentence embedding)
│       ├── location.py          # Haversine distance
│       └── ranker.py            # Score combiner
├── frontend/                    # Vue 3 (Vite)
│   ├── src/
│   │   ├── main.js
│   │   ├── App.vue
│   │   ├── router/index.js
│   │   ├── views/
│   │   │   ├── WorkerRegister.vue
│   │   │   ├── WorkerDashboard.vue
│   │   │   ├── EmployerPost.vue
│   │   │   └── EmployerDashboard.vue
│   │   └── components/
│   │       ├── MatchCard.vue
│   │       └── MapView.vue      # Leaflet wrapper
│   ├── index.html
│   └── vite.config.js
├── data/
│   └── seed.py                  # Synthetic data generator
├── docs/
│   ├── roadmap.md
│   ├── project.md
│   ├── architecture.md
│   └── implementation.md
├── requirements.txt
└── docker-compose.yml           # PostgreSQL + pgvector container
```

---

## Week 1 — Core System Setup

### Day 1 — Project Setup

```bash
# Backend
python -m venv venv && venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy psycopg2-binary pgvector spacy python-dotenv
python -m spacy download en_core_web_sm

# Frontend
npm create vite@latest frontend -- --template vue
cd frontend && npm install vue-router axios leaflet
```

`docker-compose.yml`
```yaml
services:
  db:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: velai
      POSTGRES_USER: velai
      POSTGRES_PASSWORD: velai
    ports:
      - "5432:5432"
```

```bash
docker-compose up -d
```

Enable pgvector in PostgreSQL:
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

---

### Day 2–3 — Backend APIs

`backend/database.py`
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://velai:velai@localhost:5432/velai"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

`backend/main.py`
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import workers, jobs
from database import engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_methods=["*"], allow_headers=["*"])
app.include_router(workers.router)
app.include_router(jobs.router)
```

---

### Day 4 — Database Models with pgvector

`backend/models.py`
```python
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()
VECTOR_DIM = 128

class Worker(Base):
    __tablename__ = "workers"
    worker_id    = Column(Integer, primary_key=True, index=True)
    name         = Column(String)
    skills       = Column(String)          # raw comma-separated
    skill_vector = Column(Vector(VECTOR_DIM))
    experience   = Column(Integer)
    lat          = Column(Float)
    lon          = Column(Float)
    availability = Column(Boolean, default=True)

class Job(Base):
    __tablename__ = "jobs"
    job_id        = Column(Integer, primary_key=True, index=True)
    employer_name = Column(String)
    skills_required = Column(String)
    skill_vector  = Column(Vector(VECTOR_DIM))
    salary        = Column(Integer)
    lat           = Column(Float)
    lon           = Column(Float)
    urgency       = Column(Integer, default=1)
```

Add IVFFlat index after seeding data:
```sql
CREATE INDEX ON workers USING ivfflat (skill_vector vector_cosine_ops) WITH (lists = 100);
CREATE INDEX ON jobs    USING ivfflat (skill_vector vector_cosine_ops) WITH (lists = 100);
```

---

### Day 5 — Vue Frontend Scaffold

`frontend/src/router/index.js`
```js
import { createRouter, createWebHistory } from 'vue-router'
import WorkerRegister   from '../views/WorkerRegister.vue'
import WorkerDashboard  from '../views/WorkerDashboard.vue'
import EmployerPost     from '../views/EmployerPost.vue'
import EmployerDashboard from '../views/EmployerDashboard.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/worker/register',   component: WorkerRegister },
    { path: '/worker/dashboard',  component: WorkerDashboard },
    { path: '/employer/post',     component: EmployerPost },
    { path: '/employer/dashboard',component: EmployerDashboard },
  ]
})
```

`frontend/src/views/WorkerRegister.vue`
```vue
<template>
  <form @submit.prevent="submit">
    <input v-model="form.name"       placeholder="Name" required />
    <input v-model="form.skills"     placeholder="Skills (comma separated)" required />
    <input v-model.number="form.experience" placeholder="Years of experience" />
    <input v-model.number="form.lat" placeholder="Latitude" />
    <input v-model.number="form.lon" placeholder="Longitude" />
    <button type="submit">Register</button>
  </form>
</template>

<script setup>
import axios from 'axios'
const form = reactive({ name: '', skills: '', experience: 0, lat: 0, lon: 0 })
const submit = () => axios.post('http://localhost:8000/register_worker', form)
</script>
```

---

### Day 6–7 — Basic Skill Overlap (Pre-AI fallback)

```python
def basic_match(worker_skills: str, job_skills: str) -> float:
    w = set(worker_skills.lower().split(","))
    j = set(job_skills.lower().split(","))
    return len(w & j) / max(len(j), 1)
```

Used as fallback when vectors are not yet populated.

---

## Week 2 — AI Implementation

### Day 8 — Skill Extraction

`backend/ai/extractor.py`
```python
import spacy
nlp = spacy.load("en_core_web_sm")

def extract_skills(text: str) -> list[str]:
    doc = nlp(text.lower())
    return [t.lemma_ for t in doc if not t.is_stop and not t.is_punct and t.pos_ in ("NOUN", "VERB")]
```

---

### Day 9 — Embedder (TF-IDF → pgvector)

`backend/ai/embedder.py`
```python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

_vectorizer = TfidfVectorizer(max_features=512)
_svd = TruncatedSVD(n_components=128)   # reduce to VECTOR_DIM
_fitted = False

def fit(corpus: list[str]):
    global _fitted
    tfidf = _vectorizer.fit_transform(corpus)
    _svd.fit(tfidf)
    _fitted = True

def embed(text: str) -> list[float]:
    tfidf = _vectorizer.transform([text])
    vec = _svd.transform(tfidf)[0]
    # L2 normalize for cosine similarity via pgvector
    norm = np.linalg.norm(vec)
    return (vec / norm if norm > 0 else vec).tolist()
```

Called once at startup with all existing skills corpus, then used per registration/job post.

---

### Day 10 — Store + Query Vectors via pgvector

`backend/routes/workers.py`
```python
from ai.extractor import extract_skills
from ai.embedder  import embed

@router.post("/register_worker")
def register_worker(worker: WorkerSchema, db: Session = Depends(get_db)):
    skills_text = " ".join(extract_skills(worker.skills))
    vector = embed(skills_text)
    db_worker = Worker(**worker.dict(), skill_vector=vector)
    db.add(db_worker)
    db.commit()
    return {"status": "registered"}
```

---

### Day 11 — Haversine Distance

`backend/ai/location.py`
```python
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2) -> float:
    R = 6371
    dlat, dlon = radians(lat2 - lat1), radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))
```

---

### Day 12 — Ranking Engine

`backend/ai/ranker.py`
```python
def compute_score(skill_sim: float, distance_km: float, experience: int) -> float:
    proximity  = max(0.0, 1 - distance_km / 50)
    exp_score  = min(experience / 10, 1.0)
    return round((0.5 * skill_sim) + (0.3 * proximity) + (0.2 * exp_score), 4)
```

---

### Day 13–14 — Full AI Match Pipeline

`backend/routes/jobs.py`
```python
from pgvector.sqlalchemy import Vector
from sqlalchemy import text
from ai.location import haversine
from ai.ranker   import compute_score
from ai.embedder import embed
from ai.extractor import extract_skills

@router.get("/match_workers/{job_id}")
def match_workers(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.job_id == job_id).first()

    # pgvector cosine similarity — top 20 candidates
    candidates = db.execute(
        text("""
            SELECT worker_id, name, skills, experience, lat, lon,
                   1 - (skill_vector <=> :vec) AS skill_sim
            FROM workers
            WHERE availability = true
            ORDER BY skill_vector <=> :vec
            LIMIT 20
        """),
        {"vec": str(job.skill_vector)}
    ).fetchall()

    results = []
    for c in candidates:
        dist  = haversine(c.lat, c.lon, job.lat, job.lon)
        score = compute_score(c.skill_sim, dist, c.experience)
        results.append({"worker_id": c.worker_id, "name": c.name, "score": score, "distance_km": round(dist, 1)})

    return sorted(results, key=lambda x: x["score"], reverse=True)[:5]
```

---

## Week 3 — Demo Polish

### Day 15 — Worker Dashboard (Vue)

`frontend/src/views/WorkerDashboard.vue`
```vue
<template>
  <div>
    <MatchCard v-for="job in matches" :key="job.job_id" :data="job" />
    <MapView :markers="matches" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import MatchCard from '../components/MatchCard.vue'
import MapView   from '../components/MapView.vue'

const matches = ref([])
onMounted(async () => {
  const res = await axios.get(`http://localhost:8000/match_jobs/${workerId}`)
  matches.value = res.data
})
</script>
```

---

### Day 16 — Analytics Dashboard

Use Plotly.js in Vue:
```bash
npm install plotly.js-dist
```

Charts to render:
- Top 10 demanded skills (bar)
- Match score distribution (histogram)
- Daily job postings (line)

---

### Day 17 — Map Visualization

`frontend/src/components/MapView.vue`
```vue
<template><div id="map" style="height:400px" /></template>

<script setup>
import { onMounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const props = defineProps(['markers'])
onMounted(() => {
  const map = L.map('map').setView([11.0168, 76.9558], 12)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map)
  props.markers.forEach(m => L.marker([m.lat, m.lon]).bindPopup(`Score: ${m.score}`).addTo(map))
})
</script>
```

---

### Day 18 — Performance Testing

`data/seed.py`
```python
import random, psycopg2
from ai.embedder import fit, embed
from ai.extractor import extract_skills

skills_pool = ["mechanic", "driver", "electrician", "plumber", "carpenter", "welder", "painter"]
conn = psycopg2.connect("postgresql://velai:velai@localhost:5432/velai")
cur  = conn.cursor()

corpus = [" ".join(random.sample(skills_pool, 3)) for _ in range(1000)]
fit(corpus)

for i in range(1000):
    skills = ", ".join(random.sample(skills_pool, 2))
    vec    = embed(" ".join(extract_skills(skills)))
    lat    = 11.0 + random.uniform(-0.5, 0.5)
    lon    = 76.9 + random.uniform(-0.5, 0.5)
    cur.execute(
        "INSERT INTO workers (name, skills, skill_vector, experience, lat, lon, availability) VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (f"Worker_{i}", skills, vec, random.randint(1, 10), lat, lon, True)
    )

conn.commit()
```

---

### Day 19 — Demo Dataset

Run `seed.py` with 500 workers + 200 jobs using realistic Coimbatore-area coordinates.

---

### Day 20 — Presentation Slides

1. Problem + motivation
2. System architecture diagram
3. AI pipeline: spaCy → embed → pgvector query
4. Live demo: Vue UI + map + match scores
5. Performance results (query time with IVFFlat index)
6. Future scope

---

### Day 21 — Final Integration + Demo Run

- End-to-end: register worker → post job → pgvector match → Vue dashboard → map
- Verify CORS, DB connections, vector index
- Rehearse demo flow

---

## Requirements

`requirements.txt`
```
fastapi
uvicorn
sqlalchemy
psycopg2-binary
pgvector
spacy
scikit-learn
python-dotenv
```

`frontend` dependencies (package.json):
```
vue
vue-router
axios
leaflet
plotly.js-dist
```
