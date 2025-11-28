34# ======================================================
# MAIN.PY - Programa principal
# ======================================================
# Trabajo Práctico Integrador - Algoritmos y Estructuras de Datos I
# UADE - Prof. David Yaps
# ======================================================

from matrices import crear_calendario, dia_con_mayor_gasto, total_por_semana, total_por_dia_semana, dias_sin_gastos
from operaciones import (
    agregar_gasto, editar_gasto, eliminar_gasto, restaurar_gasto,
    filtrar_por_categoria, filtrar_por_fecha, filtrar_por_monto_mayor,
    buscar_gastos_por_palabra, ids_por_categoria, ids_por_monto_mayor,
    gastos_por_ids, categorias_faltantes, porcentaje_cobertura,
    resumen_por_categoria, gastos_ordenados_por_monto, gastos_ordenados_por_fecha,
    gastos_importantes, total_montos, promedio_gastos, 
    obtener_montos_con_iva, obtener_mes, filtrar_rango_fechas,
    obtener_gastos_eliminados, numeros_en_descripciones
)
from analisis_recursivo import (
    mostrar_jerarquia_categorias,
    buscar_categoria_recursiva,
    generar_reporte_recursivo,
    sumar_lista_recursiva,
    encontrar_maximo_recursivo,
    CATEGORIAS_JERARQUICAS
)
from validaciones import (
    pedir_fecha, pedir_monto, pedir_categoria, pedir_descripcion,
    pedir_opcion_numerica, pedir_palabra, pedir_id
)
from archivos import (
    guardar_gastos_csv, cargar_gastos_csv,
    guardar_calendario, cargar_calendario
)
from presentacion import (
    mostrar_lista, mostrar_calendario, mostrar_menu_principal,
    mostrar_submenu_gestion, mostrar_submenu_consultas, 
    mostrar_submenu_estadisticas, mostrar_submenu_herramientas, 
    mostrar_submenu_recursivo, mostrar_submenu_papelera, 
    mostrar_submenu_archivos, mostrar_resumen_categoria, 
    mostrar_analisis_categorias, mostrar_dias_sin_movimientos, 
    confirmar_accion, mostrar_gasto_individual, mostrar_iva_gastos
)


class SistemaGastos:
    def __init__(self):
        self.dias_mes = 30
        self.gastos = {}
        self.orden = []
        self.categorias_usadas = set()
        self.calendario = crear_calendario(self.dias_mes)
        self.ultimo_id = 0
        self.modificado = False


def menu_gestion(sistema):
    """Menú recursivo para gestión de gastos."""
    while True:
        mostrar_submenu_gestion()
        opcion = pedir_opcion_numerica()
        
        if opcion == 0:
            return
        
        elif opcion == 1:  # Agregar
            print("\n--- AGREGAR NUEVO GASTO ---")
            fecha = pedir_fecha()
            monto = pedir_monto()
            categoria = pedir_categoria()
            descripcion = pedir_descripcion()
            
            sistema.ultimo_id = agregar_gasto(
                sistema.gastos, sistema.orden, sistema.categorias_usadas,
                sistema.calendario, sistema.ultimo_id,
                fecha, monto, categoria, descripcion
            )
            sistema.modificado = True
            print(f"\n✓ Gasto #{sistema.ultimo_id} agregado correctamente.")
        
        elif opcion == 2:  # Editar
            print("\n--- EDITAR GASTO ---")
            gid = pedir_id()
            if gid not in sistema.gastos:
                print("❌ ID no encontrado.")
            elif sistema.gastos[gid].get('estado') != 'activo':
                print("❌ Este gasto está eliminado.")
            else:
                mostrar_gasto_individual(sistema.gastos[gid])
                print("\n¿Qué desea modificar?")
                print("1) Monto")
                print("2) Descripción")
                print("3) Ambos")
                sub = pedir_opcion_numerica()
                
                nuevo_monto = None
                nueva_desc = None
                
                if sub in [1, 3]:
                    nuevo_monto = pedir_monto()
                if sub in [2, 3]:
                    nueva_desc = pedir_descripcion()
                
                if editar_gasto(sistema.gastos, sistema.calendario, gid, nuevo_monto, nueva_desc):
                    sistema.modificado = True
                    print("\n Gasto modificado correctamente.")
                else:
                    print("Error al modificar gasto.")
        
        elif opcion == 3:  # Eliminar
            print("\n--- ELIMINAR GASTO ---")
            gid = pedir_id()
            if gid in sistema.gastos and sistema.gastos[gid].get('estado') == 'activo':
                mostrar_gasto_individual(sistema.gastos[gid])
                if confirmar_accion("\n¿Confirma eliminar este gasto?"):
                    if eliminar_gasto(sistema.gastos, sistema.orden, gid):
                        sistema.modificado = True
                        print("\n✓ Gasto movido a la papelera.")
                    else:
                        print("Error al eliminar.")
            else:
                print("ID no encontrado o ya eliminado.")
        
        elif opcion == 4:  # Ver todos
            print("\n--- TODOS LOS GASTOS ---")
            mostrar_lista(gastos_ordenados_por_fecha(sistema.gastos))


