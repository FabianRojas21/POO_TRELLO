"""
presentacion/menu.py
Menú de consola. Solo habla con la capa de negocio.
"""

from functools import wraps

from prettytable import PrettyTable

from auxiliares import nombre_app, version_app
from auxiliares.opciones_menu import (
    mostrar_menu, elegir_opcion, pedir_texto, pedir_entero,
    pedir_fecha, pedir_estado, confirmar,
)
from negocio import proyecto, tablero, lista, tarjeta, usuario, etiqueta, comentario


def seguro(funcion):
    """Evita que un error (dato repetido, id inexistente...) cierre el programa."""
    @wraps(funcion)
    def envoltura(*args, **kwargs):
        try:
            return funcion(*args, **kwargs)
        except EOFError:
            raise
        except Exception as error:
            print(f"No se pudo completar la acción: {error}")
    return envoltura


def _tabla(columnas, filas):
    t = PrettyTable(columnas)
    t.align = 'l'
    for fila in filas:
        t.add_row(fila)
    print(t)


def _fecha(valor):
    return str(valor) if valor else '-'


# ---------------------------------------------------------------- Proyectos

@seguro
def op_crear_proyecto():
    codigo = pedir_texto("Código del proyecto")
    nombre = pedir_texto("Nombre del proyecto")
    inicio = pedir_fecha("Fecha de inicio")
    fin = pedir_fecha("Fecha de fin (Enter para omitir)", obligatorio=False)
    proyecto.crear_proyecto(codigo, nombre, inicio, fin)
    print(f"Proyecto {codigo} creado junto con su tablero.")


@seguro
def op_listar_proyectos():
    proyectos = proyecto.listado_proyectos()
    if not proyectos:
        print("No hay proyectos.")
        return
    _tabla(
        ['Código', 'Nombre', 'Inicio', 'Fin'],
        [[p.codigo_proyecto, p.nombre, _fecha(p.fecha_inicio), _fecha(p.fecha_fin)]
         for p in proyectos],
    )


@seguro
def op_ver_avance():
    codigo = pedir_texto("Código del proyecto")
    avance = proyecto.consultar_avance(codigo)
    if avance is None:
        print("No existe ese proyecto.")
    else:
        print(f"Avance de {codigo}: {avance} % de las tarjetas están completadas.")


@seguro
def op_agregar_usuario_proyecto():
    codigo = pedir_texto("Código del proyecto")
    id_usuario = pedir_entero("ID del usuario")
    if proyecto.agregar_usuario(codigo, id_usuario):
        print("Usuario agregado al proyecto.")
    else:
        print("No se pudo: revisa el código del proyecto y el ID del usuario.")


@seguro
def op_quitar_usuario_proyecto():
    codigo = pedir_texto("Código del proyecto")
    id_usuario = pedir_entero("ID del usuario")
    if proyecto.remover_usuario(codigo, id_usuario):
        print("Usuario quitado del proyecto.")
    else:
        print("No se pudo: el usuario no participa en ese proyecto o los datos no existen.")


@seguro
def op_ver_participantes():
    codigo = pedir_texto("Código del proyecto")
    participantes = proyecto.usuarios_del_proyecto(codigo)
    if participantes is None:
        print("No existe ese proyecto.")
    elif not participantes:
        print("El proyecto aún no tiene participantes.")
    else:
        _tabla(['ID', 'Nombre', 'Rol'],
               [[u.id_usuario, u.nombre, u.rol] for u in participantes])


@seguro
def op_eliminar_proyecto():
    codigo = pedir_texto("Código del proyecto")
    if not confirmar("El proyecto y todo lo que contiene (tablero, listas y tarjetas) irán a la papelera y podrás restaurarlos. ¿Continuar?"):
        print("Cancelado.")
        return
    if proyecto.eliminar_proyecto(codigo):
        print("Proyecto enviado a la papelera.")
    else:
        print("No existe ese proyecto.")


# ------------------------------------------------------------------ Tablero

