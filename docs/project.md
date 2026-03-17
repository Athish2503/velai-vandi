# Velai Vandi — Project Document

**AI-Driven Geospatial Job Matching System for Informal Employment**

---

## Overview

Velai Vandi matches local job seekers with nearby employers using AI-based skill extraction, pgvector similarity search, and geospatial ranking. Built for informal/blue-collar employment in Tamil Nadu.

---

## Problem Statement

Informal workers (mechanics, electricians, drivers) and local employers have no efficient way to find each other. Existing platforms are too complex, English-heavy, and ignore proximity.

---

## Goals

- Match workers to jobs based on skill relevance + location proximity
- Extract skills automatically from free-text job descriptions
- Store and query skill vectors directly in PostgreSQL via pgvector
- Rank matches using a weighted AI scoring model
- Visualize matches on a map for demo impact

---

## Scope (3 Weeks)

In scope:
- Worker and employer registration
- AI skill extraction (spaCy)
- Skill vectorization stored as pgvector embeddings in PostgreSQL
- Cosine similarity search via pgvector (`<=>` operator)
- Haversine distance filtering
- Ranked match results (top 5)
- Map visualization
- Analytics dashboard

Out of scope:
- Payment integration
- Mobile app
- Real-time chat
- Multi-language NLP

---

## Team

| Role | Responsibilities |
|------|-----------------|
| AI Engineer | NLP extraction, pgvector embedding pipeline, similarity queries, ranking, dataset generation |
| System Engineer | Backend APIs, PostgreSQL setup, Vue frontend, integration, visualization |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vue 3 (Vite) |
| Backend | FastAPI |
| AI/ML | Python, spaCy, scikit-learn (TF-IDF → embedding only) |
| Database | PostgreSQL + pgvector extension |
| Visualization | Leaflet, Plotly |

---

## Why pgvector

- Skill vectors live in the same DB as worker/job records — no separate vector store
- Native cosine similarity queries: `ORDER BY skill_vector <=> query_vector`
- Scales with PostgreSQL indexing (IVFFlat index for large datasets)
- Eliminates in-memory TF-IDF recomputation on every request

---

## Key Metrics (Demo)

- Match accuracy on synthetic dataset (500 workers, 200 jobs)
- Top-5 match relevance score
- Response time under load (1000 workers, 1000 jobs)

---

## Academic Positioning

Title: **AI-Driven Geospatial Job Matching System for Informal Employment**

AI techniques to highlight:
- NLP skill extraction (spaCy)
- Vector similarity search (pgvector cosine distance)
- Geospatial intelligence (Haversine Distance / PostGIS)
- Content-based recommendation filtering
