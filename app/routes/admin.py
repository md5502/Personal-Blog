from flask import Blueprint,flash, request,  redirect, render_template, url_for
from app import db
from app.models import Article, User
from app.permissions import login_required, admin_required
from datetime import datetime
from werkzeug.security import generate_password_hash



bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/articles')
@login_required
def article_list():
    articles = db.session.execute(db.select(Article).order_by(Article.title)).scalars()
    return render_template("admin/article_list.html", articles=articles)


@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template("admin/dashboard.html")


@bp.route('/article/create', methods=['GET', 'POST'])
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

            return redirect(url_for('blog.home'))
    return render_template('admin/add-article.html')

@bp.route('/article/edit/<id>', methods=['GET', 'POST'])
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

            return redirect(url_for('article_list'))
    return render_template('admin/edit-article.html', old_article = old_article)

@bp.route('/article/delete/<id>', methods= ['GET', 'POST'])
def delete_article(id):
    article = db.get_or_404(Article, id)
    if request.method == "POST":
        db.session.delete(article)
        db.session.commit()
        flash("article deleted successfully", 'success')
        return redirect(url_for('article_list'))
    return render_template("admin/delete_article.html", article=article)




@bp.route("/users")
@login_required
@admin_required
def user_list():
    users = db.session.execute(db.select(User).order_by(User.name)).scalars()
    return render_template("user/list.html", users=users)

@bp.route("/users/create", methods=["GET", "POST"])
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

@bp.route("/user/<int:id>")
@login_required
@admin_required
def user_detail(id):
    user = db.get_or_404(User, id)
    return render_template("user/detail.html", user=user)

@bp.route("/user/<int:id>/delete", methods=["GET", "POST"])
@login_required
@admin_required
def user_delete(id):
    user = db.get_or_404(User, id)
    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("user_list"))

    return render_template("user/delete.html", user=user)
