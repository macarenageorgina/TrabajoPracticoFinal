# ======================================================
# PRESENTACION.PY - Interfaz y visualización
# ======================================================

def mostrar_encabezado():
    """Muestra encabezado de tabla de gastos."""
    print("\n" + "="*85)
    print(f"{'ID':<5} {'FECHA':<12} {'MONTO':>12} {'CATEGORÍA':<15} {'DESCRIPCIÓN':<30}")
    print("="*85)


def mostrar_gasto_individual(gasto):
    """
    Muestra un gasto de forma detallada.
    """
    print("\n" + "="*85)
    print(" "*30 + "DATOS DEL GASTO")
    print("="*85)
    print(f"  ID:          {gasto['id']}")
    print(f"  Fecha:       {gasto['fecha']}")
    print(f"  Monto:       ${gasto['monto']:,.2f}")
    print(f"  Categoría:   {gasto['categoria']}")
    print(f"  Descripción: {gasto['descripcion']}")
    print(f"  Estado:      {gasto.get('estado', 'activo').upper()}")
    print("="*85)


def mostrar_lista(lista, incluir_eliminados=False):
    """
    Muestra lista de gastos en formato tabla.
    """
    if not incluir_eliminados:
        lista = [g for g in lista if g.get('estado', 'activo') == 'activo']
    
    if len(lista) == 0:
        print("\nNo hay gastos para mostrar.")
        return
    
    mostrar_encabezado()
    for g in lista:
        estado_marca = " [ELIMINADO]" if g.get('estado') == 'eliminado' else ""
        print(f"{g['id']:<5} {g['fecha']:<12} ${g['monto']:>11,.2f} "
            f"{g['categoria']:<15} {g['descripcion']:<30}{estado_marca}")
    print("="*85)
    print(f"Total de registros: {len(lista)}")


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


def mostrar_menu_principal():
    """
    Muestra menú principal simplificado con submenús.
    """
    print("\n" + "="*80)
    print(" "*25 + "GESTOR DE GASTOS PERSONALES")
    print("="*80)
    
    print("\n  1)  Gestión de Gastos")
    print("  2)  Consultas y Filtros")
    print("  3)  Estadísticas y Reportes")
    print("  4)  Herramientas Avanzadas")
    print("  5)  Análisis Recursivo")
    print("  6)  Papelera y Backups")
    print("  7)  Archivos y Datos")
    print("  0)  Salir del Sistema")
    
    print("="*80)


def mostrar_submenu_gestion():
    """
    Submenú: Gestión de Gastos.
    """
    print("\n--- GESTIÓN DE GASTOS ---")
    print("  1) Agregar nuevo gasto")
    print("  2) Editar gasto existente")
    print("  3) Eliminar gasto")
    print("  4) Ver todos los gastos")
    print("  0) Volver al menú principal")


def mostrar_submenu_consultas():
    """
    Submenú: Consultas y Filtros.
    """
    print("\n--- CONSULTAS Y FILTROS ---")
    print("  1) Ver últimos 10 gastos")
    print("  2) Ver primeros 10 gastos")
    print("  3) Buscar por categoría")
    print("  4) Buscar por fecha específica")
    print("  5) Buscar por monto mínimo")
    print("  6) Buscar por palabra en descripción")
    print("  7) Búsqueda avanzada (categoría + monto)")
    print("  8) Filtrar por rango de fechas")
    print("  9) Ver gastos ordenados por monto")
    print("  0) Volver al menú principal")


def mostrar_submenu_estadisticas():
    """
    Submenú: Estadísticas y Reportes.
    """
    print("\n--- ESTADÍSTICAS Y REPORTES ---")
    print("  1) Resumen por categoría")
    print("  2) Calendario mensual")
    print("  3) Día con mayor gasto")
    print("  4) Totales por semana")
    print("  5) Totales por día de la semana")
    print("  6) Análisis de categorías utilizadas")
    print("  7) Días sin movimientos")
    print("  8) Promedio de gastos")
    print("  0) Volver al menú principal")


def mostrar_submenu_herramientas():
    """
    Submenú: Herramientas Avanzadas.
    """
    print("\n--- HERRAMIENTAS AVANZADAS ---")
    print("  1) Calcular IVA de los gastos")
    print("  2) Filtrar gastos importantes")
    print("  3) Calcular total general")
    print("  4) Ver mes de una fecha")
    print("  5) Buscar números en descripciones")
    print("  0) Volver al menú principal")


def mostrar_submenu_recursivo():
    """
    Submenú: Análisis Recursivo.
    """
    print("\n--- ANÁLISIS RECURSIVO ---")
    print("  1) Ver jerarquía de categorías")
    print("  2) Buscar categoría en árbol")
    print("  3) Reporte jerárquico de gastos")
    print("  4) Suma recursiva de montos")
    print("  5) Máximo recursivo en lista")
    print("  0) Volver al menú principal")


def mostrar_submenu_papelera():
    """
    Submenú: Papelera y Backups.
    """
    print("\n--- PAPELERA Y BACKUPS ---")
    print("  1) Ver gastos eliminados")
    print("  2) Restaurar gasto eliminado")
    print("  3) Ver archivo de backups")
    print("  4) Limpiar gastos eliminados permanentemente")
    print("  0) Volver al menú principal")


def mostrar_submenu_archivos():
    """
    Submenú: Archivos y Datos.
    """
    print("\n--- ARCHIVOS Y DATOS ---")
    print("  1) Guardar datos")
    print("  2) Cargar datos")
    print("  3) Ver log del sistema")
    print("  0) Volver al menú principal")


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


def mostrar_iva_gastos(gastos_con_iva):
    """
    Muestra gastos con su IVA calculado.
    """
    print("\n" + "="*90)
    print(" "*30 + "CÁLCULO DE IVA (21%)")
    print("="*90)
    print(f"{'ID':<5} {'DESCRIPCIÓN':<35} {'MONTO':>12} {'IVA':>12} {'TOTAL':>12}")
    print("="*90)
    
    for item in gastos_con_iva:
        total = item['monto'] + item['iva']
        print(f"{item['id']:<5} {item['descripcion']:<35} "
            f"${item['monto']:>11,.2f} ${item['iva']:>11,.2f} ${total:>11,.2f}")
    
    print("="*90)