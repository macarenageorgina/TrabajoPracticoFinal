# ======================================================
# TEST_GASTOS.PY - Pruebas unitarias con pytest
# ======================================================
# Ejecutar con: pytest test_gastos.py -v

from operaciones import (
    agregar_gasto, filtrar_por_categoria, filtrar_por_monto_mayor,
    total_montos, promedio_gastos, gastos_importantes,
    categorias_faltantes, porcentaje_cobertura
)
from matrices import crear_calendario, dia_con_mayor_gasto, total_por_semana
from validaciones import validar_fecha_regex
from analisis_recursivo import sumar_lista_recursiva, encontrar_maximo_recursivo
from constantes import COD_CATEGORIAS

# ======================================================
# TESTS DE VALIDACIONES
# ======================================================

def test_validar_fecha_correcta():
    """Verifica que fechas válidas sean aceptadas."""
    assert validar_fecha_regex("15/11/2025") == True
    assert validar_fecha_regex("01/01/2024") == True
    assert validar_fecha_regex("31/12/2025") == True


def test_validar_fecha_incorrecta():
    """Verifica que fechas inválidas sean rechazadas."""
    assert validar_fecha_regex("32/11/2025") == False
    assert validar_fecha_regex("15/13/2025") == False
    assert validar_fecha_regex("15-11-2025") == False
    assert validar_fecha_regex("15/11/25") == False


# ======================================================
# TESTS DE OPERACIONES BÁSICAS
# ======================================================

def test_agregar_gasto():
    """Verifica que un gasto se agregue correctamente."""
    gastos = {}
    orden = []
    categorias_usadas = set()
    calendario = crear_calendario(30)
    
    nuevo_id = agregar_gasto(
        gastos, orden, categorias_usadas, calendario,
        0, "15/11/2025", 1500.50, "Alimentación", "Supermercado"
    )
    
    assert nuevo_id == 1
    assert "1" in gastos
    assert gastos["1"]["monto"] == 1500.50
    assert gastos["1"]["categoria"] == "Alimentación"
    assert "Alimentación" in categorias_usadas
    assert len(orden) == 1


def test_filtrar_por_categoria():
    """Verifica el filtrado por categoría."""
    gastos = {
        "1": {"id": "1", "fecha": "15/11/2025", "monto": 1000, "categoria": "Alimentación", "descripcion": "Test1"},
        "2": {"id": "2", "fecha": "16/11/2025", "monto": 2000, "categoria": "Transporte", "descripcion": "Test2"},
        "3": {"id": "3", "fecha": "17/11/2025", "monto": 1500, "categoria": "Alimentación", "descripcion": "Test3"}
    }
    
    resultado = filtrar_por_categoria(gastos, "Alimentación")
    
    assert len(resultado) == 2
    assert all(g["categoria"] == "Alimentación" for g in resultado)


def test_filtrar_por_monto():
    """Verifica el filtrado por monto mínimo."""
    gastos = {
        "1": {"id": "1", "fecha": "15/11/2025", "monto": 1000, "categoria": "Alimentación", "descripcion": "Test1"},
        "2": {"id": "2", "fecha": "16/11/2025", "monto": 2000, "categoria": "Transporte", "descripcion": "Test2"},
        "3": {"id": "3", "fecha": "17/11/2025", "monto": 500, "categoria": "Ocio", "descripcion": "Test3"}
    }
    
    resultado = filtrar_por_monto_mayor(gastos, 1000)
    
    assert len(resultado) == 1
    assert all(g["monto"] > 1000 for g in resultado)


# ======================================================
# TESTS DE ESTADÍSTICAS
# ======================================================

def test_total_montos():
    """Verifica cálculo del total usando reduce."""
    gastos = {
        "1": {"id": "1", "fecha": "15/11/2025", "monto": 1000, "categoria": "Alimentación", "descripcion": "Test1"},
        "2": {"id": "2", "fecha": "16/11/2025", "monto": 2000, "categoria": "Transporte", "descripcion": "Test2"},
        "3": {"id": "3", "fecha": "17/11/2025", "monto": 1500, "categoria": "Ocio", "descripcion": "Test3"}
    }
    
    total = total_montos(gastos)
    assert total == 4500


def test_total_montos_vacio():
    """Verifica que el total de un diccionario vacío sea 0."""
    assert total_montos({}) == 0


def test_promedio_gastos():
    """Verifica cálculo de promedio."""
    gastos = {
        "1": {"id": "1", "fecha": "15/11/2025", "monto": 1000, "categoria": "Alimentación", "descripcion": "Test1"},
        "2": {"id": "2", "fecha": "16/11/2025", "monto": 2000, "categoria": "Transporte", "descripcion": "Test2"},
        "3": {"id": "3", "fecha": "17/11/2025", "monto": 1500, "categoria": "Ocio", "descripcion": "Test3"}
    }
    
    promedio = promedio_gastos(gastos)
    assert promedio == 1500


