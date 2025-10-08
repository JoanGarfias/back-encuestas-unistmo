from extensions import db

class Respuesta(db.Model):
    __tablename__ = 'respuestas'
    id_r = db.Column(db.Integer, primary_key=True, autoincrement=True)
    correo = db.Column(db.String(255), nullable=False)
    carrera = db.Column(db.String(255), nullable=False)
    semestre = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    sexo = db.Column(db.Enum('M', 'F'), nullable=False)
    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    promedio_anterior = db.Column(db.Float, nullable=True, default=0.0)
    tiempo_traslado = db.Column(db.Integer, nullable=True)
    trabaja = db.Column(db.Boolean, nullable=False)
    gasto_mensual = db.Column(db.Float, nullable=True)
    discapacidad = db.Column(db.Boolean, nullable=False)
    peso = db.Column(db.Float, nullable=True)
    altura = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id_r": self.id_r,
            "correo": self.correo,
            "carrera": self.carrera,
            "nombre": self.nombre,
            "edad": self.edad,
            "sexo": self.sexo,
            "fecha_registro": self.fecha_registro,
            "promedio_anterior": self.promedio_anterior,
            "tiempo_traslado": self.tiempo_traslado,
            "trabaja": self.trabaja,
            "gasto_mensual": self.gasto_mensual,
            "discapacidad": self.discapacidad,
            "peso": self.peso,
            "altura": self.altura,
            "edad": self.edad
        }
