
from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

class HeroListResource(Resource):
    def get(self):
        heroes = Hero.query.all()
        return [hero.to_dict() for hero in heroes], 200

class HeroResource(Resource):
    def get(self, id):
        # Use db.session.get() to retrieve the hero by ID
        hero = db.session.get(Hero, id)
        if hero:
            # Include hero_powers when retrieving a single hero
            return hero.to_dict(include_powers=True), 200
        return {'error': 'Hero not found'}, 404

class PowerListResource(Resource):
    def get(self):
        powers = Power.query.all()
        return [power.to_dict() for power in powers], 200

class PowerResource(Resource):
    def get(self, id):
        power = db.session.get(Power, id)
        if power:
            return power.to_dict(), 200
        return {'error': 'Power not found'}, 404

    def patch(self, id):
        power = db.session.get(Power, id)
        if not power:
            return {'error': 'Power not found'}, 404

        data = request.get_json()

        # Validation for description
        if 'description' in data:
            description = data['description']
            if not isinstance(description, str) or len(description) < 20:
                return {'errors': ['validation errors']}, 400  # General validation error message

        try:
            if 'description' in data:
                power.description = data['description']
            db.session.commit()
            return power.to_dict(), 200
        except ValueError as e:
            return {'errors': [str(e)]}, 400


class HeroPowerResource(Resource):
    def post(self):
        data = request.get_json()

        # Validation for strength
        if data['strength'] not in ['Strong', 'Weak', 'Average']:
            return {'errors': ['validation errors']}, 400

        try:
            # Create the HeroPower
            hero_power = HeroPower(
                hero_id=data['hero_id'],
                power_id=data['power_id'],
                strength=data['strength']
            )
            db.session.add(hero_power)
            db.session.commit()

            # Retrieve related Hero and Power
            hero = db.session.get(Hero, data['hero_id'])
            power = db.session.get(Power, data['power_id'])

            # Return the HeroPower, Hero, and Power in the response
            return {
                'id': hero_power.id,
                'strength': hero_power.strength,
                'hero_id': hero_power.hero_id,
                'power_id': hero_power.power_id,
                'hero': hero.to_dict(),
                'power': power.to_dict()
            }, 201
        except ValueError as e:
            return {'errors': [str(e)]}, 400
        except Exception as e:
            return {'error': str(e)}, 500


api.add_resource(HeroListResource, '/heroes')
api.add_resource(HeroResource, '/heroes/<int:id>')
api.add_resource(PowerListResource, '/powers')
api.add_resource(PowerResource, '/powers/<int:id>')
api.add_resource(HeroPowerResource, '/hero_powers')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
