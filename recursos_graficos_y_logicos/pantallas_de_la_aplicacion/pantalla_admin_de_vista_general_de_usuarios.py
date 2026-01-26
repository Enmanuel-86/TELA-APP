from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
import os
from PyQt5.QtWidgets import (QWidget, QMessageBox, QHeaderView)

from ..elementos_graficos_a_py import Ui_VistaGeneralUsuarios
from recursos_graficos_y_logicos.utilidades.funciones_sistema import FuncionSistema

# IMPORTACIONES DE BASE DE DATOS
from recursos_graficos_y_logicos.utilidades.base_de_datos import usuario_servicio
from recursos_graficos_y_logicos.utilidades.base_de_datos import rol_servicio
from recursos_graficos_y_logicos.utilidades.base_de_datos import empleado_servicio
from excepciones.base_datos_error import BaseDatosError



class PantallaAdminVistaGeneralUsuarios(QWidget, Ui_VistaGeneralUsuarios):
    def __init__(self, stacked_widget):
        super().__init__()
        
        self.stacked_widget = stacked_widget
        self.setupUi(self)
        
        # LISTA CON LA DATA DE USUAIOS
        self.usuario_data = []
        
        # CONFIGURACIÓN DE LAS SEÑALES
        self.boton_agregar.clicked.connect(self.registrar_usuario)
        self.comboBox_filtro_rol.currentIndexChanged.connect(self.filtrar_usuarios_por_rol_e_identificador)
        self.boton_buscar.clicked.connect(self.filtrar_usuarios_por_rol_e_identificador)
        
        # ELEMENTOS DE UTILIDAD
        self.lista_roles = rol_servicio.obtener_todos_roles()
        
        self.lista_inputs = [
            self.input_cedula_empleado,
            self.input_nombre_usuario,
            self.input_clave_usuario
        ]
        
        # CARGAR LOS ROLES EN LOS COMBOBOX
        FuncionSistema.cargar_elementos_para_el_combobox(self.lista_roles, self.comboBox_rol, 1)
        FuncionSistema.cargar_elementos_para_el_combobox(self.lista_roles, self.comboBox_filtro_rol, 1)
    
    def registrar_usuario(self):
        """
            Método para registrar a un usuario
            
            Este método funciona de la siguiente manera:
            
            - Primero obtenemos los datos ingresados
            - Le pasamos el diccionario con los datos para registrar el usuario (**empleado_id**, **rol_id**, **nombre_usuario** y **clave_usuario**)
            - Validamos antes de registrar si todo lo ingresado está correctamente (en caso de que no, no registramos y mostramos los errores)
            - Limpiamos los inputs
            - Actualizamos el filtro cargando así los registros actuales de los usuarios en el Table View
        """
        try:
            # OBTENEMOS LOS DATOS INGRESADOS PARA REGISTRAR EL USUARIO
            cedula_empleado = self.input_cedula_empleado.text()
            empleado = empleado_servicio.obtener_empleado_por_cedula(cedula_empleado)
            empleado_id = None
            
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
            else:
                # REGISTRAMOS AL USUARIO
                usuario_servicio.registrar_usuario(campos_usuario)
                
                # LIMPIAMOS LOS INPUTS
                for campo_input in self.lista_inputs:
                    campo_input.clear()
                
                # ACTUALIZAMOS LA TABLA LLAMANDO AL FILTRO DE LOS USUARIOS
                self.filtrar_usuarios_por_rol_e_identificador()
        except BaseDatosError as error:
            QMessageBox.warning(self, "Error al registrar al usuario", str(error))
    
    def filtrar_usuarios_por_rol_e_identificador(self):
        """
            Método para filtrar a los usuarios por el rol y su cédula
            
            Este método funciona de la siguiente manera:
            
            - Primero obtenemso el rol seleccionado del combobox para el filtro
            - Luego obtenemos la cédula de la barra de búsqueda y verificamos si tiene contenido
            - Creamos una lista de tuplas de usuarios a partir de los parámetros obtenidos de los pasos anteriores
            - Creamos el modelo de datos e insertamos en cada celda de la fila el contenido correspondiente
            - Le asignamos ese modelo de datos al Table View
            - En caso de que haya un error limpiamos el Table View y la data de usuarios pasa a ser una lista vacía
        """
        try:
            # LE ASIGNAMOS LA LISTA DE TUPLAS ACTUAL DE USUARIOS A LA DATA CON EL PARÁMETRO DEL ROL Y LA CÉDULA DEL EMPLEADO (SI LA INGRESA)
            rol_seleccionado = self.comboBox_filtro_rol
            rol_id = FuncionSistema.obtener_id_del_elemento_del_combobox(rol_seleccionado, self.lista_roles, 1, 0)
            
            cedula_empleado_buscar = self.barra_de_busqueda.text()
            
            if (cedula_empleado_buscar.strip() == ""):
                cedula_empleado_buscar = None
            
            usuarios = usuario_servicio.obtener_usuario_por_rol_o_cedula_empleado(rol_id, cedula_empleado_buscar)
            self.usuario_data = usuarios
            
            # SI NO HAY USUARIOS AL LLAMAR AL MÉTODO LA DATA PASA A SER UNA LISTA VACÍA
            if not(usuarios):
                self.usuario_data = []
                return
            
            # CREAMOS EL MODELO DE DATOS CON LA CANTIDAD DE FILAS, COLUMNAS Y PONEMOS EL NOMBRE DE CADA COLUMNA
            CANTIDAD_FILAS = len(usuarios)
            CANTIDAD_COLUMNAS = 5
            
            modelo_datos = QStandardItemModel(CANTIDAD_FILAS, CANTIDAD_COLUMNAS)
            modelo_datos.setHorizontalHeaderLabels([
                "Cédula de empleado",
                "Nombre",
                "Apellido",
                "Nombre de usuario",
                "Opciones"
            ])
            
            # RECORREMOS CADA FILA PARA QUE EN CADA CELDA ASIGNARLE EL VALOR QUE LE CORRESPONDE A ESA FILA EN CONCRETO
            for fila, usuario in enumerate(usuarios):
                cedula_empleado = usuario[1]
                nombre_empleado = usuario[2]
                apellido_empleado = usuario[3]
                nombre_usuario = usuario[4]
                
                items = [
                    QStandardItem(str(cedula_empleado)),
                    QStandardItem(str(nombre_empleado)),
                    QStandardItem(str(apellido_empleado)),
                    QStandardItem(str(nombre_usuario))
                ]
                
                for columna, item in enumerate(items):
                    modelo_datos.setItem(fila, columna, item)
                    
                    # Evita la edición de las celdas por parte del usuario
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            
            # ASIGNAMOS EL MODELO DE DATOS AL TABLE VIEW
            self.tbl_usuarios.setModel(modelo_datos)
        except BaseDatosError as error:
            # SI HAY UN ERROR DE BASE DE DATOS QUE LIMPIE LA TABLA Y LA DATA DE USUARIOS ESTÉ VACÍA
            self.limpiar_tabla(str(error))
            self.usuario_data = []
        finally:
            header = self.tbl_usuarios.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
    
    def limpiar_tabla(self, mensaje_error: str):
        """
            Método para limpiar el Table View
            
            Este método funciona de la siguiente manera:
            
            - Primero creamos un modelo vacío sin filas pero con sus respectivas columnas
            - Asignamos ese modelo vacío al Table View
            - Se muestra un mensaje de error al usuario cuando no haya coincidencia con el filtro
        """
        CANTIDAD_FILAS = 0
        CANTIDAD_COLUMNAS = 5
        
        # CREAMOS UN MODELO DE DATOS VACÍO
        modelo_vacio = QStandardItemModel(CANTIDAD_FILAS, CANTIDAD_COLUMNAS)
        modelo_vacio.setHorizontalHeaderLabels([
                "Cédula de empleado",
                "Nombre",
                "Apellido",
                "Nombre de usuario",
                "Opciones"
            ])
        
        # LE ASIGNAMOS EL MODELO VACÍO AL TABLE VIEW
        self.tbl_usuarios.setModel(modelo_vacio)
        
        # MOSTRAMOS UN MENSAJE DE ERROR AL USUARIO EN CASO DE QUE HAYA UN ERROR EN EL FILTRO
        if (mensaje_error):
            QMessageBox.warning(self, "Error al filtrar los usuarios", mensaje_error)