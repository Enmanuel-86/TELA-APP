from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  QWidget
from PyQt5 import QtGui
import os

from ..elementos_graficos_a_py import Ui_PantallaDeOpciones




class PantallaDeOpciones(QWidget, Ui_PantallaDeOpciones):
    def __init__(self, stacked_widget):
        super().__init__()


        self.stacked_widget = stacked_widget
        
        self.setupUi(self)
        
        


        ## rutas relativas de las imagenes ##
        self.imagen_personal.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "foto_personal.png")))
        self.imagen_alumno.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "foto_alumnos.png")))
        self.boton_de_regreso.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "flecha_izquierda_2.png")))


        self.boton_opcion_personal.clicked.connect(self.ir_a_vista_general_del_personal)
        self.boton_opcion_alumno.clicked.connect(self.ir_a_vista_general_de_alumnos)
        self.boton_de_regreso.clicked.connect(self.volver_al_login)
        
        
        

    def ir_a_vista_general_del_personal(self):

        
        #pantalla_vista_personal = self.stacked_widget.widget(2)
        #pantalla_vista_personal.boton_de_opciones.setCurrentIndex(1)

        self.stacked_widget.setCurrentIndex(2)
        
    def ir_a_vista_general_de_alumnos(self):

        self.stacked_widget.setCurrentIndex(5)
        

        


    def volver_al_login(self):
        self.stacked_widget.setCurrentIndex(0)
        
