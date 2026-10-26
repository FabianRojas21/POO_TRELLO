"""
datos/repositorios/repo_etiqueta.py
"""

from datos.modelos.models import Etiqueta


def guardar_etiqueta(etiqueta):
    etiqueta.save()
    return True


def eliminar_etiqueta(etiqueta):
    Etiqueta.update(activo=False).where(Etiqueta.id_etiqueta == etiqueta.id_etiqueta).execute()
    etiqueta.activo = False
    return True


def restaurar_etiqueta(etiqueta):
    Etiqueta.update(activo=True).where(Etiqueta.id_etiqueta == etiqueta.id_etiqueta).execute()
    etiqueta.activo = True
    return True


def actualizar_etiqueta(etiqueta):
    etiqueta.save()
    return True


def obtener_etiqueta(id_etiqueta, papelera=False):
    return Etiqueta.get_or_none(
        (Etiqueta.id_etiqueta == id_etiqueta) & (Etiqueta.activo == (not papelera))
    )


def listado_etiquetas(papelera=False):
    return list(Etiqueta.select().where(Etiqueta.activo == (not papelera)))
