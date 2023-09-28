from app import db, app  
from models import Hero, Power, HeroPower


def create_heroes():
    heroes_data = [
        {"name": "Clark Kent", "super_name": "Superman"},
        {"name": "Bruce Wayne", "super_name": "Batman"},
        {"name": "Peter Parker",  "super_name": "Spiderman"}
    ]

    for data in heroes_data:
        hero = Hero(**data)
        db.session.add(hero)

def create_powers():
    powers_data = [
        {"name": "Super Strength", "description": "Incredibly strong"},
        {"name": "Flight", "description": "Can fly at high speeds"},
        {"name": "agility", "description": "Can move efficiently from building to building"}
        
    ]

    for data in powers_data:
        power = Power(**data)
        db.session.add(power)

def create_hero_powers():
    hero_powers_data = [
        {"strength": "High", "hero_id": 1, "power_id": 1},
        {"strength": "Medium", "hero_id": 2, "power_id": 2},
        
    ]

    for data in hero_powers_data:
        hero_power = HeroPower(**data)
        db.session.add(hero_power)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
        create_heroes()
        create_powers()
        create_hero_powers()

        db.session.commit()  
