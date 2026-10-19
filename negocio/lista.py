"""
negocio/lista.py
"""

from datos.modelos.models import Lista
from datos.repositorios import repo_lista, repo_tablero, repo_tarjeta


def crear_lista(id_tablero, nombre, orden):
    tablero = repo_tablero.obtener_tablero(id_tablero)
    if tablero is None:
        return None
    lista = Lista(id_tablero=tablero, nombre=nombre, orden=orden)
    repo_lista.guardar_lista(lista)
    return lista


def obtener_lista(id_lista):
    return repo_lista.obtener_lista(id_lista)


def listado_listas(id_tablero=None):
    return repo_lista.listado_listas(id_tablero)


def actualizar_lista(id_lista, **cambios):
    lista = repo_lista.obtener_lista(id_lista)
    if lista is None:
        return None
    for campo, valor in cambios.items():
        setattr(lista, campo, valor)
    repo_lista.actualizar_lista(lista)
    return lista


def eliminar_lista(id_lista):
    lista = repo_lista.obtener_lista(id_lista)
    if lista is None:
        return False
    return repo_lista.eliminar_lista(lista)


def agregar_tarjeta(id_lista, tarjeta):
    """Paso interno de Tarjeta.mover(): deja la tarjeta en esta lista."""
    tarjeta.id_lista = id_lista
    repo_tarjeta.actualizar_tarjeta(tarjeta)
    return tarjeta


def quitar_tarjeta(tarjeta):
    """
    Paso interno de Tarjeta.mover(). La FK id_lista es obligatoria (no existe
    'tarjeta sin lista'), así que no borra nada: agregar_tarjeta() hace el cambio.
    """
    return tarjeta
