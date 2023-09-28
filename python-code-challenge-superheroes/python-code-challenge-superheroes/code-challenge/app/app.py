from flask import Flask, jsonify, request
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route("/")
def home ():
    return "home"



def validate_hero_power_data(data):
    valid_strengths = ['Strong', 'Weak', 'Average']
    errors = []

    if 'strength' not in data:
        errors.append('Strength is required.')
    elif data['strength'] not in valid_strengths:
        errors.append('Strength must be one of: Strong, Weak, Average')

    if 'power_id' not in data:
        errors.append('Power ID is required.')
    if 'hero_id' not in data:
        errors.append('Hero ID is required.')

    return errors

def validate_power_data(data):
    errors = []

    if 'description' not in data:
        errors.append('Description is required and must be at least 20 characters long.')
    elif len(data['description']) < 20:
        errors.append('Description must be at least 20 characters long.')

    return errors


@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_list = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
    return jsonify(hero_list)

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero is None:
        return jsonify({'error': 'Hero not found'}), 404

    powers = [{'id': power.id, 'name': power.name, 'description': power.description} for power in hero.powers]
    hero_data = {'id': hero.id, 'name': hero.name, 'super_name': hero.super_name, 'powers': powers}
    return jsonify(hero_data)

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_list = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(power_list)

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({'error': 'Power not found'}), 404
    power_data = {'id': power.id, 'name': power.name, 'description': power.description}
    return jsonify(power_data)

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({'error': 'Power not found'}), 404

    data = request.get_json()
    errors = validate_power_data(data)
    if errors:
        return jsonify({'errors': errors}), 400

    power.description = data['description']
    db.session.commit()
    return jsonify({'id': power.id, 'name': power.name, 'description': power.description})

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    errors = validate_hero_power_data(data)
    if errors:
        return jsonify({'errors': errors}), 400

    hero = Hero.query.get(data['hero_id'])
    power = Power.query.get(data['power_id'])

    if hero is None or power is None:
        return jsonify({'error': 'Hero or Power not found'}), 404

    hero_power = HeroPower(strength=data['strength'], hero=hero, power=power)
    db.session.add(hero_power)
    db.session.commit()

    powers = [{'id': p.id, 'name': p.name, 'description': p.description} for p in hero.powers]
    hero_data = {'id': hero.id, 'name': hero.name, 'super_name': hero.super_name, 'powers': powers}
    return jsonify(hero_data)
if __name__ == '__main__':
    app.run(debug=True, port=5555)
