"""
negocio/comentario.py
"""

from datos.modelos.models import Comentario
from datos.repositorios import repo_comentario, repo_tarjeta, repo_usuario


def crear_comentario(id_tarjeta, id_usuario, texto):
    tarjeta = repo_tarjeta.obtener_tarjeta(id_tarjeta)
    usuario = repo_usuario.obtener_usuario(id_usuario)
    if tarjeta is None or usuario is None:
        return None
    comentario = Comentario(id_tarjeta=tarjeta, id_usuario=usuario, texto=texto)
    repo_comentario.guardar_comentario(comentario)
    return comentario


def obtener_comentario(id_comentario):
    return repo_comentario.obtener_comentario(id_comentario)


def listado_comentarios(id_tarjeta=None):
    return repo_comentario.listado_comentarios(id_tarjeta)


def actualizar_comentario(id_comentario, **cambios):
    comentario = repo_comentario.obtener_comentario(id_comentario)
    if comentario is None:
        return None
    for campo, valor in cambios.items():
        setattr(comentario, campo, valor)
    repo_comentario.actualizar_comentario(comentario)
    return comentario


def eliminar_comentario(id_comentario):
    comentario = repo_comentario.obtener_comentario(id_comentario)
    if comentario is None:
        return False
    return repo_comentario.eliminar_comentario(comentario)
