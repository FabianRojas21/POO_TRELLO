"""
datos/repositorios/repo_tablero.py
El Tablero no tiene borrado lógico propio: vive y se oculta con su Proyecto.
"""

from datos.modelos.models import Tablero, Proyecto


def guardar_tablero(tablero):
    tablero.save()
    return True


def eliminar_tablero(tablero):
    tablero.delete_instance()
    return True


def actualizar_tablero(tablero):
    tablero.save()
    return True


def obtener_tablero(id_tablero):
    """Solo devuelve el tablero si su proyecto está activo."""
    return (Tablero.select().join(Proyecto)
            .where((Tablero.id_tablero == id_tablero) & (Proyecto.activo == True))
            .first())


def obtener_tablero_por_proyecto(proyecto):
    return Tablero.get_or_none(Tablero.id_proyecto == proyecto)


def listado_tableros():
    return list(Tablero.select())
