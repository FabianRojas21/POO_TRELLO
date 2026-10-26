"""
negocio/etiqueta.py
"""

from datos.modelos.models import Etiqueta
from datos.repositorios import repo_etiqueta


def crear_etiqueta(nombre, color):
    etiqueta = Etiqueta(nombre=nombre, color=color)
    repo_etiqueta.guardar_etiqueta(etiqueta)
    return etiqueta


def obtener_etiqueta(id_etiqueta, papelera=False):
    return repo_etiqueta.obtener_etiqueta(id_etiqueta, papelera)


def listado_etiquetas(papelera=False):
    return repo_etiqueta.listado_etiquetas(papelera)


def actualizar_etiqueta(id_etiqueta, **cambios):
    etiqueta = repo_etiqueta.obtener_etiqueta(id_etiqueta)
    if etiqueta is None:
        return None
    if not cambios.keys() <= {'nombre', 'color'}:
        raise ValueError("Solo se pueden actualizar el nombre y el color de la etiqueta.")
    for campo, valor in cambios.items():
        setattr(etiqueta, campo, valor)
    repo_etiqueta.actualizar_etiqueta(etiqueta)
    return etiqueta


def eliminar_etiqueta(id_etiqueta):
    etiqueta = repo_etiqueta.obtener_etiqueta(id_etiqueta)
    if etiqueta is None:
        return False
    return repo_etiqueta.eliminar_etiqueta(etiqueta)


def restaurar_etiqueta(id_etiqueta):
    etiqueta = repo_etiqueta.obtener_etiqueta(id_etiqueta, papelera=True)
    if etiqueta is None:
        return False
    return repo_etiqueta.restaurar_etiqueta(etiqueta)
