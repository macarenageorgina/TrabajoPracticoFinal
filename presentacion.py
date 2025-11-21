# ======================================================
# PRESENTACION.PY - Interfaz y visualización
# ======================================================

def mostrar_encabezado():
    """Muestra encabezado de tabla de gastos."""
    print("\n" + "="*80)
    print(f"{'ID':<5} {'FECHA':<12} {'MONTO':>12} {'CATEGORÍA':<15} {'DESCRIPCIÓN':<30}")
    print("="*80)


def mostrar_lista(lista):
    """
    Muestra lista de gastos en formato tabla.
    """
    if len(lista) == 0:
        print("\nNo hay gastos para mostrar.")
        return
    
    mostrar_encabezado()
    for g in lista:
        print(f"{g['id']:<5} {g['fecha']:<12} ${g['monto']:>11,.2f} "
              f"{g['categoria']:<15} {g['descripcion']:<30}")
    print("="*80)


def mostrar_calendario(calendario):
    """
    Muestra calendario mensual con gastos por día.
    """
    print("\n" + "="*80)
    print("CALENDARIO MENSUAL DE GASTOS")
    print("="*80)
    dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    
    encabezado = "  ".join(f"{d:>8}" for d in dias_semana)
    print(f"\n{encabezado}")
    print("-" * 80)
    
    dia = 1
    for fila in calendario:
        fila_txt = "  ".join(f"${v:7.2f}" for v in fila)
        print(f"{fila_txt}")
        dia += 7
    print("="*80)


def mostrar_menu():
    """
    Muestra menú principal del sistema.
    """
    print("\n" + "="*80)
    print(" "*25 + "GESTOR DE GASTOS PERSONALES")
    print("="*80)
    
    print("\nGESTIÓN DE GASTOS")
    print("  1)  Agregar nuevo gasto")
    print("  2)  Editar gasto existente")
    print("  3)  Eliminar gasto")
    
    print("\nCONSULTAS Y FILTROS")
    print("  4)  Ver todos los gastos")
    print("  5)  Ver últimos 5 gastos")
    print("  6)  Ver primeros 5 gastos")
    print("  7)  Ver gastos recientes (últimos 10)")
    print("  8)  Buscar por categoría")
    print("  9)  Buscar por fecha específica")
    print("  10) Buscar por monto mínimo")
    print("  11) Buscar por palabra en descripción")
    print("  12) Buscar por categoría y monto (avanzado)")
    print("  13) Filtrar por rango de fechas")
    print("  14) Ver gastos ordenados por monto")

    print("\nESTADÍSTICAS Y REPORTES")
    print("  15) Resumen por categoría")
    print("  16) Calendario mensual")
    print("  17) Día con mayor gasto")
    print("  18) Totales por semana")
    print("  19) Totales por día de la semana")
    print("  20) Análisis de categorías utilizadas")
    print("  21) Días sin movimientos")
    print("  22) Promedio de gastos")
    
    print("\nHERRAMIENTAS AVANZADAS")
    print("  23) Aplicar descuento a gastos altos")
    print("  24) Filtrar gastos importantes")
    print("  25) Calcular total general")
    print("  26) Ver mes de una fecha")
    print("  27) Analizar descripciones")
    
    print("\nANÁLISIS RECURSIVO")
    print("  28) Ver jerarquía de categorías")
    print("  29) Buscar categoría en árbol")
    print("  30) Reporte jerárquico de gastos")
    print("  31) Suma recursiva de montos")
    print("  32) Máximo recursivo en lista")
    
    print("\nDATOS")
    print("  33) Guardar datos")
    print("  34) Cargar datos")
    
    print("\nSALIR")
    print("  35) Salir del sistema")
    
    print("="*80)



def mostrar_resumen_categoria(resumen):
    """
    Muestra resumen de gastos agrupados por categoría.
    """
    print("\n" + "="*80)
    print(" "*25 + "RESUMEN POR CATEGORÍA")
    print("="*80)
    
    if not resumen:
        print("\nNo hay gastos registrados.")
        return
    
    print(f"\n{'CATEGORÍA':<20} {'TOTAL':>15} {'%':>10}")
    print("-" * 80)
    
    total_general = sum(resumen.values())
    
    for cat, monto in sorted(resumen.items(), key=lambda x: x[1], reverse=True):
        porcentaje = (monto / total_general * 100) if total_general > 0 else 0
        print(f"{cat:<20} ${monto:>14,.2f} {porcentaje:>9.1f}%")
    
    print("-" * 80)
    print(f"{'TOTAL GENERAL':<20} ${total_general:>14,.2f} {'100.0%':>10}")
    print("="*80)


def mostrar_analisis_categorias(categorias_usadas, faltantes, porcentaje):
    """
    Muestra análisis de uso de categorías.
    """
    print("\n" + "="*80)
    print(" "*25 + "ANÁLISIS DE CATEGORÍAS")
    print("="*80)
    
    print(f"\nCategorías utilizadas ({len(categorias_usadas)}):")
    for cat in sorted(categorias_usadas):
        print(f"  • {cat}")
    
    if faltantes:
        print(f"\nCategorías sin uso ({len(faltantes)}):")
        for cat in sorted(faltantes):
            print(f"  • {cat}")
    else:
        print("\nTodas las categorías han sido utilizadas.")
    
    print(f"\nCobertura: {porcentaje:.1f}%")
    print("="*80)


def mostrar_dias_sin_movimientos(dias):
    """
    Muestra días del mes sin gastos.
    """
    print("\n" + "="*80)
    print(" "*25 + "DÍAS SIN MOVIMIENTOS")
    print("="*80)
    
    if not dias:
        print("\nTodos los días tienen gastos registrados.")
    else:
        print(f"\nHay {len(dias)} día(s) sin gastos:")
        dias_ordenados = sorted(dias)
        for i in range(0, len(dias_ordenados), 10):
            grupo = dias_ordenados[i:i+10]
            print("  " + ", ".join(f"día {d}" for d in grupo))
    
    print("="*80)


def confirmar_accion(mensaje):
    """
    Pide confirmación para acciones importantes.
    """
    respuesta = input(f"{mensaje} (s/n): ").strip().lower()
    return respuesta == "s"
