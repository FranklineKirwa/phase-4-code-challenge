from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)

    # Serialization rules
    serialize_only = ('id', 'name', 'super_name')

    def __repr__(self):
        return f'<Hero {self.id}>'

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

    # Serialization rules
    serialize_only = ('id', 'name', 'description')

    # Validation
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) < 1:
            raise ValueError('Power name must not be empty')
        return name

    def __repr__(self):
        return f'<Power {self.id}>'

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)

    # Relationships
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)

    hero = db.relationship('Hero', backref='hero_powers')
    power = db.relationship('Power', backref='hero_powers')

    # Serialization rules
    serialize_only = ('id', 'strength', 'hero_id', 'power_id')

    # Validation
    @validates('strength')
    def validate_strength(self, key, strength):
        if not strength or len(strength) < 1:
            raise ValueError('Strength must not be empty')
        return strength

    def __repr__(self):
        return f'<HeroPower {self.id}>'