def menu_consultas(sistema):
    """Menú recursivo para consultas y filtros."""
    while True:
        mostrar_submenu_consultas()
        opcion = pedir_opcion_numerica()
        
        if opcion == 0:
            return
        
        elif opcion == 1:  # Últimos 10
            print("\n--- ÚLTIMOS 10 GASTOS ---")
            gastos_activos = [gid for gid in sistema.orden if sistema.gastos.get(gid, {}).get('estado') == 'activo']
            ultimos = gastos_activos[-10:]
            mostrar_lista([sistema.gastos[g] for g in reversed(ultimos)])
        
        elif opcion == 2:  # Primeros 10
            print("\n--- PRIMEROS 10 GASTOS ---")
            gastos_activos = [gid for gid in sistema.orden if sistema.gastos.get(gid, {}).get('estado') == 'activo']
            primeros = gastos_activos[:10]
            mostrar_lista([sistema.gastos[g] for g in primeros])
        
        elif opcion == 3:  # Por categoría
            print("\n--- FILTRAR POR CATEGORÍA ---")
            categoria = pedir_categoria()
            mostrar_lista(filtrar_por_categoria(sistema.gastos, categoria))
        
        elif opcion == 4:  # Por fecha
            print("\n--- FILTRAR POR FECHA ---")
            fecha = pedir_fecha()
            mostrar_lista(filtrar_por_fecha(sistema.gastos, fecha))
        
        elif opcion == 5:  # Por monto
            print("\n--- FILTRAR POR MONTO MÍNIMO ---")
            umbral = pedir_monto()
            mostrar_lista(filtrar_por_monto_mayor(sistema.gastos, umbral))
        
        elif opcion == 6:  # Por palabra
            print("\n--- BUSCAR EN DESCRIPCIONES ---")
            palabra = pedir_palabra()
            resultados = buscar_gastos_por_palabra(sistema.gastos, palabra)
            if resultados:
                mostrar_lista(resultados)
            else:
                print(f"No se encontraron gastos con '{palabra}'.")
        
        elif opcion == 7:  # Búsqueda avanzada
            print("\n--- BÚSQUEDA AVANZADA (Categoría + Monto) ---")
            categoria = pedir_categoria()
            umbral = pedir_monto()
            
            ids_cat = ids_por_categoria(sistema.gastos, categoria)
            ids_monto = ids_por_monto_mayor(sistema.gastos, umbral)
            ids_comunes = ids_cat & ids_monto
            
            if ids_comunes:
                print(f"\n✓ Encontrados {len(ids_comunes)} gastos:")
                mostrar_lista(gastos_por_ids(sistema.gastos, ids_comunes))
            else:
                print("No hay gastos que cumplan ambas condiciones.")
        
        elif opcion == 8:  # Rango de fechas
            print("\n--- FILTRAR POR RANGO DE FECHAS ---")
            fecha_desde = pedir_fecha()
            fecha_hasta = pedir_fecha()
            mostrar_lista(filtrar_rango_fechas(sistema.gastos, fecha_desde, fecha_hasta))
        
        elif opcion == 9:  # Ordenados por monto
            print("\n--- GASTOS ORDENADOS POR MONTO (Mayor a Menor) ---")
            mostrar_lista(gastos_ordenados_por_monto(sistema.gastos))


