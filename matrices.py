# ======================================================
# MATRICES.PY - Operaciones con matrices (calendario)
# ======================================================

from math import ceil

def crear_calendario(dias_mes):
    """
    Crea una matriz para el calendario mensual (semanas x 7 días).
    """
    filas = ceil(dias_mes / 7)
    return [[0.0 for _ in range(7)] for _ in range(filas)]


def dia_a_posicion(dia):
    """
    Convierte un día del mes (1-30) a coordenadas (fila, columna).
    """
    dia = int(dia)
    return ((dia - 1) // 7, (dia - 1) % 7)


def dia_con_mayor_gasto(calendario):
    """
    Encuentra el día con mayor gasto registrado en el mes.
    """
    mayor = -1
    dia_max = -1
    dia = 1
    for fila in calendario:
        for valor in fila:
            if valor > mayor:
                mayor = valor
                dia_max = dia
            dia += 1
    return dia_max, mayor


def total_por_semana(calendario):
    """
    Calcula el total gastado por semana.
    """
    return [sum(fila) for fila in calendario]


def total_por_dia_semana(calendario):
    """
    Calcula el total por día de la semana (lunes a domingo).
    """
    totales = [0] * 7
    for fila in calendario:
        for i, valor in enumerate(fila):
            totales[i] += valor
    return totales


def dias_con_gasto_mayor(calendario, umbral):
    """
    Devuelve una lista de días donde el gasto supera el umbral indicado.
    """
    dias = []
    dia = 1
    for fila in calendario:
        for valor in fila:
            if valor > umbral:
                dias.append(dia)
            dia += 1
    return dias


def modificar_gasto_en_dia(calendario, dia, nuevo_monto):
    """
    Actualiza el monto total de un día específico.
    """
    fila, col = dia_a_posicion(dia)
    if 0 <= fila < len(calendario) and 0 <= col < 7:
        calendario[fila][col] = nuevo_monto
        return True
    return False


def agregar_monto_a_dia(calendario, dia, monto):
    """
    Suma un monto al día correspondiente en el calendario.
    """
    fila, col = dia_a_posicion(dia)
    if 0 <= fila < len(calendario) and 0 <= col < 7:
        calendario[fila][col] += monto
        return True
    return False


def dias_con_gastos(calendario):
    """
    Devuelve un conjunto con los días que tienen gastos registrados.
    """
    usados = set()
    dia = 1
    for fila in calendario:
        for valor in fila:
            if valor > 0:
                usados.add(dia)
            dia += 1
    return usados


def dias_sin_gastos(calendario, dias_mes):
    """
    Devuelve los días sin gastos registrados.
    """
    usados = dias_con_gastos(calendario)
    return set(range(1, dias_mes + 1)).difference(usados)
