from flask import Flask, redirect, render_template, request, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column 
from datetime import datetime
from flask_httpauth import HTTPBasicAuth


from forms import RegistrationForm

from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
auth = HTTPBasicAuth()

app.secret_key = 'super secret key'

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SESSION_TYPE'] = 'filesystem'

db.init_app(app)




def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            flash("You need to log in first!", "warning")
            return redirect(url_for('login'))
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
            return redirect(url_for('home'))

        return f(*args, **kwargs)
    return decorated_function




def get_current_user():
    if is_logged_in():
        return db.get_or_404(User, session['user_id'])
    return None



class Base():
    id = db.Column(db.Integer, primary_key=True, )
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


class Article(Base, db.Model):
    title = db.Column(db.String(50))
    description = db.Column(db.Text)


    def __init__(self, title, description, updated_on=''):
        self.title = title
        self.description = description
        if updated_on == '':
            self.updated_on = self.created_at
        else:
            self.updated_on = updated_on

    def __repr__(self) -> str:
        return f"{self.id}, {self.title}"


class User(Base, db.Model):
    name = db.Column(db.String(50))
    password = db.Column(db.String(255))
    role = db.Column(db.String(10))

    def __init__(self, name, password, role='user') -> None:
        self.name = name
        self.password = password
        self.role = role
    
    def __repr__(self) -> str:
        return f"{self.id}, {self.name} "


with app.app_context():
    db.create_all()




@auth.verify_password
def verify_password(username, password):
    users = db.session.execute(db.select(User).order_by(User.name)).scalars()
    for user in users:
        if user.name == username:
            if check_password_hash(user.password ,password):
                return user
    return False



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = verify_password(username, password)
        if user:
            session['user_id'] = user.id  # Store user ID in session
            flash(f"Welcome back, {user.name}!", "success")
            return redirect(url_for('dashboard' if user.role == 'admin' else 'home'))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for('login'))
    return render_template('auth/login.html')

@app.route('/signup', methods= ['GET', 'POST'])
def signup():


    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = generate_password_hash(form.password.data)

        new_user = User(username, password )
        db.session.add(new_user)
        db.session.commit()
        flash("the new user created successfully", "success")
        return redirect(url_for('login'))
    return render_template('auth/sign_up.html', form=form)


@app.route('/')
def home():
    articles = db.session.execute(db.select(Article).order_by(Article.title)).scalars()
    return render_template('blog/home.html', articles= articles)


@app.route('/detail_article/<id>')
def detail_article(id):
    article = db.get_or_404(Article, id)

    return render_template("blog/article.html", article = article)


@app.route('/admin/article/create', methods=['GET', 'POST'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']

        if title == '' or content == '':
            flash("fields can not be empty", 'warning')
            return redirect(url_for('create_article'))
        else:
            new_article = Article(title, content)
            db.session.add(new_article)
            db.session.commit()
            db.session.close()
            flash("the article created successfully", 'success')

            return redirect(url_for('home'))
    return render_template('admin/add-article.html')


@app.route('/dashboard')
@login_required
def dashboard():
    articles = db.session.execute(db.select(Article).order_by(Article.title)).scalars()
    return render_template("admin/dashboard.html", articles=articles)


@app.route('/admin/article/edit/<id>', methods=['GET', 'POST'])
def edit_article(id):
    old_article = db.get_or_404(Article, id)

    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']   
        if title == '' or content == '':
            flash("fields can not be empty", "danger")
            return redirect(url_for('edit_article', id=id))
        else:
            new_article = Article.query.filter_by(id=id).first_or_404()
            new_article.title = title
            new_article.description = content
            new_article.updated_on = datetime.now()
            db.session.commit()
            db.session.close()
            


            flash("the article update successfully", 'success')

            return redirect(url_for('dashboard'))
    return render_template('admin/edit-article.html', old_article = old_article)

@app.route('/admin/article/delete/<id>', methods= ['GET', 'POST'])
def delete_article(id):
    article = db.get_or_404(Article, id)
    if request.method == "POST":
        db.session.delete(article)
        db.session.commit()
        flash("article deleted successfully", 'success')
        return redirect(url_for('dashboard'))
    return render_template("admin/delete_article.html", article=article)


@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))


@app.route("/admin/users")
@login_required
@admin_required
def user_list():
    users = db.session.execute(db.select(User).order_by(User.name)).scalars()
    return render_template("user/list.html", users=users)

@app.route("/admin/users/create", methods=["GET", "POST"])
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
        return redirect(url_for("user_detail", id=user.id))

    return render_template("user/create.html")

@app.route("/admin/user/<int:id>")
@login_required
@admin_required
def user_detail(id):
    user = db.get_or_404(User, id)
    return render_template("user/detail.html", user=user)

@app.route("/admin/user/<int:id>/delete", methods=["GET", "POST"])
@login_required
@admin_required
def user_delete(id):
    user = db.get_or_404(User, id)
    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("user_list"))

    return render_template("user/delete.html", user=user)

if __name__ == "__main__":
   app.run(debug=True)