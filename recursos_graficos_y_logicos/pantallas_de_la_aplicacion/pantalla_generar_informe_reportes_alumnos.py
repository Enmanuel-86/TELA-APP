from PySide2.QtGui import QIcon
from PySide2.QtWidgets import  QWidget
#from PySide2 import QtGui, Qt
import os
from ..elementos_graficos_a_py import Ui_PantallaGenerarInformesReportesAlumnos




class PantallaGenerarInformesReportesAlumnos(QWidget, Ui_PantallaGenerarInformesReportesAlumnos):
    def __init__(self, stacked_widget):
        super().__init__()
        
        self.stacked_widget = stacked_widget
        self.setupUi(self)
        
        # Rutas relativas
        self.boton_de_regreso.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), "..","recursos_de_imagenes", "iconos_de_interfaz","flecha_izquierda_2.png")))
        