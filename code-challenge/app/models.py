from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Power(db.Model):
    __tablename__ = 'power'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)

    def __init__(self, name, description):
        self.name = name
        self.description = description

class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    super_name = db.Column(db.String(255))


class HeroPower(db.Model):
    __tablename__ = 'hero_power'

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'))
    strength = db.Column(db.String(10))

    hero = db.relationship('Hero', backref=db.backref('hero_powers', lazy=True))
    power = db.relationship('Power', backref=db.backref('power_heroes', lazy=True))
