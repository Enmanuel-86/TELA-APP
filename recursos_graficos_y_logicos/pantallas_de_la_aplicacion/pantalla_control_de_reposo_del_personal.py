from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
from PyQt5.QtCore import (QTime, QPoint, Qt, QDate, QSize)
import os
from datetime import datetime
from PyQt5.QtWidgets import (QWidget, QCalendarWidget, QMessageBox,
                            QApplication)

from ..elementos_graficos_a_py import Ui_VistaGeneralReposoEmpleados, Ui_VentanaAnadirReposo

from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5 import QtGui
from PyQt5.QtCore import (QPoint, Qt)
import os
from PyQt5.QtWidgets import (QWidget, QMessageBox, QApplication, QListWidget, QListWidgetItem, 
                            QLabel, QHBoxLayout, QPushButton, QHeaderView )

from ..elementos_graficos_a_py import Ui_VistaGeneralReposoEmpleados
from recursos_graficos_y_logicos.utilidades.funciones_sistema import FuncionSistema

# IMPORTACIONES DE BASE DE DATOS
from recursos_graficos_y_logicos.utilidades.base_de_datos import reposo_empleado_servicio, empleado_servicio, permiso_servicio
from excepciones.base_datos_error import BaseDatosError
from configuraciones.configuracion import app_configuracion


