
Create table Requerimiento (
	id INT AUTO_INCREMENT PRIMARY KEY,
	nombre VARCHAR(100) NOT NULL,
	telefono VARCHAR(20) NOT NULL,
	requerimiento TEXT NOT NULL,
	fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);