use encuestas;

CREATE TABLE respuestas(
	id_r INT PRIMARY KEY AUTO_INCREMENT,
	correo VARCHAR(128) NOT NULL,
	carrera VARCHAR(128) NOT NULL,
	nombre VARCHAR(255) NOT NULL,
	edad INT NOT NULL,
	sexo ENUM('M', 'F') NOT NULL,
	semestre INT NOT NULL,
	CONSTRAINT chk_semestre CHECK (semestre IN (1,2,3,4,5,6,7,8,9,10)),
	fecha_registro DATE NOT NULL,
	promedio_anterior DECIMAL(3,1),
	tiempo_traslado INT,
	trabaja BOOL NOT NULL,
	gasto_mensual DECIMAL (10, 2),
	discapacidad BOOL NOT NULL,
	peso DECIMAL(5,2),
	altura DECIMAL(5, 2) NOT NULL
);
