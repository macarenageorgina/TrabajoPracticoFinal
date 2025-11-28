# ======================================================
# TEST_GASTOS.PY - Pruebas unitarias con pytest
# ======================================================
# Ejecutar con: pytest test_gastos.py -v

from operaciones import *
from matrices import *
from validaciones import validar_fecha_regex
from analisis_recursivo import *
from constantes import COD_CATEGORIAS
import pytest

# Ejecutar: pytest test_gastos.py -v

# ======================================================
# TESTS DE VALIDACIONES
# ======================================================

def test_validar_fecha_correcta():
    """Fechas válidas deben ser aceptadas."""
    assert validar_fecha_regex("15/11/2025") == True
    assert validar_fecha_regex("01/01/2024") == True
    assert validar_fecha_regex("31/12/2025") == True


def test_validar_fecha_incorrecta():
    """Fechas inválidas deben ser rechazadas."""
    assert validar_fecha_regex("32/11/2025") == False
    assert validar_fecha_regex("15/13/2025") == False
    assert validar_fecha_regex("15-11-2025") == False


def test_fecha_a_tupla():
    """Conversión de fecha a tupla para ordenamiento."""
    assert fecha_a_tupla("15/11/2025") == (2025, 11, 15)
    assert fecha_a_tupla("01/01/2024") == (2024, 1, 1)


# ======================================================
# TESTS DE OPERACIONES CRUD
# ======================================================

def test_agregar_gasto():
    """Agregar gasto debe actualizar todas las estructuras."""
    gastos = {}
    orden = []
    cats = set()
    cal = crear_calendario(30)
    
    nuevo_id = agregar_gasto(gastos, orden, cats, cal, 0,
                        "15/11/2025", 1500, "Alimentación", "Test")
    
    assert nuevo_id == 1
    assert "1" in gastos
    assert gastos["1"]["estado"] == "activo"
    assert "Alimentación" in cats


def test_agregar_gastos_ordenados_por_fecha():
    """Los gastos deben mantenerse ordenados por fecha."""
    gastos = {}
    orden = []
    cats = set()
    cal = crear_calendario(30)
    
    agregar_gasto(gastos, orden, cats, cal, 0, "20/11/2025", 100, "Ocio", "Más reciente")
    agregar_gasto(gastos, orden, cats, cal, 1, "10/11/2025", 200, "Ocio", "Más antiguo")
    
    # El orden debe reflejar la secuencia cronológica
    fechas = [fecha_a_tupla(gastos[gid]["fecha"]) for gid in orden]
    assert fechas == sorted(fechas)


def test_eliminar_gasto_baja_logica():
    """Eliminar debe cambiar estado, no borrar el registro."""
    gastos = {"1": {"id": "1", "fecha": "15/11/2025", "monto": 1000, 
                    "categoria": "Ocio", "descripcion": "Test", "estado": "activo"}}
    orden = ["1"]
    
    assert eliminar_gasto(gastos, orden, "1") == True
    assert "1" in gastos  # No se borra
    assert gastos["1"]["estado"] == "eliminado"


def test_restaurar_gasto():
    """Restaurar debe cambiar estado de eliminado a activo."""
    gastos = {"1": {"id": "1", "fecha": "15/11/2025", "monto": 1000,
                    "categoria": "Ocio", "descripcion": "Test", "estado": "eliminado"}}
    
    assert restaurar_gasto(gastos, "1") == True
    assert gastos["1"]["estado"] == "activo"


def test_editar_gasto():
    """Editar debe actualizar campos correctamente."""
    gastos = {"1": {"id": "1", "fecha": "15/11/2025", "monto": 1000,
                    "categoria": "Ocio", "descripcion": "Original", "estado": "activo"}}
    cal = crear_calendario(30)
    
    assert editar_gasto(gastos, cal, "1", nuevo_monto=2000, nueva_desc="Modificado") == True
    assert gastos["1"]["monto"] == 2000
    assert gastos["1"]["descripcion"] == "Modificado"


# ======================================================
# TESTS DE FILTROS
# ======================================================

def test_filtrar_solo_activos():
    """Los filtros deben ignorar gastos eliminados."""
    gastos = {
        "1": {"id": "1", "fecha": "15/11/2025", "monto": 1000, "categoria": "Ocio", 
              "descripcion": "Activo", "estado": "activo"},
        "2": {"id": "2", "fecha": "16/11/2025", "monto": 2000, "categoria": "Ocio",
              "descripcion": "Eliminado", "estado": "eliminado"}
    }
    
    resultado = filtrar_por_categoria(gastos, "Ocio")
    assert len(resultado) == 1
    assert resultado[0]["id"] == "1"


