from app import db, app
import re


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    nickname = db.Column(db.String(64), unique=True)
    social_id = db.Column(db.String(64), unique=True)
    location = db.Column(db.String(64))
    markers = db.relationship('Marker', backref='owner', lazy='dynamic')


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


class Marker(db.Model):
    __tablename__ = 'markers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    long = db.Column(db.Float, nullable=False)
    latt = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime)
    description = db.Column(db.String(140), nullable=False)
    shop = db.Column(db.Boolean, default=False)
    water = db.Column(db.Boolean, default=False)
    potable = db.Column(db.Boolean, default=False)
    campfire = db.Column(db.Boolean, default=False)
    maxtentcount = db.Column(db.Integer, default=2)

    _constr = db.UniqueConstraint("long", "latt")

    @property
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns }

