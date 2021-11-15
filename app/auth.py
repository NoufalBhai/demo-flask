from flask import (
    Blueprint, render_template, request, flash, redirect, session
)
from flask.helpers import url_for
import sqlalchemy
from werkzeug.security import check_password_hash, generate_password_hash

from app.schema import User
from app import db

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("pass")
        password_hash = generate_password_hash(password)
        new_user = User(email=email, password=password_hash)
        try:
            db.session.add(new_user)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            flash("Email Already Registerd")
            return render_template("register.html", title="Registration")
        db.session.refresh(new_user)
        return  redirect(url_for("auth.login"))
    return render_template("register.html", title="Registration")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("pass")
        user = User.query.filter(User.email==email).first()
        if not user:
            flash("No User Found")
            return render_template("login.html", title="Login")
        if not check_password_hash(user.password, password):
            flash("Incorrect Password")
            return render_template("login.html", title="Login")
        session.clear()
        session["user_id"] = user.id
        return redirect(f"{url_for('main.profile')}")
    return render_template("login.html", title="Login")