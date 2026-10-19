"""
datos/repositorios/repo_etiqueta.py
"""

from datos.modelos.models import Etiqueta


def guardar_etiqueta(etiqueta):
    etiqueta.save()
    return True


def eliminar_etiqueta(etiqueta):
    etiqueta.delete_instance()
    return True


def actualizar_etiqueta(etiqueta):
    etiqueta.save()
    return True


def obtener_etiqueta(id_etiqueta):
    return Etiqueta.get_or_none(Etiqueta.id_etiqueta == id_etiqueta)


def listado_etiquetas():
    return list(Etiqueta.select())
