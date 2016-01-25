from app import db

class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())
    @property
    def as_dict(self):
        #return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
