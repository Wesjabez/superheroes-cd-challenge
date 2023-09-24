from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
db = SQLAlchemy(app)

class Hero(db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    super_name = db.Column(db.String(255), nullable=False)
    
    hero_powers = db.relationship('HeroPower', back_populates='hero')
    powers = db.relationship('Power', secondary='hero_power', back_populates='heroes')

class Power(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    
    hero_powers = db.relationship('HeroPower', back_populates='power')
    heroes = db.relationship('Hero', secondary='hero_power', back_populates='powers')

class HeroPower(db.Model):
    __tablename__ = 'hero_power'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(50), nullable=False)
    
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')

    @validates('strength')
    def validate_strength(self, key, value):
        if value not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be either 'Strong', 'Weak', 'Average'")
        return value

    @validates('description')
    def validate_description(self, key, value):
        if len(value) < 20:
            raise ValueError("Description must be at least 20 characters ")
        return value


@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_list = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
    return jsonify(hero_list)


@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if hero:
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': [{'id': power.id, 'name': power.name, 'description': power.description} for power in hero.powers]
        }
        return jsonify(hero_data)
    return jsonify({'error': 'Hero not found'}), 404

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_list = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(power_list)


@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get(id)
    if power:
        power_data = {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }
        return jsonify(power_data)
    return jsonify({'error': 'Power not found'}), 404


@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power_description(id):
    power = Power.query.get(id)
    if power:
        data = request.get_json()
        if 'description' in data:
            new_description = data['description']
            if len(new_description) >= 20:
                power.description = new_description
                db.session.commit()
                return jsonify({'id': power.id, 'name': power.name, 'description': power.description})
            else:
                return jsonify({'errors': ['Description must be at least 20 characters']}), 400
    return jsonify({'error': 'Power not found'}), 404


@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    if all(key in data for key in ('strength', 'power_id', 'hero_id')):
        strength = data['strength']
        power_id = data['power_id']
        hero_id = data['hero_id']
        
        if strength in ['Strong', 'Weak', 'Average']:
            hero = Hero.query.get(hero_id)
            power = Power.query.get(power_id)
            
            if hero and power:
                hero_power = HeroPower(strength=strength, hero=hero, power=power)
                db.session.add(hero_power)
                db.session.commit()
                
                hero_data = {
                    'id': hero.id,
                    'name': hero.name,
                    'super_name': hero.super_name,
                    'powers': [{'id': p.id, 'name': p.name, 'description': p.description} for p in hero.powers]
                }
                return jsonify(hero_data), 201
            else:
                return jsonify({'errors': ['Hero or Power not found']}), 404
        else:
            return jsonify({'errors': ['Strength must be either Strong, Weak, or Average']}), 400
    return jsonify({'errors': ['Invalid request data']}), 400

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
