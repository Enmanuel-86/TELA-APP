from PySide2.QtGui import QIcon
from PySide2.QtWidgets import  QWidget, QLineEdit
from PySide2 import QtGui
import os
from ..elementos_graficos_a_py import Ui_PantallaInfoCompletaDelEmpleado




class PantallaPerfilEmpleado(QWidget, Ui_PantallaInfoCompletaDelEmpleado):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.setupUi(self)
        
        # Ruta relativa de las imagenes ##
        self.boton_de_regreso.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), "..","recursos_de_imagenes", "iconos_de_interfaz","flecha_izquierda_2.png")))
        self.label_imagen_del_personal.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "..","recursos_de_imagenes", "imagen_personal_m.png")))

        self.imagen_personal_f = os.path.join(os.path.dirname(__file__), "..","recursos_de_imagenes", "imagen_personal_f.png")
        
        
        
        self.espacio_scroll_mostrar_datos_obtenidos.setWidgetResizable(True)
        
        self.boton_de_regreso.clicked.connect(self.volver_vista_general_empleados)
        
    
    
        
        
        
        
    def volver_vista_general_empleados(self):
        
        self.stacked_widget.setCurrentIndex(7)
        
        self.espacio_scroll_mostrar_datos_obtenidos.verticalScrollBar().setValue(0)

        self.mostrar_enfermedades.clear()
        self.mostrar_diagnosticos.clear()
        
        self.deshabilitar_inputs()
        
        
    def deshabilitar_inputs(self):
        
        for child in self.findChildren(QLineEdit):
            if not child.isReadOnly():
                child.setReadOnly(True)