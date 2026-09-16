CREATE DATABASE IF NOT EXISTS trello_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE trello_db;

-- 1. Tabla PROYECTO
CREATE TABLE PROYECTO (
    id_proyecto INT AUTO_INCREMENT PRIMARY KEY,
    codigo_proyecto VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NULL
) ENGINE=InnoDB;

-- 2. Tabla USUARIO
CREATE TABLE USUARIO (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    rol VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

-- 3. Tabla PROYECTO_USUARIO (Relación N:M — participación)
CREATE TABLE PROYECTO_USUARIO (
    id_proyecto INT NOT NULL,
    id_usuario INT NOT NULL,
    PRIMARY KEY (id_proyecto, id_usuario),
    CONSTRAINT fk_pu_proyecto FOREIGN KEY (id_proyecto) REFERENCES PROYECTO(id_proyecto) ON DELETE CASCADE,
    CONSTRAINT fk_pu_usuario FOREIGN KEY (id_usuario) REFERENCES USUARIO(id_usuario) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 4. Tabla TABLERO (relación 1–1 con PROYECTO, forzada con UNIQUE)
CREATE TABLE TABLERO (
    id_tablero INT AUTO_INCREMENT PRIMARY KEY,
    id_proyecto INT NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    fecha_creacion DATE NOT NULL DEFAULT (CURRENT_DATE),
    CONSTRAINT fk_tablero_proyecto FOREIGN KEY (id_proyecto) REFERENCES PROYECTO(id_proyecto) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 5. Tabla LISTA
CREATE TABLE LISTA (
    id_lista INT AUTO_INCREMENT PRIMARY KEY,
    id_tablero INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    orden INT NOT NULL,
    CONSTRAINT fk_lista_tablero FOREIGN KEY (id_tablero) REFERENCES TABLERO(id_tablero) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 6. Tabla TARJETA
CREATE TABLE TARJETA (
    id_tarjeta INT AUTO_INCREMENT PRIMARY KEY,
    id_lista INT NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT,
    fecha_limite DATE NULL,
    estado VARCHAR(50) NOT NULL DEFAULT 'pendiente',
    CONSTRAINT fk_tarjeta_lista FOREIGN KEY (id_lista) REFERENCES LISTA(id_lista) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 7. Tabla COMENTARIO
CREATE TABLE COMENTARIO (
    id_comentario INT AUTO_INCREMENT PRIMARY KEY,
    id_tarjeta INT NOT NULL,
    id_usuario INT NOT NULL,
    texto TEXT NOT NULL,
    fecha DATE NOT NULL DEFAULT (CURRENT_DATE),
    CONSTRAINT fk_comentario_tarjeta FOREIGN KEY (id_tarjeta) REFERENCES TARJETA(id_tarjeta) ON DELETE CASCADE,
    CONSTRAINT fk_comentario_usuario FOREIGN KEY (id_usuario) REFERENCES USUARIO(id_usuario) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 8. Tabla ETIQUETA
CREATE TABLE ETIQUETA (
    id_etiqueta INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    color VARCHAR(20) NOT NULL
) ENGINE=InnoDB;

-- 9. Tabla ASIGNACION_TARJETA (Relación N:M — responsables de la tarjeta)
CREATE TABLE ASIGNACION_TARJETA (
    id_tarjeta INT NOT NULL,
    id_usuario INT NOT NULL,
    PRIMARY KEY (id_tarjeta, id_usuario),
    CONSTRAINT fk_at_tarjeta FOREIGN KEY (id_tarjeta) REFERENCES TARJETA(id_tarjeta) ON DELETE CASCADE,
    CONSTRAINT fk_at_usuario FOREIGN KEY (id_usuario) REFERENCES USUARIO(id_usuario) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 10. Tabla TARJETA_ETIQUETA (Relación N:M)
CREATE TABLE TARJETA_ETIQUETA (
    id_tarjeta INT NOT NULL,
    id_etiqueta INT NOT NULL,
    PRIMARY KEY (id_tarjeta, id_etiqueta),
    CONSTRAINT fk_te_tarjeta FOREIGN KEY (id_tarjeta) REFERENCES TARJETA(id_tarjeta) ON DELETE CASCADE,
    CONSTRAINT fk_te_etiqueta FOREIGN KEY (id_etiqueta) REFERENCES ETIQUETA(id_etiqueta) ON DELETE CASCADE
) ENGINE=InnoDB;
