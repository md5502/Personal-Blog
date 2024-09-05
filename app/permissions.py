from flask import flash,session, redirect, url_for
from app.models import User 
from app import db
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            flash("You need to log in first!", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def is_logged_in():
    return 'user_id' in session

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if user.role != 'admin':
            flash("You need to be admin", "warning")
            return redirect(url_for('blog.home'))

        return f(*args, **kwargs)
    return decorated_function




def get_current_user():
    if is_logged_in():
        return db.get_or_404(User, session['user_id'])
    return None