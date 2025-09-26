# seed.py
from database import Base, engine, SessionLocal
from models import User, Goal, Category

def seed_db():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    
    # Seed default user
    if session.query(User).count() == 0:
        admin = User(
            username="Admin",
            email="admin@taskup.com",
            password_digest="adminpassword"
        )
        session.add(admin)
        session.commit()

        # Seed goals
        goal1 = Goal(
            title="Learn Flask",
            description="Understand Flask and build backend APIs",
            status="pending",
            user_id=admin.id
        )
        goal2 = Goal(
            title="Build TaskUp",
            description="Finish TaskUp backend and connect frontend",
            status="pending",
            user_id=admin.id
        )
        session.add_all([goal1, goal2])
        session.commit()

        print("Database seeded with default user and goals!")
    session.close()

seed_db()