from flask import Blueprint, redirect, render_template, url_for,request, flash, session
from app import db
from app.models import User

from app.permissions import login_required, admin_required
from werkzeug.security import generate_password_hash, check_password_hash


bp = Blueprint('user', __name__, url_prefix='/users')


@bp.route("/")
@login_required
@admin_required
def user_list():
    users = db.session.execute(db.select(User).order_by(User.name)).scalars()
    return render_template("user/list.html", users=users)

@bp.route("/create", methods=["GET", "POST"])
@login_required
@admin_required
def user_create():
    if request.method == "POST":
        user = User(
            name=request.form["username"],
            password=generate_password_hash(request.form["password"]),
            role = request.form['role']
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user.user_detail", id=user.id))

    return render_template("user/create.html")

@bp.route("/<int:id>")
@login_required
@admin_required
def user_detail(id):
    user = db.get_or_404(User, id)
    return render_template("user/detail.html", user=user)

@bp.route("/<int:id>/delete", methods=["GET", "POST"])
@login_required
@admin_required
def user_delete(id):
    user = db.get_or_404(User, id)
    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("user.user_list"))

    return render_template("user/delete.html", user=user)