@seguro
def op_ver_tablero():
    codigo = pedir_texto("Código del proyecto")
    tab = tablero.obtener_tablero_de_proyecto(codigo)
    if tab is None:
        print("No existe ese proyecto.")
        return
    print(f"\nTablero: {tab.nombre}")
    listas = tablero.mostrar_listas(tab.id_tablero)
    if not listas:
        print("El tablero aún no tiene listas.")
        return
    for l in listas:
        print(f"\n[Lista {l.id_lista}] {l.nombre}")
        tarjetas = tarjeta.listado_tarjetas(l.id_lista)
        if not tarjetas:
            print("  (sin tarjetas)")
            continue
        _tabla(['ID', 'Título', 'Estado', 'Fecha límite'],
               [[t.id_tarjeta, t.titulo, t.estado, _fecha(t.fecha_limite)] for t in tarjetas])


@seguro
def op_agregar_lista():
    codigo = pedir_texto("Código del proyecto")
    tab = tablero.obtener_tablero_de_proyecto(codigo)
    if tab is None:
        print("No existe ese proyecto.")
        return
    nombre = pedir_texto("Nombre de la lista")
    tablero.agregar_lista(tab.id_tablero, nombre)
    print(f"Lista '{nombre}' agregada al final del tablero.")


@seguro
def op_quitar_lista():
    id_lista = pedir_entero("ID de la lista")
    if not confirmar("La lista y sus tarjetas irán a la papelera y podrás restaurarlas. ¿Continuar?"):
        print("Cancelado.")
        return
    if tablero.quitar_lista(id_lista):
        print("Lista enviada a la papelera.")
    else:
        print("No existe esa lista.")


# ----------------------------------------------------------------- Tarjetas

@seguro
def op_crear_tarjeta():
    id_lista = pedir_entero("ID de la lista donde va la tarjeta")
    if lista.obtener_lista(id_lista) is None:
        print("No existe esa lista.")
        return
    titulo = pedir_texto("Título")
    descripcion = pedir_texto("Descripción (Enter para omitir)", obligatorio=False)
    limite = pedir_fecha("Fecha límite (Enter para omitir)", obligatorio=False)
    nueva = tarjeta.crear_tarjeta(id_lista, titulo, descripcion, limite)
    print(f"Tarjeta creada con ID {nueva.id_tarjeta}.")


@seguro
def op_ver_detalle_tarjeta():
    id_tarjeta = pedir_entero("ID de la tarjeta")
    t = tarjeta.obtener_tarjeta(id_tarjeta)
    if t is None:
        print("No existe esa tarjeta.")
        return
    responsables = tarjeta.usuarios_de_tarjeta(id_tarjeta)
    etiquetas = tarjeta.etiquetas_de_tarjeta(id_tarjeta)
    print(f"\nTarjeta {t.id_tarjeta}: {t.titulo}")
    print(f"  Lista:        {t.id_lista.nombre}")
    print(f"  Estado:       {t.estado}")
    print(f"  Fecha límite: {_fecha(t.fecha_limite)}")
    print(f"  Descripción:  {t.descripcion or '-'}")
    print("  Responsables: " + (", ".join(u.nombre for u in responsables) or "-"))
    print("  Etiquetas:    " + (", ".join(e.nombre for e in etiquetas) or "-"))
    comentarios = comentario.listado_comentarios(id_tarjeta)
    print("  Comentarios:" + ("" if comentarios else " -"))
    for c in comentarios:
        print(f"    - {c.id_usuario.nombre} ({c.fecha}): {c.texto}")


@seguro
def op_mover_tarjeta():
    id_tarjeta = pedir_entero("ID de la tarjeta")
    id_destino = pedir_entero("ID de la lista destino")
    if tarjeta.obtener_tarjeta(id_tarjeta) is None:
        print("No existe esa tarjeta.")
    elif lista.obtener_lista(id_destino) is None:
        print("No existe la lista destino.")
    else:
        tarjeta.mover(id_tarjeta, id_destino)
        print("Tarjeta movida.")


@seguro
def op_cambiar_estado():
    id_tarjeta = pedir_entero("ID de la tarjeta")
    if tarjeta.obtener_tarjeta(id_tarjeta) is None:
        print("No existe esa tarjeta.")
        return
    nuevo = pedir_estado()
    tarjeta.cambiar_estado(id_tarjeta, nuevo)
    print(f"Estado actualizado a '{nuevo}'.")


