from PyQt5.QtWidgets import (QWidget, QMessageBox, QApplication, QListWidget, QListWidgetItem, 
                            QLabel, QHBoxLayout, QPushButton )
from PyQt5.QtCore import QSize, QPoint, Qt, QDate
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtCore
import os
from ..elementos_graficos_a_py import Ui_VistaGeneralAsistenciaAlumnos
from ..utilidades.funciones_sistema import FuncionSistema
from datetime import datetime, date


##################################
# importaciones de base de datos #
##################################

# Repositorios

from repositorios.especialidades.especialidad_repositorio import EspecialidadRepositorio
from repositorios.alumnos.alumno_repositorio import AlumnoRepositorio
from repositorios.alumnos.inscripcion_repositorio import InscripcionRepositorio
from repositorios.alumnos.asistencia_alumno_repositorio import AsistenciaAlumnoRepositorio

# Servicios

from servicios.especialidades.especialidad_servicio import EspecialidadServicio
from servicios.alumnos.alumno_servicio import AlumnoServicio
from servicios.alumnos.inscripcion_servicio import InscripcionServicio
from servicios.alumnos.asistencia_alumno_servicio import AsistenciaAlumnoServicio

# Instanacias Repositorios

especialidad_repositorio = EspecialidadRepositorio()

alumnos_repositorio = AlumnoRepositorio()

inscripcion_repositorio = InscripcionRepositorio()

asistencia_alumno_repositorio = AsistenciaAlumnoRepositorio()


# Instancia Servicios

especialidad_servicio = EspecialidadServicio(especialidad_repositorio)

alumnos_servicio = AlumnoServicio(alumnos_repositorio)

inscripcion_servicio = InscripcionServicio(inscripcion_repositorio)

asistencia_alumno_servicio = AsistenciaAlumnoServicio(asistencia_alumno_repositorio)



##################################
# importaciones de base de datos #
##################################


lista_especialidades = especialidad_servicio.obtener_todos_especialidades()



# Dia actual
today = datetime.now()
dia_de_hoy = today.strftime("%Y-%m-%d")


