from PyQt5.QtWidgets import (QWidget, QMessageBox, QApplication, QListWidget, QListWidgetItem, 
                            QLabel, QHBoxLayout, QPushButton, QHeaderView )
from PyQt5.QtCore import (QTime, QPoint, Qt, QDate, QSize)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5 import QtGui, QtCore
import os
from ..elementos_graficos_a_py import  Ui_VistaGeneralAsistenciaEmpleados
from ..utilidades.funciones_sistema import FuncionSistema
from datetime import (datetime, time, date)

##################################
# importaciones de base de datos #
##################################

# Repositorios
from repositorios.empleados.empleado_repositorio import EmpleadoRepositorio
from repositorios.empleados.asistencia_empleado_repositorio import AsistenciaEmpleadoRepositorio
from repositorios.empleados.tipo_cargo_repositorio import TipoCargoRepositorio

# Servicios
from servicios.empleados.empleado_servicio import EmpleadoServicio
from servicios.empleados.asistencia_empleado_servicio import AsistenciaEmpleadoServicio
from servicios.empleados.tipo_cargo_servicio import TipoCargoServicio

##################################
# importaciones de base de datos #
##################################

# Instancia del repositorio
empleado_repositorio = EmpleadoRepositorio()
asistetencia_empleado_repositorio = AsistenciaEmpleadoRepositorio()
tipo_cargo_repositorio = TipoCargoRepositorio()

# Instancia del servicio
empleado_servicio = EmpleadoServicio(empleado_repositorio)
asistencia_empleado_servicio = AsistenciaEmpleadoServicio(asistetencia_empleado_repositorio)
tipo_cargo_servicio = TipoCargoServicio(tipo_cargo_repositorio)



# Dia actual
today = datetime.now()
dia_de_hoy = today.strftime("%Y-%m-%d")



