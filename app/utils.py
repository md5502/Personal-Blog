from app import auth, db
from app.models import User
from werkzeug.security import check_password_hash, generate_password_hash



@auth.verify_password
def verify_password(username, password):
    users = db.session.execute(db.select(User).order_by(User.name)).scalars()
    for user in users:
        if user.name == username:
            if check_password_hash(user.password ,password):
                return user
    return False

def create_super_user(username, password):
    admin_user = User(username, generate_password_hash(password), "admin")
    db.session.add(admin_user)
    db.session.commit()
    print("super user created successfully")
