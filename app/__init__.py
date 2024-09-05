from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app)


    from .routes import admin, auth, blog, user

    # app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(blog.bp)
    # app.register_blueprint(user.bp)

    return app