# ======================================================
# CONSTANTES.PY - Tuplas y configuración del sistema
# ======================================================

# Tupla con nombres de meses
MESES = (
    "Enero", "Febrero", "Marzo", "Abril",
    "Mayo", "Junio", "Julio", "Agosto",
    "Septiembre", "Octubre", "Noviembre", "Diciembre"
)

# Tupla con categorías disponibles
CATEGORIAS_TUPLA = (
    "Alimentación",
    "Transporte",
    "Ocio",
    "Servicios"
)

# Diccionario para mapear códigos a categorías
COD_CATEGORIAS = {
    "1": "Alimentación",
    "2": "Transporte",
    "3": "Ocio",
    "4": "Servicios"
}

# Fecha del sistema representada como tupla (año, mes)
FECHA_SISTEMA = (2025, 11)

# Formato regex para validar fechas
FORMATO_FECHA_REGEX = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/[0-9]{4}$"
