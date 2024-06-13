from app import db


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    watching = db.relationship("WatchingModel")


class ShowModel(db.Model):
    __tablename__ = "shows"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, unique=True)
    air_date = db.Column(db.Date, nullable=False)
    watching = db.relationship("WatchingModel")


class WatchingModel(db.Model):
    __tablename__ = "watching"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey("users.id"))
    show_id = db.Column(db.ForeignKey("shows.id"))