def menu_estadisticas(sistema):
    """Menú recursivo para estadísticas."""
    while True:
        mostrar_submenu_estadisticas()
        opcion = pedir_opcion_numerica()
        
        if opcion == 0:
            return
        
        elif opcion == 1:  # Resumen por categoría
            print("\n--- RESUMEN POR CATEGORÍA ---")
            resumen = resumen_por_categoria(sistema.gastos)
            mostrar_resumen_categoria(resumen)
        
        elif opcion == 2:  # Calendario
            print("\n--- CALENDARIO MENSUAL ---")
            mostrar_calendario(sistema.calendario)
        
        elif opcion == 3:  # Día con mayor gasto
            print("\n--- DÍA CON MAYOR GASTO ---")
            dia, monto = dia_con_mayor_gasto(sistema.calendario)
            if monto > 0:
                print(f"Día {dia}: ${monto:,.2f}")
            else:
                print("No hay gastos registrados.")
        
        elif opcion == 4:  # Por semana
            print("\n--- TOTALES POR SEMANA ---")
            totales = total_por_semana(sistema.calendario)
            for i, total in enumerate(totales, 1):
                print(f"  Semana {i}: ${total:,.2f}")
        
        elif opcion == 5:  # Por día de la semana
            print("\n--- TOTALES POR DÍA DE LA SEMANA ---")
            dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            totales = total_por_dia_semana(sistema.calendario)
            for dia, total in zip(dias_semana, totales):
                print(f"  {dia:<10}: ${total:,.2f}")
        
        elif opcion == 6:  # Análisis de categorías
            print("\n--- ANÁLISIS DE CATEGORÍAS ---")
            faltantes = categorias_faltantes(sistema.categorias_usadas)
            porcentaje = porcentaje_cobertura(sistema.categorias_usadas)
            mostrar_analisis_categorias(sistema.categorias_usadas, faltantes, porcentaje)
        
        elif opcion == 7:  # Días sin gastos
            print("\n--- DÍAS SIN MOVIMIENTOS ---")
            dias_vacios = dias_sin_gastos(sistema.calendario, sistema.dias_mes)
            mostrar_dias_sin_movimientos(dias_vacios)
        
        elif opcion == 8:  # Promedio
            print("\n--- PROMEDIO DE GASTOS ---")
            promedio = promedio_gastos(sistema.gastos)
            gastos_activos = len([g for g in sistema.gastos.values() if g.get('estado') == 'activo'])
            print(f"  Promedio: ${promedio:,.2f}")
            print(f"  Total de gastos activos: {gastos_activos}")


def menu_herramientas(sistema):
    """Menú recursivo para herramientas avanzadas."""
    while True:
        mostrar_submenu_herramientas()
        opcion = pedir_opcion_numerica()
        
        if opcion == 0:
            return
        
        elif opcion == 1:  # IVA
            print("\n--- CÁLCULO DE IVA (21%) ---")
            gastos_con_iva = obtener_montos_con_iva(sistema.gastos)
            if gastos_con_iva:
                mostrar_iva_gastos(gastos_con_iva)
            else:
                print(" No hay gastos registrados.")
        
        elif opcion == 2:  # Filtrar importantes
            print("\n--- FILTRAR GASTOS IMPORTANTES ---")
            umbral = pedir_monto()
            importantes = gastos_importantes(sistema.gastos, umbral)
            if importantes:
                mostrar_lista(importantes)
            else:
                print(f" No hay gastos mayores a ${umbral:,.2f}")
        
        elif opcion == 3:  # Total general
            print("\n--- TOTAL GENERAL ---")
            total = total_montos(sistema.gastos)
            gastos_activos = len([g for g in sistema.gastos.values() if g.get('estado') == 'activo'])
            print(f"  Total acumulado: ${total:,.2f}")
            print(f"  Cantidad de gastos: {gastos_activos}")
        
        elif opcion == 4:  # Ver mes
            print("\n--- CONSULTAR MES DE UNA FECHA ---")
            fecha = pedir_fecha()
            mes = obtener_mes(fecha)
            print(f"  Mes: {mes}")
        
        elif opcion == 5:  # Números en descripciones
            print("\n--- NÚMEROS EN DESCRIPCIONES ---")
            numeros = numeros_en_descripciones(sistema.gastos)
            if numeros:
                print(f"\n✓ Se encontraron {len(numeros)} número(s):")
                print("  " + ", ".join(numeros))
            else:
                print("No se encontraron números en las descripciones.")


