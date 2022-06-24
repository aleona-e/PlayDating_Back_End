from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    __tablename__= "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(250), nullable=False)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name
            # do not serialize the password, its a security breach
            }

class Favorites(db.Model):
    __tablename__= 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=True)
    users = db.relationship('User')
    characters = db.relationship('Characters')
    planets = db.relationship('Planets')
    vehicles = db.relationship('Vehicles')

    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "vehicle_id": self.vehicle_id
            }
        
class Vehicles(db.Model):
    __tablename__='vehicles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    model = db.Column(db.String(120))
    vehicle_class = db.Column(db.String(120))
    manufacturers = db.Column(db.String(120))
    cost = db.Column(db.Integer)
    length = db.Column(db.Integer)
    crew = db.Column(db.Integer)
    passengers = db.Column(db.Integer)
    pilots_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    pilots = db.relationship('Characters')

    def __repr__(self):
        return '<Vehicles %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturers": self.manufacturers,
            "cost": self.cost,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,
            "pilots_id": self.pilots_id
            }


class Planets(db.Model):
    __tablename__='planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120)) 
    terrain = db.Column(db.String(10))
    population = db.Column(db.Integer)
    diameter = db.Column(db.Integer) 
    surface_water = db.Column(db.Integer) 
    gravity = db.Column(db.String(120))
    climate = db.Column(db.String(120)) 
    orbital_period = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "population": self.population,
            "diameter": self.diameter,
            "surface_water": self.surface_water,
            "gravity": self.gravity,
            "climate": self.climate,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period
            }

class Characters(db.Model):
    __tablename__='characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    gender = db.Column(db.String(120))
    hair_color = db.Column(db.String(120))
    eye_color = db.Column(db.String(120))
    mass = db.Column(db.Integer)
    height = db.Column(db.Integer)
    birth_year = db.Column(db.String(120)) 
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id')) #tablename
    planets = db.relationship('Planets') #class

    def __repr__(self):
        return '<Characters %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "mass": self.mass,
            "height": self.height,
            "birth_year": self.birth_year,
            "planet_id": self.planet_id,
            
            }
