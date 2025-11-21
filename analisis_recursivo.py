# ======================================================
# ANALISIS_RECURSIVO.PY - Funciones recursivas
# ======================================================

def buscar_categoria_recursiva(categorias, nombre, nivel=0):
    """
    Busca una categoría en una estructura jerárquica anidada.
    Caso base: Si el nombre coincide, retorna True.
    Caso recursivo: Recorre subcategorías.
    """
    for cat, subcats in categorias.items():
        # Caso base
        if cat.lower() == nombre.lower():
            print("\t" * nivel + f"Encontrado: {cat}")
            return True
        
        # Caso recursivo
        if isinstance(subcats, dict) and subcats:
            print("\t" * nivel + f"Buscando en {cat}...")
            if buscar_categoria_recursiva(subcats, nombre, nivel + 1):
                return True
    
    return False


def mostrar_jerarquia_categorias(categorias, nivel=0):
    """
    Muestra un árbol de categorías de forma jerárquica.
    """
    for categoria, subcategorias in categorias.items():
        print("\t" * nivel + f"- {categoria}")
        
        if isinstance(subcategorias, dict) and subcategorias:
            mostrar_jerarquia_categorias(subcategorias, nivel + 1)


def contar_gastos_por_categoria_recursiva(gastos, categorias, cat_actual):
    """
    Cuenta gastos en una categoría y sus subcategorías.
    """
    total = sum(1 for g in gastos.values() if g["categoria"] == cat_actual)
    
    if cat_actual in categorias and isinstance(categorias[cat_actual], dict):
        for subcat in categorias[cat_actual].keys():
            total += contar_gastos_por_categoria_recursiva(
                gastos, categorias[cat_actual], subcat
            )
    
    return total


def calcular_total_recursivo(gastos, categorias, cat_actual):
    """
    Calcula el monto total gastado en una categoría y sus subcategorías.
    """
    total = sum(g["monto"] for g in gastos.values() if g["categoria"] == cat_actual)
    
    if cat_actual in categorias and isinstance(categorias[cat_actual], dict):
        for subcat in categorias[cat_actual].keys():
            total += calcular_total_recursivo(
                gastos, categorias[cat_actual], subcat
            )
    
    return total


def generar_reporte_recursivo(gastos, categorias, cat_actual, nivel=0):
    """
    Genera un reporte jerárquico de gastos por categorías.
    """
    gastos_directos = [g for g in gastos.values() if g["categoria"] == cat_actual]
    monto_directo = sum(g["monto"] for g in gastos_directos)
    
    if gastos_directos:
        print("\t" * nivel + f"{cat_actual}: ${monto_directo:,.2f} ({len(gastos_directos)} gastos)")
    else:
        print("\t" * nivel + f"{cat_actual}: Sin gastos")
    
    if cat_actual in categorias and isinstance(categorias[cat_actual], dict):
        for subcat in categorias[cat_actual].keys():
            generar_reporte_recursivo(gastos, categorias[cat_actual], subcat, nivel + 1)


# ======================================================
# FUNCIONES RECURSIVAS DE APOYO
# ======================================================

def sumar_lista_recursiva(lista, indice=0):
    """
    Suma elementos de una lista de forma recursiva.
    """
    if indice >= len(lista):
        return 0
    
    return lista[indice] + sumar_lista_recursiva(lista, indice + 1)


def encontrar_maximo_recursivo(lista, indice=0, maximo_actual=float('-inf')):
    """
    Encuentra el valor máximo en una lista de manera recursiva.
    """
    if indice >= len(lista):
        return maximo_actual
    
    nuevo_maximo = max(maximo_actual, lista[indice])
    return encontrar_maximo_recursivo(lista, indice + 1, nuevo_maximo)


def filtrar_gastos_recursivo(gastos_lista, umbral, indice=0):
    """
    Filtra los gastos mayores a un umbral de forma recursiva.
    """
    if indice >= len(gastos_lista):
        return []
    
    if gastos_lista[indice]["monto"] > umbral:
        return [gastos_lista[indice]] + filtrar_gastos_recursivo(
            gastos_lista, umbral, indice + 1
        )
    else:
        return filtrar_gastos_recursivo(gastos_lista, umbral, indice + 1)


# ======================================================
# ESTRUCTURA DE CATEGORÍAS JERÁRQUICAS (EJEMPLO)
# ======================================================

CATEGORIAS_JERARQUICAS = {
    "Alimentación": {
        "Supermercado": {},
        "Restaurantes": {
            "Comida rápida": {},
            "Gourmet": {}
        },
        "Delivery": {}
    },
    "Transporte": {
        "Combustible": {},
        "Mantenimiento": {},
        "Estacionamiento": {}
    },
    "Ocio": {
        "Entretenimiento": {
            "Cine": {},
            "Teatro": {}
        },
        "Deportes": {}
    },
    "Servicios": {
        "Básicos": {
            "Luz": {},
            "Gas": {},
            "Agua": {}
        },
        "Internet": {},
        "Telefonía": {}
    }
}