def test_filtrar_ordenado_por_fecha():
    """Los filtros deben devolver resultados ordenados."""
    gastos = {
        "1": {"id": "1", "fecha": "20/11/2025", "monto": 1000, "categoria": "Ocio",
              "descripcion": "Último", "estado": "activo"},
        "2": {"id": "2", "fecha": "10/11/2025", "monto": 2000, "categoria": "Ocio",
              "descripcion": "Primero", "estado": "activo"}
    }
    
    resultado = filtrar_por_categoria(gastos, "Ocio")
    fechas = [r["fecha"] for r in resultado]
    assert fechas == ["10/11/2025", "20/11/2025"]


def test_filtrar_por_monto():
    """Filtrar por monto debe funcionar correctamente."""
    gastos = {
        "1": {"id": "1", "fecha": "15/11/2025", "monto": 500, "categoria": "Ocio",
              "descripcion": "Bajo", "estado": "activo"},
        "2": {"id": "2", "fecha": "16/11/2025", "monto": 2000, "categoria": "Ocio",
              "descripcion": "Alto", "estado": "activo"}
    }
    
    resultado = filtrar_por_monto_mayor(gastos, 1000)
    assert len(resultado) == 1
    assert resultado[0]["monto"] == 2000


def test_buscar_por_palabra():
    """Búsqueda por palabra debe funcionar correctamente."""
    gastos = {
        "1": {"id": "1", "fecha": "15/11/2025", "monto": 100, "categoria": "Ocio",
              "descripcion": "Cine con amigos", "estado": "activo"},
        "2": {"id": "2", "fecha": "16/11/2025", "monto": 200, "categoria": "Ocio",
              "descripcion": "Teatro", "estado": "activo"}
    }
    
    resultado = buscar_gastos_por_palabra(gastos, "cine")
    assert len(resultado) == 1
    assert "Cine" in resultado[0]["descripcion"]


# ======================================================
# TESTS DE CONJUNTOS
# ======================================================

def test_ids_por_categoria():
    """Obtener IDs por categoría debe funcionar correctamente."""
    gastos = {
        "1": {"id": "1", "categoria": "Ocio", "estado": "activo"},
        "2": {"id": "2", "categoria": "Transporte", "estado": "activo"},
        "3": {"id": "3", "categoria": "Ocio", "estado": "activo"}
    }
    
    ids = ids_por_categoria(gastos, "Ocio")
    assert ids == {"1", "3"}


def test_categorias_faltantes():
    """Detectar categorías no utilizadas."""
    usadas = {"Alimentación", "Transporte"}
    faltantes = categorias_faltantes(usadas)
    
    assert "Ocio" in faltantes
    assert "Servicios" in faltantes


def test_porcentaje_cobertura():
    """Calcular porcentaje de categorías usadas."""
    usadas = {"Alimentación", "Transporte"}
    porcentaje = porcentaje_cobertura(usadas)
    assert porcentaje == 50.0


# ======================================================
# TESTS DE ESTADÍSTICAS
# ======================================================

def test_total_montos_con_activos():
    """Total debe considerar solo gastos activos."""
    gastos = {
        "1": {"id": "1", "monto": 1000, "estado": "activo"},
        "2": {"id": "2", "monto": 2000, "estado": "eliminado"},
        "3": {"id": "3", "monto": 1500, "estado": "activo"}
    }
    
    total = total_montos(gastos)
    assert total == 2500


def test_promedio_gastos():
    """Promedio debe calcularse correctamente."""
    gastos = {
        "1": {"id": "1", "monto": 1000, "estado": "activo"},
        "2": {"id": "2", "monto": 2000, "estado": "activo"}
    }
    
    promedio = promedio_gastos(gastos)
    assert promedio == 1500


def test_resumen_por_categoria():
    """Resumen por categoría debe agrupar correctamente."""
    gastos = {
        "1": {"id": "1", "monto": 1000, "categoria": "Ocio", "estado": "activo"},
        "2": {"id": "2", "monto": 1500, "categoria": "Ocio", "estado": "activo"},
        "3": {"id": "3", "monto": 2000, "categoria": "Transporte", "estado": "activo"}
    }
    
    resumen = resumen_por_categoria(gastos)
    assert resumen["Ocio"] == 2500
    assert resumen["Transporte"] == 2000


# ======================================================
# TESTS DE LAMBDA Y FUNCIONES
# ======================================================

def test_calcular_iva():
    """Cálculo de IVA debe ser correcto."""
    from operaciones import calcular_iva
    assert calcular_iva(1000) == 210


# Función aplicar_descuento eliminada del proyecto
# def test_aplicar_descuento():
#     pass


def test_gastos_importantes_con_filter():
    """Filtrar gastos importantes usando filter."""
    gastos = {
        "1": {"id": "1", "monto": 500, "estado": "activo"},
        "2": {"id": "2", "monto": 5000, "estado": "activo"}
    }
    
    importantes = gastos_importantes(gastos, 1000)
    assert len(importantes) == 1
    assert importantes[0]["monto"] == 5000


