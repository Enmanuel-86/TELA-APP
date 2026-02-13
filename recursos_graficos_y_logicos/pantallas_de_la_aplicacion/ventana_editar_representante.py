from PyQt5.QtWidgets import (QWidget, QMessageBox, QApplication, QListWidget, QListWidgetItem, 
                            QLabel, QHBoxLayout, QPushButton, QHeaderView )
from PyQt5.QtCore import (QTime, QPoint, Qt, QDate, QSize)
from PyQt5 import QtGui, QtCore
import os
from ..elementos_graficos_a_py import  Ui_VentanaEditarRepresentante
from ..utilidades.funciones_sistema import FuncionSistema
from ..utilidades.base_de_datos import (permiso_servicio, representante_servicio)


class VentanaEditarRepresentante(QWidget, Ui_VentanaEditarRepresentante):
    def __init__(self):
        super().__init__()
        
        self.setupUi(self)
        
        # Variable para guardar el id del representante temporalmente
        self.representante_id = None
        
        self.filtrar_por_ente_seleccionado = None
        
        self.msg_box = QMessageBox(self)
        # Crear botones personalizados
        self.boton_si = self.msg_box.addButton("Sí", QMessageBox.YesRole)
        self.boton_no = self.msg_box.addButton("No", QMessageBox.NoRole)
        
        # Tupla para agrupar los campos para deshabilitarlo o limpiarlos
        self.tupla_de_campos = (self.input_mostrar_nombre, self.input_mostrar_apellido, self.input_mostrar_carga_familiar,
                                self.input_mostrar_direccion_residencial, self.input_mostrar_cedula_representante, self.input_mostrar_estado_civil,
                                self.input_mostrar_numero_telefono, self.input_mostrar_numero_telefono_adicional)
        
        self.boton_editar.clicked.connect(self.editar_informacion_representante)
        self.boton_cancelar.clicked.connect(self.cancelar_edicion_de_datos_representante)
        
    def mostrar_informacion_representante(self, datos_representante):
        """
            Este metodo sirve para darle la informacion del representante a los campos que se usaran para editar:
            
            1. Tomamos los datos a partir de una lista (en este caso la lista de representantes)
            2. Le asignamos a cada campo el dato en su respectivo lugar
            3. Y el usuario se encargara editar o no la informacion
        
        """
        try:
            self.representante_id = datos_representante[0]
            self.input_mostrar_nombre.setText(datos_representante[2])
            self.input_mostrar_apellido.setText(datos_representante[3])   
            #self.input_mostrar_relacion_alumno.setText(info_inscripcion[10])
            self.input_mostrar_cedula_representante.setText(datos_representante[1])
            
            self.input_mostrar_direccion_residencial.setText(datos_representante[4])
            self.input_mostrar_numero_telefono.setText(datos_representante[5])
            
            if datos_representante[6] == None:
                self.input_mostrar_numero_telefono_adicional.setText("")
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
            
            
    def editar_informacion_representante(self):
        """
            Este metodo sirve para editar la informacion del representante de la siguiente manera:
            
            1. Le preguntamos al usuario si quiere realizar el proceso de editar
            2. Tomamos los datos editados o no
            3. Los agrupamos en un diccionario
            4. Comprobamos si no hay errores
            5. Editamos la informacion
            6. Le indicamos al usuario que la informacion se edito correctamente
        """
        
        self.msg_box.setWindowTitle("Advertencia")
        self.msg_box.setIcon(QMessageBox.Warning)
        self.msg_box.setText(f"¿Seguro que quiere editar la información de {self.input_mostrar_nombre.text()} {self.input_mostrar_apellido.text()}? ")
        QApplication.beep()
        
        # Mostrar el cuadro de diálogo y esperar respuesta
        self.msg_box.exec_()
        
        # si le da a SI, verificamos primero
        if self.msg_box.clickedButton() == self.boton_si:

            try: 
                cedula = self.input_mostrar_cedula_representante.text().strip()
                nombre = self.input_mostrar_nombre.text().strip().capitalize()
                apellido = self.input_mostrar_apellido.text().strip().capitalize()
                direccion_residencia = self.input_mostrar_direccion_residencial.text().strip()
                num_telefono = self.input_mostrar_numero_telefono.text().strip()
                num_telefono_adicional = self.input_mostrar_numero_telefono_adicional.text() if not self.input_mostrar_numero_telefono_adicional.text() == "" else None 
                carga_familiar = int(self.input_mostrar_carga_familiar.text())
                estado_civil = self.input_mostrar_estado_civil.text().strip().capitalize()
                
                campos_representante = {
                "cedula": cedula,
                "nombre": nombre,
                "apellido": apellido,
                "direccion_residencia": direccion_residencia,
                "num_telefono": num_telefono,
                "num_telefono_adicional": num_telefono_adicional,
                "carga_familiar": carga_familiar,
                "estado_civil": estado_civil
                }
                
                errores_totales = representante_servicio.validar_campos_representante(
                campos_representante.get("cedula"),
                campos_representante.get("nombre"),
                campos_representante.get("apellido"),
                campos_representante.get("direccion_residencia"),
                campos_representante.get("num_telefono"),
                campos_representante.get("num_telefono_adicional"),
                campos_representante.get("carga_familiar"),
                campos_representante.get("estado_civil")
                )
            
                if errores_totales:
                    FuncionSistema.mostrar_errores_verificados(self, errores_totales, "Editar representante")
                    return
                
                else:
                    representante_servicio.actualizar_representante(self.representante_id, campos_representante)
                    print("Actualizacion de datos del representante exitoso.")
                    QMessageBox.information(self, "Proceso exitoso", "Se a editado correctamente la información del representante")
                
                    self.representante_id = None
                    FuncionSistema.limpiar_inputs_de_qt(self.tupla_de_campos)
                    self.filtrar_por_ente_seleccionado()
                    
                    
                    self.close()
                    
            except Exception as e:
                print(f"No se puedo editar la informacion del representante: {e}")
            
            
    def cancelar_edicion_de_datos_representante(self):
        """
            Este metodo sirve para cancelar la edicion de los datos del representante
        
        """       
        self.msg_box.setWindowTitle("Advertencia")
        self.msg_box.setIcon(QMessageBox.Warning)
        self.msg_box.setText(f"¿Seguro que quiere cancelar la edición de la información de {self.input_mostrar_nombre.text()} {self.input_mostrar_apellido.text()}? ")
        QApplication.beep()
        
        # Mostrar el cuadro de diálogo y esperar respuesta
        self.msg_box.exec_()
        
        # si le da a SI, verificamos primero
        if self.msg_box.clickedButton() == self.boton_si:
            
            self.representante_id = None
            FuncionSistema.limpiar_inputs_de_qt(self.tupla_de_campos)
            self.close()