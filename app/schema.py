from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.Text)

    profile = db.relationship("Profile")


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String,)
    dob = db.Column(db.Date)
    gender = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    login = db.relationship("User")

