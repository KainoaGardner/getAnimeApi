from app import db


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    watching = db.relationship("WatchingModel")


class WatchingModel(db.Model):
    __tablename__ = "watching"
    id = db.Column(db.Integer, primary_key=True)
    show_title = db.Column(db.String(500))
    show_id = db.Column(db.String(500))
    user_id = db.Column(db.ForeignKey("users.id"))