def menu_recursivo_analisis(sistema):
    """Menú recursivo para análisis recursivo."""
    while True:
        mostrar_submenu_recursivo()
        opcion = pedir_opcion_numerica()
        
        if opcion == 0:
            return
        
        elif opcion == 1:  # Jerarquía
            print("\n--- JERARQUÍA DE CATEGORÍAS ---")
            print("\nEstructura de categorías disponibles:\n")
            mostrar_jerarquia_categorias(CATEGORIAS_JERARQUICAS)
        
        elif opcion == 2:  # Buscar categoría
            print("\n--- BUSCAR CATEGORÍA EN ÁRBOL ---")
            nombre = input("Nombre de categoría: ").strip()
            print()
            if buscar_categoria_recursiva(CATEGORIAS_JERARQUICAS, nombre):
                print(f"\n✓ Categoría '{nombre}' encontrada.")
            else:
                print(f"\n Categoría '{nombre}' no existe.")
        
        elif opcion == 3:  # Reporte jerárquico
            print("\n--- REPORTE JERÁRQUICO DE GASTOS ---")
            print("\nAnálisis por categorías y subcategorías:\n")
            for cat in CATEGORIAS_JERARQUICAS.keys():
                generar_reporte_recursivo(sistema.gastos, CATEGORIAS_JERARQUICAS, cat)
                print()
        
        elif opcion == 4:  # Suma recursiva
            print("\n--- SUMA RECURSIVA DE MONTOS ---")
            gastos_activos = [g for g in sistema.gastos.values() if g.get('estado') == 'activo']
            if gastos_activos:
                lista_montos = [g["monto"] for g in gastos_activos]
                total = sumar_lista_recursiva(lista_montos)
                print(f"  Total recursivo: ${total:,.2f}")
                print(f"   Cantidad de gastos: {len(lista_montos)}")
            else:
                print(" No hay gastos.")
        
        elif opcion == 5:  # Máximo recursivo
            print("\n--- MONTO MÁXIMO (BÚSQUEDA RECURSIVA) ---")
            gastos_activos = [g for g in sistema.gastos.values() if g.get('estado') == 'activo']
            if gastos_activos:
                lista_montos = [g["monto"] for g in gastos_activos]
                maximo = encontrar_maximo_recursivo(lista_montos)
                print(f"  💎 Monto máximo: ${maximo:,.2f}")
                gastos_max = [g for g in gastos_activos if g["monto"] == maximo]
                print(f"\n  Corresponde a {len(gastos_max)} gasto(s):")
                for g in gastos_max:
                    print(f"    • ID {g['id']}: {g['descripcion']} ({g['categoria']})")
            else:
                print("No hay gastos.")


