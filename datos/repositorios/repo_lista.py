"""
datos/repositorios/repo_lista.py
"""

from datos.modelos.models import Lista


def guardar_lista(lista):
    lista.save()
    return True


def eliminar_lista(lista):
    lista.delete_instance()
    return True


def actualizar_lista(lista):
    lista.save()
    return True


def obtener_lista(id_lista):
    return Lista.get_or_none(Lista.id_lista == id_lista)


def listado_listas(id_tablero=None):
    consulta = Lista.select().order_by(Lista.orden)
    if id_tablero is not None:
        consulta = consulta.where(Lista.id_tablero == id_tablero)
    return list(consulta)
