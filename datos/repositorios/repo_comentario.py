"""
datos/repositorios/repo_comentario.py
"""

from datos.modelos.models import Comentario


def guardar_comentario(comentario):
    comentario.save()
    return True


def eliminar_comentario(comentario):
    Comentario.update(activo=False).where(
        Comentario.id_comentario == comentario.id_comentario
    ).execute()
    comentario.activo = False
    return True


def restaurar_comentario(comentario):
    Comentario.update(activo=True).where(
        Comentario.id_comentario == comentario.id_comentario
    ).execute()
    comentario.activo = True
    return True


def actualizar_comentario(comentario):
    comentario.save()
    return True


def obtener_comentario(id_comentario, papelera=False):
    return Comentario.get_or_none(
        (Comentario.id_comentario == id_comentario) &
        (Comentario.activo == (not papelera))
    )


def listado_comentarios(id_tarjeta=None, papelera=False):
    consulta = (Comentario.select()
                .where(Comentario.activo == (not papelera))
                .order_by(Comentario.id_comentario))
    if id_tarjeta is not None:
        consulta = consulta.where(Comentario.id_tarjeta == id_tarjeta)
    return list(consulta)
