"""
auxiliares/opciones_menu.py
Estados válidos y funciones para mostrar menús y leer datos del teclado con validación.
"""

import datetime

ESTADOS = ['pendiente', 'en progreso', 'completada']


def mostrar_menu(titulo, opciones):
    """opciones: dict {'1': 'Texto', ..., '0': 'Volver'}"""
    print(f"\n=== {titulo} ===")
    for clave, texto in opciones.items():
        print(f"  {clave}) {texto}")


def elegir_opcion(opciones):
    while True:
        eleccion = input("Opción: ").strip()
        if eleccion in opciones:
            return eleccion
        print("Opción no válida, intenta de nuevo.")


def pedir_texto(mensaje, obligatorio=True):
    while True:
        valor = input(f"{mensaje}: ").strip()
        if valor:
            return valor
        if not obligatorio:
            return None
        print("Este dato es obligatorio.")


def pedir_entero(mensaje):
    while True:
        valor = input(f"{mensaje}: ").strip()
        if valor.isdigit():
            return int(valor)
        print("Escribe un número entero.")


def pedir_fecha(mensaje, obligatorio=True):
    while True:
        valor = input(f"{mensaje} [AAAA-MM-DD]: ").strip()
        if not valor and not obligatorio:
            return None
        try:
            return datetime.date.fromisoformat(valor)
        except ValueError:
            print("Fecha no válida. Ejemplo: 2026-10-31")


def pedir_estado():
    print("Estados disponibles:")
    for i, estado in enumerate(ESTADOS, start=1):
        print(f"  {i}) {estado}")
    while True:
        valor = input("Elige el estado: ").strip()
        if valor.isdigit() and 1 <= int(valor) <= len(ESTADOS):
            return ESTADOS[int(valor) - 1]
        print("Opción no válida.")


def confirmar(mensaje):
    return input(f"{mensaje} (s/n): ").strip().lower() == 's'
