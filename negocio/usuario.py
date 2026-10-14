"""
negocio/usuario.py
Usuario solo tiene CRUD: interactúa con el sistema a través de otras clases
(Proyecto.agregar_usuario, Tarjeta.asignar_usuario, etc.).
"""

from datos.modelos.models import Usuario


def crear_usuario(nombre, rol):
    return Usuario.create(nombre=nombre, rol=rol)


def obtener_usuario(id_usuario):
    return Usuario.get_or_none(Usuario.id_usuario == id_usuario)


def listado_usuarios():
    return list(Usuario.select())


def actualizar_usuario(id_usuario, **cambios):
    usuario = obtener_usuario(id_usuario)
    if usuario is None:
        return None
    for campo, valor in cambios.items():
        setattr(usuario, campo, valor)
    usuario.save()
    return usuario


def eliminar_usuario(id_usuario):
    usuario = obtener_usuario(id_usuario)
    if usuario is None:
        return False
    usuario.delete_instance()
    return True
