"""
datos/repositorios/repo_proyecto.py
Acceso a la base de datos para Proyecto (CRUD + tablas asociadas).

Borrado lógico: eliminar_proyecto() manda el proyecto a la papelera (activo = 0) junto con
sus listas y tarjetas; restaurar_proyecto() los devuelve; purgar_proyecto() borra de verdad.
"""

from datos.modelos.models import Proyecto, ProyectoUsuario, Tablero, Lista, Tarjeta, Usuario


def guardar_proyecto(proyecto):
    proyecto.save()
    return True


def actualizar_proyecto(proyecto):
    proyecto.save()
    return True


def obtener_proyecto(codigo_proyecto, papelera=False):
    """papelera=False: solo proyectos activos. papelera=True: solo los eliminados."""
    return Proyecto.get_or_none(
        (Proyecto.codigo_proyecto == codigo_proyecto) & (Proyecto.activo == (not papelera))
    )


def listado_proyectos(papelera=False):
    return list(Proyecto.select().where(Proyecto.activo == (not papelera)))


def _cambiar_activo(proyecto, valor):
    """Marca qué listas y tarjetas deben restaurarse junto con el proyecto."""
    tableros = Tablero.select(Tablero.id_tablero).where(Tablero.id_proyecto == proyecto.id_proyecto)
    listas = Lista.select(Lista.id_lista).where(Lista.id_tablero.in_(tableros))
    with Proyecto._meta.database.atomic():
        if valor:
            Tarjeta.update(activo=True, restaurar_con_proyecto=False).where(
                (Tarjeta.id_lista.in_(listas)) & (Tarjeta.restaurar_con_proyecto == True)
            ).execute()
            Lista.update(activo=True, restaurar_con_proyecto=False).where(
                (Lista.id_tablero.in_(tableros)) & (Lista.restaurar_con_proyecto == True)
            ).execute()
        else:
            Tarjeta.update(activo=False, restaurar_con_proyecto=True).where(
                (Tarjeta.id_lista.in_(
                    Lista.select(Lista.id_lista).where(
                        (Lista.id_tablero.in_(tableros)) & (Lista.activo == True)
                    )
                )) & (Tarjeta.activo == True)
            ).execute()
            Lista.update(activo=False, restaurar_con_proyecto=True).where(
                (Lista.id_tablero.in_(tableros)) & (Lista.activo == True)
            ).execute()
        Proyecto.update(activo=valor).where(Proyecto.id_proyecto == proyecto.id_proyecto).execute()
    proyecto.activo = valor


def eliminar_proyecto(proyecto):
    _cambiar_activo(proyecto, False)
    return True


def restaurar_proyecto(proyecto):
    _cambiar_activo(proyecto, True)
    return True


def purgar_proyecto(proyecto):
    """Borrado real e irreversible (la base cascadea a tablero, listas, tarjetas, etc.)."""
    proyecto.delete_instance()
    return True


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
    """Cuenta las tarjetas activas del proyecto (Tablero -> Lista -> Tarjeta)."""
    consulta = (Tarjeta.select().join(Lista).join(Tablero)
                .where((Tablero.id_proyecto == proyecto) & (Tarjeta.activo == True)))
    if estado is not None:
        consulta = consulta.where(Tarjeta.estado == estado)
    return consulta.count()


def usuarios_de_proyecto(proyecto):
    return list(
        Usuario.select().join(ProyectoUsuario)
        .where(
            (ProyectoUsuario.id_proyecto == proyecto) &
            (Usuario.activo == True)
        )
    )