@seguro
def op_asignar_usuario():
    id_tarjeta = pedir_entero("ID de la tarjeta")
    id_usuario = pedir_entero("ID del usuario")
    if tarjeta.asignar_usuario(id_tarjeta, id_usuario):
        print("Usuario asignado como responsable.")
    else:
        print("No se pudo: revisa los IDs.")


@seguro
def op_quitar_usuario_asignado():
    id_tarjeta = pedir_entero("ID de la tarjeta")
    id_usuario = pedir_entero("ID del usuario")
    if tarjeta.quitar_usuario_asignado(id_tarjeta, id_usuario):
        print("Responsable quitado.")
    else:
        print("No se pudo: ese usuario no estaba asignado o los IDs no existen.")


@seguro
def op_agregar_etiqueta():
    id_tarjeta = pedir_entero("ID de la tarjeta")
    id_etiqueta = pedir_entero("ID de la etiqueta")
    if tarjeta.agregar_etiqueta(id_tarjeta, id_etiqueta):
        print("Etiqueta agregada.")
    else:
        print("No se pudo: revisa los IDs.")


@seguro
def op_quitar_etiqueta():
    id_tarjeta = pedir_entero("ID de la tarjeta")
    id_etiqueta = pedir_entero("ID de la etiqueta")
    if tarjeta.quitar_etiqueta(id_tarjeta, id_etiqueta):
        print("Etiqueta quitada.")
    else:
        print("No se pudo: esa etiqueta no estaba en la tarjeta o los IDs no existen.")


@seguro
def op_comentar():
    id_tarjeta = pedir_entero("ID de la tarjeta")
    id_usuario = pedir_entero("ID del usuario que comenta")
    texto = pedir_texto("Comentario")
    if tarjeta.agregar_comentario(id_tarjeta, id_usuario, texto) is None:
        print("No se pudo: revisa los IDs.")
    else:
        print("Comentario agregado.")


@seguro
def op_eliminar_tarjeta():
    id_tarjeta = pedir_entero("ID de la tarjeta")
    if not confirmar("¿Enviar la tarjeta a la papelera?"):
        print("Cancelado.")
        return
    if tarjeta.eliminar_tarjeta(id_tarjeta):
        print("Tarjeta enviada a la papelera.")
    else:
        print("No existe esa tarjeta.")


# ----------------------------------------------------- Usuarios y etiquetas

@seguro
def op_crear_usuario():
    nombre = pedir_texto("Nombre")
    rol = pedir_texto("Rol (por ejemplo: Jefe de proyecto, Trabajador)")
    nuevo = usuario.crear_usuario(nombre, rol)
    print(f"Usuario creado con ID {nuevo.id_usuario}.")


@seguro
def op_listar_usuarios():
    usuarios = usuario.listado_usuarios()
    if not usuarios:
        print("No hay usuarios.")
        return
    _tabla(['ID', 'Nombre', 'Rol'], [[u.id_usuario, u.nombre, u.rol] for u in usuarios])


@seguro
def op_eliminar_usuario():
    id_usuario = pedir_entero("ID del usuario")
    if not confirmar("Se eliminarán también sus comentarios y asignaciones. ¿Continuar?"):
        print("Cancelado.")
        return
    if usuario.eliminar_usuario(id_usuario):
        print("Usuario eliminado.")
    else:
        print("No existe ese usuario.")


@seguro
def op_crear_etiqueta():
    nombre = pedir_texto("Nombre de la etiqueta")
    color = pedir_texto("Color")
    nueva = etiqueta.crear_etiqueta(nombre, color)
    print(f"Etiqueta creada con ID {nueva.id_etiqueta}.")


@seguro
def op_listar_etiquetas():
    etiquetas = etiqueta.listado_etiquetas()
    if not etiquetas:
        print("No hay etiquetas.")
        return
    _tabla(['ID', 'Nombre', 'Color'], [[e.id_etiqueta, e.nombre, e.color] for e in etiquetas])


@seguro
def op_eliminar_etiqueta():
    id_etiqueta = pedir_entero("ID de la etiqueta")
    if not confirmar("Se quitará de todas las tarjetas que la usan. ¿Continuar?"):
        print("Cancelado.")
        return
    if etiqueta.eliminar_etiqueta(id_etiqueta):
        print("Etiqueta eliminada.")
    else:
        print("No existe esa etiqueta.")


