from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  QWidget
from PyQt5 import QtGui
import os
from elementos_graficos_a_py import Ui_PantallaDeOpcionesAdmin


class PantallaAdminOpciones(QWidget, Ui_PantallaDeOpcionesAdmin):
    def __init__(self, stacked_widget):
        super().__init__()
        
        self.stacked_widget = stacked_widget
        self.setupUi(self)

        ## rutas relativas de las imagenes ##
        self.boton_de_regreso.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz","flecha_izquierda_2.png")))
        self.imagen_personal.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "foto_personal.png")))
        self.imagen_alumno.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "foto_alumnos.png")))
        self.imagen_crear_usuario.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz","agregar-usuario.png")))
        self.imagen_respaldo.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "respaldo.png")))



        # Conexion de metodos a los botones
        self.boton_de_regreso.clicked.connect(self.volver_al_login)
        self.boton_opcion_personal.clicked.connect(self.ir_vista_general_personal)
        self.boton_opcion_alumno.clicked.connect(self.ir_vista_general_alumnos)
        self.boton_crear_usuario.clicked.connect(self.ir_crear_nuevo_usuario)
        self.boton_importar_exportar.clicked.connect(self.ir_crear_respaldo)
        
    
    

    def ir_vista_general_personal(self):
        
        self.stacked_widget.setCurrentIndex(2)

        
    def ir_vista_general_alumnos(self):

        self.stacked_widget.setCurrentIndex(5)
        
    
    def ir_crear_nuevo_usuario(self):
        
        self.stacked_widget.setCurrentIndex(8)
     
    def ir_crear_respaldo(self):
        
        self.stacked_widget.setCurrentIndex(9)


    def volver_al_login(self):
        
        
        self.stacked_widget.setCurrentIndex(0)
        
            
            
