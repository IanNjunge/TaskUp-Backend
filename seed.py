from app import app, db  
from models import User, Goal, Category

with app.app_context():  
    db.create_all()

    # default user 
    admin = User(
        username="Admin",
        email="admin@taskup.com",
        password_digest="adminpassword"  # for testing
    )
    db.session.add(admin)
    db.session.commit()  

    # Some goals for admin
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
    db.session.add_all([goal1, goal2])
    db.session.commit()

    print("Database seeded with default user and goals!")
