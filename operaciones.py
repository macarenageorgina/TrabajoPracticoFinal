# ======================================================
# OPERACIONES.PY - Lógica principal de gastos
# ======================================================

from functools import reduce
from constantes import MESES, CATEGORIAS_TUPLA, COD_CATEGORIAS
from matrices import agregar_monto_a_dia, dia_a_posicion
import re

# ======================================================
# OPERACIONES CON TUPLAS
# ======================================================

def obtener_mes(fecha):
    """
    Extrae el mes de una fecha y retorna su nombre.
    """
    dia, mes, anio = fecha.split("/")
    return MESES[int(mes) - 1]


# ======================================================
# OPERACIONES CON STRINGS
# ======================================================

def descripcion_contiene_palabra(gasto, palabra):
    """
    Verifica si la descripción contiene una palabra específica.
    """
    palabras = gasto["descripcion"].lower().split()
    return palabra.lower() in palabras


def buscar_gastos_por_palabra(gastos, palabra):
    """
    Retorna gastos cuya descripción contiene la palabra indicada.
    """
    palabra = palabra.lower()
    return [
        g for g in gastos.values()
        if palabra in g["descripcion"].lower()
    ]


# ======================================================
# OPERACIONES CRUD
# ======================================================

def agregar_gasto(gastos, orden, categorias_usadas, calendario,
            ultimo_id, fecha, monto, categoria, descripcion):
    """
    Agrega un nuevo gasto al sistema.
    """
    nuevo_id = ultimo_id + 1
    sid = str(nuevo_id)
    
    gasto = {
        "id": sid,
        "fecha": fecha,
        "monto": monto,
        "categoria": categoria,
        "descripcion": descripcion
    }
    
    gastos[sid] = gasto
    orden.append(sid)
    categorias_usadas.add(categoria)
    
    dia = fecha.split("/")[0]
    agregar_monto_a_dia(calendario, dia, monto)
    
    return nuevo_id


def editar_gasto(gastos, calendario, gid, nuevo_monto=None, nueva_desc=None):
    """
    Modifica un gasto existente.
    """
    g = gastos.get(gid)
    if g is None:
        return False
    
    if nuevo_monto is not None:
        diferencia = nuevo_monto - g["monto"]
        dia = g["fecha"].split("/")[0]
        fila, col = dia_a_posicion(dia)
        if 0 <= fila < len(calendario) and 0 <= col < 7:
            calendario[fila][col] += diferencia
        g["monto"] = nuevo_monto
    
    if nueva_desc is not None:
        g["descripcion"] = nueva_desc
    
    return True


def eliminar_gasto(gastos, orden, gid):
    """
    Elimina un gasto del sistema.
    """
    if gid in gastos:
        del gastos[gid]
        if gid in orden:
            orden.remove(gid)
        return True
    return False


# ======================================================
# FILTROS
# ======================================================

def filtrar_por_monto_mayor(gastos, umbral):
    """
    Filtra gastos con monto mayor al umbral.
    """
    return [g for g in gastos.values() if g["monto"] > umbral]


def filtrar_por_categoria(gastos, categoria):
    """
    Filtra gastos de una categoría específica.
    """
    return [g for g in gastos.values() if g["categoria"] == categoria]


def filtrar_por_fecha(gastos, fecha):
    """
    Filtra gastos de una fecha específica.
    """
    return [g for g in gastos.values() if g["fecha"] == fecha]


def filtrar_rango_fechas(gastos, fecha_desde, fecha_hasta):
    """
    Filtra gastos en un rango de fechas.
    """
    return [
        g for g in gastos.values()
        if fecha_desde <= g["fecha"] <= fecha_hasta
    ]


# ======================================================
# OPERACIONES CON CONJUNTOS
# ======================================================

def ids_por_categoria(gastos, categoria):
    """
    Retorna el conjunto de IDs de una categoría.
    """
    return {gid for gid, g in gastos.items() if g["categoria"] == categoria}


def ids_por_monto_mayor(gastos, umbral):
    """
    Retorna el conjunto de IDs con monto mayor al umbral.
    """
    return {gid for gid, g in gastos.items() if g["monto"] > umbral}


def gastos_por_ids(gastos, ids_):
    """
    Obtiene gastos a partir de un conjunto de IDs.
    """
    return [gastos[gid] for gid in ids_ if gid in gastos]


def categorias_faltantes(categorias_usadas):
    """
    Retorna categorías no utilizadas aún.
    """
    todas = set(COD_CATEGORIAS.values())
    return todas.difference(categorias_usadas)


def porcentaje_cobertura(categorias_usadas):
    """
    Calcula el porcentaje de categorías utilizadas.
    """
    todas = set(COD_CATEGORIAS.values())
    if len(todas) == 0:
        return 0
    return (len(categorias_usadas) * 100) / len(todas)


# ======================================================
# ESTADÍSTICAS Y AGRUPACIONES
# ======================================================

def gastos_por_categoria(gastos):
    """
    Agrupa gastos por categoría.
    """
    salida = {}
    for g in gastos.values():
        cat = g["categoria"]
        salida.setdefault(cat, []).append(g)
    return salida


def resumen_por_categoria(gastos):
    """
    Calcula el total gastado por categoría.
    """
    resumen = {}
    for g in gastos.values():
        cat = g["categoria"]
        resumen[cat] = resumen.get(cat, 0) + g["monto"]
    return resumen


def gastos_ordenados_por_monto(gastos):
    """
    Ordena gastos de mayor a menor monto.
    """
    return sorted(gastos.values(), key=lambda g: g["monto"], reverse=True)


# ======================================================
# LAMBDA, MAP, FILTER, REDUCE
# ======================================================

calcular_iva = lambda monto:monto * 0.21

def gastos_importantes(gastos, umbral):
    """
    Retorna los gastos que superan un monto determinado.
    """
    return list(filter(lambda g: g["monto"] > umbral, gastos.values()))


def total_montos(gastos):
    """
    Suma todos los montos usando reduce.
    """
    if not gastos:
        return 0
    return reduce(lambda acum, g: acum + g["monto"], gastos.values(), 0)


def montos_redondeados_mayores(gastos, minimo):
    """
    Redondea los montos y retorna los mayores al mínimo indicado.
    """
    redondeados = map(lambda g: round(g["monto"]), gastos.values())
    return list(filter(lambda m: m > minimo, redondeados))


def promedio_gastos(gastos):
    """
    Calcula el promedio de los montos registrados.
    """
    if not gastos:
        return 0
    total = reduce(lambda acum, g: acum + g["monto"], gastos.values(), 0)
    return total / len(gastos)

def obtener_montos_con_iva(gastos):
    return [
        {"id": g["id"], "monto": g["monto"], "iva": calcular_iva(g["monto"])}
        for g in gastos.values()
        if g.get('estado', 'activo') == 'activo'
    ]

# ======================================================
# REGEX
# ======================================================

def numeros_en_descripciones(gastos):
    """
    Extrae todos los números presentes en las descripciones.
    """
    patron = r"[0-9]+"
    encontrados = []
    for g in gastos.values():
        encontrados.extend(re.findall(patron, g["descripcion"]))
    return encontrados
