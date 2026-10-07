"""
negocio/lista.py
"""

from datos.modelos.models import Lista


def crear_lista(id_tablero, nombre, orden):
    return Lista.create(id_tablero=id_tablero, nombre=nombre, orden=orden)


def obtener_lista(id_lista):
    return Lista.get_or_none(Lista.id_lista == id_lista)


def listado_listas(id_tablero):
    return list(
        Lista.select().where(Lista.id_tablero == id_tablero).order_by(Lista.orden)
    )


def actualizar_lista(id_lista, **cambios):
    lista = obtener_lista(id_lista)
    if lista is None:
        return None
    for campo, valor in cambios.items():
        setattr(lista, campo, valor)
    lista.save()
    return lista


def eliminar_lista(id_lista):
    lista = obtener_lista(id_lista)
    if lista is None:
        return False
    lista.delete_instance()
    return True


def agregar_tarjeta(id_lista, tarjeta):
    tarjeta.id_lista = id_lista
    tarjeta.save()
    return tarjeta


def quitar_tarjeta(tarjeta):
    return tarjeta
