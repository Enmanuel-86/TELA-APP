from PyQt5.QtWidgets import (QWidget, QMessageBox, QApplication, QListWidget, QListWidgetItem, 
                            QLabel, QHBoxLayout, QPushButton )
from PyQt5.QtCore import QTime, QPoint, Qt
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtCore
import os
from elementos_graficos_a_py import  Ui_PantallaControlDeLlegada
from datetime import datetime

##################################
# importaciones de base de datos #
##################################

# Repositorios
from repositorios.empleados.empleado_repositorio import EmpleadoRepositorio

# Servicios
from servicios.empleados.empleado_servicio import EmpleadoServicio

##################################
# importaciones de base de datos #
##################################

# Instancia del repositorio
empleado_repositorio = EmpleadoRepositorio()

# Instancia del servicio
empleado_servicio = EmpleadoServicio(empleado_repositorio)



# Dia actual
today = datetime.now()
dia_de_hoy = today.strftime("%Y-%d-%m")

class PantallaControlDeLlegada(QWidget, Ui_PantallaControlDeLlegada):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.setupUi(self)

        self.lista_de_asistencias = []

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
        self.actualizar_lista_busqueda()

        #funcion para habilitar los input segun el estado de asistencia

        self.input_asistente.toggled.connect(self.cuando_asiste_el_personal)
        self.input_inasistente.toggled.connect(self.cuando_no_asiste_el_personal)
        self.boton_de_suministrar.clicked.connect(self.suministrar_info)
        
        self.input_cedula_empleado.textChanged.connect(self.filtrar_resultados)


        # Lista de coincidencias
        self.resultados = QListWidget(self)
        self.resultados.setFocusPolicy(Qt.NoFocus)
        self.resultados.setMouseTracking(True)
        self.resultados.setStyleSheet("background-color: white; border: 1px solid gray;border-radius:0px; padding:10px;")
        self.resultados.itemClicked.connect(self.seleccionar_item)
        self.resultados.hide() 


    ########################################################################################################
    ########################################################################################################

    # Funciones para la busqueda dinamica del empleado
    
    def actualizar_lista_busqueda(self):
        
        self.lista_empleados_actual = empleado_servicio.obtener_todos_empleados()
    
    
    def filtrar_resultados(self, texto):
        texto = texto.strip().lower()
        self.resultados.clear()

        if not texto:
            self.resultados.hide()
            return
        
    
        
        coincidencias = [
            persona for persona in self.lista_empleados_actual
            if texto in persona[5] or texto in persona[1].lower()
        ]

        if not coincidencias:
            self.resultados.hide()
            return

        for persona in coincidencias:
            item = f'{persona[5]} - {persona[1]} {persona[3]}'
            self.resultados.addItem(QListWidgetItem(item))

        # Ocultar si hay una coincidencia exacta por cédula
        if len(coincidencias) == 1 and coincidencias[0][1] == texto:
            self.resultados.hide()
        else:
            self.mostrar_lista()




    def mostrar_lista(self):
        pos = self.input_cedula_empleado.mapTo(self, QPoint(0, self.input_cedula_empleado.height()))
        self.resultados.move(pos)
        self.resultados.resize(self.input_cedula_empleado.width(), 100)
        self.resultados.show()
        
        
        
        
    def seleccionar_item(self, item):
        cedula = item.text().split(" - ")[0]
        self.input_cedula_empleado.setText(cedula)
        self.resultados.hide()

    ########################################################################################################
    ########################################################################################################

    
    # Metodo para suministrar la informacion a la lista de asistencias
    def suministrar_info(self):
        
        
        empleado_n = []
        
        cedula = self.input_cedula_empleado.text().strip()
        empleado_id = self.buscar_id_empleado(cedula)
        
        empleado = empleado_servicio.obtener_empleado_por_id(empleado_id)
        
        
        
        # la lista se compone de: id_empleado, fecha_asistencia, hora_entrada, hora_salida,
        # estado_asistencia, motivo_retraso, motivo_inasistencia, nombre y apellido del empleado 
        # (estas ultimas son para mostrar nada mas)
        
        # 0) Empleado ID
        empleado_n.append(empleado_id)
        
        # 1) Fecha de asistencia
        empleado_n.append(dia_de_hoy)
        
        # 2) Hora de entrada
        hora_entrada = self.input_hora_de_llegada.time().toString("HH:mm")
        empleado_n.append(hora_entrada)
        
        # 3) Hora de salida
        hora_salida = self.input_hora_de_salida.time().toString("HH:mm")
        empleado_n.append(hora_salida)
        
        # 4) Estado de asistencia
        if self.input_asistente.isChecked():
            estado_asistencia = "PRESENTE"
            empleado_n.append(estado_asistencia)
        
        elif self.input_inasistente.isChecked():
            estado_asistencia = "AUSENTE"
            empleado_n.append(estado_asistencia)
            
            
        # 5) Motivo de retraso
        if self.input_motivo_de_retraso.text().strip():
            motivo_retraso = self.input_motivo_de_retraso.text().strip()
            empleado_n.append(motivo_retraso)
        else:
            empleado_n.append(None)
            
            
        # 6) Motivo de inasistencia
        if self.input_motivo_de_inasistencia.text().strip():
            motivo_inasistencia = self.input_motivo_de_inasistencia.text().strip()
            empleado_n.append(motivo_inasistencia)
        else:
            empleado_n.append(None)
        
        # 7) cedula
        empleado_n.append(cedula)
        
        #8) nombre
        empleado_n.append(empleado[1])
        
        #9) apellido
        empleado_n.append(empleado[3])
        
        
        
        texto_a_mostrar = f"{empleado_n[7]} - {empleado_n[8]} {empleado_n[9]}"
        
        
        empleado_n = tuple(empleado_n)
        
        self.lista_de_asistencias.append(empleado_n)
        print(empleado_n)
        
        # Agregamos los elementos al "carrito"
        self.agg_empleado_a_lista(self.lista_asistencia, self.lista_de_asistencias, self.input_cedula_empleado, texto_a_mostrar)
        
        
        
        # Limpiamos los inputs
        self.limpiar_inputs(self.lista_qlineedits, self.lista_radiobuttons, self.lista_timeedits)


    
    # Metodo "carrito" para agregar a los empleados a la lista de asistencia
    def agg_empleado_a_lista(self, nombre_qlistwidget, nombre_lista, enfoca_input, texto_a_mostrar=None):
        
        # Crear un QListWidgetItem
        item = QListWidgetItem()
        nombre_qlistwidget.addItem(item)
        
        

        # Crear un widget personalizado para la fila
        widget = QWidget()
        row_layout = QHBoxLayout()
        widget.setLayout(row_layout)

        # Label para el texto
        if self.input_asistente.isChecked():
            
                
            label = QLabel(texto_a_mostrar if texto_a_mostrar else f"Elemento {self.list_widget.count() + 1}")
            label.setStyleSheet("""
                                
                                QLabel{
                                    
                                    background:#b5ffb0;
                                    font-family: 'Arial';
                                    font-size: 14pt;
                                    padding-left:5px;
                                    
                                    
                                }
                                
                                """)
            row_layout.addWidget(label)
        
        elif self.input_inasistente.isChecked():
            
            label = QLabel(texto_a_mostrar if texto_a_mostrar else f"Elemento {self.list_widget.count() + 1}")
            label.setStyleSheet("""
                                
                                QLabel{
                                    
                                    background:#ffacac;
                                    font-family: 'Arial';
                                    font-size: 14pt;
                                    padding-left:5px;
                                    
                                    
                                }
                                
                                """)
            row_layout.addWidget(label)

        # Botón para eliminar
        delete_button = QPushButton()
        delete_button.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "borrar.png")))
        delete_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        delete_button.setFixedSize(40,40)
        delete_button.setStyleSheet("""
                                    
                                    QPushButton{
                                        background:red;
                                        border-radius:20px;
                                        icon-size:28px;
                                    
                                    }
                                    
                                    QPushButton:hover{
                                        
                                        background:#9e0000
                                        
                                        
                                    }
                                    
                                    
                                    """)
        
        delete_button.clicked.connect(lambda: self.borrar_elementos_a_la_vista_previa(nombre_qlistwidget, nombre_lista, enfoca_input, item))
        row_layout.addWidget(delete_button)

        # Asignar el widget al QListWidgetItem
        item.setSizeHint(widget.sizeHint())
        nombre_qlistwidget.setItemWidget(item, widget)

    
    def borrar_elementos_a_la_vista_previa(self, nombre_qlistwidget, nombre_lista, enfoca_input,  item):
        
        
        # Logica para borrar el registro del diagnostico de la lista
        
        # indice del listwidget
        indice_vista_previa = nombre_qlistwidget.row(item)
        
        # borramos el elemento de la lista segun el indice del listwidget
        del nombre_lista[indice_vista_previa]
        
        # darle foco al input del segmento
        # esto lo hice porque al borrar toda la lista de X segmento, esta se subia al arriba del todo del formulario
        
        
        enfoca_input.setFocus()
        
        
        
        
        
        
        ##########################################################################
        # Obtener la fila del item y eliminarlo
        row = nombre_qlistwidget.row(item)
        nombre_qlistwidget.takeItem(row)
    
        print(f"lista actualizada: {nombre_lista}")
    


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


        
    # Metodo para limpiar los inputs
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
            
        
    
      # Metodo para volver a la pantalla anterior
    
    
    
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
                
                # Limpiamos la lista de asistencias
                self.lista_asistencia.clear()
                
                self.stacked_widget.setCurrentIndex(2)
                
                
            except Exception as e:
                print(f"Error al limpiar los inputs: {e}")
            

        elif self.msg_box.clickedButton() == self.boton_no:
            pass
        
        
    


    # Metodo para buscar al empleado por su id
    def buscar_id_empleado(self, cedula):
        
        for empleado in self.lista_empleados_actual:
            
            if cedula in empleado:
                
                empleado_id = empleado[0]
                
                return empleado_id
                
                break
            
            else:
                
                pass

"""

Esto no se borra, lo usare luego

self.msg_box.setWindowTitle("Confirmar información")
        self.msg_box.setText("¿Seguro que quiere registrar?")
        QApplication.beep()
        self.msg_box.exec_()



        if self.msg_box.clickedButton() == self.boton_si:
            

            pass
        

        elif self.msg_box.clickedButton() == self.boton_no:
            pass




"""
