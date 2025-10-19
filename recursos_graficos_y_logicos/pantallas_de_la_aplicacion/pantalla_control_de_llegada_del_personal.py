from PySide2.QtWidgets import (QWidget, QMessageBox, QApplication, QListWidget, QListWidgetItem, 
                            QLabel, QHBoxLayout, QPushButton )
from PySide2.QtCore import QTime, QPoint, Qt
from PySide2.QtGui import QIcon
from PySide2 import QtGui, QtCore
import os
from ..elementos_graficos_a_py import  Ui_PantallaControlDeLlegada
from datetime import datetime, time

##################################
# importaciones de base de datos #
##################################

# Repositorios
from repositorios.empleados.empleado_repositorio import EmpleadoRepositorio
from repositorios.empleados.asistencia_empleado_repositorio import AsistenciaEmpleadoRepositorio

# Servicios
from servicios.empleados.empleado_servicio import EmpleadoServicio
from servicios.empleados.asistencia_empleado_servicio import AsistenciaEmpleadoServicio

##################################
# importaciones de base de datos #
##################################

# Instancia del repositorio
empleado_repositorio = EmpleadoRepositorio()
asistetencia_empleado_repositorio = AsistenciaEmpleadoRepositorio()

# Instancia del servicio
empleado_servicio = EmpleadoServicio(empleado_repositorio)
asistencia_empleado_servicio = AsistenciaEmpleadoServicio(asistetencia_empleado_repositorio)



# Dia actual
today = datetime.now()
dia_de_hoy = today.strftime("%Y-%m-%d")



