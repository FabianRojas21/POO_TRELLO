"""
app.py
Punto de entrada: python3 app.py
"""

from getpass import getpass

from datos.modelos.models import Usuario
from negocio import sesion, usuario
from presentacion.menu import cargar_menu


def _configurar_jefe_inicial():
    print("No hay una cuenta con contraseña configurada.")
    print("Crea la cuenta inicial de jefe de proyecto.")
    nombre = input("Nombre: ").strip()
    while not nombre:
        print("El nombre es obligatorio.")
        nombre = input("Nombre: ").strip()
    while True:
        contrasena = getpass("Contraseña: ")
        confirmacion = getpass("Confirma la contraseña: ")
        if contrasena and contrasena == confirmacion:
            return usuario.crear_primer_jefe(nombre, contrasena)
        print("Las contraseñas deben coincidir y no pueden estar vacías.")


def _iniciar_sesion():
    cuenta_configurada = Usuario.select().where(
        (Usuario.activo == True) &
        Usuario.contraseña.is_null(False) &
        (Usuario.contraseña != '')
    ).exists()
    if not cuenta_configurada:
        jefe = _configurar_jefe_inicial()
        sesion.iniciar(jefe)
        print(f"Jefe inicial creado. Tu ID para iniciar sesión es {jefe.id_usuario}.")
        return jefe

    while True:
        valor_id = input("ID de usuario: ").strip()
        if not valor_id.isdigit():
            print("El ID debe ser un número.")
            continue
        contrasena = getpass("Contraseña: ")
        autenticado = usuario.iniciar_sesion(int(valor_id), contrasena)
        if autenticado is not None:
            print(f"Bienvenido/a, {autenticado.nombre} ({autenticado.rol}).")
            return autenticado
        print("ID o contraseña incorrectos.")


if __name__ == '__main__':
    try:
        _iniciar_sesion()
        cargar_menu()
    except (KeyboardInterrupt, EOFError):
        print("\nHasta pronto.")
    finally:
        sesion.cerrar()
