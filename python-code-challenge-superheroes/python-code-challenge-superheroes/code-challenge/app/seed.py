from flask import Flask
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heroes.db'
db.init_app(app)

with app.app_context():
    db.create_all()

    power1 = Power(name="Super Strength", description="Gives the wielder super-human strengths")
    power2 = Power(name="Flight", description="Gives the wielder the ability to fly through the skies at supersonic speed")
    power3 = Power(name="Telekinesis", description="Allows the wielder to move objects with their mind")

    db.session.add_all([power1, power2, power3])
    db.session.commit()

    hero1 = Hero(name="Kamala Khan", super_name="Ms. Marvel")
    hero2 = Hero(name="Doreen Green", super_name="Squirrel Girl")
    hero3 = Hero(name="Gwen Stacy", super_name="Spider-Gwen")

    db.session.add_all([hero1, hero2, hero3])
    db.session.commit()

    hero_power1 = HeroPower(hero=hero1, power=power1, strength="Strong")
    hero_power2 = HeroPower(hero=hero1, power=power2, strength="Average")
    hero_power3 = HeroPower(hero=hero2, power=power1, strength="Strong")
    hero_power4 = HeroPower(hero=hero2, power=power3, strength="Average")
    hero_power5 = HeroPower(hero=hero3, power=power2, strength="Weak")

    db.session.add_all([hero_power1, hero_power2, hero_power3, hero_power4, hero_power5])
    db.session.commit()

print("Database seeding completed.")
