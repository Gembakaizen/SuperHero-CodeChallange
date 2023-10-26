from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'  # Use your database URL
db = SQLAlchemy(app)

class Power(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

class HeroPower(db.Model):
    __tablename__ = 'hero_power'

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'))  # Define the foreign key to hero
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))  # Define the foreign key to powers
    strength = db.Column(db.String(255))

class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    super_name = db.Column(db.String(255))
    powers = db.relationship('Power', secondary='hero_power', backref='heroes')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
