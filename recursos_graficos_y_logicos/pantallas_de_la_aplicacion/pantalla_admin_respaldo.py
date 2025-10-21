from PyQt5.QtGui import QIcon,  QDesktopServices
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import  QWidget, QFileDialog, QMessageBox, QApplication
from PyQt5 import QtGui
import os
import platform
from ..elementos_graficos_a_py import Ui_PantallaCrearRespaldo

from conexiones.respaldo import RespaldoLocal

respaldo_bd = RespaldoLocal()


class PantallaAdminCrearRespaldo(QWidget, Ui_PantallaCrearRespaldo):
    def __init__(self, stacked_widget):
        super().__init__()
        
        self.stacked_widget = stacked_widget
        self.setupUi(self)
        
        #Rutas de las imagenes
        self.boton_exportar.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz","exportar.png")))
        self.boton_importar.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz","importar.png")))
        self.boton_respaldo_correo.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz","mail.png")))
        self.boton_ruta_importar.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz","base_de_datos.png")))
        
        self.ruta = None 
        
        self.boton_exportar.clicked.connect(self.exportar_datos)
        self.boton_ruta_importar.clicked.connect(self.seleccionar_archivo_db_importar_datos)
        self.boton_importar.clicked.connect(self.importar_archivo_sql)
        
    

    
    def exportar_datos(self):
        QApplication.beep()
        
        try:
            
            from configuraciones.configuracion import app_configuracion
            carpeta_respaldos = str(app_configuracion.DIRECTORIO_RESPALDO)
            
            QMessageBox.information(self, "Éxito", f"Respaldo guardado en:\n{carpeta_respaldos}")
            
            
            # 1. Exportar la base de datos (esto debería guardar en TELAAPPBackups)
            respaldo_bd.exportar()  # Asegúrate de que RespaldoLocal use app_configuracion.DIRECTORIO_RESPALDO
            
            # 2. Obtener la ruta de la carpeta de respaldos desde Configuracion
            
            
            # 3. Verificar que existe
            if not os.path.exists(carpeta_respaldos):
                QMessageBox.warning(self, "Error", f"No se encontró la carpeta:\n{carpeta_respaldos}")
                return
            
            # 4. Abrir la carpeta
            if platform.system() == "Windows":
                os.startfile(carpeta_respaldos)
            elif platform.system() == "Darwin":  # macOS
                os.system(f'open "{carpeta_respaldos}"')
            else:  # Linux
                os.system(f'xdg-open "{carpeta_respaldos}"')
                
            
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar:\n{str(e)}")
    
    # Metodo para seleccionar la ruta para importar los datos
    def seleccionar_archivo_db_importar_datos(self):
        # Abrir el diálogo para seleccionar archivo con filtro para .db
        self.ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Archivo de SQL",
            "",  # Directorio inicial (vacío para el predeterminado)
            "Archivos sql (*.sql);;Todos los archivos (*)"
        )
        
        if self.ruta:  # Si se seleccionó una ruta (no se canceló el diálogo)
            self.label_importar_datos.setText(f"{self.ruta}")
            
    
    # Metodo para importar los datos        
    
    def importar_archivo_sql(self):
        
        if self.ruta:
            
            QMessageBox.information(self, "Importación de datos exitosa", "La base de datos a sido actualizada con la importación nueva de datos")
            respaldo_bd.importar(self.ruta)
            
            
            
        else:
            
            QMessageBox.warning(self, "Archivo no seleccionado", "Por favor seleccione el archivo .sql para importar los datos")
            
            return

    
    
    
            