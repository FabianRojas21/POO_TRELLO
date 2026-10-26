"""
negocio/tarjeta.py
Borrado lógico: eliminar_tarjeta() la manda a la papelera; restaurar_tarjeta() la devuelve
(si su lista está activa); purgar_tarjeta() la borra para siempre.
"""

from datos.modelos.models import Tarjeta
from datos.repositorios import repo_tarjeta, repo_lista, repo_usuario, repo_etiqueta
from negocio.lista import agregar_tarjeta, quitar_tarjeta
from negocio.comentario import crear_comentario
from negocio import sesion


def crear_tarjeta(id_lista, titulo, descripcion=None, fecha_limite=None, estado='pendiente'):
    lista = repo_lista.obtener_lista(id_lista)
    if lista is None:
        return None
    sesion.exigir_lista(lista)
    tarjeta = Tarjeta(
        id_lista=id_lista,
        titulo=titulo,
        descripcion=descripcion,
        fecha_limite=fecha_limite,
        estado=estado,
    )
    repo_tarjeta.guardar_tarjeta(tarjeta)
    return tarjeta


def obtener_tarjeta(id_tarjeta, papelera=False):
    if papelera:
        sesion.exigir_jefe()
    tarjeta = repo_tarjeta.obtener_tarjeta(id_tarjeta, papelera)
    if tarjeta is not None and not papelera:
        sesion.exigir_tarjeta(tarjeta)
    return tarjeta


def listado_tarjetas(id_lista=None, papelera=False):
    if papelera:
        sesion.exigir_jefe()
    elif id_lista is not None:
        lista = repo_lista.obtener_lista(id_lista)
        if lista is None:
            return []
        sesion.exigir_lista(lista)
    elif not sesion.es_jefe():
        raise PermissionError("Los trabajadores solo pueden ver tarjetas de proyectos asignados.")
    return repo_tarjeta.listado_tarjetas(id_lista, papelera)

def actualizar_tarjeta(id_tarjeta, **cambios):
    tarjeta = repo_tarjeta.obtener_tarjeta(id_tarjeta)
    if tarjeta is None:
        return None
    sesion.exigir_tarjeta(tarjeta)
    campos_permitidos = {'titulo', 'descripcion', 'fecha_limite', 'estado'}
    if not cambios.keys() <= campos_permitidos:
        raise ValueError("Solo se pueden actualizar título, descripción, fecha límite y estado.")
    for campo, valor in cambios.items():
        setattr(tarjeta, campo, valor)
    repo_tarjeta.actualizar_tarjeta(tarjeta)
    return tarjeta


def eliminar_tarjeta(id_tarjeta):
    tarjeta = repo_tarjeta.obtener_tarjeta(id_tarjeta)
    if tarjeta is None:
        return False
    sesion.exigir_tarjeta(tarjeta)
    return repo_tarjeta.eliminar_tarjeta(tarjeta)


def restaurar_tarjeta(id_tarjeta):
    """No se puede restaurar una tarjeta cuya lista está en la papelera: primero la lista."""
    sesion.exigir_jefe()
    tarjeta = repo_tarjeta.obtener_tarjeta(id_tarjeta, papelera=True)
    if tarjeta is None or not repo_tarjeta.lista_esta_activa(tarjeta):
        return False
    return repo_tarjeta.restaurar_tarjeta(tarjeta)


def purgar_tarjeta(id_tarjeta):
    """Borrado definitivo. Solo se permite sobre tarjetas que ya están en la papelera."""
    sesion.exigir_jefe()
    tarjeta = repo_tarjeta.obtener_tarjeta(id_tarjeta, papelera=True)
    if tarjeta is None:
        return False
    return repo_tarjeta.purgar_tarjeta(tarjeta)


