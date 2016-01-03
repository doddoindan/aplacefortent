from app import db, app
import re

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    nickname = db.Column(db.String(64), unique=True)
    social_id = db.Column(db.String(64), unique=True)
    location = db.Column(db.String(64))
 
    def __init__(self, social_id	, email, nickname=None):
        self.email = email.lower()
        self.social_id = social_id
        self.nickname = nickname
 
    # These four methods are for Flask-Login
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)
    @staticmethod
    def make_valid_nickname(nickname):
         return re.sub('[^a-zA-Z0-9_\.]', '', nickname)   
		        
    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first() is None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first() is None:
                break
            version += 1
        return new_nickname

     