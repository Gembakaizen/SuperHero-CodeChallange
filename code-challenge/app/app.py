#!/usr/bin/env python3

from flask import Flask, make_response, render_template, request, redirect, url_for
from flask_migrate import Migrate

from models import db, Hero, Power  # Import the Power model

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables

    @app.route('/')
    def index():
        heroes = Hero.query.all()
        return render_template('index.html', heroes=heroes)

    @app.route('/powers')
    def list_powers():
        powers = Power.query.all()
        return render_template('powers.html', powers=powers)

    @app.route('/heroes/<int:hero_id>')
    def hero_details(hero_id):
        hero = Hero.query.get(hero_id)
        return render_template('hero_details.html', hero=hero)

    @app.route('/powers/<int:power_id>')
    def power_details(power_id):
        power = Power.query.get(power_id)
        return render_template('power_details.html', power=power)

    app.run(debug=True)
