from flask import Blueprint, redirect, render_template, url_for,request, flash, session
from app import db
from app.models import Article

bp = Blueprint('blog', __name__)



@bp.route('/')
def home():
    articles = db.session.execute(db.select(Article).order_by(Article.title)).scalars()
    return render_template('blog/home.html', articles= articles)


@bp.route('/detail_article/<id>')
def detail_article(id):
    article = db.get_or_404(Article, id)

    return render_template("blog/article.html", article = article)
