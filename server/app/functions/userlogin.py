from app.tables import UserModel
from app import db


def login(username, password):
    user = UserModel.query.filter_by(username=username, password=password).first()
    if user:
        return {"result": f"Logged into {username}", "id": user.id}, 200
    else:
        return {"result": f"User {username} not found"}, 404


def register(username, password):
    exists = UserModel.query.filter_by(username=username).scalar() is not None

    if exists:
        return {"result": f"Username {username} already taken"}, 404
    else:
        user = UserModel(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return {"result": f"{username} has been register"}, 200
