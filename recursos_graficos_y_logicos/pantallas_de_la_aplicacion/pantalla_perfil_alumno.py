from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  QWidget, QDockWidget
from PyQt5 import QtGui
import os
from ..elementos_graficos_a_py import Ui_PantallaInfoCompletaDelAlumno




class PantallaPerfilAlumno(QWidget, Ui_PantallaInfoCompletaDelAlumno):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.setupUi(self)
        
    
        # Ruta relativa de las imagenes ##
        self.boton_de_regreso.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), "..","recursos_de_imagenes", "iconos_de_interfaz","flecha_izquierda_2.png")))
        self.label_imagen_del_alumno.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "..","recursos_de_imagenes", "estudiante_m.png")))
        
        #self.dockWidget_diagnostico.hide()
        
        
        self.lista_labels_mostrar = [self.input_mostrar_cedula_representante, self.input_mostrar_cedula_representante, self.input_mostrar_apellido, self.input_mostrar_nombre, self.input_mostrar_carga_familiar,
                                self.input_mostrar_direccion_residencial, self.input_mostrar_cedula, self.input_mostrar_escolaridad, self.input_mostrar_especialidad, self.input_mostrar_procedencia,
                                self.input_mostrar_primer_nombre, self.input_mostrar_segundo_nombre, self.input_mostrar_apellido_materno, self.input_mostrar_apellido_paterno, self.input_mostrar_estado_civil,
                                self.label_mostrar_estado, self.input_mostrar_tiempo, self.input_mostrar_fecha_ingreso, self.input_mostrar_edad, self.input_mostrar_fecha_nacimiento, self.input_mostrar_lugar_nacimiento, 
                                self.input_mostrar_numero_telefono,  self.input_mostrar_relacion_alumno, self.lista_cuentas_alumno, self.lista_diagnostico_alumno
                                
                                ]
        
        
     
        
        self.boton_de_regreso.clicked.connect(self.volver_vista_general_alumnos)
        
        
        self.dockWidget_diagnostico.hide()
        
    # Metodo para volver a la pantalla anterior
    def volver_vista_general_alumnos(self):
        
        self.stacked_widget.setCurrentIndex(2)
        self.dockWidget_diagnostico.hide()

        
        self.limpiar_inputs(self.lista_labels_mostrar)
    
    
    def mostrar(self, titulo,nombre_diag, fecha_diag, medico, medicacion ,  certificado ,fecha_venc ):
        
        self.dockWidget_diagnostico.setWindowTitle(f"{titulo}: {nombre_diag}")
        self.titulo.setText(titulo)
        self.label_mostrar_diagnostico.setText(nombre_diag)
        self.label_mostrar_fecha_diagnostico.setText(fecha_diag)
        self.label_mostrar_medico_tratante.setText(medico)
        self.label_mostrar_certificado_discap.setText(certificado)
        self.label_mostrar_fecha_venc_certificado.setText(fecha_venc)
        self.label_mostrar_medicacion.setText(medicacion)
        
        self.dockWidget_diagnostico.show()
    
        

    
    # Metodo para limpiar los inputs que usen .clear()
    
    def limpiar_inputs(self, lista_de_inputs):
        
        for qtinput in lista_de_inputs:
            
            qtinput.clear()