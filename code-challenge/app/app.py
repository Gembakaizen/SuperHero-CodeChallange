#!/usr/bin/env python3

from flask import Flask, make_response, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return 'Welcome to the Heroes and Powers App'

@app.route('/heroes')
def list_heroes():
    heroes = Hero.query.all()
    return render_template('heroes.html', heroes=heroes)

@app.route('/powers')
def list_powers():
    powers = Power.query.all()
    return render_template('powers.html', powers=powers)

if __name__ == '__main__':
    app.run(port=5555)
