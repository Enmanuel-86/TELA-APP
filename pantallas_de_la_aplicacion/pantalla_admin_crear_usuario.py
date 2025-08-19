from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  QWidget
from PyQt5 import QtGui
import os
from elementos_graficos_a_py import Ui_CrearNuevoUsuario


class PantallaAdminCrearUsuario(QWidget, Ui_CrearNuevoUsuario):
    def __init__(self, stacked_widget):
        super().__init__()
        
        self.stacked_widget = stacked_widget
        self.setupUi(self)
        
        #Rutas de las imagenes
        self.boton_de_regreso.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz","flecha_izquierda_2.png")))
        self.icono_usuario.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "icono_de_usuario.png")))
        self.icono_usuario_2.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "icono_de_usuario.png")))
        self.icono_contrasena.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "icono_contraseña.png")))
        
        self.boton_de_regreso.clicked.connect(self.volver_atras)
        
        
    def volver_atras(self):
        self.stacked_widget.setCurrentIndex(7)