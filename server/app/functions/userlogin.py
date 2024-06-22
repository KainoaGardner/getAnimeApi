from app.tables import UserModel
from app import db, jwt
from flask_jwt_extended import create_access_token


def login(username, password):
    user = UserModel.query.filter_by(username=username, password=password).first()
    if user:
        token = create_access_token(identity=user.id)
        return {"token": token}, 200
    else:
        return {"result": "not found"}, 404


def register(username, password):
    exists = UserModel.query.filter_by(username=username).scalar() is not None

    if exists:
        return {"result": f"Username {username} already taken"}, 404
    else:
        user = UserModel(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return {"result": f"{username} has been register"}, 200


def delete_user(username, password):
    user = UserModel.query.filter_by(username=username, password=password).first()

    if user:
        db.session.delete(user)
        db.session.commit()
        return {"result": f"{username} has been deleted"}, 200
    else:
        return {"result": f"Incorrect information"}, 404
