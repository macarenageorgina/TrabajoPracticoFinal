# ======================================================
# ARCHIVOS.PY - Lectura y escritura de datos
# ======================================================
import os
from matrices import crear_calendario

def guardar_en_archivo(ruta, gastos, orden, categorias_usadas, calendario, ultimo_id):
    try:
        base_dir = os.path.dirname(__file__)
        ruta_completa = os.path.join(base_dir, ruta)

        with open(ruta_completa, "w", encoding="utf-8") as f:
            # Guardar ID actual
            f.write(f"ULTIMO_ID={ultimo_id}\n")
            
            # Guardar categorías usadas
            f.write("CATEGORIAS=" + ",".join(sorted(categorias_usadas)) + "\n")
            
            # Guardar calendario
            for fila in calendario:
                f.write("CALENDARIO=" + ",".join(str(v) for v in fila) + "\n")
            
            # Guardar gastos
            for gid in orden:
                g = gastos[gid]
                linea = f"GASTO={g['id']};{g['fecha']};{g['categoria']};{g['descripcion']};{g['monto']}\n"
                f.write(linea)
        
        print("Datos guardados correctamente.")
        return True
        
    except FileNotFoundError:
        print("Error: Ruta de archivo incorrecta.")
        return False
    except PermissionError:
        print("Error: No tiene permiso para escribir en el archivo.")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False


def cargar_desde_archivo(ruta, dias_mes):
    """
    Carga datos del sistema desde un archivo de texto.
    """
    try:
        base_dir = os.path.dirname(__file__)
        ruta_completa = os.path.join(base_dir, ruta)

        with open(ruta_completa, "r", encoding="utf-8") as f:
            gastos = {}
            orden = []
            categorias_usadas = set()
            calendario = []
            ultimo_id = 0
            
            for linea in f:
                linea = linea.strip()
                
                # Leer ID actual
                if linea.startswith("ULTIMO_ID="):
                    ultimo_id = int(linea.split("=")[1])
                
                # Leer categorías
                elif linea.startswith("CATEGORIAS="):
                    texto = linea.split("=")[1]
                    if texto:
                        categorias_usadas = set(texto.split(","))
                
                # Leer calendario
                elif linea.startswith("CALENDARIO="):
                    fila = [float(v) for v in linea.split("=")[1].split(",")]
                    calendario.append(fila)
                
                # Leer gasto individual
                elif linea.startswith("GASTO="):
                    datos = linea.split("=")[1].split(";")
                    if len(datos) != 5:
                        continue
                    
                    gid, fecha, cat, desc, monto_txt = datos
                    try:
                        monto = float(monto_txt)
                    except ValueError:
                        continue
                    
                    gastos[gid] = {
                        "id": gid,
                        "fecha": fecha,
                        "monto": monto,
                        "categoria": cat,
                        "descripcion": desc
                    }
                    orden.append(gid)
                    categorias_usadas.add(cat)
        
        print("Datos cargados correctamente.")
        return True, gastos, orden, categorias_usadas, calendario, ultimo_id
        
    except FileNotFoundError:
        print("Archivo no encontrado. Se creará uno nuevo al guardar.")
        return False, {}, [], set(), crear_calendario(dias_mes), 0
    except PermissionError:
        print("Error: Permiso denegado para leer el archivo.")
        return False, {}, [], set(), crear_calendario(dias_mes), 0
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False, {}, [], set(), crear_calendario(dias_mes), 0
    finally:
        pass
