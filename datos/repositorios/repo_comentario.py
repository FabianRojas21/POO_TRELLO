"""
datos/repositorios/repo_comentario.py
"""

from datos.modelos.models import Comentario


def guardar_comentario(comentario):
    comentario.save()
    return True


def eliminar_comentario(comentario):
    comentario.delete_instance()
    return True


def actualizar_comentario(comentario):
    comentario.save()
    return True


def obtener_comentario(id_comentario):
    return Comentario.get_or_none(Comentario.id_comentario == id_comentario)


def listado_comentarios(id_tarjeta=None):
    consulta = Comentario.select().order_by(Comentario.id_comentario)
    if id_tarjeta is not None:
        consulta = consulta.where(Comentario.id_tarjeta == id_tarjeta)
    return list(consulta)
