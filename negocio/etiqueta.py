"""
negocio/etiqueta.py
"""

from datos.modelos.models import Etiqueta


def crear_etiqueta(nombre, color):
    return Etiqueta.create(nombre=nombre, color=color)


def obtener_etiqueta(id_etiqueta):
    return Etiqueta.get_or_none(Etiqueta.id_etiqueta == id_etiqueta)


def listado_etiquetas():
    return list(Etiqueta.select())


def actualizar_etiqueta(id_etiqueta, **cambios):
    etiqueta = obtener_etiqueta(id_etiqueta)
    if etiqueta is None:
        return None
    for campo, valor in cambios.items():
        setattr(etiqueta, campo, valor)
    etiqueta.save()
    return etiqueta


def eliminar_etiqueta(id_etiqueta):
    etiqueta = obtener_etiqueta(id_etiqueta)
    if etiqueta is None:
        return False
    etiqueta.delete_instance()
    return True
