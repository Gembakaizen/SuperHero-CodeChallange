#!/usr/bin/env python3

from flask import Flask, make_response, render_template, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api,Resource
from models import Hero, Power, HeroPower, db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

class HeroResource(Resource):
    def get(self, id):
        hero = Hero.query.get(id)
        if hero:
            hero_info = {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
                "powers": [
                    {
                        "id": hp.power.id,
                        "name": hp.power.name,
                        "description": hp.power.description
                    }
                    for hp in hero.powers
                ]
            }
            return jsonify(hero_info)
        else:
            return {"error": "Hero not found"}, 404
@app.route('/')
def home():
    return 'Welcome to the Heroes and Powers App'

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_list = [
        {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name
        }
        for hero in heroes
    ]
    return jsonify(heroes_list)

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if hero is not None:
        hero_info = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [
                {
                    "id": hp.power.id,
                    "name": hp.power.name,
                    "description": hp.power.description
                }
                for hp in hero.powers
            ]
        }
        return jsonify(hero_info)
    else:
        return jsonify({"error": "Hero not found"}), 404

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_list = [
        {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
        for power in powers
    ]
    return jsonify(powers_list)

@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get(id)
    if power is not None:
        power_info = {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
        return jsonify(power_info)
    else:
        return jsonify({"error": "Power not found"}), 404

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power is not None:
        try:
            data = request.get_json()
            updated_description = data.get("description")
            if updated_description and len(updated_description) >= 20:
                power.description = updated_description
                db.session.commit()
                return jsonify({
                    "id": power.id,
                    "name": power.name,
                    "description": power.description
                })
            else:
                return jsonify({"errors": ["Description must be at least 20 characters long"]}), 400
        except Exception as e:
            return jsonify({"errors": ["Validation errors"]}), 400
    else:
        return jsonify({"error": "Power not found"}), 404
    
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    hero_id = data.get("hero_id")
    power_id = data.get("power_id")
    strength = data.get("strength")

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if hero is None or power is None:
        return jsonify({"errors": ["Validation errors"]}), 400

    hero_power = HeroPower(hero=hero, power=power, strength=strength)
    try:
        db.session.add(hero_power)
        db.session.commit()
        # Construct and return the JSON response
        hero_info = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [
                {
                    "id": hp.power.id,
                    "name": hp.power.name,
                    "description": hp.power.description
                }
                for hp in hero.powers
            ]
        }
        return jsonify(hero_info)
    except Exception as e:
        return jsonify({"errors": ["Validation errors"]}), 400

#resource to the API with a URL endpoint
api.add_resource(HeroResource, '/heroes/<int:id>')

if __name__ == '__main__':
    app.run(port=5555)
