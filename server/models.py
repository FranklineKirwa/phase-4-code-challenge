
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

# Initialize the SQLAlchemy object
db = SQLAlchemy()

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes' # Define the name of the database table

    id = db.Column(db.Integer, primary_key=True)  # Primary key for the Hero
    name = db.Column(db.String, nullable=False)  # Name of the hero
    super_name = db.Column(db.String, nullable=False) # Superhero name

    # Define a one-to-many relationship with the HeroPower model
    hero_powers = db.relationship('HeroPower', backref='hero_assoc', lazy=True)

    # Serializer rules: Exclude 'hero_powers' by default from serialization
    serialize_rules = ('-hero_powers.powers_assoc',)

    def __repr__(self):
        return f'<Hero {self.id}>'  # String representation of the Hero object

    def to_dict(self, include_powers=False):
        """Custom method to include hero_powers in the serialized output."""
        hero_dict = {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name,
        }
        if include_powers:
             # If include_powers is True, include hero_powers
            hero_dict['hero_powers'] = [hp.to_dict() for hp in self.hero_powers]
        return hero_dict

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'  # Define the name of the database table

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

     # Define a one-to-many relationship with the HeroPower model
    hero_powers = db.relationship('HeroPower', backref='power_assoc', lazy=True)

    # Serializer rules: Exclude 'hero_powers' from serialization
    serialize_rules = ('-hero_powers',)

    def __repr__(self):
        return f'<Power {self.id}>' # String representation of the Power object

    @staticmethod
    def validate_description(description):
        """Raise ValueError if description is too short."""
        if not isinstance(description, str) or len(description) < 20:
            raise ValueError("Description must be at least 20 characters long.")

    def __init__(self, name, description, *args, **kwargs):
        self.validate_description(description)  # Validate description before assigning
        super().__init__(name=name, description=description, *args, **kwargs) # Call parent constructor


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'  # Define the name of the database table

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    _strength = db.Column('strength', db.String, nullable=False)

     # Serializer rules: Exclude associated Hero and Power from serialization
    serialize_rules = ('-hero_assoc', '-power_assoc',)

    VALID_STRENGTHS = ['Strong', 'Weak', 'Average']  # Valid strength values

    def __repr__(self):
        return f'<HeroPower {self.id}>' # String representation of the HeroPower object

    @property
    def strength(self):
        return self._strength

    @strength.setter
    def strength(self, value):
        if value not in self.VALID_STRENGTHS:
            raise ValueError(f"Invalid strength value: {value}. Must be one of {self.VALID_STRENGTHS}.")
        self._strength = value

    def __init__(self, hero_id, power_id, strength, *args, **kwargs):
        self.hero_id = hero_id # Assign the hero ID
        self.power_id = power_id  # Assign the power ID
        self.strength = strength  # Assign the strength
        super().__init__(*args, **kwargs) # Call parent constructor




