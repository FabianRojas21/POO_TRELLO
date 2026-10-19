"""
datos/repositorios/repo_tablero.py
"""

from datos.modelos.models import Tablero


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
    return Tablero.get_or_none(Tablero.id_tablero == id_tablero)


def obtener_tablero_por_proyecto(proyecto):
    return Tablero.get_or_none(Tablero.id_proyecto == proyecto)


def listado_tableros():
    return list(Tablero.select())