def mover(id_tarjeta, id_lista_destino):
    """
    Mueve la tarjeta a otra lista. Completar una tarea NO pasa por aquí:
    eso es solo cambiar_estado(), la tarjeta sigue en su lista.
    """
    tarjeta = repo_tarjeta.obtener_tarjeta(id_tarjeta)
    lista_destino = repo_lista.obtener_lista(id_lista_destino)
    if tarjeta is None or lista_destino is None:
        return None
    sesion.exigir_tarjeta(tarjeta)
    sesion.exigir_lista(lista_destino)
    if tarjeta.id_lista.id_tablero.id_proyecto_id != lista_destino.id_tablero.id_proyecto_id:
        raise ValueError("No se puede mover una tarjeta a otro proyecto.")
    quitar_tarjeta(tarjeta)
    agregar_tarjeta(id_lista_destino, tarjeta)
    return tarjeta


def cambiar_estado(id_tarjeta, nuevo_estado):
    return actualizar_tarjeta(id_tarjeta, estado=nuevo_estado)


def asignar_usuario(id_tarjeta, id_usuario):
    tarjeta = repo_tarjeta.obtener_tarjeta(id_tarjeta)
    usuario = repo_usuario.obtener_usuario(id_usuario)
    if tarjeta is None or usuario is None:
        return False
    sesion.exigir_tarjeta(tarjeta)
    if not sesion.es_jefe() and sesion.usuario_actual().id_usuario != id_usuario:
        raise PermissionError("Los trabajadores solo pueden asignarse a sí mismos.")
    return repo_tarjeta.asignar_usuario(tarjeta, usuario)


def quitar_usuario_asignado(id_tarjeta, id_usuario):
    tarjeta = repo_tarjeta.obtener_tarjeta(id_tarjeta)
    usuario = repo_usuario.obtener_usuario(id_usuario)
    if tarjeta is None or usuario is None:
        return False
    sesion.exigir_tarjeta(tarjeta)
    if not sesion.es_jefe() and sesion.usuario_actual().id_usuario != id_usuario:
        raise PermissionError("Los trabajadores solo pueden quitar su propia asignación.")
    return repo_tarjeta.quitar_usuario(tarjeta, usuario)


def agregar_etiqueta(id_tarjeta, id_etiqueta):
    tarjeta = repo_tarjeta.obtener_tarjeta(id_tarjeta)
    etiqueta = repo_etiqueta.obtener_etiqueta(id_etiqueta)
    if tarjeta is None or etiqueta is None:
        return False
    sesion.exigir_tarjeta(tarjeta)
    return repo_tarjeta.agregar_etiqueta(tarjeta, etiqueta)


def quitar_etiqueta(id_tarjeta, id_etiqueta):
    tarjeta = repo_tarjeta.obtener_tarjeta(id_tarjeta)
    etiqueta = repo_etiqueta.obtener_etiqueta(id_etiqueta)
    if tarjeta is None or etiqueta is None:
        return False
    sesion.exigir_tarjeta(tarjeta)
    return repo_tarjeta.quitar_etiqueta(tarjeta, etiqueta)


def agregar_comentario(id_tarjeta, id_usuario, texto):
    actual = sesion.usuario_actual()
    if actual is None:
        raise PermissionError("Debes iniciar sesión para comentar.")
    if not sesion.es_jefe() and actual.id_usuario != id_usuario:
        raise PermissionError("El comentario debe pertenecer al usuario autenticado.")
    return crear_comentario(id_tarjeta, actual.id_usuario, texto)


def usuarios_de_tarjeta(id_tarjeta):
    tarjeta = repo_tarjeta.obtener_tarjeta(id_tarjeta)
    if tarjeta is None:
        return None
    sesion.exigir_tarjeta(tarjeta)
    return repo_tarjeta.usuarios_de_tarjeta(tarjeta)


def etiquetas_de_tarjeta(id_tarjeta):
    tarjeta = repo_tarjeta.obtener_tarjeta(id_tarjeta)
    if tarjeta is None:
        return None
    sesion.exigir_tarjeta(tarjeta)
    return repo_tarjeta.etiquetas_de_tarjeta(tarjeta)
