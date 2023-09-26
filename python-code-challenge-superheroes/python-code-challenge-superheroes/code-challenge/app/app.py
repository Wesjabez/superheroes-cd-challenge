from flask import Flask, request, jsonify
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heroes.db'
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_list = [{"id": hero.id, "name": hero.name, "super_name": hero.super_name} for hero in heroes]
    return jsonify(hero_list)

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero is None:
        return jsonify({"error": "Hero not found"}), 404

    hero_data = {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "powers": [{"id": power.id, "name": power.name, "description": power.description} for power in hero.powers]
    }
    return jsonify(hero_data)

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_list = [{"id": power.id, "name": power.name, "description": power.description} for power in powers]
    return jsonify(power_list)

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({"error": "Power not found"}), 404
    power_data = {"id": power.id, "name": power.name, "description": power.description}
    return jsonify(power_data)

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({"error": "Power not found"}), 404

    data = request.get_json()
    description = data.get("description")

    if description:
        power.description = description
        db.session.commit()
        return jsonify({"id": power.id, "name": power.name, "description": power.description})
    else:
        return jsonify({"errors": ["validation errors"]}), 400

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    strength = data.get("strength")
    power_id = data.get("power_id")
    hero_id = data.get("hero_id")

    if not (strength and power_id and hero_id):
        return jsonify({"errors": ["validation errors"]}), 400

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if hero is None or power is None:
        return jsonify({"errors": ["Hero or Power not found"]}), 404

    hero_power = HeroPower(hero=hero, power=power, strength=strength)
    db.session.add(hero_power)
    db.session.commit()

    hero_data = {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "powers": [{"id": p.id, "name": p.name, "description": p.description} for p in hero.powers]
    }
    return jsonify(hero_data), 201

if __name__ == '__main__':
    app.run(debug=True)
