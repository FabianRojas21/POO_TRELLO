"""
negocio/tablero.py
El Tablero se crea junto con su Proyecto (ver negocio/proyecto.py),
por eso aquí no hay crear_tablero ni eliminar_tablero.
"""

from datos.repositorios import repo_tablero, repo_lista, repo_proyecto
from negocio.lista import crear_lista


def obtener_tablero(id_tablero):
    return repo_tablero.obtener_tablero(id_tablero)


def obtener_tablero_de_proyecto(codigo_proyecto):
    proyecto = repo_proyecto.obtener_proyecto(codigo_proyecto)
    if proyecto is None:
        return None
    return repo_tablero.obtener_tablero_por_proyecto(proyecto)


def actualizar_tablero(id_tablero, **cambios):
    tablero = repo_tablero.obtener_tablero(id_tablero)
    if tablero is None:
        return None
    for campo, valor in cambios.items():
        setattr(tablero, campo, valor)
    repo_tablero.actualizar_tablero(tablero)
    return tablero


def agregar_lista(id_tablero, nombre, orden=None):
    """Si no se indica el orden, la lista queda al final del tablero."""
    if orden is None:
        orden = len(repo_lista.listado_listas(id_tablero)) + 1
    return crear_lista(id_tablero, nombre, orden)


def mostrar_listas(id_tablero):
    return repo_lista.listado_listas(id_tablero)


def quitar_lista(id_lista):
    lista = repo_lista.obtener_lista(id_lista)
    if lista is None:
        return False
    return repo_lista.eliminar_lista(lista)
