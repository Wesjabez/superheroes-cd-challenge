
from flask import Flask, jsonify, request, abort
from models import db, Hero, Power, HeroPower
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/')
def home ():
     return ""

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_data = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
    return jsonify(hero_data)


@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404

    hero_data = {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "powers": [
            {
                "id": power.id,
                "name": power.name,
                "description": power.description
            } for power in hero.powers
        ]
    }
    return jsonify(hero_data)

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_data = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(power_data)

@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    power_data = {
        "id": power.id,
        "name": power.name,
        "description": power.description
    }
    return jsonify(power_data)

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    form = PowerForm(request.form)
    if form.validate():
        description = request.json.get("description")
        power.description = description
        db.session.commit()
        return jsonify({
            "id": power.id,
            "name": power.name,
            "description": power.description
        })
    else:
        return jsonify({"errors": form.errors}), 400

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    form = HeroPowerForm(request.form)
    if form.validate():
        power_id = request.json.get("power_id")
        hero_id = request.json.get("hero_id")
        strength = request.json.get("strength")

        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)

        if not hero or not power:
            return jsonify({"error": "Hero or Power not found"}), 404

        hero_power = HeroPower(strength=strength, power=power, hero=hero)
        db.session.add(hero_power)
        db.session.commit()
aoo
        hero_data = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [
                {
                    "id": power.id,
                    "name": power.name,
                    "description": power.description
                } for power in hero.powers
            ]
        }
        return jsonify(hero_data), 201
    else:
        return jsonify({"errors": form.errors}), 400



if __name__ == '__main__':
    app.run(port=5555)
