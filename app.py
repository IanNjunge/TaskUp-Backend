import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from models import db, User, Goal, Category

app = Flask(__name__)
CORS(app)


app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI", "sqlite:///dev.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

@app.route("/")
def index():
    return "Welcome to the TaskUp API!"

#USERS 
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    new_user = User(
        username=data["username"],
        email=data["email"],
        password_digest=data.get("password_digest", "12345") 
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

# GOALS 
@app.route("/goals", methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    return jsonify([g.to_dict() for g in goals])

@app.route("/goals/<int:id>", methods=["GET"])
def get_goal(id):
    goal = Goal.query.get_or_404(id)
    return jsonify(goal.to_dict())

@app.route("/goals", methods=["POST"])
def create_goal():
    data = request.json
    new_goal = Goal(
        title=data["title"],
        description=data.get("description", ""),
        status=data.get("status", "pending"),
        deadline=data.get("deadline"),
        priority=data.get("priority"),
        user_id=1  # default user
    )
    db.session.add(new_goal)
    db.session.commit()
    return jsonify(new_goal.to_dict()), 201

@app.route("/goals/<int:id>", methods=["PUT"])
def update_goal(id):
    goal = Goal.query.get_or_404(id)
    data = request.json
    goal.title = data.get("title", goal.title)
    goal.description = data.get("description", goal.description)
    goal.status = data.get("status", goal.status)
    goal.deadline = data.get("deadline", goal.deadline)
    goal.priority = data.get("priority", goal.priority)
    db.session.commit()
    return jsonify(goal.to_dict())

@app.route("/goals/<int:id>", methods=["DELETE"])
def delete_goal(id):
    goal = Goal.query.get_or_404(id)
    db.session.delete(goal)
    db.session.commit()
    return "", 204

# CATEGORIES 
@app.route("/categories", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories])

@app.route("/categories/<int:id>", methods=["GET"])
def get_category(id):
    category = Category.query.get_or_404(id)
    return jsonify(category.to_dict())

@app.route("/categories", methods=["POST"])
def create_category():
    data = request.json
    new_category = Category(
        name=data["name"],
        description=data.get("description", "")
    )
    db.session.add(new_category)
    db.session.commit()
    return jsonify(new_category.to_dict()), 201


@app.route("/seed", methods=["POST"])
def run_seed():
    from seed import seed_db
    seed_db()
    return {"message": "Database seeded!"}, 200



if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
