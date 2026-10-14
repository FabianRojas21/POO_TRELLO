"""
negocio/comentario.py
"""

from datos.modelos.models import Comentario, Tarjeta, Usuario


def crear_comentario(id_tarjeta, id_usuario, texto):
    tarjeta = Tarjeta.get_or_none(Tarjeta.id_tarjeta == id_tarjeta)
    usuario = Usuario.get_or_none(Usuario.id_usuario == id_usuario)
    if tarjeta is None or usuario is None:
        return None
    return Comentario.create(id_tarjeta=tarjeta, id_usuario=usuario, texto=texto)


def obtener_comentario(id_comentario):
    return Comentario.get_or_none(Comentario.id_comentario == id_comentario)


def listado_comentarios(id_tarjeta):
    return list(
        Comentario.select().where(Comentario.id_tarjeta == id_tarjeta).order_by(Comentario.fecha)
    )


def actualizar_comentario(id_comentario, **cambios):
    comentario = obtener_comentario(id_comentario)
    if comentario is None:
        return None
    for campo, valor in cambios.items():
        setattr(comentario, campo, valor)
    comentario.save()
    return comentario


def eliminar_comentario(id_comentario):
    comentario = obtener_comentario(id_comentario)
    if comentario is None:
        return False
    comentario.delete_instance()
    return True
