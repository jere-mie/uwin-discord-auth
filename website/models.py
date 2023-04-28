from website import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    discord_id = db.Column(db.String, unique=True)
    def __repr__(self):
        return f'<User: {self.id} ~ {self.email} ~ {self.name}>'
