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
from models import db, Usuario, Actividad, Evento, Provincia, Lugar_Evento, Participantes_Evento, Tipo_De_Actividad, Estados

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


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

#guardar data de usuario y validar
@app.route('/nuevo/registro', methods=['POST'])    
def registro():
    body = request.get_json()
    email = body['email']
    password = body['password']
    nombre = body['nombre']
    provincia = body['provincia']
    numero_hijos = body['numero_hijos']
    aux_usuario = Usuario.query.filter_by(email=email).first()
    if not (aux_usuario is None):
       raise APIException("Usuario ya existe.")
    usuario = Usuario(email=email, password=password, is_active=True)
    db.session.add(usuario)
    db.session.commit()
    return jsonify(usuario.serialize()),201

#validar usuario y generar token
@app.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    email = body['email']
    password = body['password']
    usuario = Usuario.query.filter_by(email=email).first()
    if usuario is None:
        raise APIException("Usuario no existe")
    if usuario.password != password:
        raise APIException("Usuario no encontrado")
    data = {
        'email': usuario.email,
        'usuario_id': usuario.id
    }
    token = create_access_token(identity=data)
    return jsonify(token)

#obtener toda la info de todas las actividades
@app.route('/actividades', methods=['GET'])
@jwt_required()
def get_actividades():
    actividades = Actividad.query.all()
    all_actividades = list(map(lambda actividad: actividad.serialize(), actividades))
    return jsonify(all_actividades)

#obtener detalle actividad por id
@app.route('/actividades/<int:actividad_id>', methods=['GET'])
def get_actividad(actividad_id):
    if request.method == 'GET':
        actividad = Actividad.query.get(actividad_id)
        if actividad is None:
            raise APIException("Actividad no encontrada")
        return jsonify(actividad.serialize())

#obtener eventos en provincia especifica  SOS
@app.route('/eventos/<int:provincia_id>', methods=['GET'])
@jwt_required()
def get_eventos(provincia_id):
    lugares = Lugar_Evento.query.filter_by(provincia_id = provincia_id).all()
    #db lugar_evento: id, evento_id, provincia_id, direccion
    all_eventos = []
    for lugar in lugares:
        eventos = Evento.query.filter_by(ubicacion_id = lugar.id).all()
        for evento in eventos:
           all_eventos.append(evento) 
    all_eventos_serialized = list(map(lambda evento: evento.serialize(), all_eventos))
    return jsonify(all_eventos_serialized)

#obtener informacion detalle de evento por id
@app.route('/evento/<int:evento_id>', methods=['GET'])
@jwt_required()
def get_evento(evento_id):
    if request.method == 'GET':
        evento = Evento.query.get(evento_id)
        if evento is None:
            raise APIException("Evento no encontrado")
        return jsonify(evento.serialize())

@app.route('/eventoscreados/usuario/<int:usuario_id>', methods=['GET'])
@jwt_required()
def get_eventos_creados_usuario(usuario_id):
    eventos = Evento.query.filter_by(creador_id = usuario_id).all()
    eventos_creados = list(map(lambda evento: evento.serialize(), eventos))
    return jsonify(eventos_creados)

# #hasta aquí todos los endpoints están probados, para probarlos sin token solo quitar el decorador de JWT_required
    
# this only runs if `$  ` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