# ----------------------------------------------------------------- Papelera

@seguro
def op_ver_papelera():
    proyectos = proyecto.listado_proyectos(papelera=True)
    listas = lista.listado_listas(papelera=True)
    tarjetas = tarjeta.listado_tarjetas(papelera=True)
    if not (proyectos or listas or tarjetas):
        print("La papelera está vacía.")
        return
    if proyectos:
        print("\nProyectos eliminados:")
        _tabla(['Código', 'Nombre'], [[p.codigo_proyecto, p.nombre] for p in proyectos])
    if listas:
        print("\nListas eliminadas:")
        _tabla(['ID', 'Nombre'], [[l.id_lista, l.nombre] for l in listas])
    if tarjetas:
        print("\nTarjetas eliminadas:")
        _tabla(['ID', 'Título', 'Lista'],
               [[t.id_tarjeta, t.titulo, t.id_lista.nombre] for t in tarjetas])
    print("\nLas listas y tarjetas que se eliminaron junto con su proyecto o su lista "
          "vuelven al restaurar ese proyecto o esa lista.")


@seguro
def op_restaurar_proyecto():
    codigo = pedir_texto("Código del proyecto a restaurar")
    if proyecto.restaurar_proyecto(codigo):
        print("Proyecto restaurado con sus listas y tarjetas.")
    else:
        print("No se pudo: ese código no está en la papelera.")


@seguro
def op_restaurar_lista():
    id_lista = pedir_entero("ID de la lista a restaurar")
    if lista.restaurar_lista(id_lista):
        print("Lista restaurada con sus tarjetas.")
    else:
        print("No se pudo: ese ID no está en la papelera, o su proyecto sigue eliminado "
              "(restaura primero el proyecto).")


@seguro
def op_restaurar_tarjeta():
    id_tarjeta = pedir_entero("ID de la tarjeta a restaurar")
    if tarjeta.restaurar_tarjeta(id_tarjeta):
        print("Tarjeta restaurada.")
    else:
        print("No se pudo: ese ID no está en la papelera, o su lista sigue eliminada "
              "(restaura primero la lista).")


@seguro
def op_purgar_proyecto():
    codigo = pedir_texto("Código del proyecto a eliminar definitivamente")
    if not confirmar("Se borrará para siempre, con su tablero, listas, tarjetas y comentarios. "
                     "No se puede deshacer. ¿Continuar?"):
        print("Cancelado.")
        return
    if proyecto.purgar_proyecto(codigo):
        print("Proyecto eliminado definitivamente.")
    else:
        print("No se pudo: ese código no está en la papelera.")


@seguro
def op_purgar_lista():
    id_lista = pedir_entero("ID de la lista a eliminar definitivamente")
    if not confirmar("Se borrará para siempre, con sus tarjetas. No se puede deshacer. ¿Continuar?"):
        print("Cancelado.")
        return
    if lista.purgar_lista(id_lista):
        print("Lista eliminada definitivamente.")
    else:
        print("No se pudo: ese ID no está en la papelera.")


@seguro
def op_purgar_tarjeta():
    id_tarjeta = pedir_entero("ID de la tarjeta a eliminar definitivamente")
    if not confirmar("Se borrará para siempre, con sus comentarios. No se puede deshacer. ¿Continuar?"):
        print("Cancelado.")
        return
    if tarjeta.purgar_tarjeta(id_tarjeta):
        print("Tarjeta eliminada definitivamente.")
    else:
        print("No se pudo: ese ID no está en la papelera.")


# -------------------------------------------------------------------- Menús

def _ejecutar_menu(titulo, opciones, acciones):
    while True:
        mostrar_menu(titulo, opciones)
        eleccion = elegir_opcion(opciones)
        if eleccion == '0':
            return
        acciones[eleccion]()


