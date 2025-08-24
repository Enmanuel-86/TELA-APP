from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication
from PyQt5.QtCore import QTime
from PyQt5.QtGui import QIcon
import os
from elementos_graficos_a_py import  Ui_PantallaControlDeLlegada
from datetime import datetime


today = datetime.now()
dia_de_hoy = today.strftime("%Y-%d-%m")

class PantallaControlDeLlegada(QWidget, Ui_PantallaControlDeLlegada):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.setupUi(self)

        self.lista_qlineedits = [self.input_cedula_empleado, self.input_motivo_de_retraso, self.input_motivo_de_inasistencia]
        self.lista_radiobuttons = [self.input_asistente, self.input_inasistente]
        self.lista_timeedits = [self.input_hora_de_llegada, self.input_hora_de_salida]
        
        
        # Ruta relativa de las imagenes ##
        self.boton_de_regreso.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz","flecha_izquierda_2.png")))



        self.msg_box = QMessageBox(self)
        # Crear botones personalizados
        self.boton_si = self.msg_box.addButton("Sí", QMessageBox.YesRole)
        self.boton_no = self.msg_box.addButton("No", QMessageBox.NoRole)


        self.boton_de_regreso.clicked.connect(self.volver)

        self.label_mostrar_fecha.setText(dia_de_hoy)


        #funcion para habilitar los input segun el estado de asistencia

        # si esta asistente:

        self.input_asistente.toggled.connect(self.cuando_asiste_el_personal)
        self.input_inasistente.toggled.connect(self.cuando_no_asiste_el_personal)
        self.boton_de_suministrar.clicked.connect(self.suministrar_info)



    # Metodo para habilitar los inputs si asistio
    def cuando_asiste_el_personal(self, ):
        
        
            self.input_motivo_de_inasistencia.setDisabled(True)
            self.input_motivo_de_inasistencia.clear()

            self.input_hora_de_llegada.setDisabled(False)
            self.input_hora_de_salida.setDisabled(False)
            self.input_motivo_de_retraso.setDisabled(False)
            


    # Metodo para deshabilitar los inputs si no asistio
    def cuando_no_asiste_el_personal(self):
        
        self.input_hora_de_llegada.setDisabled(True)
        self.input_hora_de_llegada.setTime(QTime(7,0))

        self.input_hora_de_salida.setDisabled(True)
        self.input_hora_de_salida.setTime(QTime(12,0))

        self.input_motivo_de_retraso.setDisabled(True)
        self.input_motivo_de_retraso.clear()

        self.input_motivo_de_inasistencia.setDisabled(False)
        self.label_motivo_de_inasistencia.setDisabled(False)


    def volver(self):

        self.msg_box.setWindowTitle("Confirmar salida")
        self.msg_box.setText("¿Seguro que quiere salir sin registrar?")
        self.msg_box.setIcon(QMessageBox.Question)
        QApplication.beep()



        # Mostrar el cuadro de diálogo y esperar respuesta
        self.msg_box.exec_()

        if self.msg_box.clickedButton() == self.boton_si:

            try: 
                
                self.limpiar_inputs(self.lista_qlineedits, self.lista_radiobuttons, self.lista_timeedits)
                self.stacked_widget.setCurrentIndex(2)
                
                
            except Exception as e:
                print(f"Error al limpiar los inputs: {e}")
            

        elif self.msg_box.clickedButton() == self.boton_no:
            pass
        
        
        

    def limpiar_inputs(self, lista_de_qlineedits, lista_de_radiobuttons, lista_de_timeedits):
        
        try:
            # Limpiamos los QlineEdits
            for qlineedit in lista_de_qlineedits:
                qlineedit.clear()
                qlineedit.setEnabled(True)
                
            # Limpiamos los RadioButtons
            for radiobutton in lista_de_radiobuttons:
                radiobutton.setAutoExclusive(False)
                radiobutton.setChecked(False)
                radiobutton.setAutoExclusive(True)
                
            # Limpiamos los TimeEdits
            for timeedit in lista_de_timeedits:
                timeedit.setTime(QTime(7,0) if "llegada" in timeedit.objectName() else QTime(12,0))
                
        except Exception as e:
            print(f"Error al limpiar los inputs: {e}")    
            
        
    
        
    

    def suministrar_info(self):

        self.msg_box.setWindowTitle("Confirmar información")
        self.msg_box.setText("¿Seguro que quiere registrar?")
        QApplication.beep()
        self.msg_box.exec_()



        if self.msg_box.clickedButton() == self.boton_si:

            self.input_cedula_empleado.clear()
            self.input_motivo_de_retraso.clear()
            self.input_motivo_de_inasistencia.clear()

            self.input_asistente.setAutoExclusive(False)
            self.input_inasistente.setAutoExclusive(False)

            self.input_asistente.setChecked(False)
            self.input_inasistente.setChecked(False)

            self.input_asistente.setAutoExclusive(True)
            self.input_inasistente.setAutoExclusive(True)

            self.input_motivo_de_inasistencia.setDisabled(False)
            self.label_motivo_de_inasistencia.setDisabled(False)

            self.label_hora_de_llegada.setDisabled(False)
            self.input_hora_de_llegada.setDisabled(False)
            self.input_hora_de_llegada.setTime(QTime(7, 0))

            self.label_hora_de_salida.setDisabled(False)
            self.input_hora_de_salida.setDisabled(False)
            self.input_hora_de_salida.setTime(QTime(12, 0))

            self.label_motivo_de_retraso.setDisabled(False)
            self.input_motivo_de_retraso.setDisabled(False)







        elif self.msg_box.clickedButton() == self.boton_no:
            pass


