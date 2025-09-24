from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association table for many-to-many (Goal ↔ Category)
goal_category = db.Table(
    "goal_category",
    db.Column("goal_id", db.Integer, db.ForeignKey("goals.id"), primary_key=True),
    db.Column("category_id", db.Integer, db.ForeignKey("categories.id"), primary_key=True),
    db.Column("notes", db.String(200))  # extra attribute
)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_digest = db.Column(db.String(200), nullable=False)

    goals = db.relationship("Goal", backref="user", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            # don't return password_digest for security
            "goals": [goal.id for goal in self.goals]
        }

class Goal(db.Model):
    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    status = db.Column(db.String(20), default="pending")
    deadline = db.Column(db.String(50))
    priority = db.Column(db.String(20))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    categories = db.relationship(
        "Category",
        secondary=goal_category,
        back_populates="goals"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "deadline": self.deadline,
            "priority": self.priority,
            "user_id": self.user_id,
            "categories": [cat.id for cat in self.categories]
        }

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200))

    goals = db.relationship(
        "Goal",
        secondary=goal_category,
        back_populates="categories"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "goals": [goal.id for goal in self.goals]
        }
