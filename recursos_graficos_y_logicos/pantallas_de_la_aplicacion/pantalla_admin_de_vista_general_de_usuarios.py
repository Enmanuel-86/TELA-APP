from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5 import QtGui
from PyQt5.QtCore import (QPoint, Qt)
import os
from PyQt5.QtWidgets import (QWidget, QMessageBox, QApplication, QListWidget, QListWidgetItem, 
                            QLabel, QHBoxLayout, QPushButton, QHeaderView )

from ..elementos_graficos_a_py import Ui_VistaGeneralUsuarios
from recursos_graficos_y_logicos.utilidades.funciones_sistema import FuncionSistema

# IMPORTACIONES DE BASE DE DATOS
from recursos_graficos_y_logicos.utilidades.base_de_datos import (usuario_servicio, rol_servicio, empleado_servicio,
                                                                  permiso_servicio)
from excepciones.base_datos_error import BaseDatosError
from configuraciones.configuracion import app_configuracion



class PantallaAdminVistaGeneralUsuarios(QWidget, Ui_VistaGeneralUsuarios):
    def __init__(self, stacked_widget):
        super().__init__()
        
        self.stacked_widget = stacked_widget
        self.setupUi(self)
        
            
        self.msg_box = QMessageBox(self)
        
        # Crear botones personalizados
        self.boton_si = self.msg_box.addButton("Sí", QMessageBox.YesRole)
        self.boton_no = self.msg_box.addButton("No", QMessageBox.NoRole)
        
        # definimos el modelo para el qtableview
        self.modelo = QStandardItemModel()
        
        self.tbl_usuarios.horizontalHeader().setVisible(True)

        self.tbl_usuarios.horizontalHeader().setMinimumHeight(50)
        self.tbl_usuarios.horizontalHeader().setMinimumWidth(10)
        self.tbl_usuarios.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tbl_usuarios.horizontalHeader().setSectionsClickable(False)


        self.tbl_usuarios.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tbl_usuarios.verticalHeader().setVisible(True)
        #self.tbl_usuarios.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tbl_usuarios.verticalHeader().setMinimumWidth(20)
        self.tbl_usuarios.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.tbl_usuarios.verticalHeader().setFixedWidth(20)
        #esto me da el valor de la cedula al darle click a la persona que quiero
        self.tbl_usuarios.clicked.connect(lambda index: print(index.sibling(index.row(), 0).data()))
        
        # actualizamos la barra de busqueda
        self.actualizar_lista_busqueda()
        
        # CONFIGURACIÓN DE LAS SEÑALES
        self.boton_agregar.clicked.connect(self.registrar_usuario)
        self.comboBox_filtro_rol.currentIndexChanged.connect(self.filtrar_por_rol_de_usuario)
        self.boton_crear_registro.clicked.connect(self.crear_nuevo_registro)
        self.boton_cancelar_registro.clicked.connect(self.cancelar_registro)
        self.boton_ver_auditoria.clicked.connect(lambda: self.ir_pantalla_auditoria())
        
        
        self.lista_empleados_actual = empleado_servicio.obtener_todos_empleados()
        self.lista_usuarios = usuario_servicio.obtener_todos_usuarios()
        self.barra_de_busqueda.returnPressed.connect(self.filtrar_por_rol_de_usuario)
        #self.barra_de_busqueda.textChanged.connect(self.filtrar_por_rol_de_usuario)
        self.boton_buscar.clicked.connect(self.filtrar_por_rol_de_usuario)
        
        
        
        # ELEMENTOS DE UTILIDAD
        self.lista_roles = rol_servicio.obtener_todos_roles()
        
        self.lista_inputs = (
            self.input_cedula_empleado,
            self.input_nombre_usuario,
            self.input_clave_usuario
        )
        
        # Esto es una lista (YA SE QUE ES UNA TUPLA) para habilitar o deshabiltar todos estos al mismo tiempo
        self.lista_de_widgets = (self.input_cedula_empleado, self.input_nombre_usuario, self.input_clave_usuario,
                                self.comboBox_rol, self.boton_agregar)
        
        # CARGAR LOS ROLES EN LOS COMBOBOX
        FuncionSistema.cargar_elementos_para_el_combobox(self.lista_roles, self.comboBox_rol, 1)
        FuncionSistema.cargar_elementos_para_el_combobox(self.lista_roles, self.comboBox_filtro_rol, 1)
        
        
    
    def ir_pantalla_auditoria(self):
        """
            Metodo para actualizar las auditorias en la tabla de auditorias en el sistema
        """
        
        pantalla_auditorias = self.stacked_widget.widget(15)
        pantalla_auditorias.actualizar_auditorias()
        self.stacked_widget.setCurrentIndex(15)
        
    def actualizar_lista_busqueda(self):
        
        
        
        try:
            self.lista_empleados_actual = empleado_servicio.obtener_todos_empleados()
            usuarios = usuario_servicio.obtener_todos_usuarios()
            #print(usuarios[1])
            for usuario in usuarios:
                for empleado in self.lista_empleados_actual:
                    
                    if usuario[1] == empleado[6]:
                        
                        self.lista_empleados_actual.remove(empleado)
            
        except:
            print("No se puedo actular la lista en la pantalla de usuarios")
            
        else:
            
            FuncionSistema.configurar_barra_de_busqueda(self, self.input_cedula_empleado, self.lista_empleados_actual, 6,1,4, self.label_nombre_empleado_guia)
        
    
    
    
    def crear_nuevo_registro(self):
    
        FuncionSistema.habilitar_o_deshabilitar_widget_de_qt(self.lista_de_widgets, True)
        self.boton_crear_registro.setEnabled(False)
        self.boton_cancelar_registro.setEnabled(True)
        
    def cancelar_registro(self):
        
        # Mensaje para confirmar la accion
        self.msg_box.setIcon(QMessageBox.Information)
        self.msg_box.setWindowTitle("Confirmar acción")
        self.msg_box.setText("¿Seguro quiere cancelar este registro?")
        QApplication.beep()
        self.msg_box.exec_()
        
        if self.msg_box.clickedButton() == self.boton_si:
            
            FuncionSistema.limpiar_inputs_de_qt(self.lista_inputs)
            FuncionSistema.habilitar_o_deshabilitar_widget_de_qt(self.lista_de_widgets, False)
            self.boton_crear_registro.setEnabled(True)
            self.boton_cancelar_registro.setEnabled(False)
            self.comboBox_rol.setCurrentIndex(0)

            # En caso de que este editando
            self.boton_agregar.clicked.disconnect()
            FuncionSistema.cambiar_estilo_del_boton(self.boton_agregar, "boton_anadir")
            self.boton_agregar.clicked.connect(self.registrar_usuario)


        if self.msg_box.clickedButton() == self.boton_no:
            return
    
    
    
    def registrar_usuario(self):
        """
            Método para registrar a un usuario
            
            Este método funciona de la siguiente manera:
            
            - Primero le preguntamos al usuario si quiere registrar un usuario para X empleado
            - Obtenemos los datos ingresados
            - Le pasamos el diccionario con los datos para registrar el usuario (**empleado_id**, **rol_id**, **nombre_usuario** y **clave_usuario**)
            - Validamos antes de registrar si todo lo ingresado está correctamente (en caso de que no, no registramos y mostramos los errores)
            - Limpiamos los inputs
            - Actualizamos el filtro cargando así los registros actuales de los usuarios en el Table View
            - En caso de no querrer registrar un usuario para X empleado, se limpian y deshabilitan los campos
        """
        
        
        # OBTENEMOS LOS DATOS INGRESADOS PARA REGISTRAR EL USUARIO
        cedula_empleado = self.input_cedula_empleado.text()
        empleado = empleado_servicio.obtener_empleado_por_cedula(cedula_empleado)
        empleado_id = None
        
        self.msg_box.setIcon(QMessageBox.Information)
        self.msg_box.setWindowTitle("Confirmar acción")
        self.msg_box.setText(f"¿Seguro que registrar un usuario para {empleado[1]} {empleado[4]}?")
        QApplication.beep()
        self.msg_box.exec_()
        
        if self.msg_box.clickedButton() == self.boton_si:
        
            
            try:
                
                
                if (empleado):
                    empleado_id = empleado[0]
                
                nombre_usuario = self.input_nombre_usuario.text()
                clave_usuario = self.input_clave_usuario.text()
                
                rol_seleccionado = self.comboBox_rol
                rol_id = FuncionSistema.obtener_id_del_elemento_del_combobox(rol_seleccionado, self.lista_roles, 1, 0)
                
                # CREAMOS UN DICCIONARIO CON LOS CAMPOS A REGISTRAR DEL USUARIO
                campos_usuario = {
                    "empleado_id": empleado_id,
                    "rol_id": rol_id,
                    "nombre_usuario": nombre_usuario,
                    "clave_usuario": clave_usuario
                }
                
                # VALIDAMOS LOS CAMPOS DEL USUARIO
                errores = usuario_servicio.validar_campos_usuario(
                    empleado_id = campos_usuario.get("empleado_id"),
                    rol_id = campos_usuario.get("rol_id"),
                    nombre_usuario = campos_usuario.get("nombre_usuario"),
                    clave_usuario = campos_usuario.get("clave_usuario")
                )
                
                # SI HAY ERRORES EN LA VALIDACIÓN NO REGISTRAMOS AL USUARIO Y LE MOSTRAMOS EN PANTALLA LA LISTA DE ERRORES
                if (errores):
                    QMessageBox.warning(self, "Error al registrar el usuario", "\n".join(errores))
                    return
                
                try:
                    # REGISTRAMOS AL USUARIO
                    usuario_servicio.registrar_usuario(campos_usuario)
                    
                except Exception as e:
                    QMessageBox.warning(self, "Error al registrar usuario", f"{e}")
                else:
                    
                    # Mostramos el mensaje de exito
                    QMessageBox.information(self, "Proceso exitoso", f"Se a registrado correctamente el usuario para {empleado[1]} {empleado[4]}")
                    
                    # Limpiamos inputs
                    FuncionSistema.limpiar_inputs_de_qt(self.lista_inputs)
                    
                    # Filtramos con el rol que se acaba de registrar
                    self.comboBox_filtro_rol.setCurrentText(self.comboBox_rol.currentText())
                    
                    # Posicion 0 para este combobox
                    self.comboBox_rol.setCurrentIndex(0)
                    
                    # Filtramos
                    self.filtrar_por_rol_de_usuario()
                    
                    
            except BaseDatosError as error:
                print("Error al registrar al usuario: ", str(error))
                
        if self.msg_box.clickedButton() == self.boton_no:
            
            # Limpiamos los campos
            FuncionSistema.limpiar_inputs_de_qt(self.lista_inputs)
            
            # Deshabilitamos los campos
            FuncionSistema.habilitar_o_deshabilitar_widget_de_qt(self.lista_de_widgets, False)  
            
            # Cambiamos los estados de los botones 
            self.boton_cancelar_registro.setEnabled(False)
            self.boton_crear_registro.setEnabled(True) 

        
            
    
    def habilitar_edicion_usuario(self, fila):
        """
            Este metodo es para habilitar la edicion del usuario.
            
            Aqui solamente colocamos los valores registrados a los campos para que se puedan editar
        """
        try:
            # Aqui se verifica si tiene el permiso
            permiso_editar_usuario = permiso_servicio.verificar_permiso_usuario(app_configuracion.USUARIO_ID, "GESTIONAR USUARIOS")
            
            if permiso_editar_usuario:
                print("tengo permisos para editar")
                
                # Mensaje para confirmar la accion
                self.msg_box.setIcon(QMessageBox.Information)
                self.msg_box.setWindowTitle("Confirmar acción")
                self.msg_box.setText("¿Seguro que quiere editar este usuario?")
                QApplication.beep()
                self.msg_box.exec_()
                
                if self.msg_box.clickedButton() == self.boton_si:
                    
                    self.crear_nuevo_registro()
                    
                    # Tomamos la cedula de la fila en donde pulso el boton editar
                    cedula = self.modelo.item(fila, 0).text()
                    
                    # Buscamos al empleado por su cedula
                    empleado = empleado_servicio.obtener_empleado_por_cedula(cedula)
                    empleado_id = empleado[0]
                    
                    # Buscamos el usuario a partir del id del empleado
                    usuario = usuario_servicio.obtener_usuario_por_empleado_id(empleado[0])
                    print(usuario)
                    # Colocamos los valores a los inputs
                    self.input_cedula_empleado.setText(usuario[2])
                    self.input_nombre_usuario.setText(usuario[5])
                    self.input_clave_usuario.setText(usuario[7])
                    self.comboBox_rol.setCurrentText(usuario[6])
                    
                    self.boton_agregar.clicked.disconnect()
                    
                    FuncionSistema.cambiar_estilo_del_boton(self.boton_agregar, "boton_editar")
                    
                    usuario_id = usuario[0]
                    empleado_id
                    self.boton_agregar.clicked.connect(lambda : self.editar_info_usuario(usuario_id, empleado_id))
        
        except Exception as e:
            # si el usuario no tiene permiso se le muestra un mensaje en pantalla
            QMessageBox.warning(self, "No puede", f"{e}")
    
    def editar_info_usuario(self, usuario_id, empleado_id):
        
        
        
        self.msg_box.setIcon(QMessageBox.Information)
        self.msg_box.setWindowTitle("Confirmar acción")
        self.msg_box.setText(f"¿Seguro que quiere editar este usuario?")
        QApplication.beep()
        self.msg_box.exec_()
        
        if self.msg_box.clickedButton() == self.boton_si:
        
            try:
                nombre_usuario = self.input_nombre_usuario.text()
                clave_usuario = self.input_clave_usuario.text()
                
                rol_seleccionado = self.comboBox_rol
                rol_id = FuncionSistema.obtener_id_del_elemento_del_combobox(rol_seleccionado, self.lista_roles, 1, 0)
                
                # CREAMOS UN DICCIONARIO CON LOS CAMPOS A REGISTRAR DEL USUARIO
                campos_usuario = {
                    "rol_id": rol_id,
                    "nombre_usuario": nombre_usuario,
                    "clave_usuario": clave_usuario
                }
                
                # VALIDAMOS LOS CAMPOS DEL USUARIO
                errores = usuario_servicio.validar_campos_usuario(
                    empleado_id = empleado_id,
                    rol_id = campos_usuario.get("rol_id"),
                    nombre_usuario = campos_usuario.get("nombre_usuario"),
                    clave_usuario = campos_usuario.get("clave_usuario"),
                    usuario_id = usuario_id
                )
                
                # SI HAY ERRORES EN LA VALIDACIÓN NO REGISTRAMOS AL USUARIO Y LE MOSTRAMOS EN PANTALLA LA LISTA DE ERRORES
                if (errores):
                    QMessageBox.warning(self, "Error al editar el usuario", "\n".join(errores))
                    return
                
                try:
                    # REGISTRAMOS AL USUARIO
                    usuario_servicio.actualizar_usuario(usuario_id, campos_usuario)
                    
                except Exception as e:
                    QMessageBox.warning(self, "Error al registrar usuario", f"{e}")
                    
                else:
                    # Mostramos el mensaje de exito
                    QMessageBox.information(self, "Proceso exitoso", f"Se a editado correctamente el usuario")
                    
                    # Limpiamos campos
                    FuncionSistema.limpiar_inputs_de_qt(self.lista_inputs)
                    
                    # Deshabilitamos los campos
                    FuncionSistema.habilitar_o_deshabilitar_widget_de_qt(self.lista_de_widgets, False)
                    
                    # cambiamos de funcion al boton de agregar
                    self.boton_agregar.clicked.disconnect()
                    FuncionSistema.cambiar_estilo_del_boton(self.boton_agregar, "boton_anadir")
                    self.boton_agregar.clicked.connect(self.registrar_usuario)
                    
                    self.boton_cancelar_registro.setEnabled(False)
                    self.boton_crear_registro.setEnabled(True)
                            
                    # Filtramos con el rol que se acaba de registrar
                    self.comboBox_filtro_rol.setCurrentText(self.comboBox_rol.currentText())
                    
                    # Posicion 0 para este combobox
                    self.comboBox_rol.setCurrentIndex(0)
                    
                    # Filtramos
                    self.filtrar_por_rol_de_usuario()
                    
                    
                    
            except BaseDatosError as error:
                print("Error al editar al usuario: ", str(error))
        
        if self.msg_box.clickedButton() == self.boton_no:
            # Limpiamos campos
            FuncionSistema.limpiar_inputs_de_qt(self.lista_inputs)
            
            # Deshabilitamos los campos
            FuncionSistema.habilitar_o_deshabilitar_widget_de_qt(self.lista_de_widgets, False)
            
            # cambiamos de funcion al boton de agregar
            self.boton_agregar.clicked.disconnect()
            FuncionSistema.cambiar_estilo_del_boton(self.boton_agregar, "boton_anadir")
            self.boton_agregar.clicked.connect(self.registrar_usuario)
            
            self.boton_cancelar_registro.setEnabled(False)
            self.boton_crear_registro.setEnabled(True)
    
    
                
                
    def eliminar_usuario_del_registro(self, fila):
        """"""
        
        try:
            
            permiso_eliminar_usuario = permiso_servicio.verificar_permiso_usuario(app_configuracion.USUARIO_ID, "GESTIONAR USUARIOS")
            
            if permiso_eliminar_usuario:
                
                # Mensaje para confirmar la accion
                self.msg_box.setIcon(QMessageBox.Information)
                self.msg_box.setWindowTitle("Confirmar acción")
                self.msg_box.setText("¿Seguro que quiere eliminar este usuario?")
                QApplication.beep()
                self.msg_box.exec_()
                
                if self.msg_box.clickedButton() == self.boton_si:
                    
                    # Tomamos la cedula de la fila en donde pulso el boton editar
                    cedula = self.modelo.item(fila, 0).text()
                    
                    # Buscamos al empleado por su cedula
                    empleado = empleado_servicio.obtener_empleado_por_cedula(cedula)
                    #print(empleado)
                    
                    # Buscamos el usuario a partir del id del empleado
                    usuario = usuario_servicio.obtener_usuario_por_empleado_id(empleado[0])
                    
                    if usuario[0] == FuncionSistema.id_usuario:
                        QMessageBox.warning(self, "Error al eliminar el usuario", f"No te puede eliminar a ti mismo")
                        return
                    else:
                        usuario_servicio.eliminar_usuario(usuario[0])
                    
                        print("El usuario se pudo eliminar correctamente")
                    
        except Exception as e:
            
            QMessageBox.warning(self, "Error al eliminar el usuario", f"{e}")
            
        else:
            # Mostramos el mensaje de exito
            QMessageBox.information(self, "Proceso exitoso", f"Se a Eliminado correctamente el usuario")
            self.filtrar_por_rol_de_usuario()
                    
                    
    
    def filtrar_por_rol_de_usuario(self):
        """
            Este metodo filtra segun los roles que se registraron el la base de datos. y funciona de la siguiente manera:
            
            1. Se obtiene el id del rol
            2. Se obtiene la cedula (en caso de que use la barra de busqueda)
            3. Se obtienen a los usuarios a partir del rol o la cedula con el servicio de la base de datos
            4. Si hay usuarios se cargan en el QTableView, caso contrario no muestra nada
        """
        
        try:
            
            # Obtenemos el id del rol
            rol_id = FuncionSistema.obtener_id_del_elemento_del_combobox(self.comboBox_filtro_rol, self.lista_roles, 1, 0)
            
            # Obtenemos los usuarios
            usuarios = usuario_servicio.obtener_usuario_por_rol_o_cedula_empleado(rol_id, None if self.barra_de_busqueda.text().strip() == "" else self.barra_de_busqueda.text().strip() )
            
            
        except Exception as e:
            
            print(f"filtrar_por_rol_de_usuario: no pudo filtrar con el cargo seleccionado")
            
            # Borramos el contenido de la tabla al haber una excepcion
            self.modelo.removeRows(0, self.modelo.rowCount())
        else:
            
            # Cargamos a los usuarios en caso de no haber excepciones
            self.cargar_usuario_en_tabla(self.tbl_usuarios ,usuarios)
            
            FuncionSistema.configurar_barra_de_busqueda(self, self.barra_de_busqueda, usuarios, 1,2,3)
        
        
    def filtrar_con_barra_de_busqueda(self):
        """

        """
    
        try:

            
            usuarios = usuario_servicio.obtener_usuario_por_rol_o_cedula_empleado(cedula_empleado= None if self.barra_de_busqueda.text().strip() == "" else self.barra_de_busqueda.text().strip() )
            
            
                
        except:
            # Borramos el contenido de la tabla al haber una excepcion
            self.modelo.removeRows(0, self.modelo.rowCount())
            print("No funciono el metodo: filtrar_con_barra_de_busqueda")
            
        else:
            # Cargamos a los usuarios en caso de no haber excepciones
            
            print(usuarios)
            self.cargar_usuario_en_tabla(self.tbl_usuarios ,usuarios)
            
            
            
            
    def cargar_usuario_en_tabla(self, tabla, usuarios):
        columnas = [
            "Cédula", "Nombre", "Apellido", "Nombre de usuario", "Opciones"
            
        ]

        
        self.modelo = QStandardItemModel()
        self.modelo.setHorizontalHeaderLabels(columnas)

        # Primero cargamos los datos
        for indice, usuario in enumerate(usuarios):
            datos_visibles = [
            usuario[1],  # Cedula
            usuario[2],  # Nombre
            usuario[3],  # Apellido
            usuario[4]   # usuario
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
            boton_editar.clicked.connect(lambda _, fila=fila: self.habilitar_edicion_usuario(fila))
            boton_borrar.clicked.connect(lambda _, fila=fila: self.eliminar_usuario_del_registro(fila))

            layout.addWidget(boton_editar)
            layout.addWidget(boton_borrar)
            layout.setContentsMargins(3, 3, 3, 3)
            widget.setLayout(layout)
            
            index = self.modelo.index(fila, len(columnas) - 1)  # última columna ("Opciones")
            tabla.setIndexWidget(index, widget)
        