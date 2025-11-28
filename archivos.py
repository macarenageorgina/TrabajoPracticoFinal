# ======================================================
# ARCHIVOS.PY - Lectura y escritura de datos
# ======================================================
import os
import csv
from datetime import datetime
from matrices import crear_calendario

# ======================================================
# ARCHIVOS.PY - Lectura y escritura de datos
# ======================================================
import os
import csv
from datetime import datetime
from matrices import crear_calendario

def guardar_gastos_csv(ruta, gastos, orden):
    """
    Guarda gastos en formato CSV (incluyendo estado).
    """
    try:
        base_dir = os.path.dirname(__file__)
        ruta_completa = os.path.join(base_dir, ruta)

        with open(ruta_completa, "w", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            # Encabezado
            writer.writerow(["id", "fecha", "categoria", "descripcion", "monto", "estado"])
            
            # Escribir gastos en orden
            for gid in orden:
                if gid in gastos:
                    g = gastos[gid]
                    writer.writerow([
                        g['id'],
                        g['fecha'],
                        g['categoria'],
                        g['descripcion'],
                        g['monto'],
                        g.get('estado', 'activo')
                    ])
        
        print("Gastos guardados correctamente en CSV.")
        return True
        
    except Exception as e:
        print(f"Error al guardar gastos: {e}")
        return False


def cargar_gastos_csv(ruta):
    """
    Carga gastos desde archivo CSV.
    """
    try:
        base_dir = os.path.dirname(__file__)
        ruta_completa = os.path.join(base_dir, ruta)

        gastos = {}
        orden = []
        categorias_usadas = set()
        ultimo_id = 0
        
        with open(ruta_completa, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                gid = row['id']
                try:
                    monto = float(row['monto'])
                except ValueError:
                    continue
                
                estado = row.get('estado', 'activo')
                
                gastos[gid] = {
                    "id": gid,
                    "fecha": row['fecha'],
                    "monto": monto,
                    "categoria": row['categoria'],
                    "descripcion": row['descripcion'],
                    "estado": estado
                }
                
                orden.append(gid)
                categorias_usadas.add(row['categoria'])
                
                try:
                    ultimo_id = max(ultimo_id, int(gid))
                except ValueError:
                    pass
        
        print("Gastos cargados correctamente desde CSV.")
        return True, gastos, orden, categorias_usadas, ultimo_id
        
    except FileNotFoundError:
        print("Archivo de gastos no encontrado. Se creará uno nuevo al guardar.")
        return False, {}, [], set(), 0
    except Exception as e:
        print(f"Error al cargar gastos: {e}")
        return False, {}, [], set(), 0


def guardar_calendario(ruta, calendario, ultimo_id):
    """
    Guarda el calendario y el último ID usado.
    """
    try:
        base_dir = os.path.dirname(__file__)
        ruta_completa = os.path.join(base_dir, ruta)

        with open(ruta_completa, "w", encoding="utf-8") as f:
            # Guardar ID actual
            f.write(f"ULTIMO_ID={ultimo_id}\n")
            
            # Guardar calendario
            for fila in calendario:
                f.write("CALENDARIO=" + ",".join(str(v) for v in fila) + "\n")
        
        print("Calendario guardado correctamente.")
        return True
        
    except Exception as e:
        print(f"Error al guardar calendario: {e}")
        return False


def cargar_calendario(ruta, dias_mes):
    """
    Carga el calendario desde archivo.
    """
    try:
        base_dir = os.path.dirname(__file__)
        ruta_completa = os.path.join(base_dir, ruta)

        calendario = []
        ultimo_id = 0
        
        with open(ruta_completa, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                
                # Leer ID actual
                if linea.startswith("ULTIMO_ID="):
                    ultimo_id = int(linea.split("=")[1])
                
                # Leer calendario
                elif linea.startswith("CALENDARIO="):
                    fila = [float(v) for v in linea.split("=")[1].split(",")]
                    calendario.append(fila)
        
        print("Calendario cargado correctamente.")
        return True, calendario, ultimo_id
        
    except FileNotFoundError:
        print("Archivo de calendario no encontrado. Se creará uno nuevo.")
        return False, crear_calendario(dias_mes), 0
    except Exception as e:
        print(f"Error al cargar calendario: {e}")
        return False, crear_calendario(dias_mes), 0


def crear_backup_gasto(gasto):
    """
    Crea una copia de seguridad de un gasto antes de eliminarlo.
    """
    try:
        base_dir = os.path.dirname(__file__)
        ruta_backup = os.path.join(base_dir, "gastos_eliminados.csv")
        
        file_exists = os.path.isfile(ruta_backup)
        
        with open(ruta_backup, "a", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            
            # Escribir encabezado solo si el archivo es nuevo
            if not file_exists:
                writer.writerow([
                    "id", "fecha", "categoria", "descripcion", 
                    "monto", "fecha_eliminacion", "estado_original"
                ])
            
            # Escribir gasto eliminado
            writer.writerow([
                gasto['id'],
                gasto['fecha'],
                gasto['categoria'],
                gasto['descripcion'],
                gasto['monto'],
                datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                gasto.get('estado', 'activo')
            ])
        
        return True
        
    except Exception as e:
        print(f"Error al crear backup: {e}")
        return False


def registrar_log(mensaje, tipo="INFO"):
    """
    Registra eventos en un archivo de log.
    """
    try:
        base_dir = os.path.dirname(__file__)
        ruta_log = os.path.join(base_dir, "sistema.log")
        
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        with open(ruta_log, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [{tipo}] {mensaje}\n")
        
        return True
        
    except Exception as e:
        print(f"⚠️ Error al escribir log: {e}")
        return False