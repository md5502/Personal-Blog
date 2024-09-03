from flask import Flask, redirect, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column 
from datetime import datetime

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

app.secret_key = 'super secret key'

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SESSION_TYPE'] = 'filesystem'

db.init_app(app)


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


with app.app_context():
    db.create_all()




@app.route('/')
def home():
    articles = db.session.execute(db.select(Article).order_by(Article.title)).scalars()
    return render_template('home.html', articles= articles)


@app.route('/detail_article/<id>')
def detail_article(id):
    article = db.get_or_404(Article, id)

    return render_template("article.html", article = article)


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


@app.route('/admin/dashboard')
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




if __name__ == "__main__":
   app.run(debug=True)