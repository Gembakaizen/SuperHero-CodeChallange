from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Use your database URL
db = SQLAlchemy(app)

class Power(db.Model):
    __tablename__ = 'powers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    # Define the relationship to HeroPower
    hero_powers = db.relationship('HeroPower', back_populates='power')

# Define the Hero model
class Hero(db.Model):
    __tablename__ = 'heroes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    super_name = db.Column(db.String(255), nullable=False)
    # Define the relationship to HeroPower
    hero_powers = db.relationship('HeroPower', back_populates='hero')

# Define the HeroPower model
class HeroPower(db.Model):
    __tablename__ = 'hero_powers'
    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    strength = db.Column(db.String(20), nullable=False)
    # Define the relationships to Hero and Power
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
