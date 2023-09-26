from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

hero_powers = db.Table(
    'hero_powers',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('strength', db.String),
    db.Column('created_at', db.DateTime, server_default=db.func.now()),
    db.Column('updated_at', db.DateTime, onupdate=db.func.now()),
    db.Column('hero_id', db.Integer, db.ForeignKey('heros.id'), primary_key=True),
    db.Column('power_id', db.Integer, db.ForeignKey('powers.id'), primary_key=True)
)

class Hero(db.Model):
    __tablename__ = 'heros'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    powers = db.relationship('Power', secondary=hero_powers, backref='heroes')

    @validates('super_name')
    def validate_super_name(self, key, super_name):
        if not super_name or len(super_name) < 3:
            raise ValueError("Super name cannot be null or less than 3 characters.")
        return super_name

class Power(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('description')
    def validate_description(self, key, description):
        if not description or len(description) < 20:
            raise ValueError("Description cannot be null or less than 20 characters.")
        return description
