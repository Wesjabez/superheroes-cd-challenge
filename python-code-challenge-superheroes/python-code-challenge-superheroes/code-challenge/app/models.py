from database import db

hero_powers = db.Table(
    'hero_powers',
    db.Column('hero_id', db.Integer, db.ForeignKey('hero.id'), primary_key=True),
    db.Column('power_id', db.Integer, db.ForeignKey('power.id'), primary_key=True),
    db.Column('strength', db.String(10), nullable=False),
)

class Hero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    super_name = db.Column(db.String(255), nullable=False)
    powers = db.relationship('Power', secondary=hero_powers, back_populates='heroes')

class Power(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    power_heroes = db.relationship('Hero', secondary=hero_powers, back_populates='powers')

class HeroPower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), nullable=False)
    strength = db.Column(db.String(10), nullable=False)
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='power_heroes')
