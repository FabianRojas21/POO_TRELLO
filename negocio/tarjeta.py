from datos.modelos.models import Tarjeta, Usuario, Etiqueta, AsignacionTarjeta, TarjetaEtiqueta, Comentario
from negocio.lista import agregar_tarjeta, quitar_tarjeta

def crear_tarjeta(id_lista, titulo, descripcion=None, fecha_limite=None, estado='pendiente'):
    return Tarjeta.create(
        id_lista=id_lista,
        titulo=titulo,
        descripcion=descripcion,
        fecha_limite=fecha_limite,
        estado=estado
    )


def obtener_tarjeta(id_tarjeta):
    return Tarjeta.get_or_none(Tarjeta.id_tarjeta == id_tarjeta)

def listado_tarjetas(id_lista):
    return list(Tarjeta.select().where(Tarjeta.id_lista == id_lista))


def actualizar_tarjeta(id_tarjeta, **cambios):
    tarjeta = obtener_tarjeta(id_tarjeta)
    if tarjeta is None:
        return None
    for campo, valor in cambios.items():
        setattr(tarjeta, campo, valor)
    tarjeta.save()
    return tarjeta


def eliminar_tarjeta(id_tarjeta):
    tarjeta = obtener_tarjeta(id_tarjeta)
    if tarjeta is None:
        return False
    tarjeta.delete_instance()
    return True

def mover(id_tarjeta, id_lista_destino):
    tarjeta = obtener_tarjeta(id_tarjeta)
    if tarjeta is None:
        return None
    quitar_tarjeta(tarjeta)
    agregar_tarjeta(id_lista_destino, tarjeta)
    return tarjeta

def cambiar_estado(id_tarjeta, nuevo_estado):
    return actualizar_tarjeta(id_tarjeta, estado=nuevo_estado)

def asignar_usuario(id_tarjeta, id_usuario):
    tarjeta = obtener_tarjeta(id_tarjeta)
    usuario = Usuario.get_or_none(Usuario.id_usuario == id_usuario)
    if tarjeta is None or usuario is None:
        return False
    AsignacionTarjeta.get_or_create(id_tarjeta=tarjeta, id_usuario=usuario)
    return True


def quitar_usuario(id_tarjeta, id_usuario):
    eliminados = AsignacionTarjeta.delete().where(
        (AsignacionTarjeta.id_tarjeta == id_tarjeta) &
        (AsignacionTarjeta.id_usuario == id_usuario)
    ).execute()
    return eliminados > 0


def agregar_etiqueta(id_tarjeta, id_etiqueta):
    tarjeta = obtener_tarjeta(id_tarjeta)
    etiqueta = Etiqueta.get_or_none(Etiqueta.id_etiqueta == id_etiqueta)
    if tarjeta is None or etiqueta is None:
        return False
    TarjetaEtiqueta.get_or_create(id_tarjeta=tarjeta, id_etiqueta=etiqueta)
    return True

def quitar_etiqueta(id_tarjeta, id_etiqueta):
    eliminados = TarjetaEtiqueta.delete().where(
        (TarjetaEtiqueta.id_tarjeta == id_tarjeta) &
        (TarjetaEtiqueta.id_etiqueta == id_etiqueta)
    ).execute()
    return eliminados > 0


def agregar_comentario(id_tarjeta, id_usuario, texto):
    tarjeta = obtener_tarjeta(id_tarjeta)
    usuario = Usuario.get_or_none(Usuario.id_usuario == id_usuario)
    if tarjeta is None or usuario is None:
        return None
    return Comentario.create(id_tarjeta=tarjeta, id_usuario=usuario, texto=texto)

