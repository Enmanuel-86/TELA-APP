from PyQt5.QtWidgets import (QWidget, QMessageBox, QApplication, QListWidget, QListWidgetItem, 
                            QLabel, QHBoxLayout, QPushButton, QHeaderView )
from PyQt5.QtCore import (QTime, QPoint, Qt, QDate, QSize)
from PyQt5 import QtGui, QtCore
import os
from ..elementos_graficos_a_py import  Ui_VentanaEditarRepresentante
from ..utilidades.funciones_sistema import FuncionSistema


class VentanaEditarRepresentante(QWidget, Ui_VentanaEditarRepresentante):
    def __init__(self):
        super().__init__()
        
        self.setupUi(self)
        
         
    def mostrar_informacion_representante(self, datos_representante):
        """
            Este metodo sirve para darle la informacion del representante a los campos que se usaran para editar:
            
            - Tomamos los datos a partir de una lista (en este caso la lista de representantes)
            - Le asignamos a cada campo el dato en su respectivo lugar
            - Y el usuario se encargara editar o no la informacion
        
        """
        try:
        
            
            self.input_mostrar_nombre.setText(datos_representante[2])
            self.input_mostrar_apellido.setText(datos_representante[3])   
            #self.input_mostrar_relacion_alumno.setText(info_inscripcion[10])
            self.input_mostrar_cedula_representante.setText(datos_representante[1])
            
            self.input_mostrar_direccion_residencial.setText(datos_representante[4])
            self.input_mostrar_numero_telefono.setText(datos_representante[5])
            
            if datos_representante[6] == None:
                self.input_mostrar_numero_telefono_adicional.setText("No tiene")
            else:
                self.input_mostrar_numero_telefono_adicional.setText(str(datos_representante[6]))
            
            self.input_mostrar_carga_familiar.setText(str(datos_representante[7]))   
            self.input_mostrar_estado_civil.setText(datos_representante[8])
            
            
            if datos_representante[9] == None:
                self.label_foto_representante.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "..", "recursos_de_imagenes", "iconos_de_interfaz","padres.png")))
            else:
                FuncionSistema.cargar_foto_perfil_en_la_interfaz(datos_representante[9], self.label_foto_representante)
            
            
            
        except Exception as e:
            print(f"No se puedo mostrar la informacion del representante: {e}")
            FuncionSistema.mostrar_errores_por_excepcion(e, "mostrar_informacion_representante")
            
        else:
            print("La informacion del representante a cargado correctamente")