from PyQt5.QtWidgets import (QWidget, QMessageBox, QApplication, QListWidget, QListWidgetItem, 
                            QLabel, QHBoxLayout, QPushButton )
from PyQt5.QtCore import QTime, QPoint, Qt
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtCore
import os
from elementos_graficos_a_py import Ui_PantallaAsistenciaAlumnos
from datetime import datetime, time


##################################
# importaciones de base de datos #
##################################

# Repositorios

from repositorios.especialidades.especialidad_repositorio import EspecialidadRepositorio
from repositorios.alumnos.alumno_repositorio import AlumnoRepositorio
from repositorios.alumnos.inscripcion_repositorio import InscripcionRepositorio

# Servicios

from servicios.especialidades.especialidad_servicio import EspecialidadServicio
from servicios.alumnos.alumno_servicio import AlumnoServicio
from servicios.alumnos.inscripcion_servicio import InscripcionServicio


# Instanacias Repositorios

especialidad_repositorio = EspecialidadRepositorio()

alumnos_repositorio = AlumnoRepositorio()

inscripcion_repositorio = InscripcionRepositorio()


# Instancia Servicios

especialidad_servicio = EspecialidadServicio(especialidad_repositorio)

alumnos_servicio = AlumnoServicio(alumnos_repositorio)

inscripcion_servicio = InscripcionServicio(inscripcion_repositorio)



##################################
# importaciones de base de datos #
##################################


lista_especialidades = especialidad_servicio.obtener_todos_especialidades()



# Dia actual
today = datetime.now()
dia_de_hoy = today.strftime("%Y-%m-%d")


