"""
datos/repositorios/repo_usuario.py
"""

from datos.modelos.models import Usuario


def guardar_usuario(usuario):
    usuario.save()
    return True


def eliminar_usuario(usuario):
    Usuario.update(activo=False).where(Usuario.id_usuario == usuario.id_usuario).execute()
    usuario.activo = False
    return True


def restaurar_usuario(usuario):
    Usuario.update(activo=True).where(Usuario.id_usuario == usuario.id_usuario).execute()
    usuario.activo = True
    return True


def actualizar_usuario(usuario):
    usuario.save()
    return True


def obtener_usuario(id_usuario, papelera=False):
    return Usuario.get_or_none(
        (Usuario.id_usuario == id_usuario) & (Usuario.activo == (not papelera))
    )


def listado_usuarios(papelera=False):
    return list(Usuario.select().where(Usuario.activo == (not papelera)))
