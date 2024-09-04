from app import db , User, generate_password_hash

def create_super_user(username, password):
    admin_user = User(username, generate_password_hash(password), "admin")
    db.session.add(admin_user)
    db.session.commit()
    print("super user created successfully")

create_super_user('admin', 'admin')