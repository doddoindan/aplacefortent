from app import db
from flask import g
from app.models import Base


class Marker(Base):
    __tablename__ = 'markers'
    __table_args__ = (db.UniqueConstraint("long", "latt"),)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    long = db.Column(db.Float, nullable=False)
    latt = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(140), nullable=False)
    shop = db.Column(db.Boolean, default=False)
    water = db.Column(db.Boolean, default=False)
    potable = db.Column(db.Boolean, default=False)
    campfire = db.Column(db.Boolean, default=False)
    maxtentcount = db.Column(db.Integer, default=2)



