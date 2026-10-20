"""
datos/repositorios/repo_lista.py
Borrado lógico: eliminar_lista() manda la lista y sus tarjetas a la papelera (activo = 0).
"""

from peewee import fn

from datos.modelos.models import Lista, Tablero, Proyecto, Tarjeta


def guardar_lista(lista):
    lista.save()
    return True


def actualizar_lista(lista):
    lista.save()
    return True


def obtener_lista(id_lista, papelera=False):
    """papelera=False: solo listas activas. papelera=True: solo las eliminadas."""
    return Lista.get_or_none((Lista.id_lista == id_lista) & (Lista.activo == (not papelera)))


def listado_listas(id_tablero=None, papelera=False):
    """
    papelera=True muestra solo las listas eliminadas por separado: las que se fueron
    junto con su proyecto vuelven al restaurar el proyecto.
    """
    consulta = Lista.select().order_by(Lista.orden)
    if papelera:
        consulta = (consulta.join(Tablero).join(Proyecto)
                    .where((Lista.activo == False) & (Proyecto.activo == True)))
    else:
        consulta = consulta.where(Lista.activo == True)
    if id_tablero is not None:
        consulta = consulta.where(Lista.id_tablero == id_tablero)
    return list(consulta)


def siguiente_orden(id_tablero):
    """Orden de una lista nueva: después de la última, contando también las de la papelera."""
    maximo = Lista.select(fn.MAX(Lista.orden)).where(Lista.id_tablero == id_tablero).scalar()
    return (maximo or 0) + 1


def proyecto_esta_activo(lista):
    return (Proyecto.select().join(Tablero)
            .where((Tablero.id_tablero == lista.id_tablero_id) & (Proyecto.activo == True))
            .exists())


def _cambiar_activo(lista, valor):
    with Lista._meta.database.atomic():
        Tarjeta.update(activo=valor).where(Tarjeta.id_lista == lista.id_lista).execute()
        Lista.update(activo=valor).where(Lista.id_lista == lista.id_lista).execute()
    lista.activo = valor


def eliminar_lista(lista):
    _cambiar_activo(lista, False)
    return True


def restaurar_lista(lista):
    _cambiar_activo(lista, True)
    return True


def purgar_lista(lista):
    """Borrado real e irreversible (la base cascadea a sus tarjetas)."""
    lista.delete_instance()
    return True
