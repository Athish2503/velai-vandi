import random
import sys
import os

# Add backend directory to sys.path so we can import modules when running this script
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, init_db, engine
from models import Worker, Job, Base
from ai.embedder import fit, embed
from ai.extractor import extract_skills

skills_pool = [
    "mechanic", "driver", "electrician", "plumber", "carpenter",
    "welder", "painter", "mason", "cleaner", "cook", "gardener",
    "guard", "maid", "tailor", "weaver", "barber", "potter",
    "washer", "cobbler", "blacksmith", "sweeper"
]

def seed_db():
    print("Initializing database...")
    init_db()
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Create corpus and train embedder
    print("Training embedder...")
    corpus = [" ".join(random.sample(skills_pool, min(len(skills_pool), 5))) for _ in range(2000)]
    fit(corpus)

    print("Generating workers...")
    workers_to_create = 500
    for i in range(workers_to_create):
        num_skills = random.randint(1, 4)
        skills_list = random.sample(skills_pool, num_skills)
        skills_str = ", ".join(skills_list)

        skills_extracted = " ".join(extract_skills(skills_str))
        vec = embed(skills_extracted)

        # Coimbatore region approx bounds: 10.9 to 11.1 Lat, 76.8 to 77.1 Lon
        lat = 11.0168 + random.uniform(-0.1, 0.1)
        lon = 76.9558 + random.uniform(-0.1, 0.1)

        worker = Worker(
            name=f"Worker_{i+1}",
            skills=skills_str,
            skill_vector=vec,
            experience=random.randint(1, 15),
            lat=lat,
            lon=lon,
            availability=True
        )
        db.add(worker)

        if (i + 1) % 100 == 0:
            print(f"  Inserted {i + 1} workers...")
            db.commit()

    db.commit()

    print("Generating jobs...")
    jobs_to_create = 200
    for i in range(jobs_to_create):
        num_skills = random.randint(1, 3)
        skills_list = random.sample(skills_pool, num_skills)
        skills_str = ", ".join(skills_list)

        skills_extracted = " ".join(extract_skills(skills_str))
        vec = embed(skills_extracted)

        lat = 11.0168 + random.uniform(-0.1, 0.1)
        lon = 76.9558 + random.uniform(-0.1, 0.1)

        job = Job(
            employer_name=f"Employer_{i+1}",
            skills_required=skills_str,
            skill_vector=vec,
            salary=random.randint(5000, 25000),
            lat=lat,
            lon=lon,
            urgency=random.randint(1, 3)
        )
        db.add(job)

        if (i + 1) % 50 == 0:
            print(f"  Inserted {i + 1} jobs...")
            db.commit()

    db.commit()
    db.close()
    print("Database seeding completed.")

if __name__ == "__main__":
    seed_db()
