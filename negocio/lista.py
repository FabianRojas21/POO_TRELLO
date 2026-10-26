"""
negocio/lista.py
Borrado lógico: eliminar_lista() manda la lista y sus tarjetas a la papelera;
restaurar_lista() las devuelve (si su proyecto está activo); purgar_lista() borra para siempre.
"""

from datos.modelos.models import Lista
from datos.repositorios import repo_lista, repo_tablero, repo_tarjeta
from negocio import sesion


def crear_lista(id_tablero, nombre, orden):
    sesion.exigir_jefe()
    tablero = repo_tablero.obtener_tablero(id_tablero)
    if tablero is None:
        return None
    lista = Lista(id_tablero=tablero, nombre=nombre, orden=orden)
    repo_lista.guardar_lista(lista)
    return lista


def obtener_lista(id_lista, papelera=False):
    if papelera:
        sesion.exigir_jefe()
    lista = repo_lista.obtener_lista(id_lista, papelera)
    if lista is not None and not papelera:
        sesion.exigir_lista(lista)
    return lista


def listado_listas(id_tablero=None, papelera=False):
    if papelera:
        sesion.exigir_jefe()
    elif id_tablero is not None:
        tablero = repo_tablero.obtener_tablero(id_tablero)
        if tablero is None:
            return []
        sesion.exigir_tablero(tablero)
    elif not sesion.es_jefe():
        raise PermissionError("Los trabajadores solo pueden ver listas de proyectos asignados.")
    return repo_lista.listado_listas(id_tablero, papelera)

def actualizar_lista(id_lista, **cambios):
    sesion.exigir_jefe()
    lista = repo_lista.obtener_lista(id_lista)
    if lista is None:
        return None
    if not cambios.keys() <= {'nombre', 'orden'}:
        raise ValueError("Solo se pueden actualizar el nombre y el orden de la lista.")
    for campo, valor in cambios.items():
        setattr(lista, campo, valor)
    repo_lista.actualizar_lista(lista)
    return lista


def eliminar_lista(id_lista):
    sesion.exigir_jefe()
    lista = repo_lista.obtener_lista(id_lista)
    if lista is None:
        return False
    return repo_lista.eliminar_lista(lista)


def restaurar_lista(id_lista):
    sesion.exigir_jefe()
    """No se puede restaurar una lista cuyo proyecto está en la papelera: primero el proyecto."""
    lista = repo_lista.obtener_lista(id_lista, papelera=True)
    if lista is None or not repo_lista.proyecto_esta_activo(lista):
        return False
    return repo_lista.restaurar_lista(lista)


def purgar_lista(id_lista):
    sesion.exigir_jefe()
    """Borrado definitivo. Solo se permite sobre listas que ya están en la papelera."""
    lista = repo_lista.obtener_lista(id_lista, papelera=True)
    if lista is None:
        return False
    return repo_lista.purgar_lista(lista)


def agregar_tarjeta(id_lista, tarjeta):
    """Paso interno de Tarjeta.mover(): deja la tarjeta en esta lista."""
    lista = repo_lista.obtener_lista(id_lista)
    if lista is None:
        raise ValueError("La lista destino no existe o no está activa.")
    sesion.exigir_lista(lista)
    tarjeta.id_lista = id_lista
    repo_tarjeta.actualizar_tarjeta(tarjeta)
    return tarjeta


def quitar_tarjeta(tarjeta):
    """
    Paso interno de Tarjeta.mover(). La FK id_lista es obligatoria (no existe
    'tarjeta sin lista'), así que no borra nada: agregar_tarjeta() hace el cambio.
    """
    return tarjeta
