
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)

    hero_powers = db.relationship('HeroPower', backref='hero_assoc', lazy=True)

    # Exclude 'hero_powers' by default but can be included via the custom to_dict method
    serialize_rules = ('-hero_powers.powers_assoc',)

    def __repr__(self):
        return f'<Hero {self.id}>'

    def to_dict(self, include_powers=False):
        """Custom method to include hero_powers in the serialized output."""
        hero_dict = {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name,
        }
        if include_powers:
            hero_dict['hero_powers'] = [hp.to_dict() for hp in self.hero_powers]
        return hero_dict


class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    hero_powers = db.relationship('HeroPower', backref='power_assoc', lazy=True)

    serialize_rules = ('-hero_powers',)

    def __repr__(self):
        return f'<Power {self.id}>'

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    strength = db.Column(db.String, nullable=False)

    serialize_rules = ('-hero_assoc', '-power_assoc',)

    def __repr__(self):
        return f'<HeroPower {self.id}>'



