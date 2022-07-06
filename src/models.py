from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__= "usuario"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nombre = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    provincia_id = db.Column(db.Integer, db.ForeignKey('provincia.id'), nullable=False)
    numero_hijos = db.Column(db.Integer, nullable=False)
    provincia = db.relationship('Provincia')

    def __repr__(self):
        return '<Usuario %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "nombre": self.nombre,
            "provincia": self.provincia_id,
            "numero_hijos": self.last_name
            # do not serialize the password, its a security breach
            }

class Actividad(db.Model):
    __tablename__= 'actividad'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    descripcion = db.Column(db.String(250), nullable=False)
    tipo_de_actividad_id = db.Column(db.Integer, db.ForeignKey('tipo_de_actividad.id'))
    imagen = db.Column(db.String(250), nullable=False)
    tipo_de_actividad = db.relationship('Tipo_De_Actividad')

    def __repr__(self):
        return '<Actividad %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "tipo_de_actividad": repr(self.tipo_de_actividad),
            "imagen": self.imagen
            }

class Tipo_De_Actividad(db.Model):
    __tablename__='tipo_de_actividad'
    id = db.Column(db.Integer, primary_key=True) 
    tipo = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Tipo_De_Actividad %r>' % self.tipo

    def serialize(self):
        return {
            "id": self.id,
            "tipo": self.tipo
            }
class Estados(db.Model):
    __tablename__='estados'
    id = db.Column(db.Integer, primary_key=True) 
    estado = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Estados %r>' % self.estado

    def serialize(self):
        return {
            "id": self.id,
            "estado": self.estado,
            }
        
class Evento(db.Model):
    __tablename__='evento'
    id = db.Column(db.Integer, primary_key=True)
    fecha_y_hora = db.Column(db.DateTime, nullable=False)
    creador_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    minimo_participantes = db.Column(db.Integer)
    maximo_participantes = db.Column(db.Integer)
    edad_minima = db.Column(db.Integer)
    edad_maxima = db.Column(db.Integer)
    ubicacion_id = db.Column(db.Integer, db.ForeignKey('lugar_evento.id'), nullable=False)
    estado_id = db.Column(db.Integer, db.ForeignKey('estados.id'), nullable=False)
    actividad_id = db.Column(db.Integer, db.ForeignKey('actividad.id'), nullable=False)
    creador = db.relationship('Usuario')
    ubicacion = db.relationship('Lugar_Evento')
    actividad = db.relationship('Actividad')
    estado = db.relationship('Estados')

    def __repr__(self):
        return '<Evento %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "fecha_y_hora": self.fecha_y_hora,
            "creador": self.creador_id,
            "minimo_participantes": self.minimo_participantes,
            "maximo_participantes": self.maximo_participantes,
            "ubicacion": self.ubicacion.serialize(),
            "estado": repr(self.estado),
            "actividad": repr(self.actividad)
            }


class Provincia(db.Model):
    __tablename__='provincia'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False) 

    def __repr__(self):
        return '<Provincia %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre
            }

class Lugar_Evento(db.Model):
    __tablename__='lugar_evento'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=True)
    provincia_id = db.Column(db.Integer, db.ForeignKey('provincia.id'), nullable=False)
    direccion = db.Column(db.String(150), nullable=False)
    provincia = db.relationship('Provincia')

    def __repr__(self):
        return '<Lugar_Evento %r>' % self.direccion

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "provincia": self.provincia_id,
            "direccion": self.direccion,
             }

class Participantes_Evento(db.Model):
    __tablename__='participantes_evento'
    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(db.Integer, db.ForeignKey('evento.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    num_participantes_por_usuario = db.Column(db.Integer, nullable=False)
    evento = db.relationship('Evento')
    usuario = db.relationship('Usuario')

    def __repr__(self):
        return '<Participantes_Evento %r>' % self.cantidad_participantes

    def serialize(self):
        return {
            "id": self.id,
            "evento": self.evento_id,
            "usuario": self.usuario_id,
            "num_participantes_por_usuario": self.num_participantes_por_usuario,
             }
