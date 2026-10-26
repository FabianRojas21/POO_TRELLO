"""
negocio/tablero.py
El Tablero se crea junto con su Proyecto (ver negocio/proyecto.py) y se oculta con él,
por eso aquí no hay crear_tablero ni eliminar_tablero.
"""

from datos.repositorios import repo_tablero, repo_lista, repo_proyecto
from negocio.lista import crear_lista, eliminar_lista
from negocio import sesion


def obtener_tablero(id_tablero):
    tablero = repo_tablero.obtener_tablero(id_tablero)
    if tablero is not None:
        sesion.exigir_tablero(tablero)
    return tablero


def obtener_tablero_de_proyecto(codigo_proyecto):
    proyecto = repo_proyecto.obtener_proyecto(codigo_proyecto)
    if proyecto is None:
        return None
    sesion.exigir_proyecto(proyecto)
    return repo_tablero.obtener_tablero_por_proyecto(proyecto)


def actualizar_tablero(id_tablero, **cambios):
    sesion.exigir_jefe()
    tablero = repo_tablero.obtener_tablero(id_tablero)
    if tablero is None:
        return None
    if not cambios.keys() <= {'nombre'}:
        raise ValueError("Solo se puede actualizar el nombre del tablero.")
    for campo, valor in cambios.items():
        setattr(tablero, campo, valor)
    repo_tablero.actualizar_tablero(tablero)
    return tablero


def agregar_lista(id_tablero, nombre, orden=None):
    sesion.exigir_jefe()
    """Si no se indica el orden, la lista queda al final (después de las de la papelera también)."""
    if orden is None:
        orden = repo_lista.siguiente_orden(id_tablero)
    return crear_lista(id_tablero, nombre, orden)


def mostrar_listas(id_tablero):
    tablero = repo_tablero.obtener_tablero(id_tablero)
    if tablero is None:
        return []
    sesion.exigir_tablero(tablero)
    return repo_lista.listado_listas(id_tablero)


def quitar_lista(id_lista):
    sesion.exigir_jefe()
    """Manda la lista y sus tarjetas a la papelera (se puede restaurar)."""
    return eliminar_lista(id_lista)
