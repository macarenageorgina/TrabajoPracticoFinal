# ======================================================
# VALIDACIONES.PY - Funciones de validación y entrada
# ======================================================

import re
from constantes import COD_CATEGORIAS, FORMATO_FECHA_REGEX

# ======================================================
# VALIDACIONES BÁSICAS
# ======================================================

def validar_fecha_simple(fecha):
    """
    Valida formato básico de fecha sin regex.
    """
    partes = fecha.split("/")
    if len(partes) != 3:
        return False
    d, m, a = partes
    if not (d.isdigit() and m.isdigit() and a.isdigit()):
        return False
    d, m, a = int(d), int(m), int(a)
    return 1 <= d <= 31 and 1 <= m <= 12 and a > 0


# ======================================================
# VALIDACIONES AVANZADAS CON REGEX
# ======================================================

def validar_fecha_regex(fecha):
    """
    Valida formato de fecha con expresiones regulares.
    """
    return re.match(FORMATO_FECHA_REGEX, fecha) is not None


# ======================================================
# ENTRADA DE DATOS CON MANEJO DE EXCEPCIONES
# ======================================================

def pedir_fecha():
    """
    Solicita una fecha validándola con regex.
    """
    while True:
        fecha = input("Fecha (dd/mm/aaaa): ").strip()
        try:
            if not validar_fecha_regex(fecha):
                raise ValueError("Formato inválido. Ejemplo: 03/11/2025")
            return fecha
        except ValueError as e:
            print(f"Error: {e}")


def pedir_opcion_numerica():
    """
    Pide una opción numérica manejando errores de conversión.
    """
    try:
        return int(input("Opción: ").strip())
    except ValueError:
        print("Debe ingresar un número.")
        return -1


def pedir_monto():
    """
    Solicita un monto validando que sea numérico y positivo.
    """
    while True:
        entrada = input("Monto (ej: 1234.56): ").strip()
        try:
            valor = float(entrada.replace(",", "."))
            if valor < 0:
                raise ValueError("El monto no puede ser negativo.")
            return valor
        except ValueError as e:
            print(f"Error: {e}")


def pedir_descripcion():
    """
    Solicita una descripción con validación mínima.
    """
    desc = input("Descripción (opcional): ").strip().title()
    if desc == "":
        return ""
    while not any(c.isalpha() for c in desc):
        print("La descripción debe contener al menos una letra.")
        desc = input("Descripción: ").strip().title()
    return desc


def pedir_categoria():
    """
    Muestra categorías y pide una selección válida.
    """
    print("Categorías disponibles:")
    for codigo, nombre in COD_CATEGORIAS.items():
        print(f"{codigo}) {nombre}")
    opcion = input("Seleccione categoría: ").strip()
    while opcion not in COD_CATEGORIAS:
        print("Opción inválida.")
        opcion = input("Seleccione categoría: ").strip()
    return COD_CATEGORIAS[opcion]


def pedir_palabra():
    """Solicita una palabra para búsqueda."""
    return input("Palabra a buscar: ").strip()


def pedir_id():
    """Solicita un ID de gasto."""
    return input("ID del gasto: ").strip()