def menu_papelera(sistema):
    """Menú recursivo para papelera."""
    while True:
        mostrar_submenu_papelera()
        opcion = pedir_opcion_numerica()
        
        if opcion == 0:
            return
        
        elif opcion == 1:  # Ver eliminados
            print("\n--- GASTOS ELIMINADOS ---")
            eliminados = obtener_gastos_eliminados(sistema.gastos)
            if eliminados:
                mostrar_lista(list(eliminados.values()), incluir_eliminados=True)
            else:
                print(" La papelera está vacía.")
        
        elif opcion == 2:  # Restaurar
            print("\n--- RESTAURAR GASTO ---")
            gid = pedir_id()
            if restaurar_gasto(sistema.gastos, gid):
                sistema.modificado = True
                print(f"\n✓ Gasto #{gid} restaurado.")
            else:
                print(" ID no encontrado o no está eliminado.")
        
        elif opcion == 3:  # Ver backups
            print("\n--- VER ARCHIVO DE BACKUPS ---")
            print("(Consulte el archivo 'gastos_eliminados.csv')")
        
        elif opcion == 4:  # Limpiar permanentemente
            print("\n--- LIMPIAR PAPELERA ---")
            if confirmar_accion("¿Eliminar permanentemente todos los gastos de la papelera?"):
                eliminados = [k for k, v in sistema.gastos.items() if v.get('estado') == 'eliminado']
                for gid in eliminados:
                    del sistema.gastos[gid]
                sistema.modificado = True
                print(f" {len(eliminados)} gasto(s) eliminado(s) permanentemente.")

def menu_archivos(sistema):
    """Menú recursivo para archivos."""
    while True:
        mostrar_submenu_archivos()
        opcion = pedir_opcion_numerica()
        
        if opcion == 0:
            return
        
        elif opcion == 1:  # Guardar
            guardar_gastos_csv("gastos.csv", sistema.gastos, sistema.orden)
            guardar_calendario("calendario.txt", sistema.calendario, sistema.ultimo_id)
            sistema.modificado = False
        
        elif opcion == 2:  # Cargar
            ok1, g, o, cu, uid = cargar_gastos_csv("gastos.csv")
            ok2, cal, _ = cargar_calendario("calendario.txt", sistema.dias_mes)
            if ok1:
                sistema.gastos = g
                sistema.orden = o
                sistema.categorias_usadas = cu
                sistema.ultimo_id = uid
            if ok2:
                sistema.calendario = cal
        
        elif opcion == 3:  
            print("\n--- LOG DEL SISTEMA ---")
            try:
                import os
                base_dir = os.path.dirname(__file__)
                ruta_log = os.path.join(base_dir, "sistema.log")
                
                with open(ruta_log, "r", encoding="utf-8") as f:
                    lineas = f.readlines()
                    if lineas:
                        print("\nÚltimas 20 entradas del log:\n")
                        for linea in lineas[-20:]:
                            print(linea.strip())
                    else:
                        print("El archivo de log está vacío.")
            except FileNotFoundError:
                print("No se encontró el archivo de log.")
                print(f"Ruta buscada: {ruta_log}")
            except Exception as e:
                print(f"Error al leer el log: {e}")

def main():
    sistema = SistemaGastos()
    
    print("\n" + "="*80)
    print(" "*20 + "BIENVENIDO AL GESTOR DE GASTOS PERSONALES")
    print("="*80)
    
    # Cargar datos automáticamente
    ok1, g, o, cu, uid = cargar_gastos_csv("gastos.csv")
    ok2, cal, _ = cargar_calendario("calendario.txt", sistema.dias_mes)
    if ok1:
        sistema.gastos = g
        sistema.orden = o
        sistema.categorias_usadas = cu
        sistema.ultimo_id = uid
    if ok2:
        sistema.calendario = cal
    
    while True:
        mostrar_menu_principal()
        opcion = pedir_opcion_numerica()
        
        if opcion == 1:
            menu_gestion(sistema)
        elif opcion == 2:
            menu_consultas(sistema)
        elif opcion == 3:
            menu_estadisticas(sistema)
        elif opcion == 4:
            menu_herramientas(sistema)
        elif opcion == 5:
            menu_recursivo_analisis(sistema)
        elif opcion == 6:
            menu_papelera(sistema)
        elif opcion == 7:
            menu_archivos(sistema)
        elif opcion == 0:
            if sistema.modificado and not confirmar_accion("¿Salir sin guardar?"):
                continue
            print("\n" + "="*80)
            print(" "*25 + "GRACIAS POR USAR EL SISTEMA")
            print("="*80 + "\n")
            break


if __name__ == "__main__":
    main()