class PantallaControlRepososPersonal(QWidget, Ui_VistaGeneralReposoEmpleados):
    def __init__(self, stacked_widget):
        super().__init__()


        self.stacked_widget = stacked_widget
        
        self.setupUi(self)
        
        self.msg_box = QMessageBox(self)
        
        # CREAR BOTONES PERSONALIZADOS
        self.boton_si = self.msg_box.addButton("Sí", QMessageBox.YesRole)
        self.boton_no = self.msg_box.addButton("No", QMessageBox.NoRole)
        
        # DEFINIMOS EL MODELO PARA EL QTABLEVIEW
        self.modelo = QStandardItemModel()
        
        # ELEMENTOS DE UTILIDAD
        self.lista_empleados_actual = empleado_servicio.obtener_todos_empleados()
        
        # CONFIGURACIÓN DE LAS SEÑALES
        self.boton_agregar.clicked.connect(self.registrar_reposo)
        self.dateEdit_filtro_fecha_reposo.dateChanged.connect(self.filtrar_reposo_por_fecha)
        self.boton_buscar.clicked.connect(self.filtrar_reposo_por_fecha)
        self.boton_de_regreso.clicked.connect(self.regresar_pantalla_anterior)
        FuncionSistema.configurar_barra_de_busqueda(self, self.input_cedula_empleado, self.lista_empleados_actual, 6, 1, 4, self.label_nombre_empleado_guia)
        self.boton_crear_registro.clicked.connect(self.crear_nuevo_registro)
        self.boton_cancelar_registro.clicked.connect(self.cancelar_nuevo_registro)
        
        self.lista_reposos_registrados = reposo_empleado_servicio.obtener_todos_reposos()
        FuncionSistema.configurar_barra_de_busqueda(self, self.barra_de_busqueda, self.lista_reposos_registrados, 0, 1, 2)
        self.barra_de_busqueda.returnPressed.connect(self.filtrar_por_barra_de_busqueda)
        self.boton_buscar.clicked.connect(self.filtrar_por_barra_de_busqueda)
        
        # ESTABLECIENDO VALORES POR DEFECTO
        self.tbl_reposos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.dateEdit_fecha_solicitud.setDate(QDate.currentDate())
        self.dateEdit_fecha_reingreso.setDate(QDate.currentDate())
        self.dateEdit_filtro_fecha_reposo.setDate(QDate.currentDate())
        
        
        
        
        self.tupla_inputs = (
            self.input_cedula_empleado,
            self.input_motivo_reposo,
            self.barra_de_busqueda
        )
        
        self.tupla_dateedits = (
            self.dateEdit_fecha_solicitud,
            self.dateEdit_fecha_reingreso,
            self.dateEdit_filtro_fecha_reposo
        )
        
        self.tupla_de_campos = (self.input_cedula_empleado, self.input_motivo_reposo, 
                                self.dateEdit_fecha_solicitud, self.dateEdit_fecha_reingreso, 
                                self.boton_agregar
                                )
        
        
    
    def crear_nuevo_registro(self):
        """
            Este metodo sirve para crear un nuevo registro de reposos de la siguiente manera:
            
            Solamente habilitamos todos los campos necesarios
        """
        
        try:
            
            FuncionSistema.habilitar_o_deshabilitar_widget_de_qt(self.tupla_de_campos, True)
            self.boton_cancelar_registro.setEnabled(True)
            self.boton_crear_registro.setEnabled(False)
            
        except Exception as e:
            print(f"No se pudo crear un nuevo registro: {e}")
            
    def cancelar_nuevo_registro(self):
        """
            Este metodo sirve para cancelar el registro de reposo de la siguiente manera:
            
            1. Le preguntamos al usuario si quiere cancelar
            2. Si lo hace se limpian y se deshabilitan los campos
            3. Caso contrario no pasa nada
        """
        try:
            self.msg_box.setIcon(QMessageBox.Information)
            self.msg_box.setWindowTitle("Confirmar acción")
            self.msg_box.setText("¿Seguro que quiere cancelar el registro?")
            QApplication.beep()
            self.msg_box.exec_()
            
            if self.msg_box.clickedButton() == self.boton_si:
            
                FuncionSistema.habilitar_o_deshabilitar_widget_de_qt(self.tupla_de_campos, False)
                FuncionSistema.limpiar_inputs_de_qt(self.tupla_inputs)
                self.boton_cancelar_registro.setEnabled(False)
                self.boton_crear_registro.setEnabled(True)
                
                # en caso de que este en modo edicion
                FuncionSistema.cambiar_estilo_del_boton(self.boton_agregar, "boton_anadir", "registrar")
                self.boton_agregar.disconnect()
                self.boton_agregar.clicked.connect(self.registrar_reposo)
                
            elif self.msg_box.clickedButton() == self.boton_no:
                return
                
                
        except Exception as e:
            print(f"No se pudo cancelar un nuevo registro: {e}")
    
    
    
    def registrar_reposo(self):
        """
        Este método es para registrar un reposo de empleado. El proceso es el siguiente:
        
        - Obtenemos el valor de cada campo: cedula del empleado, motivo del reposo, fecha desde y fecha hasta
        - Guardamos en un diccionario esos valores obtenidos de los campos para validarlos
        - Una vez validado procedemos a registrar el reposo si todo salió correctamente, sino, le mostramos una alerta de los errores cometidos
        - Refrescamos el filtro de los reposos registrados
        - Y limpiamos los campos
        """
        try:
            cedula_empleado = self.input_cedula_empleado.text()
            empleado = empleado_servicio.obtener_empleado_por_cedula(cedula_empleado)
            
            if (empleado):
                empleado_id = empleado[0]
            else:
                empleado_id = None
                
            # MENSAJE PARA CONFIRMAR LA ACCIÓN
            self.msg_box.setIcon(QMessageBox.Information)
            self.msg_box.setWindowTitle("Confirmar acción")
            self.msg_box.setText("¿Seguro que quiere editar este reposo?")
            QApplication.beep()
            self.msg_box.exec_()
            
            if self.msg_box.clickedButton() == self.boton_si:
            
                motivo_reposo = self.input_motivo_reposo.text()
                fecha_desde = self.dateEdit_fecha_solicitud.date().toPyDate()
                fecha_hasta = self.dateEdit_fecha_reingreso.date().toPyDate()
                
                campos_reposo_empleado = {
                    "empleado_id": empleado_id,
                    "motivo_reposo": motivo_reposo,
                    "fecha_emision": fecha_desde,
                    "fecha_reingreso": fecha_hasta
                }
                
                errores = reposo_empleado_servicio.validar_campos_reposo(
                    empleado_id = campos_reposo_empleado.get("empleado_id"),
                    motivo_reposo = campos_reposo_empleado.get("motivo_reposo"),
                    fecha_reingreso = campos_reposo_empleado.get("fecha_reingreso"),
                    fecha_emision = campos_reposo_empleado.get("fecha_emision")
                )
                
                if (errores):
                    QMessageBox.warning(self, "Error al registrar el reposo", "\n".join(errores))
                    return
                
                reposo_empleado_servicio.registrar_reposo(campos_reposo_empleado)
                
                QMessageBox.information(self, "Registro exitoso", "El reposo se ha registrado correctamente.")
                FuncionSistema.habilitar_o_deshabilitar_widget_de_qt(self.tupla_de_campos, False)
                FuncionSistema.limpiar_inputs_de_qt(self.tupla_inputs)
                self.boton_cancelar_registro.setEnabled(False)
                self.boton_crear_registro.setEnabled(True)
            
        except BaseDatosError as error:
            QMessageBox.warning(self, "Error al registrar al usuario", str(error))
            
        else:
            self.lista_reposos_registrados = reposo_empleado_servicio.obtener_todos_reposos()
            FuncionSistema.configurar_barra_de_busqueda(self, self.barra_de_busqueda, self.lista_reposos_registrados, 0, 1, 2)
            self.filtrar_reposo_por_fecha()
    
    def habilitar_edicion_reposo(self, fila):
        """
        Este método es para registrar un habilitar la edición de un reposo de empleado. El proceso es el siguiente:
        
        - A partir del USUARIO_ID de aquella persona que inició sesión en el sistema validamos si tiene el permiso de realizar la edición
        - Si tiene el permiso seteamos los campos del registro específico en los qlineedits y los qdateedits
        - Cambiamos el botón de registrar tanto en apariencia como su señal para que se comporte como botón de editar
        """
        try:
            USUARIO_ID_LOGUEADO = app_configuracion.USUARIO_ID
            # ESTO YA DESPUÉS SERÁ UN PERMISO ESPECÍFICO DE LOS REPOSOS, MIENTRAS TANTO SERÁ ESTE
            permiso_editar_info_reposo = permiso_servicio.verificar_permiso_usuario(USUARIO_ID_LOGUEADO, "ACTUALIZAR EMPLEADOS")
            
            if (permiso_editar_info_reposo):
                # MENSAJE PARA CONFIRMAR LA ACCIÓN
                self.msg_box.setIcon(QMessageBox.Information)
                self.msg_box.setWindowTitle("Confirmar acción")
                self.msg_box.setText("¿Seguro que quiere editar este reposo?")
                QApplication.beep()
                self.msg_box.exec_()
                
                if self.msg_box.clickedButton() == self.boton_si:
                    # TOMAMOS LA CÉDULA DE LA FILA DONDE SE PULSÓ EL BOTÓN DE EDITAR
                    cedula = self.modelo.item(fila, 0).text()
                    
                    # BUSCAMOS AL EMPLEADO POR SU CÉDULA
                    empleado = empleado_servicio.obtener_empleado_por_cedula(cedula)
                    empleado_id = empleado[0]
                    
                    reposo_empleado_id = reposo_empleado_servicio.obtener_reposo_por_empleado_id(empleado_id)[6]
                    reposo_empleado = reposo_empleado_servicio.obtener_reposo_por_id(reposo_empleado_id)
                    
                    self.input_cedula_empleado.setText(reposo_empleado[0])
                    self.input_motivo_reposo.setText(reposo_empleado[3])
                    
                    fecha_solicitud_str = reposo_empleado[4]
                    fecha_solicitud_qt = QDate.fromString(fecha_solicitud_str, "yyyy-MM-dd")
                    self.dateEdit_fecha_solicitud.setDate(fecha_solicitud_qt)
                    
                    fecha_reingreso_str = reposo_empleado[5]
                    fecha_reingreso_qt = QDate.fromString(fecha_reingreso_str, "yyyy-MM-dd")
                    self.dateEdit_fecha_reingreso.setDate(fecha_reingreso_qt)
                    
                    self.boton_agregar.clicked.disconnect()
                    
                    FuncionSistema.cambiar_estilo_del_boton(self.boton_agregar, "boton_editar")
                    self.boton_agregar.clicked.connect(lambda : self.editar_info_reposo(reposo_empleado_id))
                    
                    FuncionSistema.habilitar_o_deshabilitar_widget_de_qt(self.tupla_de_campos, True)
                    self.boton_cancelar_registro.setEnabled(True)
                    self.boton_crear_registro.setEnabled(False)
                    
        except Exception as error:
            QMessageBox.warning(self, "No puede", f"{error}")
    
    
    def editar_info_reposo(self, reposo_empleado_id: int):
        """
        Este método es para editar un reposo de empleado. El proceso es el siguiente:
        
        - Preguntamos si quiere realizar dicha acción
        - Validamos los campos a actualizar
        - Una vez validado los campos procedemos a actualizar el reposo si todo salió correctamente, sino, le mostramos una alerta de los errores cometidos
        - Refrescamos el filtro de los reposos registrados
        - Regresamos a su estado normal del botón registrar
        - Y limpiamos los campos
        """
        self.msg_box.setIcon(QMessageBox.Information)
        self.msg_box.setWindowTitle("Confirmar acción")
        self.msg_box.setText(f"¿Seguro que quiere editar este reposo?")
        QApplication.beep()
        self.msg_box.exec_()
        
        if self.msg_box.clickedButton() == self.boton_si:
            cedula_empleado = self.input_cedula_empleado.text()
            empleado = empleado_servicio.obtener_empleado_por_cedula(cedula_empleado)
            empleado_id = empleado[0]
            
            motivo_reposo = self.input_motivo_reposo.text()
            fecha_desde = self.dateEdit_fecha_solicitud.date().toPyDate()
            fecha_hasta = self.dateEdit_fecha_reingreso.date().toPyDate()
            
            campos_reposo_empleado = {
                "empleado_id": empleado_id,
                "motivo_reposo": motivo_reposo,
                "fecha_emision": fecha_desde,
                "fecha_reingreso": fecha_hasta
            }
            
            errores = reposo_empleado_servicio.validar_campos_reposo(
                empleado_id = campos_reposo_empleado.get("empleado_id"),
                motivo_reposo = campos_reposo_empleado.get("motivo_reposo"),
                fecha_reingreso = campos_reposo_empleado.get("fecha_reingreso"),
                fecha_emision = campos_reposo_empleado.get("fecha_emision"),
                reposo_empleado_id = reposo_empleado_id
            )
            
            if (errores):
                QMessageBox.warning(self, "Error al editar el reposo", "\n".join(errores))
                return
            
            reposo_empleado_servicio.actualizar_reposo(reposo_empleado_id, campos_reposo_empleado)
            QMessageBox.information(self, "Proceso exitoso", f"Se a editado correctamente el reposo")
            
            self.boton_agregar.clicked.disconnect()
            FuncionSistema.cambiar_estilo_del_boton(self.boton_agregar, "boton_anadir")
            self.boton_agregar.clicked.connect(self.registrar_reposo)
            
            self.filtrar_reposo_por_fecha()
            FuncionSistema.limpiar_inputs_de_qt(self.tupla_inputs)
            
        if self.msg_box.clickedButton() == self.boton_no:
            FuncionSistema.habilitar_o_deshabilitar_widget_de_qt(self.tupla_de_campos, False)
            FuncionSistema.limpiar_inputs_de_qt(self.tupla_inputs)
            self.boton_cancelar_registro.setEnabled(False)
            self.boton_crear_registro.setEnabled(True)

            FuncionSistema.cambiar_estilo_del_boton(self.boton_agregar, "boton_anadir", "registrar")
            self.boton_agregar.disconnect()
            self.boton_agregar.clicked.connect(self.registrar_reposo)

    def eliminar_info_reposo(self, fila):
        """
        Este método es para eliminar un reposo de empleado. El proceso es el siguiente:
        
        - A partir del USUARIO_ID de aquella persona que inició sesión en el sistema validamos si tiene el permiso de realizar la edición
        - Si tiene el permiso obtenemos el reposo_empleado_id para proceder con la eliminación de dicho registro seleccionado
        - Refrescamos el filtro de los reposos registrados
        - Y limpiamos los campos
        """
        try:
            USUARIO_ID_LOGUEADO = app_configuracion.USUARIO_ID
            permiso_eliminar_reposos = permiso_servicio.verificar_permiso_usuario(USUARIO_ID_LOGUEADO, "ELIMINAR EMPLEADOS")
            
            if (permiso_eliminar_reposos):
                # Mensaje para confirmar la accion
                self.msg_box.setIcon(QMessageBox.Information)
                self.msg_box.setWindowTitle("Confirmar acción")
                self.msg_box.setText("¿Seguro que quiere eliminar este reposo?")
                QApplication.beep()
                self.msg_box.exec_()
                
                if self.msg_box.clickedButton() == self.boton_si:
                    # Tomamos la cedula de la fila en donde pulso el boton editar
                    cedula = self.modelo.item(fila, 0).text()
                    
                    # Buscamos al empleado por su cedula
                    empleado_id = empleado_servicio.obtener_empleado_por_cedula(cedula)[0]
                    reposo_empleado_id = reposo_empleado_servicio.obtener_reposo_por_empleado_id(empleado_id)[6]
                    
                    reposo_empleado_servicio.eliminar_reposo(reposo_empleado_id)
                    QMessageBox.information(self, "Proceso exitoso", f"Se a Eliminado correctamente el reposo")
                    self.filtrar_reposo_por_fecha()
        except Exception as error:
            QMessageBox.warning(self, "Error al eliminar el reposo", str(error))
    
    def filtrar_reposo_por_fecha(self):
        """
        Este método es para filtrar los reposos de empleados por la fecha. El proceso es el siguiente:
        
        - A partir de la fecha de emisión y la cédula del empleado obtenidos en la interfaz los usamos para el método que obtenga los registros
        - Si no hubo errores cargamos los registros obtenidos en la tabla
        - Configuramos la barra de búsqueda para pasarle la cédula junto con el nombre y apellido del empleado en una lista de coincidencias
        """
        try:
            fecha_emision = self.dateEdit_filtro_fecha_reposo.date().toPyDate()
            cedula_empleado = self.barra_de_busqueda.text().strip()
            
            if (cedula_empleado == ""):
                cedula_empleado = None
            
            reposos_empleados = reposo_empleado_servicio.obtener_reposo_por_fecha_emision_o_cedula(fecha_emision, cedula_empleado)
        except BaseDatosError:
            self.modelo.removeRows(0, self.modelo.rowCount())
        else:
            self.cargar_reposos_en_tabla(self.tbl_reposos, reposos_empleados)
            
            
    def filtrar_por_barra_de_busqueda(self):
        """
            Este metodo sirve para filtrar los reposos de todos lo empleados que tienen un reposo registrado, esto funciona asi:
            
            1. Obtenemos la cedula de la barra de busqueda
            2. A partir de la cedula buscamos el id del empleado
            3. Con el ID del empleado obtenemos el reposo
            4. Con el reposo del empleado obtenemos la fecha
            5. Con la fecha del reposo del empleado se la asignamos al QDateEdit que filtra por fecha, y al darle la fecha este automaticamente refresca la tabla
        """
        try:
            cedula = self.barra_de_busqueda.text().strip()
            empleado = empleado_servicio.obtener_empleado_por_cedula(cedula)
            empleado_id = empleado[0]
            reposo_actual = reposo_empleado_servicio.obtener_reposo_por_empleado_id(empleado_id)
            fecha_reposo_empleado = reposo_actual[4]
            
            self.dateEdit_filtro_fecha_reposo.setDate(QDate.fromString(fecha_reposo_empleado, "yyyy-MM-dd"))
            
            
        except Exception as e:
            print(f"No se pudo filtrar por la barra de busqueda: {e}")
        
    
    def cargar_reposos_en_tabla(self, tabla, reposos):
        """
        Este método es para cargar los reposos obtenidos a la tabla. El proceso es el siguiente:
        
        - Definimos el nombre de cada columna
        - Definimos el modelo junto con cada columna del paso anterior
        - Añadimos los datos visibles en cada fila
        - Seteamos el modelo con las filas ingresadas
        - Añadimos los botones de editar y borrar en la última columna junto con sus respectivas señales
        """
        COLUMNAS = [
            "Cédula",
            "Primer nombre",
            "Apellido Paterno",
            "Fecha de emisión",
            "Fecha de reingreso",
            "Opciones"
        ]
        
        self.modelo = QStandardItemModel()
        self.modelo.setHorizontalHeaderLabels(COLUMNAS)
        
        for indice, fila_reposo in enumerate(reposos):
            datos_visibles = [
                fila_reposo[0],
                fila_reposo[1],
                fila_reposo[2],
                fila_reposo[4],
                fila_reposo[5]
            ]
            
            items = []
            
            for dato in datos_visibles:
                item = QStandardItem(str(dato) if (dato is not None) else "")
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                items.append(item)
            
            self.modelo.appendRow(items)
            
            header_item = QStandardItem(str(indice + 1))
            header_item.setFlags(Qt.ItemIsEnabled)
            self.modelo.setVerticalHeaderItem(indice, header_item)
        
        tabla.setModel(self.modelo)
        
        for fila in range(self.modelo.rowCount()):
            tabla.setRowHeight(fila, 40)
        
        # AÑADIMOS LOS BOTONES DE EDITAR Y BORRAR EN CADA FILA
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
            

            # CONECTAMOS LOS BOTONES CON SU RESPECTIVA FUNCIÓN
            boton_editar.clicked.connect(lambda _, fila=fila: self.habilitar_edicion_reposo(fila))
            boton_borrar.clicked.connect(lambda _, fila=fila: self.eliminar_info_reposo(fila))

            layout.addWidget(boton_editar)
            layout.addWidget(boton_borrar)
            layout.setContentsMargins(3, 3, 3, 3)
            widget.setLayout(layout)
            
            index = self.modelo.index(fila, len(COLUMNAS) - 1)  # ÚLTIMA COLUMNA (OPCIONES)
            tabla.setIndexWidget(index, widget)
    
    def regresar_pantalla_anterior(self):
        """
            Esta metodo sirve para regresa a la pantalla anterio, pero advirtiendo le al usuario que si se va de
            la pantalla todo su progreso se perdera.
        """
        
        self.msg_box.setIcon(QMessageBox.Information)
        self.msg_box.setWindowTitle("Confirmar acción")
        self.msg_box.setText("¿Seguro que quiere irse de esta pantalla?")
        QApplication.beep()
        self.msg_box.exec_()
        
        if self.msg_box.clickedButton() == self.boton_si:
            self.boton_agregar.clicked.disconnect()
            FuncionSistema.cambiar_estilo_del_boton(self.boton_agregar, "boton_anadir")
            self.boton_agregar.clicked.connect(self.registrar_reposo)

            self.stacked_widget.setCurrentIndex(7)
            FuncionSistema.limpiar_inputs_de_qt(self.tupla_inputs)
    
    