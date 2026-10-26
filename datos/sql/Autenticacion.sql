-- Ejecutar una sola vez en bases de datos existentes.
ALTER TABLE USUARIO
    ADD COLUMN `contraseña` VARCHAR(255) NULL;
