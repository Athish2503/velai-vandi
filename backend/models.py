from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()
VECTOR_DIM = 128

from sqlalchemy import Index

class Worker(Base):
    __tablename__ = "workers"
    worker_id    = Column(Integer, primary_key=True, index=True)
    name         = Column(String, nullable=False)
    skills       = Column(Text, nullable=False)  # raw comma-separated
    skill_vector = Column(Vector(VECTOR_DIM), nullable=True) # allow null until AI is ready
    experience   = Column(Integer, nullable=False)
    lat          = Column(Float, nullable=False)
    lon          = Column(Float, nullable=False)
    availability = Column(Boolean, default=True)

class Job(Base):
    __tablename__ = "jobs"
    job_id        = Column(Integer, primary_key=True, index=True)
    employer_name = Column(String, nullable=False)
    skills_required = Column(Text, nullable=False)
    skill_vector  = Column(Vector(VECTOR_DIM), nullable=True) # allow null until AI is ready
    salary        = Column(Integer, nullable=False)
    lat           = Column(Float, nullable=False)
    lon           = Column(Float, nullable=False)
    urgency       = Column(Integer, default=1)

# Note: IVFFlat requires the table to have some data before building effectively,
# but we define it here for schema completeness.
Index('ix_worker_skill_vector', Worker.skill_vector, postgresql_using='ivfflat', postgresql_ops={'skill_vector': 'vector_cosine_ops'}, postgresql_with={'lists': 100})
Index('ix_job_skill_vector', Job.skill_vector, postgresql_using='ivfflat', postgresql_ops={'skill_vector': 'vector_cosine_ops'}, postgresql_with={'lists': 100})
