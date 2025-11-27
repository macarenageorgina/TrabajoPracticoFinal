# ======================================================
# OPERACIONES.PY - Lógica principal de gastos
# ======================================================

from functools import reduce
from constantes import MESES, CATEGORIAS_TUPLA, COD_CATEGORIAS
from matrices import agregar_monto_a_dia, dia_a_posicion
from archivos import crear_backup_gasto, registrar_log
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

def fecha_a_tupla(fecha):
    """
    Convierte una fecha string a tupla (año, mes, día).
    """
    d, m, a = fecha.split("/")
    return (int(a), int(m), int(d))


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
    Agrega un nuevo gasto al sistema, insertándolo ordenado por fecha.
    """
    nuevo_id = ultimo_id + 1
    sid = str(nuevo_id)
    
    gasto = {
        "id": sid,
        "fecha": fecha,
        "monto": monto,
        "categoria": categoria,
        "descripcion": descripcion,
        "estado": "activo"
    }
    
    gastos[sid] = gasto
    
    # Insertar en orden cronológico
    fecha_nueva = fecha_a_tupla(fecha)
    pos = 0
    for i, gid in enumerate(orden):
        if gid in gastos and gastos[gid].get('estado') == 'activo':
            fecha_existente = fecha_a_tupla(gastos[gid]["fecha"])
            if fecha_nueva > fecha_existente:
                pos = i + 1
            else:
                break
    
    orden.insert(pos, sid)
    categorias_usadas.add(categoria)
    
    dia = fecha.split("/")[0]
    agregar_monto_a_dia(calendario, dia, monto)
    
    registrar_log(f"Gasto agregado: ID={sid}, Monto=${monto}, Categoría={categoria}")
    
    return nuevo_id


def editar_gasto(gastos, calendario, gid, nuevo_monto=None, nueva_desc=None):
    """
    Modifica un gasto existente.
    """
    g = gastos.get(gid)
    if g is None or g.get('estado') != 'activo':
        return False
    
    cambios = []
    
    if nuevo_monto is not None:
        diferencia = nuevo_monto - g["monto"]
        dia = g["fecha"].split("/")[0]
        fila, col = dia_a_posicion(dia)
        if 0 <= fila < len(calendario) and 0 <= col < 7:
            calendario[fila][col] += diferencia
        cambios.append(f"Monto: ${g['monto']} → ${nuevo_monto}")
        g["monto"] = nuevo_monto
    
    if nueva_desc is not None:
        cambios.append(f"Descripción: '{g['descripcion']}' → '{nueva_desc}'")
        g["descripcion"] = nueva_desc
    
    if cambios:
        registrar_log(f"Gasto editado: ID={gid}, Cambios: {', '.join(cambios)}")
    
    return True

def eliminar_gasto(gastos, orden, gid):
    """
    Marca un gasto como eliminado (baja lógica) y crea backup.
    """
    if gid in gastos and gastos[gid].get('estado') == 'activo':
        # Crear backup antes de eliminar
        crear_backup_gasto(gastos[gid])
        
        # Marcar como eliminado
        gastos[gid]['estado'] = 'eliminado'
        
        registrar_log(f"Gasto eliminado: ID={gid}, Descripción={gastos[gid]['descripcion']}")
        
        return True
    return False


def restaurar_gasto(gastos, gid):
    """
    Restaura un gasto eliminado.
    """
    if gid in gastos and gastos[gid].get('estado') == 'eliminado':
        gastos[gid]['estado'] = 'activo'
        registrar_log(f"Gasto restaurado: ID={gid}")
        return True
    return False


def obtener_gastos_activos(gastos):
    """
    Retorna solo los gastos activos.
    """
    return {k: v for k, v in gastos.items() if v.get('estado', 'activo') == 'activo'}


def obtener_gastos_eliminados(gastos):
    """
    Retorna solo los gastos eliminados.
    """
    return {k: v for k, v in gastos.items() if v.get('estado') == 'eliminado'}


# ======================================================
# FILTROS
# ======================================================

def filtrar_por_monto_mayor(gastos, umbral):
    """
    Filtra gastos con monto mayor al umbral, ordenados por fecha.
    """
    return sorted(
        [g for g in gastos.values() 
        if g.get('estado', 'activo') == 'activo' and g["monto"] > umbral],
        key=lambda x: fecha_a_tupla(x["fecha"])
    )


def filtrar_por_categoria(gastos, categoria):
    """
    Filtra gastos de una categoría específica, ordenados por fecha.
    """
    return sorted(
        [g for g in gastos.values() 
        if g.get('estado', 'activo') == 'activo' and g["categoria"] == categoria],
        key=lambda x: fecha_a_tupla(x["fecha"])
    )


def filtrar_por_fecha(gastos, fecha):
    """
    Filtra gastos de una fecha específica.
    """
    return sorted(
        [g for g in gastos.values() 
        if g.get('estado', 'activo') == 'activo' and g["fecha"] == fecha],
        key=lambda x: x["id"]
    )


def filtrar_rango_fechas(gastos, fecha_desde, fecha_hasta):
    """
    Filtra gastos en un rango de fechas, ordenados.
    """
    return sorted(
        [g for g in gastos.values()
        if g.get('estado', 'activo') == 'activo' and 
        fecha_desde <= g["fecha"] <= fecha_hasta],
        key=lambda x: fecha_a_tupla(x["fecha"])
    )

# ======================================================
# OPERACIONES CON CONJUNTOS
# ======================================================

def ids_por_categoria(gastos, categoria):
    """
    Retorna el conjunto de IDs activos de una categoría.
    """
    return {gid for gid, g in gastos.items() 
            if g.get('estado', 'activo') == 'activo' and g["categoria"] == categoria}


def ids_por_monto_mayor(gastos, umbral):
    """
    Retorna el conjunto de IDs activos con monto mayor al umbral.
    """
    return {gid for gid, g in gastos.items() 
            if g.get('estado', 'activo') == 'activo' and g["monto"] > umbral}


def gastos_por_ids(gastos, ids_):
    """
    Obtiene gastos activos a partir de un conjunto de IDs, ordenados.
    """
    return sorted(
        [gastos[gid] for gid in ids_ 
        if gid in gastos and gastos[gid].get('estado', 'activo') == 'activo'],
        key=lambda x: fecha_a_tupla(x["fecha"])
    )


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
    Agrupa gastos activos por categoría, ordenados.
    """
    salida = {}
    for g in gastos.values():
        if g.get('estado', 'activo') == 'activo':
            cat = g["categoria"]
            if cat not in salida:
                salida[cat] = []
            salida[cat].append(g)
    
    # Ordenar cada categoría por fecha
    for cat in salida:
        salida[cat] = sorted(salida[cat], key=lambda x: fecha_a_tupla(x["fecha"]))
    
    return salida


