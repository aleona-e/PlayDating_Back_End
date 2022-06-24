"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, Vehicles, Favorites



app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Characters.query.all()
    all_characters = list(map(lambda character: character.serialize(), characters))
    return jsonify(all_characters)

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    if request.method == 'GET':
        character = Characters.query.get(character_id)
        if character is None:
            raise APIException("Character not found")
        return jsonify(character.serialize())

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    all_planets = list(map(lambda planet: planet.serialize(), planets))
    return jsonify(all_planets)

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    if request.method == 'GET':
        planet = Planets.query.get(planet_id)
        if planet is None:
            raise APIException("Planet not found")
        return jsonify(planet.serialize())

@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    all_users = list(map(lambda user: user.serialize(), users))
    return jsonify(all_users)

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if request.method == 'GET':
        user = User.query.get(user_id)
        if user is None:
            raise APIException("User not found")
        return jsonify(user.serialize())

@app.route('/favorites/user/<int:user_id>', methods=['GET'])
def get_favorites(user_id):
    favorites = Favorites.query.filter_by(user_id = user_id).all()
    return jsonify({'favorites': [favorite.serialize() for favorite in favorites]})

@app.route('/favorites/<int:user_id>/planets/<int:planet_id>', methods=['POST', 'DELETE'])
def add_favorite_planet(user_id, planet_id):
    if request.method == 'POST':
        planet_favorite = Favorites(planet_id=planet_id, user_id=user_id)
        db.session.add(planet_favorite)
        db.session.commit()
        return jsonify(planet_favorite.serialize())

    elif request.method == 'DELETE':
        planet_favorite = Favorites.query.filter_by(planet_id = planet_id, user_id = user_id).first()
        if planet_favorite is None:
            raise APIException("Planet not in this user's favorites.")
        db.session.delete(planet_favorite)
        db.session.commit()
        return jsonify(planet_favorite.serialize())

@app.route('/favorites/<int:user_id>/characters/<int:character_id>', methods=['POST', 'DELETE'])
def add_character_planet(user_id, character_id):
    if request.method == 'POST':
        character_favorite = Favorites(character_id=character_id, user_id=user_id)
        db.session.add(character_favorite)
        db.session.commit()
        return jsonify(character_favorite.serialize())
    
    elif request.method == 'DELETE':
        character_favorite = Favorites.query.filter_by(character_id = character_id, user_id = user_id).first()
        if character_favorite is None:
            raise APIException("Character not in this user's favorites.")
        db.session.delete(character_favorite)
        db.session.commit()
        return jsonify(character_favorite.serialize())
    
# this only runs if `$  ` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
