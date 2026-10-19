"""
datos/repositorios/repo_usuario.py
"""

from datos.modelos.models import Usuario


def guardar_usuario(usuario):
    usuario.save()
    return True


def eliminar_usuario(usuario):
    usuario.delete_instance()
    return True


def actualizar_usuario(usuario):
    usuario.save()
    return True


def obtener_usuario(id_usuario):
    return Usuario.get_or_none(Usuario.id_usuario == id_usuario)


def listado_usuarios():
    return list(Usuario.select())
