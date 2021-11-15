from flask import (
    Blueprint, render_template, request, url_for, redirect, session
)
from app.schema import Profile
from app import db
from datetime import date


bp = Blueprint("main", __name__, url_prefix="/")


@bp.route("/", methods=("GET",))
def index():
    if session.get("user_id"):
        return redirect(url_for("main.profile"))
    return render_template("index.html")


@bp.route("/home", methods=("GET", "POST"))
def profile():
    if request.method == "POST":
        user_id = session.get("user_id")
        name = request.form.get("name")
        gender = request.form.get("gender")
        dob = request.form.get("dob")
        print(gender)
        if dob:
            dob = date.fromisoformat(dob)
        profile = db.session.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            profile = Profile(name=name, dob=dob, gender=gender, user_id=user_id)
            db.session.add(profile)
            db.session.commit()
            db.session.refresh(profile)
        else:
            profile.name = name
            profile.dob = dob
            profile.gender = gender
            db.session.commit()
            db.session.refresh(profile)
        
        return render_template("profile.html", profile=profile)


    user_id = session.get("user_id")
    if user_id:
        profile = db.session.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            profile = {}
        return render_template("profile.html", profile=profile)
    return redirect(url_for("main.index"))

@bp.route("/logout", methods=("GET",))
def logout():
    session.clear()
    return redirect(url_for("main.index"))