def test_gastos_importantes():
    """Verifica filtrado con filter y lambda."""
    gastos = {
        "1": {"id": "1", "fecha": "15/11/2025", "monto": 1000, "categoria": "Alimentación", "descripcion": "Test1"},
        "2": {"id": "2", "fecha": "16/11/2025", "monto": 5000, "categoria": "Transporte", "descripcion": "Test2"},
        "3": {"id": "3", "fecha": "17/11/2025", "monto": 500, "categoria": "Ocio", "descripcion": "Test3"}
    }
    
    importantes = gastos_importantes(gastos, 1000)
    
    assert len(importantes) == 1
    assert importantes[0]["monto"] == 5000


# ======================================================
# TESTS DE CONJUNTOS
# ======================================================

def test_categorias_faltantes():
    """Verifica categorías no utilizadas."""
    categorias_usadas = {"Alimentación", "Transporte"}
    faltantes = categorias_faltantes(categorias_usadas)
    
    assert "Ocio" in faltantes
    assert "Servicios" in faltantes
    assert len(faltantes) == 2


def test_porcentaje_cobertura():
    """Verifica cálculo del porcentaje de categorías usadas."""
    categorias_usadas = {"Alimentación", "Transporte"}
    porcentaje = porcentaje_cobertura(categorias_usadas)
    
    assert porcentaje == 50.0


def test_porcentaje_cobertura_completo():
    """Verifica cobertura completa."""
    todas = set(COD_CATEGORIAS.values())
    porcentaje = porcentaje_cobertura(todas)
    
    assert porcentaje == 100.0


# ======================================================
# TESTS DE MATRICES
# ======================================================

def test_crear_calendario():
    """Verifica creación de matriz calendario."""
    calendario = crear_calendario(30)
    
    assert len(calendario) == 5
    assert all(len(semana) == 7 for semana in calendario)
    assert all(dia == 0.0 for semana in calendario for dia in semana)


def test_dia_con_mayor_gasto():
    """Verifica búsqueda del día con mayor gasto."""
    calendario = crear_calendario(30)
    calendario[0][0] = 1000
    calendario[2][3] = 5000
    calendario[1][5] = 2000
    
    dia, monto = dia_con_mayor_gasto(calendario)
    
    assert dia == 18
    assert monto == 5000


def test_total_por_semana():
    """Verifica suma semanal en matriz."""
    calendario = crear_calendario(30)
    calendario[0][0] = 1000
    calendario[0][1] = 1500
    calendario[1][0] = 2000
    
    totales = total_por_semana(calendario)
    
    assert totales[0] == 2500
    assert totales[1] == 2000


# ======================================================
# TESTS DE RECURSIVIDAD
# ======================================================

def test_sumar_lista_recursiva():
    """Verifica suma recursiva de una lista."""
    lista = [1, 2, 3, 4, 5]
    resultado = sumar_lista_recursiva(lista)
    
    assert resultado == 15


def test_sumar_lista_vacia():
    """Verifica caso base de lista vacía."""
    assert sumar_lista_recursiva([]) == 0


def test_encontrar_maximo_recursivo():
    """Verifica búsqueda recursiva de máximo."""
    lista = [3, 7, 2, 9, 1, 5]
    maximo = encontrar_maximo_recursivo(lista)
    
    assert maximo == 9


def test_encontrar_maximo_un_elemento():
    """Verifica caso con un solo elemento."""
    assert encontrar_maximo_recursivo([42]) == 42


# ======================================================
# TESTS DE INTEGRACIÓN
# ======================================================

def test_flujo_completo_agregar_y_filtrar():
    """Verifica flujo: agregar gastos, filtrar y calcular totales."""
    gastos = {}
    orden = []
    categorias_usadas = set()
    calendario = crear_calendario(30)
    ultimo_id = 0
    
    ultimo_id = agregar_gasto(
        gastos, orden, categorias_usadas, calendario,
        ultimo_id, "15/11/2025", 1000, "Alimentación", "Test1"
    )
    ultimo_id = agregar_gasto(
        gastos, orden, categorias_usadas, calendario,
        ultimo_id, "16/11/2025", 2000, "Transporte", "Test2"
    )
    ultimo_id = agregar_gasto(
        gastos, orden, categorias_usadas, calendario,
        ultimo_id, "17/11/2025", 1500, "Alimentación", "Test3"
    )
    
    assert len(gastos) == 3
    assert len(orden) == 3
    assert len(categorias_usadas) == 2
    
    alim = filtrar_por_categoria(gastos, "Alimentación")
    assert len(alim) == 2
    
    mayores = filtrar_por_monto_mayor(gastos, 1000)
    assert len(mayores) == 2
    
    assert total_montos(gastos) == 4500
