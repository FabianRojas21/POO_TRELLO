"""
negocio/comentario.py
"""

from datos.modelos.models import Comentario
from datos.repositorios import repo_comentario, repo_tarjeta, repo_usuario
from negocio import sesion


def crear_comentario(id_tarjeta, id_usuario, texto):
    tarjeta = repo_tarjeta.obtener_tarjeta(id_tarjeta)
    actual = sesion.usuario_actual()
    if actual is None:
        raise PermissionError("Debes iniciar sesión para comentar.")
    if actual.id_usuario != id_usuario:
        raise PermissionError("El comentario debe pertenecer al usuario autenticado.")
    if tarjeta is not None:
        sesion.exigir_tarjeta(tarjeta)
    usuario = repo_usuario.obtener_usuario(id_usuario)
    if tarjeta is None or usuario is None:
        return None
    comentario = Comentario(id_tarjeta=tarjeta, id_usuario=usuario, texto=texto)
    repo_comentario.guardar_comentario(comentario)
    return comentario


def obtener_comentario(id_comentario, papelera=False):
    if papelera:
        sesion.exigir_jefe()
    comentario = repo_comentario.obtener_comentario(id_comentario, papelera)
    if comentario is not None and not papelera:
        sesion.exigir_tarjeta(comentario.id_tarjeta)
    return comentario


def listado_comentarios(id_tarjeta=None, papelera=False):
    if papelera:
        sesion.exigir_jefe()
    elif id_tarjeta is not None:
        tarjeta = repo_tarjeta.obtener_tarjeta(id_tarjeta)
        if tarjeta is None:
            return []
        sesion.exigir_tarjeta(tarjeta)
    elif not sesion.es_jefe():
        raise PermissionError("Los trabajadores solo pueden ver comentarios de sus proyectos.")
    return repo_comentario.listado_comentarios(id_tarjeta, papelera)


def actualizar_comentario(id_comentario, **cambios):
    comentario = repo_comentario.obtener_comentario(id_comentario)
    if comentario is None:
        return None
    sesion.exigir_tarjeta(comentario.id_tarjeta)
    if not sesion.es_jefe() and comentario.id_usuario_id != sesion.usuario_actual().id_usuario:
        raise PermissionError("Solo puedes editar tus propios comentarios.")
    if not cambios.keys() <= {'texto'}:
        raise ValueError("Solo se puede actualizar el texto del comentario.")
    for campo, valor in cambios.items():
        setattr(comentario, campo, valor)
    repo_comentario.actualizar_comentario(comentario)
    return comentario


def eliminar_comentario(id_comentario):
    comentario = repo_comentario.obtener_comentario(id_comentario)
    if comentario is None:
        return False
    sesion.exigir_tarjeta(comentario.id_tarjeta)
    if not sesion.es_jefe() and comentario.id_usuario_id != sesion.usuario_actual().id_usuario:
        raise PermissionError("Solo puedes eliminar tus propios comentarios.")
    return repo_comentario.eliminar_comentario(comentario)


def restaurar_comentario(id_comentario):
    sesion.exigir_jefe()
    comentario = repo_comentario.obtener_comentario(id_comentario, papelera=True)
    if comentario is None:
        return False
    return repo_comentario.restaurar_comentario(comentario)