class PantallaVistaGeneralAsistenciaEmpleados(QWidget, Ui_VistaGeneralAsistenciaEmpleados):
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
        
        # esta variable es para guardar el id de la asistencia del empleado
        self.asitencia_id = None

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
        
        
        # esto es para el metodo de agregar al empleado a la lista 
        self.indice = 0

        self.lista_qlineedits = (self.input_cedula_empleado, self.input_motivo_retraso, self.input_motivo_inasistencia)
        self.lista_radiobuttons = (self.radioButton_asistente, self.radioButton_inasistente)
        self.lista_timeedits = (self.timeEdit_hora_entrada, self.timeEdit_hora_salida)
        self.lista_widget_por_deshabilitar = (self.input_cedula_empleado, self.input_motivo_retraso, self.input_motivo_inasistencia,
                                              self.radioButton_asistente, self.radioButton_inasistente, self.timeEdit_hora_entrada, 
                                              self.timeEdit_hora_salida, self.boton_cancelar_registro, self.boton_agregar, self.dateedit_fecha_asistencia
                                              )

        self.msg_box = QMessageBox(self)
        
        # Crear botones personalizados
        self.boton_si = self.msg_box.addButton("Sí", QMessageBox.YesRole)
        self.boton_no = self.msg_box.addButton("No", QMessageBox.NoRole)

        
        self.actualizar_lista_busqueda()
        
        self.input_cedula_empleado.textChanged.connect(self.filtrar_resultados)
        self.radioButton_asistente.toggled.connect(lambda: self.cuando_asiste_el_personal())
        self.radioButton_inasistente.toggled.connect(lambda: self.cuando_no_asiste_el_personal())
        self.boton_crear_registro.clicked.connect(lambda: self.crear_nuevo_registro_asistencia())
        self.boton_cancelar_registro.clicked.connect(lambda: self.cancelar_registro_asistencia())
        self.boton_agregar.clicked.connect(lambda: self.agregar_info())
        self.boton_suministrar.clicked.connect(lambda: self.suministrar_asistencias())
        self.boton_limpiar_lista.clicked.connect(lambda: self.limpiar_lista_de_asistencias())
        self.boton_de_regreso.clicked.connect(lambda: self.regresar_pantalla_anterior())
        self.dateedit_filtro_fecha_asistencia.dateChanged.connect(lambda: self.filtrar_asistencia_por_fecha())
        
        self.dateedit_fecha_asistencia.setDate(QDate.currentDate())
        self.dateedit_filtro_fecha_asistencia.setDate(QDate.currentDate())
        
        self.lista_tipo_cargo = tipo_cargo_servicio.obtener_todos_tipos_cargo()
        FuncionSistema.cargar_elementos_para_el_combobox(self.lista_tipo_cargo, self.boton_filtro_tipo_cargo, 1, 1)
        
        # Lista de coincidencias
        self.resultados = QListWidget(self)
        self.resultados.setFocusPolicy(Qt.NoFocus)
        self.resultados.setMouseTracking(True)
        self.resultados.setStyleSheet("padding:10px;")
        self.resultados.itemClicked.connect(self.seleccionar_empleado)
        self.resultados.hide() 
        
        
        
    def actualizar_lista_busqueda(self):
        
        self.lista_empleados_actual = empleado_servicio.obtener_todos_empleados()
        
    
    #################################################################################
    # Metodos para la barra de busqueda (el QLineedit de la cedula del empleado)
    
    
        

    def filtrar_resultados(self, texto):
        texto = texto.strip()
        self.resultados.clear()
        
        if not texto:
            self.resultados.hide()
            self.label_nombre_empleado_guia.clear()
            return
        
        texto_busqueda = texto.lower()
        coincidencias = []
        
        # Buscar coincidencias
        for persona in self.lista_empleados_actual:
            cedula = persona[6]  # Asumo que índice 6 es la cédula
            nombre = persona[1].lower()  # Asumo que índice 1 es el nombre
            apellido = persona[4].lower()  # Asumo que índice 4 es el apellido
            
            # Buscar por cédula exacta o parcial
            if texto_busqueda in cedula or texto_busqueda in nombre:
                coincidencias.append(persona)
        
        if not coincidencias:
            self.resultados.hide()
            self.label_nombre_empleado_guia.clear()
            return
        
        # Mostrar todas las coincidencias en el QListWidget
        for persona in coincidencias:
            cedula = persona[6]
            nombre = persona[1]
            apellido = persona[4]
            item_text = f'{cedula} - {nombre} {apellido}'
            self.resultados.addItem(QListWidgetItem(item_text))
        
        # Si hay UNA SOLA coincidencia y la cédula coincide EXACTAMENTE
        if len(coincidencias) == 1:
            persona_unica = coincidencias[0]
            # Verificar si la cédula ingresada coincide exactamente
            if persona_unica[6] == texto:  # Comparación exacta de cédula
                # Ocultar lista y mostrar nombre en el label
                self.resultados.hide()
                nombre_completo = f"{persona_unica[1].capitalize()} {persona_unica[4].capitalize()}"
                self.label_nombre_empleado_guia.setText(nombre_completo)
                return
            else:
                # Mostrar lista si es coincidencia parcial
                self.mostrar_lista()
                self.label_nombre_empleado_guia.clear()
        else:
            # Mostrar lista si hay múltiples coincidencias
            self.mostrar_lista()
            self.label_nombre_empleado_guia.clear()

    def seleccionar_empleado(self, item):
        """Maneja la selección de un empleado de la lista"""
        # Obtener el texto del item seleccionado
        texto = item.text()
        
        # Extraer la cédula (asumiendo formato "cedula - nombre apellido")
        partes = texto.split(' - ')
        if len(partes) >= 1:
            cedula_seleccionada = partes[0]
            
            # Buscar el empleado correspondiente
            for persona in self.lista_empleados_actual:
                if persona[6] == cedula_seleccionada:
                    # Poner la cédula en el QLineEdit
                    self.input_cedula_empleado.setText(cedula_seleccionada)
                    
                    # Mostrar el nombre en el label
                    nombre_completo = f"{persona[1].capitalize()} {persona[4].capitalize()}"
                    self.label_nombre_empleado_guia.setText(nombre_completo)
                    
                    # Ocultar la lista
                    self.resultados.hide()
                    break

    def mostrar_lista(self):
        """Muestra la lista de resultados debajo del QLineEdit"""
        pos = self.input_cedula_empleado.mapToGlobal(
            QPoint(0, self.input_cedula_empleado.height())
        )
        # Convertir a coordenadas del widget padre si es necesario
        pos = self.parent().mapFromGlobal(pos) if self.parent() else pos
        self.resultados.move(pos)
        self.resultados.resize(self.input_cedula_empleado.width(), 100)
        self.resultados.show()
        self.resultados.raise_()  # Traer al frente
        
    #################################################################################
    def filtrar_asistencia_por_fecha(self):
        
        """
            Este metodo sirve para mostrar las asistencias registradas segun su cargo
        
        """
        
        # Aqui esta el id del tipo de cargo
        #tipo_id_cargo = FuncionSistema.obtener_id_del_elemento_del_combobox(self.boton_filtro_tipo_cargo, self.lista_tipo_cargo, 1, 0, True)
        try:
            
            fecha = date(self.dateedit_filtro_fecha_asistencia.date().year(),
                         self.dateedit_filtro_fecha_asistencia.date().month(), 
                         self.dateedit_filtro_fecha_asistencia.date().day() )
            
            asistencia = asistencia_empleado_servicio.obtener_asistencia_empleado_por_fecha(fecha)
            
        except Exception as e:
            print(f"Algo salio mal en: Filtrar_asistencia_por_fecha: {e}")
            self.modelo.removeRows(0, self.modelo.rowCount())
        else:
            #print("La asistencia es: ")
            #print(asistencia)
            self.cargar_empleados_en_tabla(self.tbl_asistencias_registradas, asistencia)
        
  
    def cargar_empleados_en_tabla(self, tabla, empleados):
        columnas = [
            "Cédula", "Nombre", "Apellido", "Estado de asistencia", 
            "Hora de llegada", "Hora de salida", "Opciones"
            
        ]

        tooltip_text = None
        
        self.modelo = QStandardItemModel()
        self.modelo.setHorizontalHeaderLabels(columnas)

        # Primero cargamos los datos
        for indice, empleado in enumerate(empleados):
            datos_visibles = [
            empleado[2],  # Cedula
            empleado[3],  # Nombre
            empleado[4],  # Apellido
            empleado[6],  # Estado de asistencia
            empleado[7],  # Hora de llegada
            empleado[8],  # Hora de salida
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
            
            if empleado[10] != None:
                # Creamos el texto del tooltip para esta fila
                tooltip_text = f"""<html><head/><body><p><span style=" font-weight:600;">Inasistencia Justificada: {empleado[10]}</span></p></body></html>"""
                
            elif empleado[9] != None:
                # Creamos el texto del tooltip para esta fila
                tooltip_text = f"""<html><head/><body><p><span style=" font-weight:600;">Motivo del retraso: {empleado[9]}</span></p></body></html>"""
                
            if tooltip_text:
                # Aplicamos el tooltip a TODAS las celdas de esta fila
                for col in range(self.modelo.columnCount() - 1):  # -1 para excluir columna Opciones
                    item = self.modelo.item(indice, col)
                    if item:
                        item.setToolTip(tooltip_text)
            
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
            boton_editar.clicked.connect(lambda _, fila=fila: self.habilitar_edicion_del_registro_de_asistencia(fila))
            boton_borrar.clicked.connect(lambda _, fila=fila: print("Borrar"))

            layout.addWidget(boton_editar)
            layout.addWidget(boton_borrar)
            layout.setContentsMargins(3, 3, 3, 3)
            widget.setLayout(layout)
            
            index = self.modelo.index(fila, len(columnas) - 1)  # última columna ("Opciones")
            tabla.setIndexWidget(index, widget)

            
        
    def habilitar_edicion_del_registro_de_asistencia(self, fila):
        
        """
            Este metodo sirve para habilitar la edicion del registro de x empleado.
        """
        # aqui verficamos si el usuario tiene el permiso
        permiso_editar_registro_asistencia = True
        
        if permiso_editar_registro_asistencia:
            
            self.msg_box.setIcon(QMessageBox.Information)
            self.msg_box.setWindowTitle("Confirmar acción")
            self.msg_box.setText("¿Seguro que quiere editar el registro?")
            QApplication.beep()
            self.msg_box.exec_()
            
            if self.msg_box.clickedButton() == self.boton_si:
            
                try:
                    # habilitamos los inputs necesarios
                    FuncionSistema.habilitar_o_deshabilitar_widget_de_qt(self.lista_widget_por_deshabilitar, True)
                    self.input_cedula_empleado.setEnabled(False)
                    
                    # habilitamos el boton de crear registro
                    self.boton_crear_registro.setEnabled(False)
                    
                    # le cambiamos el texto al boton cancelar registro por
                    self.boton_cancelar_registro.setText("Cancelar edición")
                    
                    # le cambiamos el estilo al boton de agregar al estilo de editar 
                    FuncionSistema.cambiar_estilo_del_boton(self.boton_agregar, "boton_editar")
                    
                    # lo desconectamos del metodo que tenga
                    self.boton_agregar.disconnect()
                    
                    
                    # Obtener el texto de la primera columna (nombre)
                    cedula = self.modelo.item(fila, 0).text()

                    # la lista de los empleados registrados
                    lista_empleados = empleado_servicio.obtener_todos_empleados()
                    
                    # obtenemos el id del empleado
                    empleado_id = FuncionSistema.buscar_id_por_cedula(cedula, lista_empleados)
                    
                    # obtenemos la fecha
                    fecha = date(self.dateedit_filtro_fecha_asistencia.date().year(),
                            self.dateedit_filtro_fecha_asistencia.date().month(), 
                            self.dateedit_filtro_fecha_asistencia.date().day() )
                    
                    # obtenemos el registro de la asistencia del empleado con el id del empleado y la fecha
                    asistencia_empleado = asistencia_empleado_servicio.obtener_asistencia_por_empleado_id_y_fecha(empleado_id, fecha)
                    
                    self.asistencia_id = asistencia_empleado[0]
                    
                    # le damos la cedula
                    self.input_cedula_empleado.setText(asistencia_empleado[2])
                    
                    # le damos la fecha
                    self.dateedit_fecha_asistencia.setDate(QDate.fromString(asistencia_empleado[5], "yyyy-MM-dd"))
                    
                    # verficamos si esta presente o ausente
                    if asistencia_empleado[6] == "PRESENTE":
                        self.radioButton_asistente.setChecked(True)
                    elif asistencia_empleado[6] == "AUSENTE":   
                        self.radioButton_inasistente.setChecked(True)
                        
                    # le damos la hora a los qtimeedit
                    self.timeEdit_hora_entrada.setTime(QTime.fromString(asistencia_empleado[7], "h:mm"))
                    self.timeEdit_hora_salida.setTime(QTime.fromString(asistencia_empleado[8], "h:mm")) 
                    
                    # le damos el motivo de retraso y motivo de inasistencia
                    self.input_motivo_retraso.setText(asistencia_empleado[9] if asistencia_empleado[9] != None else None)
                    self.input_motivo_inasistencia.setText(asistencia_empleado[10] if asistencia_empleado[10] != None else None)
                    
                    # conectamos el boton al otro metodo
                    self.boton_agregar.clicked.connect(lambda: self.editar_registro_de_asistencia_empleado())
                    
                    print(f"esta editando a {asistencia_empleado}")
                    
                except Exception as e:
                    FuncionSistema.mostrar_errores_por_excepcion(e, "habilitar_edicion_del_registro_de_asistencia")
                
            if self.msg_box.clickedButton() == self.boton_no:
                
                return
                
        else:
            pass   
            
    
    def editar_registro_de_asistencia_empleado(self):
        """
            Este metodo sirve para editar/actualizar el registro de asistencia del empleado y suministrar la información a la base de datos.
            
            Lo que hacemos es capturas los datos nuevamente como en el registro de asistencia, con la unica diferencia que solo actualizamos/editamos la información
        """
        
        self.msg_box.setIcon(QMessageBox.Information)
        self.msg_box.setWindowTitle("Confirmar acción")
        self.msg_box.setText("¿Modifico los datos correctamente?")
        QApplication.beep()
        self.msg_box.exec_()
        
        if self.msg_box.clickedButton() == self.boton_si:
            
            try:
                
                # obtenemos la fecha
                fecha_asistencia = date(self.dateedit_filtro_fecha_asistencia.date().year(),
                                self.dateedit_filtro_fecha_asistencia.date().month(), 
                                self.dateedit_filtro_fecha_asistencia.date().day() )
                
                # obtenemos las horas
                hora_entrada = time(self.timeEdit_hora_entrada.time().hour() , self.timeEdit_hora_entrada.time().minute())
                hora_salida = time(self.timeEdit_hora_salida.time().hour() , self.timeEdit_hora_salida.time().minute())
                
                # obtenemos el estado de asistencia
                if self.radioButton_asistente.isChecked():
                    estado_asistencia = "PRESENTE"
                elif self.radioButton_inasistente.isChecked():
                    estado_asistencia = "AUSENTE"
                    
                # obtenemos los motivos
                motivo_retraso = self.input_motivo_retraso.text().strip() if not self.input_motivo_retraso.text().strip() == "" else None
                motivo_inasistencia = self.input_motivo_inasistencia.text().strip() == "" if self.input_motivo_inasistencia.text().strip() == "" else None
                
                campos_asistencia_empleados = {
                "fecha_asistencia": fecha_asistencia,
                "hora_entrada": hora_entrada,
                "hora_salida": hora_salida,
                "estado_asistencia": estado_asistencia,
                "motivo_retraso": motivo_retraso,
                "motivo_inasistencia": motivo_inasistencia
                }
                
                asistencia_empleado_servicio.actualizar(self.asistencia_id, campos_asistencia_empleados)
                
            
            except Exception as e:
                FuncionSistema.mostrar_errores_por_excepcion(e, "editar_registro_de_asistencia_empleado")
                
            else:
                QMessageBox.information(self, "Preceso exitoso", "El registro fue editado correctamente")
                self.filtrar_asistencia_por_fecha()
                self.asistencia_id = None
                
                FuncionSistema.cambiar_estilo_del_boton(self.boton_agregar, "boton_anadir")
                self.boton_agregar.disconnect()
                self.boton_agregar.clicked.connect(lambda: self.agregar_info())
                
                FuncionSistema.limpiar_inputs_de_qt(self.lista_qlineedits, self.lista_radiobuttons)
                FuncionSistema.habilitar_o_deshabilitar_widget_de_qt(self.lista_widget_por_deshabilitar, False)
                    
                self.timeEdit_hora_entrada.setTime(QTime(7, 0))  
                self.timeEdit_hora_salida.setTime(QTime(12, 0)) 
                    
        
        if self.msg_box.clickedButton() == self.boton_no:
            return
    
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
        
                
        for qlineedits in self.lista_qlineedits:
            qlineedits.setEnabled(True)
            
        for qradiobutton in self.lista_radiobuttons:
            qradiobutton.setEnabled(True)
            
        for qtimeedit in self.lista_timeedits:
            qtimeedit.setEnabled(True)
        
        self.dateedit_fecha_asistencia.setEnabled(True)
        
        self.boton_agregar.setEnabled(True)
        
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
            
                    
            for qlineedits in self.lista_qlineedits:
                qlineedits.setEnabled(False)
                
            for qradiobutton in self.lista_radiobuttons:
                qradiobutton.setEnabled(False)
                
            for qtimeedit in self.lista_timeedits:
                qtimeedit.setEnabled(False)
                
            self.dateedit_fecha_asistencia.setEnabled(False)
            
            self.boton_agregar.setEnabled(True)
            
            self.boton_cancelar_registro.setEnabled(False)
            
            FuncionSistema.limpiar_inputs_de_qt(self.lista_qlineedits, self.lista_radiobuttons)
            
            self.timeEdit_hora_entrada.setTime(QTime(7, 0))  
            self.timeEdit_hora_salida.setTime(QTime(12, 0))
            
            self.boton_agregar.setEnabled(False)
            
            # esto es para cuando cancele en la edicion
            self.boton_cancelar_registro.setText("Cancelar nuevo registro")
            FuncionSistema.cambiar_estilo_del_boton(self.boton_agregar, "boton_anadir")
            self.boton_agregar.disconnect()
            self.boton_agregar.clicked.connect(lambda: self.agregar_info())
            
        if self.msg_box.clickedButton() == self.boton_no:
            
            return
        
    # Metodo para agregar la informacion a la lista de asistencias
    def agregar_info(self):
        
        try: 
            
            if self.radioButton_asistente.isChecked() == False and self.radioButton_inasistente.isChecked() == False:
                
                QMessageBox.warning(self, "Error", "Por favor, seleccione si el empleado asistió o no.")
                
                
                return
            
            else:
                empleado_n = []
                
                cedula = self.input_cedula_empleado.text().strip()
                empleado_id = FuncionSistema.buscar_id_por_cedula(cedula, self.lista_empleados_actual)
                
                
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
                dia_actual = date(self.dateedit_fecha_asistencia.date().year(), self.dateedit_fecha_asistencia.date().month(), self.dateedit_fecha_asistencia.date().day())

                empleado_n.append(dia_actual)
                
                # 2) Hora de entrada
                
                
                hora_entrada = time(self.timeEdit_hora_entrada.time().hour() , self.timeEdit_hora_entrada.time().minute())

                empleado_n.append(hora_entrada)
                
                # 3) Hora de salida
                hora_salida = time(self.timeEdit_hora_salida.time().hour() , self.timeEdit_hora_salida.time().minute())
                empleado_n.append(hora_salida)
                
                # 4) Estado de asistencia
                if self.radioButton_asistente.isChecked():
                    estado_asistencia = "PRESENTE"
                    empleado_n.append(estado_asistencia)
                
                elif self.radioButton_inasistente.isChecked():
                    estado_asistencia = "AUSENTE"
                    empleado_n.append(estado_asistencia)
                    
                    
                # 5) Motivo de retraso
                if self.input_motivo_retraso.text().strip():
                    motivo_retraso = self.input_motivo_retraso.text().strip()
                    empleado_n.append(motivo_retraso)
                else:
                    empleado_n.append(None)
                    
                    
                # 6) Motivo de inasistencia
                if self.input_motivo_inasistencia.text().strip():
                    motivo_inasistencia = self.input_motivo_inasistencia.text().strip()
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
                        self.agg_empleado_a_lista(self.lista_asistencias_en_cola, self.lista_de_asistencias, self.input_cedula_empleado, texto_a_mostrar)

                        # Limpiamos los inputs
                        FuncionSistema.limpiar_inputs_de_qt(self.lista_qlineedits, self.lista_radiobuttons)
                        
                        
                        
                        
                        
                    
                    else:
                        
                        QMessageBox.warning(self, "Error", "Persona ya agregada")
                        # Limpiamos los inputs
                        FuncionSistema.limpiar_inputs_de_qt(self.lista_qlineedits, self.lista_radiobuttons)
                        
                        return
                    
                else:
                    
                    # Agregamos los elementos al "carrito"
                    if not empleado_n[7] in self.lista_de_asistencias[self.indice][7] or not empleado_n[7] == self.lista_de_asistencias[self.indice][7]:
                        
                        # si no esta los agrega a la lista de asistencia
                        self.lista_de_asistencias.append(empleado_n)
                        
                        
                        self.eliminar_empleado_de_lista(empleado)
                        
                        # lo agrega al "carrito"
                        self.agg_empleado_a_lista(self.lista_asistencias_en_cola, self.lista_de_asistencias, self.input_cedula_empleado, texto_a_mostrar)

                        # Limpiamos los inputs
                        FuncionSistema.limpiar_inputs_de_qt(self.lista_qlineedits, self.lista_radiobuttons)
                        
                        # y le sumamos uno al indice para saber la posicion actual
                        self.indice += 1
                        
                    
                    else:
                        
                        QMessageBox.warning(self, "Error", "Persona ya agregada")
                        # Limpiamos los inputs
                        FuncionSistema.limpiar_inputs_de_qt(self.lista_qlineedits, self.lista_radiobuttons)
                        self.timeEdit_hora_entrada.setTime(QTime(7, 0))  
                        self.timeEdit_hora_salida.setTime(QTime(12, 0)) 
                        
                        return
                    
                    
                    
                
                self.timeEdit_hora_entrada.setTime(QTime(7, 0))  
                self.timeEdit_hora_salida.setTime(QTime(12, 0))  
                
                # esto es para actualizar cuantas personas hay 
                self.contador_de_asistencias += 1
                self.label_titulo_asistencia.setText(f"Lista actual de asistencias: {self.contador_de_asistencias}")
                
                

        except Exception as e:
            print(f"Error al agregar la informacion: {e}")
            
            
    
    def eliminar_empleado_de_lista(self, empleado):
        
        """
            Metodo para eliminar al empleado de la lista en donde estan todos los empleados actuales
            esto es para que cuando agregue un empleado la lista de la barra de busqueda no muestre el 
            empleado que ya fue agregado a la lista de asistencias
        """
        if empleado in self.lista_empleados_actual:
                            
            self.lista_agregados.append(empleado)
            
            self.lista_empleados_actual.remove(empleado)
            
            
    
    def agg_empleado_a_lista(self, nombre_qlistwidget, nombre_lista, enfoca_input, texto_a_mostrar=None):
        
        """
            Metodo "carrito" para agregar a los empleados a la lista de asistencia
        """
        
        
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
        
        
        # Logica para borrar el empleado del QListWidget
        
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
    def cuando_asiste_el_personal(self):
        
        
            self.input_motivo_inasistencia.setDisabled(True)
            self.input_motivo_inasistencia.clear()

            self.timeEdit_hora_entrada.setDisabled(False)
            self.timeEdit_hora_salida.setDisabled(False)
            self.input_motivo_retraso.setDisabled(False)
            


    # Metodo para deshabilitar los inputs si no asistio
    def cuando_no_asiste_el_personal(self):
        
        self.timeEdit_hora_entrada.setDisabled(True)
        self.timeEdit_hora_entrada.setTime(QTime(7,0))

        self.timeEdit_hora_salida.setDisabled(True)
        self.timeEdit_hora_salida.setTime(QTime(12,0))

        self.input_motivo_retraso.setDisabled(True)
        self.input_motivo_retraso.clear()

        self.input_motivo_inasistencia.setDisabled(False)
        self.label_motivo_inasistencia.setDisabled(False)
 
 
    def limpiar_lista_de_asistencias(self):
        """
            Este metodo sirve para limpiar el QListWidget que contiene el "Carrito" que muestra a los empleado que se van
            registrando
        
        """
        
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
                    FuncionSistema.limpiar_inputs_de_qt(self.lista_qlineedits, self.lista_radiobuttons)
                    FuncionSistema.habilitar_o_deshabilitar_widget_de_qt(self.lista_widget_por_deshabilitar, False)
                    self.boton_crear_registro.setEnabled(True)
                    
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
                    
                    self.dateedit_filtro_fecha_asistencia.setDate(QtCore.QDate.currentDate())

                    
                    
                    
                        
            elif self.msg_box.clickedButton() == self.boton_no:
                
                return
                    
                    
            
        except Exception as e:
            
            print(f"algo malo paso en suministrar info : {e}")
            
        else:
            
            self.filtrar_asistencia_por_fecha()
                                    
                          
    def regresar_pantalla_anterior(self):
        """
            Esta metodo sirve para regresa a la pantalla anterio, pero advirtiendo le al usuario que si se va de
            la pantalla todo su progreso se perdera.
        """
        
        self.msg_box.setIcon(QMessageBox.Information)
        self.msg_box.setWindowTitle("Confirmar acción")
        self.msg_box.setText("¿Seguro que quiere irse de esta pantalla?")
        #self.msg_box.setInformativeText("Si se retira de la pantalla esto borrar lo que lleva registrando hasta el momento.")
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
        
            
            FuncionSistema.limpiar_inputs_de_qt(self.lista_qlineedits, self.lista_radiobuttons)
            FuncionSistema.habilitar_o_deshabilitar_widget_de_qt(self.lista_widget_por_deshabilitar, False)
            
            self.boton_crear_registro.setEnabled(True)
            self.ventanas_registro_asistencia.setCurrentIndex(0)
            self.stacked_widget.setCurrentIndex(7)
            
        elif self.msg_box.clickedButton() == self.boton_no:
            
            return  
        
        
    