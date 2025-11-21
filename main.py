34# ======================================================
# MAIN.PY - Programa principal
# ======================================================
# Trabajo Práctico Integrador - Algoritmos y Estructuras de Datos I
# UADE - Prof. David Yaps
# ======================================================

from matrices import crear_calendario, dia_con_mayor_gasto, total_por_semana, total_por_dia_semana, dias_sin_gastos
from operaciones import (
    agregar_gasto, editar_gasto, eliminar_gasto,
    filtrar_por_categoria, filtrar_por_fecha, filtrar_por_monto_mayor,
    buscar_gastos_por_palabra, ids_por_categoria, ids_por_monto_mayor,
    gastos_por_ids, categorias_faltantes, porcentaje_cobertura,
    resumen_por_categoria, gastos_ordenados_por_monto,
    obtener_montos_con_descuento, gastos_importantes, total_montos,
    promedio_gastos, numeros_en_descripciones, obtener_mes, filtrar_rango_fechas,
    gastos_ordenados_por_monto
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
from archivos import guardar_en_archivo, cargar_desde_archivo
from presentacion import (
    mostrar_menu, mostrar_lista, mostrar_calendario,
    mostrar_resumen_categoria, mostrar_analisis_categorias,
    mostrar_dias_sin_movimientos, confirmar_accion
)


def main():
    """
    Función principal del sistema de gestión de gastos.
    Maneja el menú y coordina todas las operaciones.
    """
    dias_mes = 30
    gastos = {}
    orden = []
    categorias_usadas = set()
    calendario = crear_calendario(dias_mes)
    ultimo_id = 0
    
    print("\n" + "="*80)
    print(" "*20 + "BIENVENIDO AL GESTOR DE GASTOS PERSONALES")
    print("="*80)
    
    salir = False
    while not salir:
        mostrar_menu()
        opcion = pedir_opcion_numerica()
        
        # ======================================================
        # GESTIÓN DE GASTOS
        # ======================================================
        
        if opcion == 1:  # Agregar gasto
            print("\n--- AGREGAR NUEVO GASTO ---")
            fecha = pedir_fecha()
            monto = pedir_monto()
            categoria = pedir_categoria()
            descripcion = pedir_descripcion()
            
            ultimo_id = agregar_gasto(
                gastos, orden, categorias_usadas,
                calendario, ultimo_id,
                fecha, monto, categoria, descripcion
            )
            print(f"Gasto #{ultimo_id} agregado correctamente.")
        
        elif opcion == 2:  # Editar gasto
            print("\n--- EDITAR GASTO ---")
            gid = pedir_id()
            if gid not in gastos:
                print("ID no encontrado.")
            else:
                print(f"Gasto actual: {gastos[gid]}")
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
                
                if editar_gasto(gastos, calendario, gid, nuevo_monto, nueva_desc):
                    print("Gasto modificado correctamente.")
                else:
                    print("Error al modificar gasto.")
        
        elif opcion == 3:  # Eliminar gasto
            print("\n--- ELIMINAR GASTO ---")
            gid = pedir_id()
            if confirmar_accion(f"¿Confirma eliminar gasto #{gid}?"):
                if eliminar_gasto(gastos, orden, gid):
                    print("Gasto eliminado correctamente.")
                else:
                    print("ID no encontrado.")
        
        # ======================================================
        # CONSULTAS Y FILTROS
        # ======================================================
        
        elif opcion == 4:
            print("\n--- TODOS LOS GASTOS ---")
            mostrar_lista(list(gastos.values()))
        
        elif opcion == 5:
            print("\n--- ÚLTIMOS 5 GASTOS ---")
            ultimos = orden[-5:]
            mostrar_lista([gastos[g] for g in ultimos if g in gastos])
        
        elif opcion == 6:
            print("\n--- PRIMEROS 5 GASTOS ---")
            primeros = orden[:5]
            mostrar_lista([gastos[g] for g in primeros if g in gastos])
        
        elif opcion == 7:
            print("\n--- GASTOS RECIENTES (últimos 10) ---")
            recientes = orden[-10:]
            mostrar_lista([gastos[g] for g in recientes if g in gastos])
        
        elif opcion == 8:
            print("\n--- FILTRAR POR CATEGORÍA ---")
            categoria = pedir_categoria()
            mostrar_lista(filtrar_por_categoria(gastos, categoria))
        
        elif opcion == 9:
            print("\n--- FILTRAR POR FECHA ---")
            fecha = pedir_fecha()
            mostrar_lista(filtrar_por_fecha(gastos, fecha))
        
        elif opcion == 10:
            print("\n--- FILTRAR POR MONTO MÍNIMO ---")
            umbral = pedir_monto()
            mostrar_lista(filtrar_por_monto_mayor(gastos, umbral))
        
        elif opcion == 11:
            print("\n--- BUSCAR EN DESCRIPCIONES ---")
            palabra = pedir_palabra()
            resultados = buscar_gastos_por_palabra(gastos, palabra)
            if resultados:
                mostrar_lista(resultados)
            else:
                print(f"No se encontraron gastos con '{palabra}'.")
        
        elif opcion == 12:
            print("\n--- BÚSQUEDA AVANZADA (Categoría + Monto) ---")
            categoria = pedir_categoria()
            umbral = pedir_monto()
            
            ids_cat = ids_por_categoria(gastos, categoria)
            ids_monto = ids_por_monto_mayor(gastos, umbral)
            ids_comunes = ids_cat & ids_monto
            
            if ids_comunes:
                print(f"\nEncontrados {len(ids_comunes)} gastos que cumplen ambas condiciones:")
                mostrar_lista(gastos_por_ids(gastos, ids_comunes))
            else:
                print("No hay gastos que cumplan ambas condiciones.")
        
        elif opcion == 13:
            print("\n--- FILTRAR POR RANGO DE FECHAS ---")
            fecha_desde = pedir_fecha()
            fecha_hasta = pedir_fecha()
            mostrar_lista(filtrar_rango_fechas(gastos, fecha_desde, fecha_hasta))
        
        elif opcion == 14:
            print("\n--- GASTOS ORDENADOS POR MONTO ---")
            mostrar_lista(gastos_ordenados_por_monto(gastos))
        
        # ======================================================
        # ESTADÍSTICAS Y REPORTES
        # ======================================================
        
        elif opcion == 15:
            print("\n--- RESUMEN POR CATEGORÍA ---")
            resumen = resumen_por_categoria(gastos)
            mostrar_resumen_categoria(resumen)
        
        elif opcion == 16:
            print("\n--- CALENDARIO MENSUAL ---")
            mostrar_calendario(calendario)
        
        elif opcion == 17:
            print("\n--- DÍA CON MAYOR GASTO ---")
            dia, monto = dia_con_mayor_gasto(calendario)
            if monto > 0:
                print(f"Día {dia}: ${monto:,.2f}")
            else:
                print("No hay gastos registrados.")
        
        elif opcion == 18:
            print("\n--- TOTALES POR SEMANA ---")
            totales = total_por_semana(calendario)
            for i, total in enumerate(totales, 1):
                print(f"Semana {i}: ${total:,.2f}")
        
        elif opcion == 19:
            print("\n--- TOTALES POR DÍA DE LA SEMANA ---")
            dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            totales = total_por_dia_semana(calendario)
            for dia, total in zip(dias_semana, totales):
                print(f"{dia:<10}: ${total:,.2f}")
        
        elif opcion == 20:
            print("\n--- ANÁLISIS DE CATEGORÍAS ---")
            faltantes = categorias_faltantes(categorias_usadas)
            porcentaje = porcentaje_cobertura(categorias_usadas)
            mostrar_analisis_categorias(categorias_usadas, faltantes, porcentaje)
        
        elif opcion == 21:
            print("\n--- ANÁLISIS DE MOVIMIENTOS ---")
            dias_vacios = dias_sin_gastos(calendario, dias_mes)
            mostrar_dias_sin_movimientos(dias_vacios)
        
        elif opcion == 22:
            print("\n--- PROMEDIO DE GASTOS ---")
            promedio = promedio_gastos(gastos)
            print(f"Promedio: ${promedio:,.2f}")
            print(f"Total de gastos: {len(gastos)}")
        
        # ======================================================
        # HERRAMIENTAS AVANZADAS
        # ======================================================
        
        elif opcion == 23:
            print("\n--- SIMULACIÓN DE DESCUENTOS ---")
            print("(Aplica 5% de descuento a gastos mayores a $10,000)")
            montos_desc = obtener_montos_con_descuento(gastos)
            if montos_desc:
                print("\nMontos con descuento aplicado:")
                for i, (original, descontado) in enumerate(zip(
                    [g["monto"] for g in gastos.values()], montos_desc
                ), 1):
                    ahorro = original - descontado
                    if ahorro > 0:
                        print(f"  {i}. ${original:,.2f} → ${descontado:,.2f} (ahorro: ${ahorro:,.2f})")
                    else:
                        print(f"  {i}. ${original:,.2f} (sin descuento)")
            else:
                print("No hay gastos registrados.")
        
        elif opcion == 24:
            print("\n--- GASTOS IMPORTANTES ---")
            umbral = pedir_monto()
            importantes = gastos_importantes(gastos, umbral)
            if importantes:
                print(f"\n{len(importantes)} gasto(s) encontrado(s):")
                mostrar_lista(importantes)
            else:
                print(f"No hay gastos mayores a ${umbral:,.2f}")
        
        elif opcion == 25:
            print("\n--- TOTAL GENERAL ---")
            total = total_montos(gastos)
            print(f"Total acumulado: ${total:,.2f}")
            print(f"Cantidad de gastos: {len(gastos)}")
        
        elif opcion == 26:
            print("\n--- CONSULTAR MES DE UNA FECHA ---")
            fecha = pedir_fecha()
            mes = obtener_mes(fecha)
            print(f"Mes: {mes}")
        
        elif opcion == 27:
            print("\n--- ANÁLISIS DE DESCRIPCIONES ---")
            numeros = numeros_en_descripciones(gastos)
            if numeros:
                print(f"Se encontraron {len(numeros)} número(s) en las descripciones:")
                print("  " + ", ".join(numeros))
            else:
                print("No se encontraron números en las descripciones.")
    

         
        # ======================================================
        # ANÁLISIS RECURSIVO
        # ======================================================
        
        elif opcion == 28:
            print("\n--- JERARQUÍA DE CATEGORÍAS ---")
            print("\nEstructura de categorías disponibles:\n")
            mostrar_jerarquia_categorias(CATEGORIAS_JERARQUICAS)
        
        elif opcion == 29:
            print("\n--- BUSCAR CATEGORÍA EN ÁRBOL ---")
            nombre = input("Nombre de categoría a buscar: ").strip()
            print()
            if buscar_categoria_recursiva(CATEGORIAS_JERARQUICAS, nombre):
                print(f"\nCategoría '{nombre}' encontrada en el sistema.")
            else:
                print(f"\nCategoría '{nombre}' no existe.")
        
        elif opcion == 30:
            print("\n--- REPORTE JERÁRQUICO DE GASTOS ---")
            print("\nAnálisis por categorías y subcategorías:\n")
            for categoria_principal in CATEGORIAS_JERARQUICAS.keys():
                generar_reporte_recursivo(gastos, CATEGORIAS_JERARQUICAS, categoria_principal)
                print()
        
        elif opcion == 31:
            print("\n--- SUMA RECURSIVA DE MONTOS ---")
            if not gastos:
                print("No hay gastos registrados.")
            else:
                lista_montos = [g["monto"] for g in gastos.values()]
                total_recursivo = sumar_lista_recursiva(lista_montos)
                print(f"Total calculado recursivamente: ${total_recursivo:,.2f}")
                print(f"Cantidad de gastos: {len(lista_montos)}")
        
        elif opcion == 32:
            print("\n--- MONTO MÁXIMO (BÚSQUEDA RECURSIVA) ---")
            if not gastos:
                print("No hay gastos registrados.")
            else:
                lista_montos = [g["monto"] for g in gastos.values()]
                maximo = encontrar_maximo_recursivo(lista_montos)
                print(f"Monto máximo encontrado: ${maximo:,.2f}")
                gastos_max = [g for g in gastos.values() if g["monto"] == maximo]
                print(f"Corresponde a {len(gastos_max)} gasto(s):")
                for g in gastos_max:
                    print(f"  ID {g['id']}: {g['descripcion']} ({g['categoria']})")
        


        # ======================================================
        # ARCHIVOS
        # ======================================================
        
        elif opcion == 33:
            print("\n--- GUARDAR DATOS ---")
            ruta = input("Nombre de archivo (Enter = datos.txt): ").strip()
            if not ruta:
                ruta = "datos.txt"
            guardar_en_archivo(ruta, gastos, orden, categorias_usadas, calendario, ultimo_id)
        
        elif opcion == 34:
            print("\n--- CARGAR DATOS ---")
            ruta = input("Nombre de archivo (Enter = datos.txt): ").strip()
            if not ruta:
                ruta = "datos.txt"
            ok, g, o, cu, cal, uid = cargar_desde_archivo(ruta, dias_mes)
            if ok:
                gastos = g
                orden = o
                categorias_usadas = cu
                calendario = cal
                ultimo_id = uid
        
        # ======================================================
        # SALIDA
        # ======================================================
        
        elif opcion == 35:
            if len(gastos) > 0 and not confirmar_accion("¿Desea salir sin guardar?"):
                continue
            print("\n" + "="*80)
            print(" "*25 + "GRACIAS POR USAR EL SISTEMA")
            print("="*80 + "\n")
            salir = True

        else:
            print("\nOpción inválida. Por favor elija un número del 1 al 35.")


if __name__ == "__main__":
    main()
