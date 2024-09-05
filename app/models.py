from . import db

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