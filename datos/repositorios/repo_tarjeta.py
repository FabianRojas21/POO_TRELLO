"""
datos/repositorios/repo_tarjeta.py
Incluye las tablas intermedias de la tarjeta (usuarios asignados y etiquetas).
"""

from datos.modelos.models import Tarjeta, AsignacionTarjeta, TarjetaEtiqueta, Usuario, Etiqueta


def guardar_tarjeta(tarjeta):
    tarjeta.save()
    return True


def eliminar_tarjeta(tarjeta):
    tarjeta.delete_instance()
    return True


def actualizar_tarjeta(tarjeta):
    tarjeta.save()
    return True


def obtener_tarjeta(id_tarjeta):
    return Tarjeta.get_or_none(Tarjeta.id_tarjeta == id_tarjeta)


def listado_tarjetas(id_lista=None):
    consulta = Tarjeta.select()
    if id_lista is not None:
        consulta = consulta.where(Tarjeta.id_lista == id_lista)
    return list(consulta)


def asignar_usuario(tarjeta, usuario):
    AsignacionTarjeta.get_or_create(id_tarjeta=tarjeta, id_usuario=usuario)
    return True


def quitar_usuario(tarjeta, usuario):
    eliminados = AsignacionTarjeta.delete().where(
        (AsignacionTarjeta.id_tarjeta == tarjeta) &
        (AsignacionTarjeta.id_usuario == usuario)
    ).execute()
    return eliminados > 0


def agregar_etiqueta(tarjeta, etiqueta):
    TarjetaEtiqueta.get_or_create(id_tarjeta=tarjeta, id_etiqueta=etiqueta)
    return True


def quitar_etiqueta(tarjeta, etiqueta):
    eliminados = TarjetaEtiqueta.delete().where(
        (TarjetaEtiqueta.id_tarjeta == tarjeta) &
        (TarjetaEtiqueta.id_etiqueta == etiqueta)
    ).execute()
    return eliminados > 0


def usuarios_de_tarjeta(tarjeta):
    return list(
        Usuario.select().join(AsignacionTarjeta)
        .where(AsignacionTarjeta.id_tarjeta == tarjeta)
    )


def etiquetas_de_tarjeta(tarjeta):
    return list(
        Etiqueta.select().join(TarjetaEtiqueta)
        .where(TarjetaEtiqueta.id_tarjeta == tarjeta)
    )
