from flask import url_for, request, session, redirect, render_template, flash, Blueprint
from app.utils import verify_password
from app.forms import RegistrationForm
from app.models import User
from app import db

from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = verify_password(username, password)
        if user:
            session['user_id'] = user.id  # Store user ID in session
            flash(f"Welcome back, {user.name}!", "success")
            return redirect(url_for('admin.article_list' if user.role == 'admin' else 'blog.home'))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    flash("You have been logged out.", "success")
    return redirect(url_for('auth.login'))


@bp.route('/signup', methods= ['GET', 'POST'])
def signup():


    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = generate_password_hash(form.password.data)

        new_user = User(username, password )
        db.session.add(new_user)
        db.session.commit()
        flash("the new user created successfully", "success")
        return redirect(url_for('auth.login'))
    return render_template('auth/sign_up.html', form=form)

