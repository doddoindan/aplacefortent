from app import db, app

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    nickname = db.Column(db.String(64), unique=True)

 
    def __init__(self, email, nickname=None):
        self.email = email.lower()
        self.first_name = first_name
        self.last_name = last_name
 
    # These four methods are for Flask-Login
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)