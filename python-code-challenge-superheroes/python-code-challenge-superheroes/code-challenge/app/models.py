from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    super_name = db.Column(db.String(255), nullable=False)
    
    powers = db.relationship('Power', secondary='hero_power', back_populates='heroes')

class Power(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    heroes = db.relationship('Hero', secondary='hero_power', back_populates='powers')

class HeroPower(db.Model):
    __tablename__ = 'hero_power'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(255), nullable=False)

    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    hero = db.relationship('Hero', back_populates='powers')

    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    power = db.relationship('Power', back_populates='heroes')
