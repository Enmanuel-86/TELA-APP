import sqlite3
from conexiones.respaldo_base import Respaldo
from conexiones.conexion import RUTA_BD
from datetime import datetime
from pathlib import Path
from configuraciones.configuracion import app_configuracion

DIRECTORIO_RESPALDO = app_configuracion.DIRECTORIO_RESPALDO


class RespaldoLocal(Respaldo):
    def __init__(self):
        self.DIRECTORIO_RESPALDO = DIRECTORIO_RESPALDO
    
    def exportar(self):
        self.DIRECTORIO_RESPALDO.mkdir(exist_ok = True)
        fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        ruta_respaldo = self.DIRECTORIO_RESPALDO / f"backup_tela_{fecha_actual}.sql"
        
        conexion = None
        
        try:
            conexion = sqlite3.connect(RUTA_BD)
            
            with open(ruta_respaldo, "w", encoding = "utf-8") as archivo:
                for linea in conexion.iterdump():
                    archivo.write(f"{linea}\n")
            print(f"Respaldo realizado exitosamente en: {ruta_respaldo}")
        except Exception as error:
            print(f"Error al exportar el respaldo: {error}")
        finally:
            if conexion:
                conexion.close()
    
    def limpiar_base_datos(self):
        conexion = None
        cursor = None
        
        try:
            conexion = sqlite3.connect(RUTA_BD)
            cursor = conexion.cursor()
            
            cursor.execute("SELECT type, name FROM sqlite_master WHERE type IN ('table', 'view', 'trigger');")
            objetos = cursor.fetchall()
            
            for objeto in objetos:
                tipo_objeto = objeto[0]
                nombre_objeto = objeto[1]
                
                if nombre_objeto == "sqlite_sequence":
                    continue
                
                if tipo_objeto == "table":
                    cursor.execute(f"DROP TABLE IF EXISTS '{nombre_objeto}';")
                elif tipo_objeto == "view":
                    cursor.execute(f"DROP VIEW IF EXISTS '{nombre_objeto}';")
                elif tipo_objeto == "trigger":
                    cursor.execute(f"DROP TRIGGER IF EXISTS '{nombre_objeto}';")
            
            conexion.commit()
            print("La base de datos fue limpiada exitosamente")
        except Exception as error:
            print(f"Error al limpiar la base de datos: {error}")
            if conexion:
                conexion.rollback()
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
    
    def importar(self, ruta_origen: Path):
        self.limpiar_base_datos()
        
        conexion = None
        cursor = None
        
        try:
            conexion = sqlite3.connect(RUTA_BD)
            cursor = conexion.cursor()

            with open(ruta_origen, "r", encoding = "utf-8") as archivo:
                script_sql = archivo.read()
            cursor.executescript(script_sql)
            conexion.commit()
            print(f"Respaldo importado exitosamente desde {ruta_origen}")
        except Exception as error:
            print(f"Error al importar el respaldo: {error}")
            if conexion:
                conexion.rollback()
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()


if __name__ == "__main__":
    respaldo_bd = RespaldoLocal()
    
    # Para exportar en .sql el respaldo de la base de datos
    #respaldo_bd.exportar()
    
    # Para poder importar el respaldo de la base de datos tenemos que tener la ruta de esta forma envuelta en la función Path
    #ruta_origen = Path("respaldos//backup_tela_2025-07-17_22-18-54.sql")
    
    # Para después pasar la ruta origen del respaldo y así limpiar la base de datos e importar el respaldo
    #respaldo_bd.importar(ruta_origen)