class PantallaAsistenciaAlumnos(QWidget, Ui_PantallaAsistenciaAlumnos):
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
        
        
        self.input_cedula_alumno.setDisabled(True)
        
        self.cargar_especialidades()
        
        
        self.boton_especialidades.currentIndexChanged.connect(self.actualizar_lista_busqueda)
        self.boton_agregar.clicked.connect(self.agregar_info)
        # esto es para tenerlo listo por aqui
        
        self.input_cedula_alumno.textChanged.connect(self.filtrar_resultados)
        
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
        
        try:
            
            if not self.boton_especialidades.currentIndex() == 0:
                
                self.input_cedula_alumno.setDisabled(False)
                
                especialidad_id = self.buscar_id_de_la_lista_del_combobox(self.boton_especialidades, lista_especialidades, 1, 0)

                self.lista_alumnos_actual = inscripcion_servicio.obtener_inscripcion_por_especialidad(especialidad_id)
                #print(self.lista_alumnos_actual)
                
            if self.boton_especialidades.currentIndex() == 0:
                
                self.input_cedula_alumno.setDisabled(True)
                
            
        except Exception as e:
            
            print(f"Algo malo sucedio en actualizar lista de busqueda: {e}")
            
        
        
            

        
        
        
    # Metodo para buscar el id que esta en la tupla de la lista que arroja la base de datos
    def buscar_id_de_la_lista_del_combobox(self, boton_seleccionado, lista_elementos, indice_nombre_del_elemento, indice_id_del_elemento):
            
        seleccion = boton_seleccionado.currentText()

        
        
        if  seleccion and not boton_seleccionado.currentIndex() == 0:
            
            for elemento in lista_elementos:
                
                if seleccion == elemento[indice_nombre_del_elemento]:
                    
                    id_del_elemento = elemento[indice_id_del_elemento]  
                    
                    id_del_elemento = int(id_del_elemento)
                    
                    return id_del_elemento
                    
                        
                else:
                    pass   

        
        else:
            
            
            pass

        
    
    
    def filtrar_resultados(self, texto):
        texto = texto.strip().lower()
        self.resultados.clear()

        try:
            if not texto:
                self.resultados.hide()
                self.label_nombre_alumno_guia.clear()
                return
            
        
            
            coincidencias = [
                persona for persona in self.lista_alumnos_actual
                if texto in persona[1] or texto in persona[2].lower()
            ]

            if not coincidencias:
                self.resultados.hide()
                return

            for persona in coincidencias:
                item = f'{persona[1]} - {persona[2]} {persona[3]}'
                
                global nombre_guia
                nombre_guia = f" {persona[2].capitalize()} {persona[3].capitalize()}"
                
                self.resultados.addItem(QListWidgetItem(item))

            # Ocultar si hay una coincidencia exacta por cédula
            if len(coincidencias) == 1 and coincidencias[0][1] == texto:
                self.resultados.hide()
            else:
                self.mostrar_lista()
                self.label_nombre_alumno_guia.clear()
                
        except Exception as e:
            
            pass



    def mostrar_lista(self):
        pos = self.input_cedula_alumno.mapTo(self, QPoint(0, self.input_cedula_alumno.height()))
        self.resultados.move(pos)
        self.resultados.resize(self.input_cedula_alumno.width(), 100)
        self.resultados.show()
        
        
        
        
    def seleccionar_item(self, item):
        cedula = item.text().split(" - ")[0]
        self.input_cedula_alumno.setText(cedula)
        self.label_nombre_alumno_guia.setText(nombre_guia)
        self.resultados.hide()
        
        

    ########################################################################################################
    ########################################################################################################

    
        
        
        
    
    
    # Metodo para agregar la informacion a la lista de asistencias
    def agregar_info(self):
        
        try: 
            
            if self.input_asistente.isChecked() == False and self.input_inasistente.isChecked() == False:
                
                QMessageBox.warning(self, "Error", "Por favor, seleccione si el alumno asistió o no.")
                
                
                return
            
            else:
                alumno_n = []
                
                cedula = self.input_cedula_alumno.text().strip()
                alumno_id = self.buscar_id_alumno(cedula)
                
                
                if not any(cedula in alumno[1] for alumno in self.lista_alumnos_actual):
                    
                    QMessageBox.warning(self, "Error", "La persona ya esta agregada o no existe")
                    return
                
                
                alumno = alumnos_servicio.obtener_alumno_por_id(alumno_id)
                
                            
                
                # la lista se compone de: id_empleado, fecha_asistencia, hora_entrada, hora_salida,
                # estado_asistencia, motivo_retraso, motivo_inasistencia, nombre y apellido del empleado 
                # (estas ultimas son para mostrar nada mas)
                
                # 0) alumno ID
                alumno_n.append(alumno_id)
                
                # 1) Fecha de asistencia
                dia_actual = self.fecha_de_str_a_date(dia_de_hoy)
                alumno_n.append(dia_actual)
                
                
                # 2) Estado de asistencia
                if self.input_asistente.isChecked():
                    estado_asistencia = "PRESENTE"
                    alumno_n.append(estado_asistencia)
                
                elif self.input_inasistente.isChecked():
                    estado_asistencia = "AUSENTE"
                    alumno_n.append(estado_asistencia)
                    
                    
                    
                # 3) Motivo de inasistencia
                if self.input_motivo_de_inasistencia.text().strip():
                    motivo_inasistencia = self.input_motivo_de_inasistencia.text().strip()
                    alumno_n.append(motivo_inasistencia)
                else:
                    alumno_n.append(None)
                
                # 4) cedula
                alumno_n.append(cedula)
                
                #5) nombre
                alumno_n.append(alumno[2])
                
                #6) apellido
                alumno_n.append(alumno[5])
                
                
                # el texto que quiero mostrar en la lista de asistencias es : Cedula - Nombre Apellido
                texto_a_mostrar = f"{alumno_n[4]} - {alumno_n[5]} {alumno_n[6]}"
                
                
                alumno_n = tuple(alumno_n)
                
                alumno = alumnos_servicio.obtener_alumno_por_id(alumno_n[0])
                
                print(f"la lista es {alumno_n}")
                
                
                    
                
                
                
                if not len(self.lista_de_asistencias) > 0:
                
                    # Agregamos los elementos al "carrito"
                    if not alumno_n in self.lista_de_asistencias:
                        
                        
                        
                        #self.eliminar_empleado_de_lista(alumno)
                        
                        print(alumno_n)
                        # si no esta los agrega a la lista de asistencia
                        self.lista_de_asistencias.append(alumno_n)
                        
                        
                        # lo agrega al "carrito"
                        self.agg_alumno_a_lista(self.lista_asistencia, self.lista_de_asistencias, self.input_cedula_alumno, texto_a_mostrar)

                        # Limpiamos los inputs
                        #self.limpiar_inputs(self.lista_qlineedits, self.lista_radiobuttons, self.lista_timeedits)
                        
                        
                        
                        
                        
                    
                    else:
                        
                        QMessageBox.warning(self, "Error", "Persona ya agregada")
                        # Limpiamos los inputs
                        #self.limpiar_inputs(self.lista_qlineedits, self.lista_radiobuttons, self.lista_timeedits)
                        
                        return
                    
                else:
                    
                    # Agregamos los elementos al "carrito"
                    if not alumno_n[4] in self.lista_de_asistencias[self.indice][4] or not alumno_n[4] == self.lista_de_asistencias[self.indice][4]:
                        
                        # si no esta los agrega a la lista de asistencia
                        self.lista_de_asistencias.append(alumno_n)
                        
                        
                        #self.eliminar_empleado_de_lista(alumno)
                        
                        # lo agrega al "carrito"
                        self.agg_alumno_a_lista(self.lista_asistencia, self.lista_de_asistencias, self.input_cedula_alumno, texto_a_mostrar)

                        # Limpiamos los inputs
                        #self.limpiar_inputs(self.lista_qlineedits, self.lista_radiobuttons, self.lista_timeedits)
                        
                        # y le sumamos uno al indice para saber la posicion actual
                        self.indice += 1
                        
                    
                    else:
                        
                        QMessageBox.warning(self, "Error", "Persona ya agregada")
                        # Limpiamos los inputs
                        #self.limpiar_inputs(self.lista_qlineedits, self.lista_radiobuttons, self.lista_timeedits)
                        
                        return
                    
                    
                    
                
                    
                
                # esto es para actualizar cuantas personas hay 
                self.contador_de_asistencias += 1
                self.label_titulo_asistencia.setText(f"Lista actual de asistencias: {self.contador_de_asistencias}")
                
                

        except Exception as e:
            print(f"Error al agregar la informacion: {e}")
    
        
    # Metodo "carrito" para agregar a los empleados a la lista de asistencia
    def agg_alumno_a_lista(self, nombre_qlistwidget, nombre_lista, enfoca_input, texto_a_mostrar=None):
        
        
        
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
    

        
        
    # Metodo para cargar las especialidades en el boton de especialidades   
    def cargar_especialidades(self):
        
        #print(lista_especialidades)
        self.boton_especialidades.addItem("Selecciona aqui")
        for especialidad in lista_especialidades:
            
            self.boton_especialidades.addItem(especialidad[1])
    
        
    
    # Metodo para buscar el id del empleado 
    def buscar_id_alumno(self, cedula):
        
        for alumno in self.lista_alumnos_actual:
            
            if cedula in alumno:
                
                alumno_id = alumno[0]
                
                return alumno_id
                
                
            
            else:
                
                pass

    
    
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




    # Metodo convertir la fecha de str a date
    def fecha_de_str_a_date(self, fecha_string):
        
        # Convertir el string a objeto date
        try:
            fecha_date = datetime.strptime(fecha_string, "%Y-%m-%d").date()
            
            return fecha_date
            #print(type(fecha_nacimiento))
        except ValueError as e:
            print(f"Error al convertir la fecha: {e}")
            
        
        
            
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
                #self.limpiar_inputs(self.lista_qlineedits, self.lista_radiobuttons, self.lista_timeedits)
                
                # Limpiamos las lista de asistencias
                self.lista_asistencia.clear()
                
                self.lista_de_asistencias.clear()
                
                self.lista_agregados.clear()
                
                #self.actualizar_lista_busqueda()
                
                
                self.indice = 0
                self.contador_de_asistencias = 0
                self.label_titulo_asistencia.setText(f"Lista actual de asistencias: {self.contador_de_asistencias}")
                
                # nos devolvemos a la pantalla anterior
                self.stacked_widget.setCurrentIndex(5)
                
                
            except Exception as e:
                print(f"Error al salir en esta pantalla: {e}")
            

        elif self.msg_box.clickedButton() == self.boton_no:
            pass
        
        
    
