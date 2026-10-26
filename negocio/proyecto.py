"""
negocio/proyecto.py
Reglas de negocio de Proyecto. El acceso a la base vive en datos/repositorios.
Borrado lógico: eliminar_proyecto() lo manda a la papelera; restaurar_proyecto() lo devuelve;
purgar_proyecto() lo borra para siempre (solo si ya está en la papelera).
"""

from datos.modelos.models import Proyecto, Tablero
from datos.repositorios import repo_proyecto, repo_tablero, repo_usuario
from negocio import sesion


def crear_proyecto(codigo_proyecto, nombre, fecha_inicio, fecha_fin=None, nombre_tablero=None):
    """El Proyecto se crea siempre junto con su Tablero (relación 1-1)."""
    sesion.exigir_jefe()
    if repo_proyecto.obtener_proyecto(codigo_proyecto) is not None:
        raise ValueError(f"Ya existe un proyecto con el código {codigo_proyecto}.")
    if repo_proyecto.obtener_proyecto(codigo_proyecto, papelera=True) is not None:
        raise ValueError(
            f"El código {codigo_proyecto} pertenece a un proyecto en la papelera: "
            "restáuralo o elimínalo definitivamente."
        )
    proyecto = Proyecto(
        codigo_proyecto=codigo_proyecto,
        nombre=nombre,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
    )
    with Proyecto._meta.database.atomic():
        repo_proyecto.guardar_proyecto(proyecto)
        tablero = Tablero(
            id_proyecto=proyecto,
            nombre=nombre_tablero or f"Tablero de {nombre}",
        )
        repo_tablero.guardar_tablero(tablero)
    return proyecto


def obtener_proyecto(codigo_proyecto, papelera=False):
    if papelera:
        sesion.exigir_jefe()
    proyecto = repo_proyecto.obtener_proyecto(codigo_proyecto, papelera)
    if proyecto is not None and not papelera:
        sesion.exigir_proyecto(proyecto)
    return proyecto


def listado_proyectos(papelera=False):
    if papelera:
        sesion.exigir_jefe()
    elif not sesion.es_jefe():
        actual = sesion.usuario_actual()
        if actual is None:
            raise PermissionError("Debes iniciar sesión para ver proyectos.")
        return repo_proyecto.proyectos_de_usuario(actual)
    return repo_proyecto.listado_proyectos(papelera)


def actualizar_proyecto(codigo_proyecto, **cambios):
    sesion.exigir_jefe()
    proyecto = repo_proyecto.obtener_proyecto(codigo_proyecto)
    if proyecto is None:
        return None
    campos_permitidos = {'codigo_proyecto', 'nombre', 'fecha_inicio', 'fecha_fin'}
    if not cambios.keys() <= campos_permitidos:
        raise ValueError("Solo se pueden actualizar código, nombre y fechas del proyecto.")
    for campo, valor in cambios.items():
        setattr(proyecto, campo, valor)
    repo_proyecto.actualizar_proyecto(proyecto)
    return proyecto


def eliminar_proyecto(codigo_proyecto):
    """Lo manda a la papelera junto con su tablero, listas y tarjetas."""
    sesion.exigir_jefe()
    proyecto = repo_proyecto.obtener_proyecto(codigo_proyecto)
    if proyecto is None:
        return False
    return repo_proyecto.eliminar_proyecto(proyecto)


def restaurar_proyecto(codigo_proyecto):
    """Lo saca de la papelera con todo lo que contenía (listas y tarjetas)."""
    sesion.exigir_jefe()
    proyecto = repo_proyecto.obtener_proyecto(codigo_proyecto, papelera=True)
    if proyecto is None:
        return False
    return repo_proyecto.restaurar_proyecto(proyecto)


def purgar_proyecto(codigo_proyecto):
    """Borrado definitivo. Solo se permite sobre proyectos que ya están en la papelera."""
    sesion.exigir_jefe()
    proyecto = repo_proyecto.obtener_proyecto(codigo_proyecto, papelera=True)
    if proyecto is None:
        return False
    return repo_proyecto.purgar_proyecto(proyecto)


def agregar_usuario(codigo_proyecto, id_usuario):
    sesion.exigir_jefe()
    proyecto = repo_proyecto.obtener_proyecto(codigo_proyecto)
    usuario = repo_usuario.obtener_usuario(id_usuario)
    if proyecto is None or usuario is None:
        return False
    return repo_proyecto.agregar_usuario(proyecto, usuario)


def remover_usuario(codigo_proyecto, id_usuario):
    sesion.exigir_jefe()
    proyecto = repo_proyecto.obtener_proyecto(codigo_proyecto)
    usuario = repo_usuario.obtener_usuario(id_usuario)
    if proyecto is None or usuario is None:
        return False
    return repo_proyecto.remover_usuario(proyecto, usuario)


def consultar_avance(codigo_proyecto):
    """% de tarjetas activas en estado 'completada' sobre el total del proyecto."""
    proyecto = repo_proyecto.obtener_proyecto(codigo_proyecto)
    if proyecto is None:
        return None
    total = repo_proyecto.contar_tarjetas(proyecto)
    if total == 0:
        return 0.0
    completadas = repo_proyecto.contar_tarjetas(proyecto, estado='completada')
    return round(completadas / total * 100, 2)


def usuarios_del_proyecto(codigo_proyecto):
    proyecto = repo_proyecto.obtener_proyecto(codigo_proyecto)
    if proyecto is None:
        return None
    return repo_proyecto.usuarios_de_proyecto(proyecto)