class PantallaVistaGeneralAsistenciaAlumnos(QWidget, Ui_VistaGeneralAsistenciaAlumnos):
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
        
        self.lista_qlineedits = (self.input_cedula_alumno, self.input_dia_feriado)
        self.lista_radiobuttons = (self.radioButton_inasistente, self.radioButton_asistente)
        
        
        self.checkbox_estado_combobox.setText("Activado")
        self.checkbox_estado_combobox.setChecked(True)
        

        self.msg_box = QMessageBox(self)
        
        # Crear botones personalizados
        self.boton_si = self.msg_box.addButton("Sí", QMessageBox.YesRole)
        self.boton_no = self.msg_box.addButton("No", QMessageBox.NoRole)
        
        self.dateedit_fecha_asistencia.setDate(QDate.currentDate())
        
        self.input_cedula_alumno.setDisabled(True)
        
        FuncionSistema.cargar_elementos_para_el_combobox(lista_especialidades, self.boton_especialidades, 1, 1)
        
        # Conexion de botones
        
        self.boton_crear_registro.clicked.connect(lambda: self.crear_nuevo_registro_asistencia())
        self.boton_cancelar_registro.clicked.connect(lambda: self.cancelar_registro_asistencia())
        self.boton_especialidades.currentIndexChanged.connect(lambda: self.actualizar_lista_busqueda())
        self.checkbox_estado_combobox.clicked.connect(lambda: self.verficacion_combobox())
        self.input_cedula_alumno.textChanged.connect(lambda texto: self.filtrar_resultados(texto))


        # Lista de coincidencias
        self.resultados = QListWidget(self)
        self.resultados.setFocusPolicy(Qt.NoFocus)
        self.resultados.setMouseTracking(True)
        self.resultados.setStyleSheet("padding:10px;")
        self.resultados.itemClicked.connect(self.seleccionar_item)
        self.resultados.hide() 
        
        
        
    # Metodo para verificar el estado del combobox que contiene las especialidades
    def verficacion_combobox(self):
        
        # Primero verificamos que el combobox no tenga el indice 0 que es el "Seleccione aqui"
        if not self.boton_especialidades.currentIndex() == 0:
            
            # Si el indice no es 0 entonces que le avise al usuario el siguiente mensaje
            
            self.msg_box.setWindowTitle("Advertencia")
            self.msg_box.setText("¿Seguro que quiere habilitar el boton desplegable?\n\n Si pulsa (SI) se borrara la lista de asistencia actual y podra elegir otra especialdad \n\n Si pulsa (NO) puede continuar con la asistencia de la especialidad actual")
            QApplication.beep()
            
            # Mostrar el cuadro de diálogo y esperar respuesta
            self.msg_box.exec_()
            
            # si le da a SI, verificamos primero
            if self.msg_box.clickedButton() == self.boton_si:
                
                # Si el checkbox esta marcado/activado entonces 
                # Lo que queremos es que si esta activado el checkbox el combobox tambien
                if self.checkbox_estado_combobox.isChecked():
                    
                    # Le indicicamos al checkbox que diga activado mientras esta marcado
                    self.estado_checkbox(1) # esto es igual a ACTIVADO
                    
                    # Activamos el combobox
                    self.boton_especialidades.setEnabled(True)
                    
                    # le decimos que este en el indice 0
                    self.boton_especialidades.setCurrentIndex(0)
                    
                    # limpiamos la lista de asistencia
                    self.lista_asistencias_en_cola.clear()
                    
                    # y usamos la funcion para limpiar los inputs
                    FuncionSistema.limpiar_inputs_de_qt(self.lista_qlineedits, self.lista_radiobuttons)
                    
                    
                
            # si le a da a no
            elif self.msg_box.clickedButton() == self.boton_no:
                    
                # le indicamos al checkbox que diga que esta desactivado mientras no este marcado
                self.estado_checkbox(0)
                
                # Y deshabilitamos el combobox
                self.boton_especialidades.setEnabled(False)
            
        else:
            # en caso contrario de que le indice del combo box no sea 0 que deje el checkbox activado
            # indicando asi que el combobox esta habilitado
            self.estado_checkbox(1)
            
        




    def actualizar_lista_busqueda(self):
        
        try:
            
            
            # Si el boton de especialidades su indice no es 0
            if not self.boton_especialidades.currentIndex() == 0:
                
                #limpiamos el input
                self.input_cedula_alumno.clear()
                
                # Habilitamos el input de cedula alumno
                self.input_cedula_alumno.setDisabled(False)
                
                # guardamos el id de la especialidad seleccionada
                especialidad_id = FuncionSistema.obtener_id_del_elemento_del_combobox(self.boton_especialidades, lista_especialidades, 1, 0, True)

                # y se lo asignamos a la lista actual de alumnos, para ir cambiandola segun 
                # la especialidad seleccionada
                self.lista_alumnos_actual = inscripcion_servicio.obtener_inscripcion_por_especialidad(especialidad_id)
                
                
                self.boton_especialidades.setEnabled(False)
                
                self.estado_checkbox(0)
                
                # Activamos los campos/inputs para que el usuario haga el registro
                self.input_cedula_alumno.setEnabled(True)
                        
                for qradiobutton in self.lista_radiobuttons:
                    qradiobutton.setEnabled(True)
                    
                self.dateedit_fecha_asistencia.setEnabled(True)
                
                self.boton_agregar.setEnabled(True)
                
                self.boton_establecer_dia_feriado.setEnabled(True)
            
            
            
            
            # Si es igual a 0
            if self.boton_especialidades.currentIndex() == 0:
                
                # que desabilite el input, para evitar errores
                self.input_cedula_alumno.setDisabled(True)
                
                self.boton_especialidades.setEnabled(True)
                
                self.estado_checkbox(1)
                
            
        except Exception as e:
            
            print(f"Algo malo sucedio en actualizar lista de busqueda: {e}")
            
        
    # Metodo para indicar en que estado queremos el checkbox que
    # verifica el estado del combobox que contiene las especialidades
    def estado_checkbox(self, estado: int)->int:
        
        if estado == 1:
            
            self.checkbox_estado_combobox.setChecked(True)
            self.checkbox_estado_combobox.setText("Activado") 
            
        elif estado == 0:
            
            self.checkbox_estado_combobox.setChecked(False)
            self.checkbox_estado_combobox.setText("Desactivado")
            
            
    #################################################################
    
    
    
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
        
        

    
    ################################################################
    
    def crear_nuevo_registro_asistencia(self):
        """
            Este metodo sirve para empezar a crear un nuevo registro de asistencia de los empleados, hace lo siguiente
            
            1. Al darle click al boton nuevo registro este cambia el stackedWidget que esta en el frame inferior a la posicion 1 en donde tiene el QListWidget
            2. Deshabilita el boton crear nuevo registro, para que los dos botones tenga efecto switch
            3. Habilitamos los campos que se utilizan para el registro (los QLineEdits, RadioButton, QDateEdit, QTimeEdit)
            4. Habilita el boton de cancelar registro
            
        """
        self.ventanas_registro_asistencia.setCurrentIndex(1)
        
        self.boton_crear_registro.setEnabled(False)
        
        self.boton_especialidades.setEnabled(True)
        
        self.boton_especialidades.setCurrentIndex(0)
        
        self.checkbox_estado_combobox.setEnabled(True)
                                    
        self.boton_cancelar_registro.setEnabled(True)
    
    
    def cancelar_registro_asistencia(self):
        """
            Este metodo sirve para cancelar el registro de asistencia que se esta realizando, haciendo lo siguiente:
            
            1. Este le aviasa al usuario si esta seguro que si quiere cancelar el registro, si lo hace:
                * Restablecemos las listas internas que llevan el control de la asistencia a su estado inicial
                * Al darle click la boton de cancelar registro, este cambia el stackedWidget que esta en el frame inferior a la posicion 0 para ver el QTableView
                * Deshabilita el boton de cancelar registro de asistencia
                * Deshabilitamos los campos que se utilizan para el registro (los QLineEdits, RadioButton, QDateEdit, QTimeEdit)
                * Habilita el boton de crear nuevo registro de asistencia
                
            2. Si le da a NO, no pasa nada y el usuario sigue con lo suyo
        """
        
        self.msg_box.setIcon(QMessageBox.Information)
        self.msg_box.setWindowTitle("Confirmar acción")
        self.msg_box.setText("¿Seguro que quiere cancelar el registro?")
        self.msg_box.setInformativeText("Esto borrar lo que lleva registrando hasta el momento.")
        QApplication.beep()
        self.msg_box.exec_()
        
        if self.msg_box.clickedButton() == self.boton_si:
            

            # Limpiamos las listas y los contadores
            self.lista_asistencias_en_cola.clear()
            self.lista_de_asistencias.clear()
            self.lista_agregados.clear()
            self.indice = 0
            self.contador_de_asistencias = 0
            
            # restablecemos el contador de asistencias
            self.label_titulo_asistencia.setText(f"Lista actual de asistencias: {self.contador_de_asistencias}")
            
            # restablecemos la lista de empleados actuales de la bd
            self.actualizar_lista_busqueda()
        
            self.ventanas_registro_asistencia.setCurrentIndex(0)
            
            self.boton_crear_registro.setEnabled(True)
            
            self.boton_especialidades.setEnabled(False)
            
            self.boton_especialidades.setCurrentIndex(0)
            
            self.checkbox_estado_combobox.setEnabled(False)
                    
            for qlineedits in self.lista_qlineedits:
                qlineedits.setEnabled(False)
                
            for qradiobutton in self.lista_radiobuttons:
                qradiobutton.setEnabled(False)
                
            self.dateedit_fecha_asistencia.setEnabled(False)
            
            self.boton_agregar.setEnabled(True)
            
            self.boton_cancelar_registro.setEnabled(False)
            
            FuncionSistema.limpiar_inputs_de_qt(self.lista_qlineedits, self.lista_radiobuttons)
            
            
            
            self.boton_agregar.setEnabled(False)
            
        if self.msg_box.clickedButton() == self.boton_no:
            
            return
     
     
    def limpiar_lista_de_asistencias(self):
        

        self.msg_box.setWindowTitle("Confirmar acción")
        self.msg_box.setText("¿Seguro que quiere borrar la lista y empezar de nuevo?")
        self.msg_box.setIcon(QMessageBox.Warning)
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
            
            # establecemos el indice 0 del combo box
            self.boton_especialidades.setCurrentIndex(0)
            
            # limpiamos el input
            self.input_cedula_alumno.clear()
            
            # limpiamos los inputs
            self.limpiar_inputs(self.lista_qlineedits, self.lista_radiobuttons)
            
            # restablecemos la lista de empleados actuales de la bd
            self.actualizar_lista_busqueda()
            
        if self.msg_box.clickedButton() == self.boton_no:
            
            return