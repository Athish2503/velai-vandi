# Architecture — Velai Vandi

---

## System Layers

```
┌─────────────────────────────┐
│      User Interface Layer   │  React / Flask Templates
├─────────────────────────────┤
│      Application Layer      │  FastAPI (REST)
├─────────────────────────────┤
│      AI Processing Layer    │  spaCy · TF-IDF · Cosine Similarity
├─────────────────────────────┤
│      Matching Engine        │  Ranking · Haversine · Score Combiner
├─────────────────────────────┤
│      Database Layer         │  SQLite / PostgreSQL
└─────────────────────────────┘
```

---

## Layer Details

### 1. User Interface Layer

Two portals:

**Job Seeker**
- Register profile (name, skills, location, availability)
- View top-5 matched jobs with AI score
- Accept / reject job

**Employer**
- Post job (description, location, salary, urgency)
- View top-5 matched workers

---

### 2. Application Layer (FastAPI)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/register_worker` | POST | Create worker profile |
| `/post_job` | POST | Create job listing |
| `/match_jobs` | GET | Return top jobs for a worker |
| `/match_workers` | GET | Return top workers for a job |

---

### 3. AI Processing Layer

**Module 1 — Skill Extraction**
- Input: raw text (`"Need bike mechanic who knows wiring"`)
- Process: spaCy tokenization → stopword removal → keyword extraction
- Output: `["mechanic", "electrical", "repair"]`

**Module 2 — TF-IDF Vectorization**
- Converts skill lists into numerical feature vectors
- Corpus: all worker skills + all job requirements

**Module 3 — Cosine Similarity**
- Compares worker vector vs job vector
- Score range: 0.0 (no match) → 1.0 (perfect match)

---

### 4. Matching Engine

**Haversine Distance**
```
distance = haversine(worker_lat, worker_lon, job_lat, job_lon)
```

**Final Score Formula**
```
score = (0.5 × skill_similarity) + (0.3 × proximity_score) + (0.2 × experience_score)
```

Pipeline:
```
Input → Skill Extraction → Vectorization → Cosine Similarity
      → Haversine Filter → Score Combiner → Top 5 Results
```

---

### 5. Database Layer

**workers**
```
worker_id | name | skills | experience | lat | lon | availability
```

**jobs**
```
job_id | employer_name | skills_required | salary | lat | lon | urgency
```

**matches**
```
worker_id | job_id | match_score
```

---

## Data Flow

```
Worker registers
      ↓
Skills extracted + vectorized → stored in DB
      ↓
Employer posts job
      ↓
Job skills extracted + vectorized
      ↓
Cosine similarity computed against all workers
      ↓
Haversine distance computed
      ↓
Scores combined + ranked
      ↓
Top 5 results returned
```

---

## Visualization Layer

- Leaflet map: plot worker/job pins, draw match lines
- Plotly dashboard: skill demand chart, hiring success rate, match score distribution
