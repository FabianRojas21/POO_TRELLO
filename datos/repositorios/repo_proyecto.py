"""
datos/repositorios/repo_proyecto.py
Acceso a la base de datos para Proyecto (CRUD + tablas asociadas).
"""

from datos.modelos.models import Proyecto, ProyectoUsuario, Tablero, Lista, Tarjeta


def guardar_proyecto(proyecto):
    proyecto.save()
    return True


def eliminar_proyecto(proyecto):
    proyecto.delete_instance()
    return True


def actualizar_proyecto(proyecto):
    proyecto.save()
    return True


def obtener_proyecto(codigo_proyecto):
    return Proyecto.get_or_none(Proyecto.codigo_proyecto == codigo_proyecto)


def listado_proyectos():
    return list(Proyecto.select())


def agregar_usuario(proyecto, usuario):
    ProyectoUsuario.get_or_create(id_proyecto=proyecto, id_usuario=usuario)
    return True


def remover_usuario(proyecto, usuario):
    eliminados = ProyectoUsuario.delete().where(
        (ProyectoUsuario.id_proyecto == proyecto) &
        (ProyectoUsuario.id_usuario == usuario)
    ).execute()
    return eliminados > 0


def contar_tarjetas(proyecto, estado=None):
    """Cuenta las tarjetas del proyecto (Tablero -> Lista -> Tarjeta)."""
    consulta = (Tarjeta.select().join(Lista).join(Tablero)
                .where(Tablero.id_proyecto == proyecto))
    if estado is not None:
        consulta = consulta.where(Tarjeta.estado == estado)
    return consulta.count()
