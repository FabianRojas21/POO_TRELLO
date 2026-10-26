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


def obtener_usuario(id_usuario, papelera=False):
    return repo_usuario.obtener_usuario(id_usuario, papelera)


def listado_usuarios(papelera=False):
    return repo_usuario.listado_usuarios(papelera)


def actualizar_usuario(id_usuario, **cambios):
    usuario = repo_usuario.obtener_usuario(id_usuario)
    if usuario is None:
        return None
    if not cambios.keys() <= {'nombre', 'rol'}:
        raise ValueError("Solo se pueden actualizar el nombre y el rol del usuario.")
    for campo, valor in cambios.items():
        setattr(usuario, campo, valor)
    repo_usuario.actualizar_usuario(usuario)
    return usuario


def eliminar_usuario(id_usuario):
    usuario = repo_usuario.obtener_usuario(id_usuario)
    if usuario is None:
        return False
    return repo_usuario.eliminar_usuario(usuario)


def restaurar_usuario(id_usuario):
    usuario = repo_usuario.obtener_usuario(id_usuario, papelera=True)
    if usuario is None:
        return False
    return repo_usuario.restaurar_usuario(usuario)