class PantallaControlDeLlegada(QWidget, Ui_PantallaControlDeLlegada):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.setupUi(self)
        
        # variable para contar las asistencias
        self.contador_de_asistencias = 0
        
        # Label que muestra el conteo de asistencias
        self.label_titulo_asistencia.setText(f"Lista actual de asistencias: {self.contador_de_asistencias}")

        # lista para almacenar los empleados que se van agregando a la lista de asistencias
        self.lista_de_asistencias = []
        
        # lista de empleados actuales en la bd
        self.lista_empleados_actual = []
        
        # esta lista guardara los empleados que se agreguen a la lista de asistencias
        self.lista_agregados = []
        
        # esto es para el metodo de agregar al empleado a la lista 
        self.indice = 0

        self.lista_qlineedits = [self.input_cedula_empleado, self.input_motivo_de_retraso, self.input_motivo_de_inasistencia]
        self.lista_radiobuttons = [self.input_asistente, self.input_inasistente]
        self.lista_timeedits = [self.input_hora_de_llegada, self.input_hora_de_salida]
        
        
        # Ruta relativa de las imagenes ##
        self.boton_de_regreso.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz","flecha_izquierda_2.png")))
        self.boton_limpiar_lista.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz","brocha.png")))
        self.boton_agregar.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz","mas_blanco.png")))
        self.boton_suministrar.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz","exportar.png")))





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
        self.boton_agregar.clicked.connect(self.agregar_info)
        self.boton_limpiar_lista.clicked.connect(self.limpiar_lista_de_asistencias)
        self.boton_suministrar.clicked.connect(self.suministrar_asistencias)
        
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
            self.label_nombre_empleado_guia.clear()
            return
        
    
        
        coincidencias = [
            persona for persona in self.lista_empleados_actual
            if texto in persona[5] or texto in persona[1].lower()
        ]

        if not coincidencias:
            self.resultados.hide()
            return

        for persona in coincidencias:
            item = f'{persona[6]} - {persona[1]} {persona[4]}'
            
            global nombre_guia
            nombre_guia = f" {persona[1].capitalize()} {persona[4].capitalize()}"
            
            self.resultados.addItem(QListWidgetItem(item))

        # Ocultar si hay una coincidencia exacta por cédula
        if len(coincidencias) == 1 and coincidencias[0][1] == texto:
            self.resultados.hide()
        else:
            self.mostrar_lista()
            self.label_nombre_empleado_guia.clear()




    def mostrar_lista(self):
        pos = self.input_cedula_empleado.mapTo(self, QPoint(0, self.input_cedula_empleado.height()))
        self.resultados.move(pos)
        self.resultados.resize(self.input_cedula_empleado.width(), 100)
        self.resultados.show()
        
        
        
        
    def seleccionar_item(self, item):
        cedula = item.text().split(" - ")[0]
        self.input_cedula_empleado.setText(cedula)
        self.label_nombre_empleado_guia.setText(nombre_guia)
        self.resultados.hide()
        
        

    ########################################################################################################
    ########################################################################################################

    
    
    # Metodo para agregar la informacion a la lista de asistencias
    def agregar_info(self):
        
        try: 
            
            if self.input_asistente.isChecked() == False and self.input_inasistente.isChecked() == False:
                
                QMessageBox.warning(self, "Error", "Por favor, seleccione si el empleado asistió o no.")
                
                
                return
            
            else:
                empleado_n = []
                
                cedula = self.input_cedula_empleado.text().strip()
                empleado_id = self.buscar_id_empleado(cedula)
                
                
                if not any(cedula in empleado[6] for empleado in self.lista_empleados_actual):
                    
                    QMessageBox.warning(self, "Error", "La persona ya esta agregada o no existe")
                    return
                
                
                empleado = empleado_servicio.obtener_empleado_por_id(empleado_id)
                
                
                            
                
                # la lista se compone de: id_empleado, fecha_asistencia, hora_entrada, hora_salida,
                # estado_asistencia, motivo_retraso, motivo_inasistencia, nombre y apellido del empleado 
                # (estas ultimas son para mostrar nada mas)
                
                # 0) Empleado ID
                empleado_n.append(empleado_id)
                
                # 1) Fecha de asistencia
                dia_actual = self.fecha_de_str_a_date(dia_de_hoy)
                empleado_n.append(dia_actual)
                
                # 2) Hora de entrada
                
                
                hora_entrada = self.de_str_a_time(self.input_hora_de_llegada.time().toString("HH:mm") )

                empleado_n.append(hora_entrada)
                
                # 3) Hora de salida
                hora_salida = self.de_str_a_time(self.input_hora_de_salida.time().toString("HH:mm") )
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
                empleado_n.append(empleado[4])
                
                
                # el texto que quiero mostrar en la lista de asistencias es : Cedula - Nombre Apellido
                texto_a_mostrar = f"{empleado_n[7]} - {empleado_n[8]} {empleado_n[9]}"
                
                
                empleado_n = tuple(empleado_n)
                
                empleado = empleado_servicio.obtener_empleado_por_id(empleado_n[0])
                
                print(empleado_n)
                
                
                    
                
                
                
                if not len(self.lista_de_asistencias) > 0:
                
                    # Agregamos los elementos al "carrito"
                    if not empleado_n in self.lista_de_asistencias:
                        
                        
                        
                        self.eliminar_empleado_de_lista(empleado)
                        
                        print(empleado_n)
                        # si no esta los agrega a la lista de asistencia
                        self.lista_de_asistencias.append(empleado_n)
                        
                        
                        # lo agrega al "carrito"
                        self.agg_empleado_a_lista(self.lista_asistencia, self.lista_de_asistencias, self.input_cedula_empleado, texto_a_mostrar)

                        # Limpiamos los inputs
                        self.limpiar_inputs(self.lista_qlineedits, self.lista_radiobuttons, self.lista_timeedits)
                        
                        
                        
                        
                        
                    
                    else:
                        
                        QMessageBox.warning(self, "Error", "Persona ya agregada")
                        # Limpiamos los inputs
                        self.limpiar_inputs(self.lista_qlineedits, self.lista_radiobuttons, self.lista_timeedits)
                        
                        return
                    
                else:
                    
                    # Agregamos los elementos al "carrito"
                    if not empleado_n[7] in self.lista_de_asistencias[self.indice][7] or not empleado_n[7] == self.lista_de_asistencias[self.indice][7]:
                        
                        # si no esta los agrega a la lista de asistencia
                        self.lista_de_asistencias.append(empleado_n)
                        
                        
                        self.eliminar_empleado_de_lista(empleado)
                        
                        # lo agrega al "carrito"
                        self.agg_empleado_a_lista(self.lista_asistencia, self.lista_de_asistencias, self.input_cedula_empleado, texto_a_mostrar)

                        # Limpiamos los inputs
                        self.limpiar_inputs(self.lista_qlineedits, self.lista_radiobuttons, self.lista_timeedits)
                        
                        # y le sumamos uno al indice para saber la posicion actual
                        self.indice += 1
                        
                    
                    else:
                        
                        QMessageBox.warning(self, "Error", "Persona ya agregada")
                        # Limpiamos los inputs
                        self.limpiar_inputs(self.lista_qlineedits, self.lista_radiobuttons, self.lista_timeedits)
                        
                        return
                    
                    
                    
                
                    
                
                # esto es para actualizar cuantas personas hay 
                self.contador_de_asistencias += 1
                self.label_titulo_asistencia.setText(f"Lista actual de asistencias: {self.contador_de_asistencias}")
                
                

        except Exception as e:
            print(f"Error al agregar la informacion: {e}")
            
            
    # Metodo para eliminar al empleado de la lista en donde estan todos los empleados actuales
    # esto es para que cuando agregue un empleado la lista de la barra de busqueda no muestre el 
    # empleado que ya fue agregado a la lista de asistencias
    def eliminar_empleado_de_lista(self, empleado):
        
        if empleado in self.lista_empleados_actual:
                            
            self.lista_agregados.append(empleado)
            
            self.lista_empleados_actual.remove(empleado)
            

            
            
            
    
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
                                    font-weight: bold;
                                    font-size: 10pt;
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
                                    font-weight: bold;
                                    font-size: 10pt;
                                    padding-left:5px;
                                    
                                    
                                    
                                }
                                
                                """)
            row_layout.addWidget(label)

        # Botón para eliminar
        delete_button = QPushButton()
        delete_button.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "borrar.png")))
        delete_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        delete_button.setFixedSize(35,35)
        delete_button.setStyleSheet("""
                                    
                                    QPushButton{
                                        background:red;
                                        border-radius:12px;
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
        self.indice -= 1
        
        # darle foco al input del segmento
        # esto lo hice porque al borrar toda la lista de X segmento, esta se subia al arriba del todo del formulario
        enfoca_input.setFocus()
        
        if not self.lista_agregados[indice_vista_previa] in self.lista_empleados_actual:
            
            empleado_restaurar = self.lista_agregados[indice_vista_previa]
            
            self.lista_empleados_actual.append(empleado_restaurar)
            
            self.lista_agregados.remove(empleado_restaurar)
        
        
        # actualizar el contador de asistencias
        self.contador_de_asistencias -= 1
        self.label_titulo_asistencia.setText(f"Lista actual de asistencias: {self.contador_de_asistencias}")
        
        
    
        
        
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
                
                # Limpiamos los inputs
                self.limpiar_inputs(self.lista_qlineedits, self.lista_radiobuttons, self.lista_timeedits)
                
                # Limpiamos las lista de asistencias
                self.lista_asistencia.clear()
                
                self.lista_de_asistencias.clear()
                
                self.lista_agregados.clear()
                
                self.actualizar_lista_busqueda()
                
                
                self.indice = 0
                self.contador_de_asistencias = 0
                self.label_titulo_asistencia.setText(f"Lista actual de asistencias: {self.contador_de_asistencias}")
                
                # nos devolvemos a la pantalla anterior
                self.stacked_widget.setCurrentIndex(7)
                
                
            except Exception as e:
                print(f"Error al salir en esta pantalla: {e}")
            

        elif self.msg_box.clickedButton() == self.boton_no:
            pass
        
        
    


    # Metodo para buscar el id del empleado 
    def buscar_id_empleado(self, cedula):
        
        for empleado in self.lista_empleados_actual:
            
            if cedula in empleado:
                
                empleado_id = empleado[0]
                
                return empleado_id
                
                break
            
            else:
                
                pass


    # Metodo para limpiar la lista de asistencias con el boton limpiar lista
    def limpiar_lista_de_asistencias(self):
        
        self.msg_box.setWindowTitle("Confirmar acción")
        self.msg_box.setText("¿Seguro que quiere borrar la lista y empezar de nuevo?")
        QApplication.beep()
        self.msg_box.exec_()



        if self.msg_box.clickedButton() == self.boton_si:
            

            # Limpiamos las listas y los contadores
            self.lista_asistencia.clear()
            self.lista_de_asistencias.clear()
            self.lista_agregados.clear()
            self.indice = 0
            self.contador_de_asistencias = 0
            
            # restablecemos el contador de asistencias
            self.label_titulo_asistencia.setText(f"Lista actual de asistencias: {self.contador_de_asistencias}")
            
            # restablecemos la lista de empleados actuales de la bd
            self.actualizar_lista_busqueda()

        

        elif self.msg_box.clickedButton() == self.boton_no:
            pass


        
        
    # Metodo para suministrar las asistencias a la base de datos
    def suministrar_asistencias(self):
        
        try:
            
             # Indice solo para ver el numero de iteraciones
            indice = 0
            
            
            self.msg_box.setWindowTitle("Confirmar registro")
            self.msg_box.setText("¿Seguro que quiere registrar esta lista de asistencia?")
            self.msg_box.setIcon(QMessageBox.Question)
            QApplication.beep()



            # Mostrar el cuadro de diálogo y esperar respuesta
            self.msg_box.exec_()

            if self.msg_box.clickedButton() == self.boton_si:
                
                
                
                
                # Iteramos cada empleado que esta en la lista de asistencia
                for empleado in self.lista_de_asistencias:
                    
                    # esto es para ver en la consola
                    print(f"Empleado {indice} ID:{empleado[0]} Nombre:{empleado[8]}")
                    indice += 1
                    
                        
                        
                    empleado_id = empleado[0]
                    
                    fecha_asistencia = empleado[1]
                    
                    hora_entrada = empleado[2]
                    
                    
                    hora_salida = empleado[3]
                    
                    estado_asistencia = empleado[4]
                    
                    motivo_retraso = empleado[5]
                    
                    motivo_inasistencia = empleado[6]
                    
                    
                    
                    
                    campos_asistencia_empleados = {
                                "empleado_id": empleado_id,
                                "fecha_asistencia": fecha_asistencia,
                                "hora_entrada": hora_entrada,
                                "hora_salida": hora_salida,
                                "estado_asistencia": estado_asistencia,
                                "motivo_retraso": motivo_retraso,
                                "motivo_inasistencia": motivo_inasistencia
                            }
                    
                    errores_totales = asistencia_empleado_servicio.validar_asistencia_empleado(
                                        campos_asistencia_empleados.get("empleado_id"), 
                                        campos_asistencia_empleados.get("fecha_asistencia"),
                                        campos_asistencia_empleados.get("estado_asistencia"),
                                        campos_asistencia_empleados.get("motivo_retraso"),
                                        campos_asistencia_empleados.get("motivo_inasistencia")
                                        )
                    
                    
                    if errores_totales:
                        
                        QMessageBox.information(self, "Error", "Tu registro de asistencia a tenido un error. ")
                        estado = False
                        return
                    else:
                        asistencia_empleado_servicio.registrar_asistencia_empleado(campos_asistencia_empleados)
                        estado = True
                        
                        
                if estado:
                    
                    QMessageBox.information(self, "Registro exitoso", "Tu registro de asistencia a sido exitoso. ")
                    self.limpiar_inputs(self.lista_qlineedits, self.lista_radiobuttons, self.lista_timeedits)
                    
                    # Limpiamos las listas y los contadores
                    self.lista_asistencia.clear()
                    self.lista_de_asistencias.clear()
                    self.lista_agregados.clear()
                    self.indice = 0
                    self.contador_de_asistencias = 0
                    
                    # restablecemos el contador de asistencias
                    self.label_titulo_asistencia.setText(f"Lista actual de asistencias: {self.contador_de_asistencias}")
                    
                    # restablecemos la lista de empleados actuales de la bd
                    self.actualizar_lista_busqueda()

                    
                    
                    
                        
            elif self.msg_box.clickedButton() == self.boton_no:
                
                return
                    
                    
            
        except Exception as e:
            
            print(f"algo malo paso en suministrar info : {e}")
                                    
                                    
                                    
                                    
    # Metodo para colocar la hora que esta en tipo string a time
    def de_str_a_time(self, acomodar_hora):
        
        try:
            
            horas, minutos = map(int, acomodar_hora.split(':'))
        
            hora_arreglada= time(horas, minutos)  # segundos=0 por defecto
            
            return hora_arreglada
            
        except Exception as e:
            print(f"algo salio mal {e}")
            
            
            
            
    # Metodo convertir la fecha de str a date
    def fecha_de_str_a_date(self, fecha_string):
        
        # Convertir el string a objeto date
        try:
            fecha_date = datetime.strptime(fecha_string, "%Y-%m-%d").date()
            
            return fecha_date
            #print(type(fecha_nacimiento))
        except ValueError as e:
            print(f"Error al convertir la fecha: {e}")
