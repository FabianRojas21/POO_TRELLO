-- Conserva el motivo del borrado logico para restaurar solo los registros afectados
-- por la eliminacion del proyecto o de la lista.
ALTER TABLE LISTA
    ADD COLUMN restaurar_con_proyecto TINYINT(1) NOT NULL DEFAULT 0;

ALTER TABLE TARJETA
    ADD COLUMN restaurar_con_lista TINYINT(1) NOT NULL DEFAULT 0,
    ADD COLUMN restaurar_con_proyecto TINYINT(1) NOT NULL DEFAULT 0;

UPDATE LISTA AS l
JOIN TABLERO AS t ON t.id_tablero = l.id_tablero
JOIN PROYECTO AS p ON p.id_proyecto = t.id_proyecto
SET l.restaurar_con_proyecto = 1
WHERE l.activo = 0 AND p.activo = 0;

UPDATE TARJETA AS ta
JOIN LISTA AS l ON l.id_lista = ta.id_lista
JOIN TABLERO AS t ON t.id_tablero = l.id_tablero
JOIN PROYECTO AS p ON p.id_proyecto = t.id_proyecto
SET ta.restaurar_con_proyecto = 1
WHERE ta.activo = 0 AND p.activo = 0;

UPDATE TARJETA AS ta
JOIN LISTA AS l ON l.id_lista = ta.id_lista
JOIN TABLERO AS t ON t.id_tablero = l.id_tablero
JOIN PROYECTO AS p ON p.id_proyecto = t.id_proyecto
SET ta.restaurar_con_lista = 1
WHERE ta.activo = 0 AND l.activo = 0 AND p.activo = 1;
