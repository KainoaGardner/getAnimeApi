from app.tables import UserModel, WatchingModel
from app import db, jwt

from flask_jwt_extended import create_access_token
import bcrypt


def login(username, password):

    user = UserModel.query.filter_by(username=username).first()
    if user:
        data_password = user.password.encode("utf-8")

        user_password = password
        user_password_b = user_password.encode("utf-8")
        result = bcrypt.checkpw(user_password_b, data_password)

        if result:

            token = create_access_token(identity=user.id)
            return {"token": token}, 200
    return {"result": "not found"}, 404


def register(username, password):
    exists = UserModel.query.filter_by(username=username).scalar() is not None

    if exists:
        return {"result": f"Username {username} already taken"}, 404
    else:
        bvalue = bytes(password, "utf-8")
        temp_hash = bcrypt.hashpw(bvalue, bcrypt.gensalt())
        hash = temp_hash.decode("utf-8")

        user = UserModel(username=username, password=hash)
        db.session.add(user)
        db.session.commit()

        return {"result": f"{username} has been register"}, 200


def delete_user(username, password):
    user = UserModel.query.filter_by(username=username).first()

    if user:
        data_password = user.password.encode("utf-8")

        user_password = password
        user_password_b = user_password.encode("utf-8")
        result = bcrypt.checkpw(user_password_b, data_password)
        if result:
            user_watching = WatchingModel.query.filter_by(user_id=user.id).all()
            for show in user_watching:
                db.session.delete(show)
            db.session.delete(user)
            db.session.commit()

            return {"result": f"{username} has been deleted"}, 200
    return {"result": f"Incorrect information"}, 404
