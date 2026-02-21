from PyQt5.QtWidgets import (QWidget, QMessageBox, QApplication, QListWidget, QListWidgetItem, 
                            QLabel, QHBoxLayout, QPushButton, QHeaderView )
from PyQt5.QtCore import QSize, QPoint, Qt, QDate
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5 import QtGui, QtCore
import os
from ..elementos_graficos_a_py import Ui_VistaGeneralAsistenciaAlumnos
from ..utilidades.funciones_sistema import FuncionSistema
from datetime import datetime, date
from configuraciones.configuracion import app_configuracion
from ..utilidades.base_de_datos import (especialidad_servicio, alumno_servicio, asistencia_alumno_servicio,
                                        inscripcion_servicio, permiso_servicio)

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
        
        # Esta variable es para guardar la lista de los alumnos que se muestran en la tabla
        self.lista_alumnos_en_tabla = None
        
        # esta lista guardara los empleados que se agreguen a la lista de asistencias
        self.lista_agregados = []
        
        # esto es para el metodo de agregar al empleado a la lista 
        self.indice = 0
        
        self.lista_qlineedits = (self.input_cedula_alumno, self.input_dia_feriado)
        self.lista_radiobuttons = (self.radioButton_inasistente, self.radioButton_asistente)
        self.lista_widget_por_deshabilitar = (self.input_cedula_alumno, self.input_dia_feriado,
                                              self.radioButton_inasistente, self.radioButton_asistente,
                                              self.boton_agregar, self.boton_registrar_dia_feriado, self.boton_especialidades,
                                              self.checkbox_estado_combobox, self.boton_cancelar_registro, self.dateedit_fecha_asistencia,
                                              self.boton_agregar
                                              )
        
        
        self.checkbox_estado_combobox.setText("Activado")
        self.checkbox_estado_combobox.setChecked(True)
        
        # definimos el modelo para el qtableview
        self.modelo = QStandardItemModel()
        
        self.tbl_asistencias_registradas.horizontalHeader().setVisible(True)

        self.tbl_asistencias_registradas.horizontalHeader().setMinimumHeight(50)
        self.tbl_asistencias_registradas.horizontalHeader().setMinimumWidth(10)
        self.tbl_asistencias_registradas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tbl_asistencias_registradas.horizontalHeader().setSectionsClickable(False)


        self.tbl_asistencias_registradas.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tbl_asistencias_registradas.verticalHeader().setVisible(True)
        #self.tbl_asistencias_registradas.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tbl_asistencias_registradas.verticalHeader().setMinimumWidth(20)
        self.tbl_asistencias_registradas.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.tbl_asistencias_registradas.verticalHeader().setFixedWidth(20)
        #esto me da el valor de la cedula al darle click a la persona que quiero
        self.tbl_asistencias_registradas.clicked.connect(lambda index: print(index.sibling(index.row(), 0).data()))

        # Opcional: desactivar clic en el encabezado vertical
        self.tbl_asistencias_registradas.verticalHeader().setSectionsClickable(True)
        

        self.msg_box = QMessageBox(self)
        
        # Crear botones personalizados
        self.boton_si = self.msg_box.addButton("Sí", QMessageBox.YesRole)
        self.boton_no = self.msg_box.addButton("No", QMessageBox.NoRole)
                
        self.input_cedula_alumno.setDisabled(True)
        
        FuncionSistema.cargar_elementos_para_el_combobox(lista_especialidades, self.boton_especialidades, 1, 1)
        FuncionSistema.cargar_elementos_para_el_combobox(lista_especialidades, self.boton_filtro_especialidades, 1, 0)
        
        # Conexion de botones
        
        self.boton_crear_registro.clicked.connect(lambda: self.crear_nuevo_registro_asistencia())
        self.boton_cancelar_registro.clicked.connect(lambda: self.cancelar_registro_asistencia())
        self.boton_especialidades.currentIndexChanged.connect(lambda: self.actualizar_lista_busqueda())
        self.checkbox_estado_combobox.clicked.connect(lambda: self.verficacion_combobox())
        self.boton_agregar.clicked.connect(lambda: self.agregar_info())
        self.boton_suministrar.clicked.connect(lambda: self.suministrar_info())
        self.dateedit_filtro_fecha_asistencia.dateChanged.connect(lambda: self.filtra_alumnos_por_fecha_de_asistencia_y_especialidad())
        self.boton_filtro_especialidades.currentIndexChanged.connect(lambda: self.filtra_alumnos_por_fecha_de_asistencia_y_especialidad())
        self.boton_de_regreso.clicked.connect(lambda: self.regresar_pantalla_anterior())
        self.boton_establecer_dia_feriado.clicked.connect(self.habilitar_campos_dia_feriado)
        self.boton_registrar_dia_feriado.clicked.connect(self.registrar_dia_feriado)

        self.dateedit_fecha_asistencia.setDate(QDate.currentDate())
        self.dateedit_filtro_fecha_asistencia.setDate(QDate.currentDate())

        
        
        
        
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
                FuncionSistema.configurar_barra_de_busqueda(self, self.input_cedula_alumno, self.lista_alumnos_actual, 1, 2, 3, self.label_nombre_alumno_guia)
                
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
    
    
    def filtra_alumnos_por_fecha_de_asistencia_y_especialidad(self):
        """
            Este metodo sirve para filtrar a los alumnos por la fecha en la que registraron la asistencia y su especialidad
        """
        
        try:
            fecha = date(self.dateedit_filtro_fecha_asistencia.date().year(),
                                self.dateedit_filtro_fecha_asistencia.date().month(), 
                                self.dateedit_filtro_fecha_asistencia.date().day() )
            
            especialidad_id = FuncionSistema.buscar_id_por_nombre_del_elemento(self.boton_filtro_especialidades.currentText(), lista_especialidades, 0)
    
            alumnos = asistencia_alumno_servicio.obtener_por_fecha_asistencia_y_especialidad(fecha, especialidad_id)
            

        except Exception as e:
            print(f"A ocorrido un error el metodo de filtra_alumnos_por_fecha_de_asistencia: {e}")
            self.modelo.removeRows(0, self.modelo.rowCount())
        else:
            
            if len(alumnos) == 0:
                self.modelo.removeRows(0, self.modelo.rowCount())
                #print("lista vacia")
            else:
                self.lista_alumnos_en_tabla = alumnos
                self.cargar_alumnos_en_tabla(self.tbl_asistencias_registradas, alumnos)
            
            
            
    ################################################################
    
    def cargar_alumnos_en_tabla(self, tabla, alumnos):
        columnas = [
            "Matricula", "Nombre", "Apellido", "Estado de asistencia", 
            "Dia No laborable", "Opciones"
            
        ]

        
        self.modelo = QStandardItemModel()
        self.modelo.setHorizontalHeaderLabels(columnas)

        # Primero cargamos los datos
        for indice, alumno in enumerate(alumnos):
            datos_visibles = [
            alumno[3],  # Matricula
            alumno[4],  # Nombre
            alumno[5],  # Apellido
            "Asistente" if alumno[7] else "Inasistente",  # Estado de asistencia
            "Ninguno" if alumno[8] == None else alumno[8],  # Dia no Laborable
            ]

            items = []
            for dato in datos_visibles:
                item = QStandardItem(str(dato) if dato is not None else "")
                # Evita edición del usuario
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                items.append(item)

            # Agregar la fila completa
            self.modelo.appendRow(items)

            # Numerar filas en el encabezado vertical
            header_item = QStandardItem(str(indice + 1))
            header_item.setFlags(Qt.ItemIsEnabled)
            self.modelo.setVerticalHeaderItem(indice, header_item)
            
        # Muy importante: asignar self.modelo primero
        tabla.setModel(self.modelo)
        
            # AJUSTES DE ALTURA DE FILAS
        for fila in range(self.modelo.rowCount()):
            tabla.setRowHeight(fila, 40)
        
        # Ahora sí añadimos los botones fila por fila
        for fila in range(self.modelo.rowCount()):
            widget = QWidget()
            layout = QHBoxLayout(widget)
            boton_editar = QPushButton("Editar")
            boton_editar.setFixedSize(60, 30)
            boton_editar.setStyleSheet("""
                    QPushButton{
                        font-size:8pt;
                    }
            """) 
            boton_editar.setProperty("tipo", "boton_editar")
            boton_borrar = QPushButton("Borrar")
            boton_borrar.setFixedSize(60, 30) 
            boton_borrar.setProperty("tipo", "boton_borrar")
            boton_borrar.setStyleSheet("""
                    QPushButton{
                        font-size:8pt;
                    }
            """) 
            

            # Conectar botones
            boton_editar.clicked.connect(lambda _, fila=fila: self.obtener_info_alumno_para_editar(fila))
            boton_borrar.clicked.connect(lambda _, fila=fila: self.eliminar_registro_de_asistencia_del_alumno(fila))

            layout.addWidget(boton_editar)
            layout.addWidget(boton_borrar)
            layout.setContentsMargins(3, 3, 3, 3)
            widget.setLayout(layout)
            
            index = self.modelo.index(fila, len(columnas) - 1)  # última columna ("Opciones")
            tabla.setIndexWidget(index, widget)

    
    
    
    
    
    def crear_nuevo_registro_asistencia(self):
        """
            Este metodo sirve para empezar a crear un nuevo registro de asistencia de los empleados, hace lo siguiente
            
            1. Al darle click al boton nuevo registro este cambia el stackedWidget que esta en el frame inferior a la posicion 1 en donde tiene el QListWidget
            2. Deshabilita el boton crear nuevo registro, para que los dos botones tenga efecto switch
            3. Habilitamos los campos que se utilizan para el registro (los QLineEdits, RadioButton, QDateEdit, QTimeEdit)
            4. Habilita el boton de cancelar registro
            
        """
        print("Proceso de crear registro de asistencia")
        
        self.ventanas_registro_asistencia.setCurrentIndex(1)
        self.boton_crear_registro.setEnabled(False)
        self.boton_especialidades.setEnabled(True)
        self.boton_especialidades.setCurrentIndex(0)
        self.checkbox_estado_combobox.setEnabled(True)
        self.boton_cancelar_registro.setEnabled(True)
        self.boton_establecer_dia_feriado.setEnabled(False)
        self.area_scroll.verticalScrollBar().setValue(0)
        #self.dateedit_filtro_fecha_asistencia.setEnabled(False)
    
        
        
        
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
        print("Proceso de cancelar registro de asistencia")
        
        self.msg_box.setIcon(QMessageBox.Information)
        self.msg_box.setWindowTitle("Confirmar acción")
        self.msg_box.setText("¿Seguro que quiere cancelar el registro?")
        self.msg_box.setInformativeText("Esto borrara lo que lleva registrando hasta el momento.")
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
            self.boton_establecer_dia_feriado.setEnabled(True)
            
            self.boton_especialidades.setCurrentIndex(0)
            FuncionSistema.habilitar_o_deshabilitar_widget_de_qt(self.lista_widget_por_deshabilitar, False)
            FuncionSistema.limpiar_inputs_de_qt(self.lista_qlineedits, self.lista_radiobuttons)         
            
            
            FuncionSistema.cambiar_estilo_del_boton(self.boton_agregar, "boton_anadir", "agregar")
            self.boton_agregar.setEnabled(False)
            self.boton_agregar.clicked.disconnect()
            self.boton_agregar.clicked.connect(self.agregar_info)
            
            self.area_scroll.verticalScrollBar().setValue(0)
            self.msg_box.setInformativeText("")
            
        if self.msg_box.clickedButton() == self.boton_no:
            
            return
     
     
    def limpiar_lista_de_asistencias(self):
        
        print("Procese de limpieza del QListWidget que contiene la lista de asistencia")
        
        
        self.msg_box.setWindowTitle("Confirmar acción")
        self.msg_box.setText("¿Seguro que quiere borrar la lista y empezar de nuevo?")
        self.msg_box.setIcon(QMessageBox.Warning)
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
            
            # establecemos el indice 0 del combo box
            self.boton_especialidades.setCurrentIndex(0)
            
            # limpiamos el input
            self.input_cedula_alumno.clear()
            
            # limpiamos los inputs
            FuncionSistema.limpiar_inputs_de_qt(self.lista_qlineedits, self.lista_radiobuttons)
            
            # restablecemos la lista de empleados actuales de la bd
            self.actualizar_lista_busqueda()
            
        if self.msg_box.clickedButton() == self.boton_no:
            
            return
        
    
    def eliminar_alumno_de_lista(self, alumno):
        """
            Metodo para eliminar al empleado de la lista en donde estan todos los empleados actuales
            esto es para que cuando agregue un empleado la lista de la barra de busqueda no muestre el 
            empleado que ya fue agregado a la lista de asistencias
        
        """
        if alumno in self.lista_alumnos_actual:
                            
            self.lista_agregados.append(alumno)
            
            self.lista_alumnos_actual.remove(alumno)
     
            
    def obtener_info_alumno_para_editar(self, fila):
        """
            Este metodo sirve para actualizar/editar el registro de asistencia del alumno
        """
    
        try:
            permiso_editar_registro_asistencia = permiso_servicio.verificar_permiso_usuario(app_configuracion.USUARIO_ID, "ACTUALIZAR ALUMNOS")
            
            if permiso_editar_registro_asistencia:
                self.msg_box.setWindowTitle("Confirmar acción")
                self.msg_box.setText(f"¿Seguro que quiere editar el registro ?")
                self.msg_box.setIcon(QMessageBox.Question)
                QApplication.beep()

                # Mostrar el cuadro de diálogo y esperar respuesta
                self.msg_box.exec_()

                if self.msg_box.clickedButton() == self.boton_si:  
        
                    matricula = self.modelo.item(fila, 0).text()
                    asistencia_alumno_id = FuncionSistema.buscar_id_por_cedula(matricula, self.lista_alumnos_en_tabla)
                    
                    # (348, 1, 'Artesanía', 'MAT-1234567', 'Ariana', 'Mijares', datetime.date(2026, 2, 20), True, None)
                    asistencia_alumno = asistencia_alumno_servicio.obtener_asistencia_alumno_por_id(asistencia_alumno_id)
                    
                    self.dateedit_fecha_asistencia.setEnabled(True)
                    self.dateedit_fecha_asistencia.setDate(asistencia_alumno[6])
                    
                    inscripcion_alumno = inscripcion_servicio.obtener_inscripcion_por_num_matricula(matricula)
                    cedula_alumno = inscripcion_alumno[1]
                    inscripcion_id = inscripcion_alumno[0]
                    nombre_y_apellido = asistencia_alumno[4] + " " + asistencia_alumno[5]
                    self.label_nombre_alumno_guia.setText(nombre_y_apellido)
                    self.input_cedula_alumno.setText(cedula_alumno)
                    
                    FuncionSistema.habilitar_o_deshabilitar_widget_de_qt(self.lista_radiobuttons, True)
                    estado_asistencia = asistencia_alumno[7]
                    if estado_asistencia:
                        self.radioButton_asistente.setChecked(True)
                    else:
                        self.radioButton_inasistente.setChecked(True)
                        
                    FuncionSistema.cambiar_estilo_del_boton(self.boton_agregar, "boton_editar")
                    self.boton_agregar.setEnabled(True)
                    self.boton_agregar.clicked.disconnect()
                    self.boton_agregar.clicked.connect(lambda: self.editar_informacion_del_registro_asistencia(inscripcion_id, asistencia_alumno_id))
                    
                    self.boton_cancelar_registro.setEnabled(True)
                    self.boton_crear_registro.setEnabled(False)
        
        except Exception as e:
            print(F"No lo puede editar: {e}")
            QMessageBox.warning(self, "No puede", f"{e}")
            
            
    def editar_informacion_del_registro_asistencia(self, inscripcion_id, asistencia_alumno_id):
        """
            Este metodo sirve para suministrar la informacion editada/actualizada del registro de asistencia del alumno a la base de datos de la siguiente manera:
            
            1. le preguntamos al usuario si esta seguro de editar el registro
            2. si es asi tomamos los datos de los campos y lo suministramos al servicioasistencia_alumno_servicio.actualizar_asistencia_alumno
            3. si no hay problemas le avisamos al usuario que todo salio bien y dejamos todo en su estado inicial
        """
        
        try:
            
            
            self.msg_box.setWindowTitle("Confirmar edición")
            self.msg_box.setText(f"¿Seguro que quiere editar el registro de asistencia?")
            self.msg_box.setIcon(QMessageBox.Question)
            QApplication.beep()

            # Mostrar el cuadro de diálogo y esperar respuesta
            self.msg_box.exec_()

            if self.msg_box.clickedButton() == self.boton_si:
                fecha = date(self.dateedit_filtro_fecha_asistencia.date().year(),
                                    self.dateedit_filtro_fecha_asistencia.date().month(), 
                                    self.dateedit_filtro_fecha_asistencia.date().day() )
                
                if self.radioButton_asistente.isChecked():
                    estado_asistencia = True
                if self.radioButton_inasistente.isChecked():
                    estado_asistencia = False

                dia_no_laborable = None
                
                campos_asistencia_alumnos = {
                "inscripcion_id": inscripcion_id,
                "fecha_asistencia": fecha,
                "estado_asistencia": estado_asistencia,
                "dia_no_laborable": dia_no_laborable
                }
            
                asistencia_alumno_servicio.actualizar_asistencia_alumno(asistencia_alumno_id, campos_asistencia_alumnos)
                QMessageBox.information(self, "Proceso exitoso", "El registro fue editado correctamente")
                
                # restablecemos la lista de empleados actuales de la bd
                self.actualizar_lista_busqueda()
                self.ventanas_registro_asistencia.setCurrentIndex(0)
                self.boton_especialidades.setCurrentIndex(0)
                
                FuncionSistema.limpiar_inputs_de_qt(self.lista_qlineedits, self.lista_radiobuttons)
                FuncionSistema.habilitar_o_deshabilitar_widget_de_qt(self.lista_widget_por_deshabilitar, False)

                self.dateedit_filtro_fecha_asistencia.setEnabled(True)
                
                # Filtramos la asistencia actual
                self.dateedit_filtro_fecha_asistencia.setDate(QDate.currentDate())
                
                self.filtra_alumnos_por_fecha_de_asistencia_y_especialidad()
                
                FuncionSistema.cambiar_estilo_del_boton(self.boton_agregar, "boton_anadir", "agregar")
                self.boton_agregar.setEnabled(False)
                self.boton_agregar.clicked.disconnect()
                self.boton_agregar.clicked.connect(self.agregar_info)
                
            if self.msg_box.clickedButton() == self.boton_no:
                
                # restablecemos la lista de empleados actuales de la bd
                self.actualizar_lista_busqueda()
                self.ventanas_registro_asistencia.setCurrentIndex(0)
                self.boton_especialidades.setCurrentIndex(0)
                
                FuncionSistema.limpiar_inputs_de_qt(self.lista_qlineedits, self.lista_radiobuttons)
                FuncionSistema.habilitar_o_deshabilitar_widget_de_qt(self.lista_widget_por_deshabilitar, False)

                self.dateedit_filtro_fecha_asistencia.setEnabled(True)
                
                # Filtramos la asistencia actual
                self.dateedit_filtro_fecha_asistencia.setDate(QDate.currentDate())
                
                self.filtra_alumnos_por_fecha_de_asistencia_y_especialidad()
                
                FuncionSistema.cambiar_estilo_del_boton(self.boton_agregar, "boton_anadir", "agregar")
                self.boton_agregar.setEnabled(False)
                self.boton_agregar.clicked.disconnect()
                self.boton_agregar.clicked.connect(self.agregar_info)
                    
        except Exception as e:
            print(F"No lo puede editar: {e}")
            QMessageBox.warning(self, "No puede", f"{e}")
            
    
    def eliminar_registro_de_asistencia_del_alumno(self, fila):
        """
            Este metodo sirve para eliminar el registro de asistencia del alumno, de la siguiente manera:
            
            1. verificamos si tiene el permiso necesario
            2. si lo tiene le preguntamos si esta seguro de realizar la eliminacion
            3. si esta seguro buscamos el id de la asistencia del alumno y se la pasamos al servicio asistencia_alumno_servicio.eliminar_asistencia_alumno
            4. si todo sale bien le avisamos al usuario que el proceso ha sido exitoso
            5. en caso de que no tenga el permiso de eliminar le saldran un mensaje en pantalla
        """
        matricula = self.modelo.item(fila, 0).text()
        nombre = self.modelo.item(fila, 1).text()
        apellido = self.modelo.item(fila, 2).text()
        
        try:
            permiso_eliminar_registro_asistencia = permiso_servicio.verificar_permiso_usuario(app_configuracion.USUARIO_ID, "ELIMINAR ALUMNOS")
            
            if permiso_eliminar_registro_asistencia:
                self.msg_box.setWindowTitle("Confirmar eliminación")
                self.msg_box.setText(f"¿Seguro que quiere eliminar a {nombre} {apellido} del registro de asistencia?")
                self.msg_box.setIcon(QMessageBox.Question)
                QApplication.beep()

                # Mostrar el cuadro de diálogo y esperar respuesta
                self.msg_box.exec_()

                if self.msg_box.clickedButton() == self.boton_si:      
                    asistencia_alumno_id = FuncionSistema.buscar_id_por_cedula(matricula, self.lista_alumnos_en_tabla)
                    asistencia_alumno_servicio.eliminar_asistencia_alumno(asistencia_alumno_id)
                    QMessageBox.information(self, "Preceso exitoso", "El registro fue eliminado correctamente")
                    self.filtra_alumnos_por_fecha_de_asistencia_y_especialidad()
                    
        
        except Exception as e:
            print(F"No lo puede eliminar: {e}")
            QMessageBox.warning(self, "No puede", f"{e}")
            
      
    def habilitar_campos_dia_feriado(self):
        """
            Este metodo sirve para habilitar los campos para establecer el dia feriado para el registro de asistencia
        """
        self.msg_box.setWindowTitle("Confirmar acción")
        self.msg_box.setText(f"¿Seguro que quiere establecer un dia feriado para el registro de asistencia?")
        self.msg_box.setIcon(QMessageBox.Question)
        QApplication.beep()

        # Mostrar el cuadro de diálogo y esperar respuesta
        self.msg_box.exec_()

        if self.msg_box.clickedButton() == self.boton_si:
            self.input_dia_feriado.setEnabled(True)
            self.boton_registrar_dia_feriado.setEnabled(True)
            self.boton_crear_registro.setEnabled(False)
            self.boton_establecer_dia_feriado.setEnabled(False)
            self.boton_cancelar_registro.setEnabled(True)
            self.dateedit_fecha_asistencia.setEnabled(True)
            
            
        
        
    def registrar_dia_feriado(self):
        """
            Este metodo funciona para registrar a todos los alumnos con el dia feriado que se establezca
        """
        
        try:
            
            self.msg_box.setWindowTitle("Confirmar acción")
            self.msg_box.setText(f"¿Seguro que quiere establecer un dia feriado para el registro de asistencia?")
            self.msg_box.setInformativeText("Esto registrara a todos los alumnos inasistentes y con el dia feriado establecido.")
            self.msg_box.setIcon(QMessageBox.Question)
            QApplication.beep()

            # Mostrar el cuadro de diálogo y esperar respuesta
            self.msg_box.exec_()

            if self.msg_box.clickedButton() == self.boton_si:
                
                if not self.input_dia_feriado.text() == "":
                    fecha = date(self.dateedit_filtro_fecha_asistencia.date().year(),
                                        self.dateedit_filtro_fecha_asistencia.date().month(), 
                                        self.dateedit_filtro_fecha_asistencia.date().day() )
                    
                    alumnos = alumno_servicio.obtener_todos_alumnos()
                    dia_no_laborable = self.input_dia_feriado.text().strip()
                    for alumno in alumnos:
                        alumno_id = alumno[0]
                        
                        campos_asistencia_alumnos = {
                            "inscripcion_id": alumno_id,
                            "fecha_asistencia": fecha,
                            "estado_asistencia": False,
                            "dia_no_laborable": dia_no_laborable.capitalize()
                        }
                        
                        
                        asistencia_alumno_servicio.registrar_asistencia_alumno(campos_asistencia_alumnos)
                    
                    QMessageBox.information(self, "Proceso exitoso", "Se a registrado correctamente la asistencia con el dia feriado")

                    self.input_dia_feriado.setEnabled(False)
                    self.boton_registrar_dia_feriado.setEnabled(False)
                    self.boton_crear_registro.setEnabled(True)
                    self.boton_establecer_dia_feriado.setEnabled(True)
                    self.boton_cancelar_registro.setEnabled(False)
                    self.dateedit_fecha_asistencia.setEnabled(False)
                    self.input_dia_feriado.clear()
                    self.input_dia_feriado.setEnabled(False)
                    self.boton_registrar_dia_feriado.setEnabled(False)
                    self.msg_box.setInformativeText("")
                    
                    # Filtramos la asistencia actual
                    self.filtra_alumnos_por_fecha_de_asistencia_y_especialidad()
                    
                else:
                    QMessageBox.warning(self, "Campo vacio", "Si va a establecer un dia feriado debe de llenar el campo (Dia Feriado)")
                    self.input_dia_feriado.setFocus()
                
            if self.msg_box.clickedButton() == self.boton_no:
                self.input_dia_feriado.setEnabled(False)
                self.boton_registrar_dia_feriado.setEnabled(False)
                self.dateedit_fecha_asistencia.setEnabled(False)
                self.boton_crear_registro.setEnabled(True)
                self.boton_establecer_dia_feriado.setEnabled(True)
                self.boton_cancelar_registro.setEnabled(False)
                self.input_dia_feriado.clear()
                
        
            
        except:
            print("No se puedo registrar el dia feriado")
            
            
            
    def agregar_info(self):
        
        """
        Metodo para agregar la informacion a la lista de asistencias
        """
        try: 
            
            """
                Primero verificamos que el usuario haya seleccionado un estado de asistencia
                asistente o inasistente.
                
                SI ninguno de los estados de asistencia esta seleccionado entonces
                
            """
            if self.radioButton_asistente.isChecked() == False and self.radioButton_inasistente.isChecked() == False:
                
                # le avisamos al usuario que seleccione un estado de asistencia
                QMessageBox.warning(self, "Error", "Por favor, seleccione si el alumno asistió o no.")
                
                
                return
            
            else:
                
                # Hacemos una lista que sera el carrito
                alumno_n = []
                
                # Guardamos la cedula que es lo que utilizaremos
                cedula = self.input_cedula_alumno.text().strip()
                
                # y buscamos el id del alumnos con el metodo self.buscar_id_alumno
                alumno_id = FuncionSistema.buscar_id_por_cedula(cedula, self.lista_alumnos_actual)
                
                
                # si algun elemento (la cedula) no esta en la tupla entonces
                if not any(cedula in alumno[1] for alumno in self.lista_alumnos_actual):
                    
                    # avisamos que ya existe en la lista de asistencia o que la persona no esta en la bd
                    QMessageBox.warning(self, "Error", "La persona ya esta agregada o no existe")
                    return
                
                # buscamos al alumno por el id
                alumno = inscripcion_servicio.obtener_inscripcion_por_id(alumno_id)
                
                            
                
                # la lista se compone de: id_alumno, fecha_asistencia,
                # motivo_inasistencia, cedula, nombre y apellido del empleado 
                # (estas 3 ultimas son para mostrar nada mas)
                
                # 0) alumno ID
                alumno_n.append(alumno_id)
                
                # 1) Fecha de asistencia
                dia_actual = date(self.dateedit_fecha_asistencia.date().year(), self.dateedit_fecha_asistencia.date().month(), self.dateedit_fecha_asistencia.date().day())
                alumno_n.append(dia_actual)
                
                
                # 2) Estado de asistencia
                if self.radioButton_asistente.isChecked():
                    estado_asistencia = 1
                    alumno_n.append(estado_asistencia)
                
                elif self.radioButton_inasistente.isChecked():
                    estado_asistencia = 0
                    alumno_n.append(estado_asistencia)
                    
                    
                
                # 3) cedula
                alumno_n.append(cedula)
                
                #4) nombre
                alumno_n.append(alumno[2])
                
                #5) apellido
                alumno_n.append(alumno[3])
                
                
                # el texto que quiero mostrar en la lista de asistencias es : Cedula - Nombre Apellido
                texto_a_mostrar = f"{alumno_n[3]} - {alumno_n[4]} {alumno_n[5]}"
                
                # lo transformamos en un tupla
                alumno_n = tuple(alumno_n)
                
                
                
                
                print(f"la lista es {alumno_n}")
                
                
                    
                
                
                # si la lista tiene una longitud mayor a 0
                # esto se hace para evitar errores al insertar al primer elemento a la lista de asistencia
                
                if not len(self.lista_de_asistencias) > 0:
                
                    # si alumno_n no esta en la lista de asistencia
                    # Agregaremos los elementos al "carrito"
                    if not alumno_n in self.lista_de_asistencias:
                        
                        
                        # eliminamos el alumno de la lista temporalmente
                        # (OJO se elimina aqui en la logica segun lo que se quiere, no se elimina de la base de datos)
                        self.eliminar_alumno_de_lista(alumno)
                        
                        
                        #print(alumno_n)
                        
                        # si no esta los agrega a la lista de asistencia
                        self.lista_de_asistencias.append(alumno_n)
                        
                        
                        # lo agrega al "carrito"
                        self.agg_alumno_a_lista(self.lista_asistencias_en_cola, self.lista_de_asistencias, self.input_cedula_alumno, texto_a_mostrar)

                        # Limpiamos los inputs
                        FuncionSistema.limpiar_inputs_de_qt(self.lista_qlineedits, self.lista_radiobuttons)
                        
                        
                        
                        
                        
                    # SI el alumno esta en la lista de asistencia que no lo agregue
                    else:
                        # Avisamos en al usuario
                        QMessageBox.warning(self, "Error", "Persona ya agregada")
                        
                        # Limpiamos los inputs
                        FuncionSistema.limpiar_inputs_de_qt(self.lista_qlineedits, self.lista_radiobuttons)
                        
                        return
                    
                # Aqui si la lista de asistencia tiene una longitud mayor a 0, es decir
                # que tiene a una persona agregada
                else:
                    
                    # Verificamos si la cedula del alumno de la lista alumno_n, esta en la lista de asistencia buscando por indice y por cedula
                    # si no esta lo agregamos, si lo esta no lo agregamos
                    if not alumno_n[3] in self.lista_de_asistencias[self.indice][3] or not alumno_n[3] == self.lista_de_asistencias[self.indice][3]:
                        
                        # si no esta los agrega a la lista de asistencia
                        self.lista_de_asistencias.append(alumno_n)
                        
                        
                        self.eliminar_alumno_de_lista(alumno)
                        
                        # lo agrega al "carrito"
                        self.agg_alumno_a_lista(self.lista_asistencias_en_cola, self.lista_de_asistencias, self.input_cedula_alumno, texto_a_mostrar)

                        # Limpiamos los inputs
                        FuncionSistema.limpiar_inputs_de_qt(self.lista_qlineedits, self.lista_radiobuttons)
                        
                        # y le sumamos uno al indice para saber la posicion actual
                        self.indice += 1
                        
                    
                    else:
                        
                        QMessageBox.warning(self, "Error", "Persona ya agregada")
                        # Limpiamos los inputs
                        FuncionSistema.limpiar_inputs_de_qt(self.lista_qlineedits, self.lista_radiobuttons)
                        
                        return
                    
                    
                    
                
                    
                
                # esto es para actualizar cuantas personas hay 
                self.contador_de_asistencias += 1
                self.label_titulo_asistencia.setText(f"Lista actual de asistencias: {self.contador_de_asistencias}")
                self.input_cedula_alumno.clear()
                
                
                

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
        if self.radioButton_asistente.isChecked():
            
                
            label = QLabel(texto_a_mostrar if texto_a_mostrar else f"Elemento {self.list_widget.count() + 1}")
            label.setProperty("tipo", "asistente")
            row_layout.addWidget(label)
            
            
        
        elif self.radioButton_inasistente.isChecked():
            
            label = QLabel(texto_a_mostrar if texto_a_mostrar else f"Elemento {self.list_widget.count() + 1}")
            label.setProperty("tipo", "inasistente")
            row_layout.addWidget(label)

        # Botón para eliminar
        boton_borrar = QPushButton()
        boton_borrar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        boton_borrar.setFixedSize(60,40)
        boton_borrar.setIconSize(QSize(30, 30))
        boton_borrar.setProperty("tipo","boton_borrar")
        
        boton_borrar.clicked.connect(lambda: self.borrar_elementos_a_la_vista_previa(nombre_qlistwidget, nombre_lista, enfoca_input, item))
        row_layout.addWidget(boton_borrar)

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
        
        if not self.lista_agregados[indice_vista_previa] in self.lista_alumnos_actual:
            
            alumno_restaurar = self.lista_agregados[indice_vista_previa]
            
            self.lista_alumnos_actual.append(alumno_restaurar)
            
            self.lista_agregados.remove(alumno_restaurar)
        
        
        # actualizar el contador de asistencias
        self.contador_de_asistencias -= 1
        self.label_titulo_asistencia.setText(f"Lista actual de asistencias: {self.contador_de_asistencias}")
        
        
    
        
        
        ##########################################################################
        # Obtener la fila del item y eliminarlo
        row = nombre_qlistwidget.row(item)
        nombre_qlistwidget.takeItem(row)
    
        print(f"lista actualizada: {nombre_lista}")
    

          
        
    def suministrar_info(self):
        """
            Este metodo sirve para cargar el registro de asistencia de los alumnos a la base de datos
            
            este metodo funciona asi:
            
            - un for va a recorrer self.lista_de_asistencias, que contiene todo lo que se ve en el qlistwidget
            - self.lista_de_asistencias sigue la siguiente estructura:
            
            
            
            self.lista_de_asistencias = [(1, datetime.date(2025, 11, 9), 'PRESENTE', '30466351', 'Ariana', 'Mijares'),
                                         (1, datetime.date(2025, 11, 9), 'PRESENTE', '30466351', 'Ariana', 'Mijares'),
                                         (1, datetime.date(2025, 11, 9), 'PRESENTE', '30466351', 'Ariana', 'Mijares')]
                                         
            donde tenemos: el ID del alumno, la fecha de actual, el estado de asistencia, la cedula, nombre y apellido del alumno
            
            - con el for vamos a pasar el id, la fecha, el estado de asistencia, y el dia laborable (todavia no esta habilitado)
            - y en cada iteracion cargamos cada alumno con le metodo de la base de datos
        
        
        """
        self.msg_box.setWindowTitle("Confirmar registro")
        self.msg_box.setText("¿Seguro que quiere registrar esta lista de asistencia?")
        self.msg_box.setIcon(QMessageBox.Question)
        QApplication.beep()



        # Mostrar el cuadro de diálogo y esperar respuesta
        self.msg_box.exec_()

        if self.msg_box.clickedButton() == self.boton_si:
        
            try:
                
                for alumno in self.lista_de_asistencias:
                    
                    id_alumno = alumno[0]
                    estado_asistencia = alumno[2]
                    
                    
                    
                    campos_asistencia_alumnos = {
                        "inscripcion_id": id_alumno,
                        "fecha_asistencia": date.today(),
                        "estado_asistencia": estado_asistencia,
                        "dia_no_laborable": None
                    }
                    
                    asistencia_alumno_servicio.registrar_asistencia_alumno(campos_asistencia_alumnos)
                
            
            except Exception as e:
                
                FuncionSistema.mostrar_errores_por_excepcion(e, "funcion_suministrar")
                QMessageBox.warning(self, "Error", "Algo salio mal, revise la consola")
                
            
            else:
                
                QMessageBox.information(self, "Proceso exitoso", "Se a registrado correctamente la asistencia")
                
                # Aqui al finalizar, como todo salio bien, deshabilitamos y limpiamos todo
                
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
                self.boton_especialidades.setCurrentIndex(0)
                FuncionSistema.limpiar_inputs_de_qt(self.lista_qlineedits, self.lista_radiobuttons)
                FuncionSistema.habilitar_o_deshabilitar_widget_de_qt(self.lista_widget_por_deshabilitar, False)
                self.boton_agregar.setEnabled(False)
                
                self.dateedit_filtro_fecha_asistencia.setEnabled(True)
                
                # Filtramos la asistencia actual
                self.dateedit_filtro_fecha_asistencia.setDate(QDate.currentDate())
                
                self.filtra_alumnos_por_fecha_de_asistencia_y_especialidad()
                
                
        elif self.msg_box.clickedButton() == self.boton_no:
            return
        
        
    def regresar_pantalla_anterior(self):
        """
            Esta metodo sirve para regresa a la pantalla anterio, pero advirtiendo le al usuario que si se va de
            la pantalla todo su progreso se perdera.
        """
        
        self.msg_box.setWindowTitle("Confirmar registro")
        self.msg_box.setText("¿Seguro que quiere irse de esta pantalla?")
        self.msg_box.setIcon(QMessageBox.Question)
        QApplication.beep()



        # Mostrar el cuadro de diálogo y esperar respuesta
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
                
            FuncionSistema.habilitar_o_deshabilitar_widget_de_qt(self.lista_widget_por_deshabilitar, False)
            FuncionSistema.limpiar_inputs_de_qt(self.lista_qlineedits, self.lista_radiobuttons)
            
            self.boton_crear_registro.setEnabled(True)
            self.area_scroll.verticalScrollBar().setValue(0)
            self.ventanas_registro_asistencia.setCurrentIndex(0)
            self.stacked_widget.setCurrentIndex(2)
            
        elif self.msg_box.clickedButton() == self.boton_no:
            return
        
        
    
        
        