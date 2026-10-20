"""
datos/repositorios/repo_tarjeta.py
Incluye las tablas intermedias de la tarjeta (usuarios asignados y etiquetas).
Borrado lógico: eliminar_tarjeta() la manda a la papelera (activo = 0).
"""

from datos.modelos.models import (
    Tarjeta, Lista, AsignacionTarjeta, TarjetaEtiqueta, Usuario, Etiqueta,
)


def guardar_tarjeta(tarjeta):
    tarjeta.save()
    return True


def actualizar_tarjeta(tarjeta):
    tarjeta.save()
    return True


def obtener_tarjeta(id_tarjeta, papelera=False):
    """papelera=False: solo tarjetas activas. papelera=True: solo las eliminadas."""
    return Tarjeta.get_or_none(
        (Tarjeta.id_tarjeta == id_tarjeta) & (Tarjeta.activo == (not papelera))
    )


def listado_tarjetas(id_lista=None, papelera=False):
    """
    papelera=True muestra solo las tarjetas eliminadas por separado: las que se fueron
    junto con su lista o su proyecto vuelven al restaurar la lista o el proyecto.
    """
    consulta = Tarjeta.select()
    if papelera:
        consulta = consulta.join(Lista).where((Tarjeta.activo == False) & (Lista.activo == True))
    else:
        consulta = consulta.where(Tarjeta.activo == True)
    if id_lista is not None:
        consulta = consulta.where(Tarjeta.id_lista == id_lista)
    return list(consulta)


def lista_esta_activa(tarjeta):
    return (Lista.select()
            .where((Lista.id_lista == tarjeta.id_lista_id) & (Lista.activo == True))
            .exists())


def _cambiar_activo(tarjeta, valor):
    Tarjeta.update(activo=valor).where(Tarjeta.id_tarjeta == tarjeta.id_tarjeta).execute()
    tarjeta.activo = valor


def eliminar_tarjeta(tarjeta):
    _cambiar_activo(tarjeta, False)
    return True


def restaurar_tarjeta(tarjeta):
    _cambiar_activo(tarjeta, True)
    return True


def purgar_tarjeta(tarjeta):
    """Borrado real e irreversible (la base cascadea a sus comentarios, etiquetas, etc.)."""
    tarjeta.delete_instance()
    return True


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
