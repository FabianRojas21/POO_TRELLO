"""
negocio/usuario.py
Usuario solo tiene CRUD: interactúa con el sistema a través de otras clases
(Proyecto.agregar_usuario, Tarjeta.asignar_usuario, etc.).
"""

from datos.modelos.models import Usuario
from datos.repositorios import repo_usuario


def crear_usuario(nombre, rol):
    usuario = Usuario(nombre=nombre, rol=rol)
    repo_usuario.guardar_usuario(usuario)
    return usuario


def obtener_usuario(id_usuario):
    return repo_usuario.obtener_usuario(id_usuario)


def listado_usuarios():
    return repo_usuario.listado_usuarios()


def actualizar_usuario(id_usuario, **cambios):
    usuario = repo_usuario.obtener_usuario(id_usuario)
    if usuario is None:
        return None
    for campo, valor in cambios.items():
        setattr(usuario, campo, valor)
    repo_usuario.actualizar_usuario(usuario)
    return usuario


def eliminar_usuario(id_usuario):
    usuario = repo_usuario.obtener_usuario(id_usuario)
    if usuario is None:
        return False
    return repo_usuario.eliminar_usuario(usuario)
