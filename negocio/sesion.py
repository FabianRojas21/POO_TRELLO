"""Usuario autenticado y comprobaciones de permisos para la aplicacion de consola."""

from datos.modelos.models import ProyectoUsuario


_usuario_actual = None


def iniciar(usuario):
    global _usuario_actual
    _usuario_actual = usuario


def cerrar():
    global _usuario_actual
    _usuario_actual = None


def usuario_actual():
    return _usuario_actual


def es_jefe():
    return _usuario_actual is not None and _usuario_actual.rol == 'Jefe de proyecto'


def exigir_jefe():
    if not es_jefe():
        raise PermissionError("Esta acción solo está permitida al jefe de proyecto.")


def puede_acceder_proyecto(proyecto):
    if _usuario_actual is None:
        return False
    if es_jefe():
        return True
    return ProyectoUsuario.select().where(
        (ProyectoUsuario.id_proyecto == proyecto.id_proyecto) &
        (ProyectoUsuario.id_usuario == _usuario_actual.id_usuario)
    ).exists()


def exigir_proyecto(proyecto):
    if not puede_acceder_proyecto(proyecto):
        raise PermissionError("No tienes acceso a ese proyecto.")


def exigir_tablero(tablero):
    exigir_proyecto(tablero.id_proyecto)


def exigir_lista(lista):
    exigir_tablero(lista.id_tablero)


def exigir_tarjeta(tarjeta):
    exigir_lista(tarjeta.id_lista)
