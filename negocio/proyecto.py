from datos.modelos.models import Proyecto, Tablero, Usuario, ProyectoUsuario, Lista, Tarjeta


def crear_proyecto(codigo_proyecto, nombre, fecha_inicio, fecha_fin=None, nombre_tablero=None):

    database = Proyecto._meta.database
    with database.atomic():
        proyecto = Proyecto.create(
            codigo_proyecto=codigo_proyecto,
            nombre=nombre,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        Tablero.create(
            id_proyecto=proyecto.id_proyecto,
            nombre=nombre_tablero or f"tablero de {nombre}"

    )
    return proyecto

def obtener_proyecto(codigo_proyecto):
    return Proyecto.get_or_none(Proyecto.codigo_proyecto == codigo_proyecto)


def listado_proyectos():
    return list(Proyecto.select())


def actualizar_proyecto(codigo_proyecto, **cambios):

    proyecto = obtener_proyecto(codigo_proyecto)
    if proyecto is None:
        return None
    for campo, valor in cambios.items():
        setattr(proyecto, campo, valor)
    proyecto.save()
    return proyecto

def eliminar_proyecto(codigo_proyecto):
    proyecto = obtener_proyecto(codigo_proyecto)
    if proyecto is None:
        return False
    proyecto.delete_instance()
    return True


def agregar_usuario(codigo_proyecto, id_usuario):
    proyecto = obtener_proyecto(codigo_proyecto)
    usuario = Usuario.get_or_none(Usuario.id_usuario == id_usuario)
    if proyecto is None or usuario is None:
        return False
    ProyectoUsuario.get_or_create(id_Proyecto=proyecto, id_usuario=usuario)
    return True

def remover_usuario(codigo_proyecto, id_usuario):
    proyecto = obtener_proyecto(codigo_proyecto)
    if proyecto is None:
        return False
    eliminados = ProyectoUsuario.delete().where(
        (ProyectoUsuario.id_proyecto == proyecto) &
        (ProyectoUsuario.id_usuario == id_usuario)
    ).execute()
    return eliminados > 0


def consultar_avance(codigo_proyecto):
    proyecto = obtener_proyecto(codigo_proyecto)
    if proyecto is None:
        return None

    total = (Tarjeta
             .select()
             .join(Lista)
             .join(Tablero)
             .where(Tablero.id_proyecto == proyecto)
             .count())

    if total == 0:
        return 0.0

    completadas = (Tarjeta
                   .select()
                   .join(Lista)
                   .join(Tablero)
                   .where((Tablero.id_proyecto == proyecto) & (Tarjeta.estado == 'completada'))
                   .count())


    return round((completadas / total) * 100, 2)