def menu_proyectos():
    opciones = {
        '1': 'Crear proyecto',
        '2': 'Listar proyectos',
        '3': 'Ver avance',
        '4': 'Agregar usuario al proyecto',
        '5': 'Quitar usuario del proyecto',
        '6': 'Ver participantes',
        '7': 'Eliminar proyecto (a la papelera)',
        '0': 'Volver',
    }
    acciones = {
        '1': op_crear_proyecto, '2': op_listar_proyectos, '3': op_ver_avance,
        '4': op_agregar_usuario_proyecto, '5': op_quitar_usuario_proyecto,
        '6': op_ver_participantes, '7': op_eliminar_proyecto,
    }
    _ejecutar_menu('Proyectos', opciones, acciones)


def menu_tablero():
    opciones = {
        '1': 'Ver tablero (listas y tarjetas)',
        '2': 'Agregar lista',
        '3': 'Quitar lista (a la papelera)',
        '0': 'Volver',
    }
    acciones = {'1': op_ver_tablero, '2': op_agregar_lista, '3': op_quitar_lista}
    _ejecutar_menu('Tablero', opciones, acciones)


def menu_tarjetas():
    opciones = {
        '1': 'Crear tarjeta',
        '2': 'Ver detalle',
        '3': 'Mover a otra lista',
        '4': 'Cambiar estado',
        '5': 'Asignar usuario responsable',
        '6': 'Quitar usuario responsable',
        '7': 'Agregar etiqueta',
        '8': 'Quitar etiqueta',
        '9': 'Agregar comentario',
        '10': 'Eliminar tarjeta (a la papelera)',
        '0': 'Volver',
    }
    acciones = {
        '1': op_crear_tarjeta, '2': op_ver_detalle_tarjeta, '3': op_mover_tarjeta,
        '4': op_cambiar_estado, '5': op_asignar_usuario, '6': op_quitar_usuario_asignado,
        '7': op_agregar_etiqueta, '8': op_quitar_etiqueta, '9': op_comentar,
        '10': op_eliminar_tarjeta,
    }
    _ejecutar_menu('Tarjetas', opciones, acciones)


def menu_usuarios():
    opciones = {'1': 'Crear usuario', '2': 'Listar usuarios', '3': 'Eliminar usuario', '0': 'Volver'}
    acciones = {'1': op_crear_usuario, '2': op_listar_usuarios, '3': op_eliminar_usuario}
    _ejecutar_menu('Usuarios', opciones, acciones)


def menu_etiquetas():
    opciones = {'1': 'Crear etiqueta', '2': 'Listar etiquetas', '3': 'Eliminar etiqueta', '0': 'Volver'}
    acciones = {'1': op_crear_etiqueta, '2': op_listar_etiquetas, '3': op_eliminar_etiqueta}
    _ejecutar_menu('Etiquetas', opciones, acciones)


def menu_papelera():
    opciones = {
        '1': 'Ver papelera',
        '2': 'Restaurar proyecto',
        '3': 'Restaurar lista',
        '4': 'Restaurar tarjeta',
        '5': 'Eliminar definitivamente un proyecto',
        '6': 'Eliminar definitivamente una lista',
        '7': 'Eliminar definitivamente una tarjeta',
        '0': 'Volver',
    }
    acciones = {
        '1': op_ver_papelera, '2': op_restaurar_proyecto, '3': op_restaurar_lista,
        '4': op_restaurar_tarjeta, '5': op_purgar_proyecto, '6': op_purgar_lista,
        '7': op_purgar_tarjeta,
    }
    _ejecutar_menu('Papelera', opciones, acciones)


def cargar_menu():
    print(f'{nombre_app} - Version: {version_app}')
    opciones = {
        '1': 'Proyectos',
        '2': 'Tablero',
        '3': 'Tarjetas',
        '4': 'Usuarios',
        '5': 'Etiquetas',
        '6': 'Papelera',
        '0': 'Salir',
    }
    submenus = {
        '1': menu_proyectos, '2': menu_tablero, '3': menu_tarjetas,
        '4': menu_usuarios, '5': menu_etiquetas, '6': menu_papelera,
    }
    try:
        while True:
            mostrar_menu('Menú principal', opciones)
            eleccion = elegir_opcion(opciones)
            if eleccion == '0':
                break
            submenus[eleccion]()
    except (KeyboardInterrupt, EOFError):
        print()
    print("Hasta pronto.")
