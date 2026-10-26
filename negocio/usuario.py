"""
negocio/usuario.py
Usuario solo tiene CRUD: interactúa con el sistema a través de otras clases
(Proyecto.agregar_usuario, Tarjeta.asignar_usuario, etc.).
"""

from datos.modelos.models import Usuario
from datos.repositorios import repo_usuario
from negocio import sesion


ROLES = ('Jefe de proyecto', 'Trabajador')


def crear_usuario(nombre, rol, contrasena):
    sesion.exigir_jefe()
    if rol not in ROLES:
        raise ValueError("El rol debe ser 'Jefe de proyecto' o 'Trabajador'.")
    if not contrasena:
        raise ValueError("La contraseña no puede estar vacía.")
    usuario = Usuario(nombre=nombre, rol=rol, contraseña=contrasena)
    repo_usuario.guardar_usuario(usuario)
    return usuario


def crear_primer_jefe(nombre, contrasena):
    if sesion.usuario_actual() is not None:
        raise PermissionError("La configuracion inicial solo se permite antes de iniciar sesión.")
    cuentas_configuradas = Usuario.select().where(
        (Usuario.activo == True) &
        Usuario.contraseña.is_null(False) &
        (Usuario.contraseña != '')
    ).exists()
    if cuentas_configuradas:
        raise PermissionError("El jefe inicial ya fue creado.")
    if not contrasena:
        raise ValueError("La contraseña no puede estar vacía.")
    usuario = Usuario(
        nombre=nombre,
        rol='Jefe de proyecto',
        contraseña=contrasena,
    )
    repo_usuario.guardar_usuario(usuario)
    return usuario


def iniciar_sesion(id_usuario, contrasena):
    usuario = repo_usuario.obtener_usuario(id_usuario)
    if (usuario is None or usuario.rol not in ROLES or
            usuario.contraseña is None or usuario.contraseña != contrasena):
        return None
    sesion.iniciar(usuario)
    return usuario


def obtener_usuario(id_usuario, papelera=False):
    if papelera:
        sesion.exigir_jefe()
    if not papelera and not sesion.es_jefe():
        if sesion.usuario_actual() is None or sesion.usuario_actual().id_usuario != id_usuario:
            return None
    return repo_usuario.obtener_usuario(id_usuario, papelera)


def listado_usuarios(papelera=False):
    sesion.exigir_jefe()
    return repo_usuario.listado_usuarios(papelera)


def actualizar_usuario(id_usuario, **cambios):
    sesion.exigir_jefe()
    usuario = repo_usuario.obtener_usuario(id_usuario)
    if usuario is None:
        return None
    if not cambios.keys() <= {'nombre', 'rol'}:
        raise ValueError("Solo se pueden actualizar el nombre y el rol del usuario.")
    if 'rol' in cambios and cambios['rol'] not in ROLES:
        raise ValueError("El rol debe ser 'Jefe de proyecto' o 'Trabajador'.")
    for campo, valor in cambios.items():
        setattr(usuario, campo, valor)
    repo_usuario.actualizar_usuario(usuario)
    if sesion.usuario_actual() is not None and sesion.usuario_actual().id_usuario == id_usuario:
        sesion.iniciar(usuario)
    return usuario


def eliminar_usuario(id_usuario):
    sesion.exigir_jefe()
    actual = sesion.usuario_actual()
    if actual is not None and actual.id_usuario == id_usuario:
        raise ValueError("No puedes deshabilitar tu propia cuenta durante la sesión.")
    usuario = repo_usuario.obtener_usuario(id_usuario)
    if usuario is None:
        return False
    return repo_usuario.eliminar_usuario(usuario)


def restaurar_usuario(id_usuario):
    sesion.exigir_jefe()
    usuario = repo_usuario.obtener_usuario(id_usuario, papelera=True)
    if usuario is None:
        return False
    return repo_usuario.restaurar_usuario(usuario)