def test_obtener_iva_de_gastos():
    """Cálculo de IVA para múltiples gastos."""
    gastos = {
        "1": {"id": "1", "descripcion": "Test1", "monto": 1000, "estado": "activo"},
        "2": {"id": "2", "descripcion": "Test2", "monto": 2000, "estado": "activo"}
    }
    
    con_iva = obtener_montos_con_iva(gastos)
    assert len(con_iva) == 2
    assert con_iva[0]["iva"] == 210
    assert con_iva[1]["iva"] == 420


# ======================================================
# TESTS DE MATRICES
# ======================================================

def test_crear_calendario():
    """Calendario debe crearse con dimensiones correctas."""
    cal = crear_calendario(30)
    assert len(cal) == 5  # 5 semanas
    assert all(len(semana) == 7 for semana in cal)


def test_dia_con_mayor_gasto():
    """Detectar día con mayor gasto."""
    cal = crear_calendario(30)
    cal[0][0] = 1000
    cal[2][3] = 5000
    
    dia, monto = dia_con_mayor_gasto(cal)
    assert dia == 18
    assert monto == 5000


def test_total_por_semana():
    """Sumar gastos por semana."""
    cal = crear_calendario(30)
    cal[0][0] = 1000
    cal[0][1] = 1500
    cal[1][0] = 2000
    
    totales = total_por_semana(cal)
    assert totales[0] == 2500
    assert totales[1] == 2000


def test_dias_sin_gastos():
    """Detectar días sin movimientos."""
    cal = crear_calendario(30)
    cal[0][0] = 100  # Día 1
    cal[0][2] = 200  # Día 3
    
    vacios = dias_sin_gastos(cal, 30)
    assert 1 not in vacios
    assert 2 in vacios
    assert 3 not in vacios


# ======================================================
# TESTS DE RECURSIVIDAD
# ======================================================

def test_sumar_lista_recursiva():
    """Suma recursiva debe funcionar correctamente."""
    assert sumar_lista_recursiva([1, 2, 3, 4, 5]) == 15
    assert sumar_lista_recursiva([]) == 0
    assert sumar_lista_recursiva([100]) == 100


def test_encontrar_maximo_recursivo():
    """Búsqueda recursiva de máximo."""
    assert encontrar_maximo_recursivo([3, 7, 2, 9, 1]) == 9
    assert encontrar_maximo_recursivo([42]) == 42
    assert encontrar_maximo_recursivo([5, 5, 5]) == 5


def test_filtrar_gastos_recursivo():
    """Filtrado recursivo debe funcionar."""
    lista = [
        {"monto": 500},
        {"monto": 1500},
        {"monto": 800},
        {"monto": 2000}
    ]
    
    resultado = filtrar_gastos_recursivo(lista, 1000)
    assert len(resultado) == 2
    assert all(g["monto"] > 1000 for g in resultado)


def test_buscar_categoria_recursiva():
    """Búsqueda en árbol jerárquico."""
    assert buscar_categoria_recursiva(CATEGORIAS_JERARQUICAS, "Alimentación") == True
    assert buscar_categoria_recursiva(CATEGORIAS_JERARQUICAS, "Cine") == True
    assert buscar_categoria_recursiva(CATEGORIAS_JERARQUICAS, "Inexistente") == False


# ======================================================
# TESTS DE INTEGRACIÓN
# ======================================================

def test_flujo_completo_crud():
    """Flujo completo: agregar, editar, eliminar, restaurar."""
    gastos = {}
    orden = []
    cats = set()
    cal = crear_calendario(30)
    
    # Agregar
    uid = agregar_gasto(gastos, orden, cats, cal, 0, "15/11/2025", 1000, "Ocio", "Test")
    assert uid == 1
    assert gastos["1"]["estado"] == "activo"
    
    # Editar
    assert editar_gasto(gastos, cal, "1", nuevo_monto=2000) == True
    assert gastos["1"]["monto"] == 2000
    
    # Eliminar
    assert eliminar_gasto(gastos, orden, "1") == True
    assert gastos["1"]["estado"] == "eliminado"
    
    # Restaurar
    assert restaurar_gasto(gastos, "1") == True
    assert gastos["1"]["estado"] == "activo"


def test_flujo_filtros_y_estadisticas():
    """Flujo completo de filtros y estadísticas."""
    gastos = {}
    orden = []
    cats = set()
    cal = crear_calendario(30)
    
    agregar_gasto(gastos, orden, cats, cal, 0, "10/11/2025", 1000, "Alimentación", "Test1")
    agregar_gasto(gastos, orden, cats, cal, 1, "15/11/2025", 2000, "Transporte", "Test2")
    agregar_gasto(gastos, orden, cats, cal, 2, "20/11/2025", 1500, "Alimentación", "Test3")
    
    # Filtrar
    alim = filtrar_por_categoria(gastos, "Alimentación")
    assert len(alim) == 2
    
    # Estadísticas
    assert total_montos(gastos) == 4500
    assert promedio_gastos(gastos) == 1500
    
    # Resumen
    resumen = resumen_por_categoria(gastos)
    assert resumen["Alimentación"] == 2500


if __name__ == "__main__":
    pytest.main([__file__, "-v"])