def resumen_por_categoria(gastos):
    """
    Calcula el total gastado por categoría (solo activos).
    """
    resumen = {}
    for g in gastos.values():
        if g.get('estado', 'activo') == 'activo':
            cat = g["categoria"]
            resumen[cat] = resumen.get(cat, 0) + g["monto"]
    return resumen


def gastos_ordenados_por_monto(gastos):
    """
    Ordena gastos activos de mayor a menor monto.
    """
    return sorted(
        [g for g in gastos.values() if g.get('estado', 'activo') == 'activo'],
        key=lambda g: g["monto"],
        reverse=True
    )


def gastos_ordenados_por_fecha(gastos):
    """
    Ordena gastos activos por fecha (más recientes primero).
    """
    return sorted(
        [g for g in gastos.values() if g.get('estado', 'activo') == 'activo'],
        key=lambda g: fecha_a_tupla(g["fecha"]),
        reverse=True
    )


# ======================================================
# LAMBDA, MAP, FILTER, REDUCE
# ======================================================

calcular_iva = lambda monto:monto * 0.21

def obtener_montos_con_iva(gastos):
    """
    Calcula el IVA de cada gasto activo.
    """
    return [
        {"id": g["id"], "descripcion": g["descripcion"], 
         "monto": g["monto"], "iva": calcular_iva(g["monto"])}
        for g in gastos.values()
        if g.get('estado', 'activo') == 'activo'
    ]


def gastos_importantes(gastos, umbral):
    """
    Retorna los gastos activos que superan un monto determinado.
    """
    return list(filter(
        lambda g: g.get('estado', 'activo') == 'activo' and g["monto"] > umbral,
        gastos.values()
    ))


def total_montos(gastos):
    """
    Suma todos los montos de gastos activos usando reduce.
    """
    gastos_activos = [g for g in gastos.values() if g.get('estado', 'activo') == 'activo']
    if not gastos_activos:
        return 0
    return reduce(lambda acum, g: acum + g["monto"], gastos_activos, 0)


def promedio_gastos(gastos):
    """
    Calcula el promedio de los montos registrados (solo activos).
    """
    gastos_activos = [g for g in gastos.values() if g.get('estado', 'activo') == 'activo']
    if not gastos_activos:
        return 0
    total = reduce(lambda acum, g: acum + g["monto"], gastos_activos, 0)
    return total / len(gastos_activos)

# ======================================================
# REGEX
# ======================================================

def numeros_en_descripciones(gastos):
    """
    Extrae todos los números presentes en las descripciones de gastos activos.
    """
    patron = r"[0-9]+"
    encontrados = []
    for g in gastos.values():
        if g.get('estado', 'activo') == 'activo':
            encontrados.extend(re.findall(patron, g["descripcion"]))
    return encontrados