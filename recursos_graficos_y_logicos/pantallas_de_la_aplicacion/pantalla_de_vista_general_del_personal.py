from PyQt5.QtCore import Qt,QPoint, QSortFilterProxyModel
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (QWidget, QHeaderView,  QHBoxLayout, 
                             QMessageBox, QListWidget, QListWidgetItem, 
                             QPushButton, QApplication)
from PyQt5 import QtGui
from configuraciones.configuracion import app_configuracion
from ..elementos_graficos_a_py import Ui_VistaGeneralDelPersonal
from ..utilidades.funciones_sistema import FuncionSistema
from ..utilidades.base_de_datos import (cargo_empleado_servicio, tipo_cargo_servicio, especialidad_servicio,
                                        empleado_servicio, detalle_cargo_servicio, permiso_servicio)



# este es por cargo
#lista_cargo_actual = detalle_cargo_servicio.obtener_todos_detalles_cargo()


## pantalla para ver el registro del personal
class PantallaDeVistaGeneralDelPersonal(QWidget, Ui_VistaGeneralDelPersonal):
    def __init__(self, stacked_widget):
        super().__init__()

        

        
        self.stacked_widget = stacked_widget
        self.setupUi(self)
        
        
        self.lista_cargos = cargo_empleado_servicio.obtener_todos_cargos_empleados()
        self.lista_tipo_cargo = tipo_cargo_servicio.obtener_todos_tipos_cargo()
        self.lista_especialidades = especialidad_servicio.obtener_todos_especialidades()
                
                
        self.msg_box = QMessageBox(self)
        
        # Crear botones personalizados
        self.boton_si = self.msg_box.addButton("Sí", QMessageBox.YesRole)
        self.boton_no = self.msg_box.addButton("No", QMessageBox.NoRole)
        
        # [(1, None, '17536256', 'DOUGLAS', 'JOSE', None, 'MARQUEZ', 'BETANCOURT', 'ADMINISTRATIVO', 'Activo'), (2, None, '5017497', 'ENMANUEL', 'JESÚS', None, 'GARCIA', 'RAMOS', 'ADMINISTRATIVO', 'Activo')]
        self.actualizar_tabla(tipo_cargo_id= 1, especialidad_id= None, situacion_selec= self.boton_de_situacion.currentText(), indice_cedula= 2, indice_1er_nombre= 3, indice_2do_nombre= 4,
                                                   indice_1er_apellido=6, indice_2do_apellido= 7, indice_estado= 9 )


        #print(self.lista_cargo_actual[1])
        #print(empleado_servicio.obtener_todos_empleados())

        self.actualizar_lista_busqueda()
        

        self.tabla_ver_personal.horizontalHeader().setVisible(True)

        self.tabla_ver_personal.horizontalHeader().setMinimumHeight(50)
        self.tabla_ver_personal.horizontalHeader().setMinimumWidth(10)
        self.tabla_ver_personal.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_ver_personal.horizontalHeader().setSectionsClickable(False)


        self.tabla_ver_personal.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tabla_ver_personal.verticalHeader().setVisible(True)
        #self.tabla_ver_personal.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_ver_personal.verticalHeader().setMinimumWidth(20)
        self.tabla_ver_personal.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.tabla_ver_personal.verticalHeader().setFixedWidth(20)
        #esto me da el valor de la cedula al darle click a la persona que quiero
        self.tabla_ver_personal.clicked.connect(lambda index: print(index.sibling(index.row(), 0).data()))

        # Opcional: desactivar clic en el encabezado vertical
        self.tabla_ver_personal.verticalHeader().setSectionsClickable(True)

        # Activar filas alternadas y aplicar estilo si quieres
        #self.tabla_ver_personal.setAlternatingRowColors(True)






        # conectar botones a los metodos para ir a las otras pantallas
        self.boton_crear_nuevo_registro.clicked.connect(self.ir_a_crear_nuevo_registro)
        self.boton_control_de_llegada.clicked.connect(self.ir_a_control_de_llegada)
        self.boton_control_de_reposos.clicked.connect(self.ir_a_control_de_reposos)
        self.boton_buscar.clicked.connect(lambda: self.aplicar_filtro(self.barra_de_busqueda.text()))     
        self.boton_de_opciones.currentIndexChanged.connect(self.filtrar_por_tipo_cargo)
        self.boton_de_situacion.currentIndexChanged.connect(self.filtrar_por_tipo_cargo)
        self.boton_especialidades.currentIndexChanged.connect(self.filtrar_por_especialidad)
        self.barra_de_busqueda.textChanged.connect(lambda texto: self.filtrar_resultados(texto) if not texto == "" else self.filtrar_por_tipo_cargo())
        self.barra_de_busqueda.returnPressed.connect(lambda: self.aplicar_filtro(self.barra_de_busqueda.text()) )

        # cargar catalogo de los tipos de cargos
        FuncionSistema.cargar_elementos_para_el_combobox(self.lista_especialidades, self.boton_especialidades, 1, 0, "Todos")
        FuncionSistema.cargar_elementos_para_el_combobox(self.lista_tipo_cargo, self.boton_de_opciones, 1, 0)
        
        ######################################################################
        # Para cargar la lista de empleados, el metodo para cargar empleados #
        # comienza por el metodo filtrar_por_tipo_cargo                      #
        ######################################################################
        
        # Conectar señal de doble click
        self.tabla_ver_personal.doubleClicked.connect(self.on_double_click)
        
        self.barra_de_busqueda.textChanged.connect(self.filtrar_resultados)
        
        
        # Lista de coincidencias
        self.resultados = QListWidget(self)
        self.resultados.setFocusPolicy(Qt.NoFocus)
        self.resultados.setMouseTracking(True)
        self.resultados.setStyleSheet("padding:10px;")
        self.resultados.itemClicked.connect(self.seleccionar_item)
        self.resultados.hide() 
    
    ##########################################################################################################################
    ##########################################################################################################################
    def actualizar_tipo_de_cargo(self):
    
        """
            Este metodo es de uso exclusivo para la pantalla de inserta_catalogo.py
        """
        self.lista_tipo_cargo = tipo_cargo_servicio.obtener_todos_tipos_cargo()
        self.boton_de_opciones.disconnect()
        FuncionSistema.cargar_elementos_para_el_combobox(self.lista_tipo_cargo, self.boton_de_opciones, 1, 1)
        self.boton_de_opciones.currentIndexChanged.connect(self.filtrar_por_tipo_cargo)

    
    # Metodo para la busqueda dinamica
    def actualizar_lista_busqueda(self):
        
        self.lista_empleados_actual = empleado_servicio.obtener_todos_empleados()
    
    
    def filtrar_resultados(self, texto):
        # Limpiamos espacios y convertimos todo a minúsculas
        texto = texto.strip().lower()

        # Limpiamos los resultados anteriores del QListWidget
        self.resultados.clear()

        # Si el campo está vacío, ocultamos la lista y salimos
        if not texto:
            self.resultados.hide()
            return

        # --------------------------------------------------------------------
        # NUEVO: Buscar según el PROXY (lo que ve el usuario en la tabla)
        # --------------------------------------------------------------------
        coincidencias = []

        # Cantidad de filas visibles en el proxy
        filas_visibles = self.proxy.rowCount()

        # Recorremos fila por fila del modelo filtrado (proxy)
        for fila in range(filas_visibles):

        
            # Obtenemos el índice del proxy
            index_proxy = self.proxy.index(fila, 0)

            # Convertimos el índice del proxy al índice original del modelo
            index_modelo = self.proxy.mapToSource(index_proxy)

            # Obtenemos la cédula desde la columna 1 del modelo
            cedula = modelo.index(index_modelo.row(), 0).data()

            # Obtenemos nombre desde la columna 2
            nombre = modelo.index(index_modelo.row(), 1).data()

            # Obtenemos apellido desde la columna 3
            apellido = modelo.index(index_modelo.row(), 3).data()

            # Convertimos todo a minúsculas para comparar
            cedula_lower = str(cedula).lower()
            nombre_lower = str(nombre).lower()
            apellido_lower = str(apellido).lower()
            
                

            # Si coincide con cedula, nombre o apellido lo agregamos a resultados
            if texto in cedula_lower or texto in nombre_lower or texto in apellido_lower:

                # Guardamos la información exacta del modelo para mostrarla luego
                coincidencias.append({
                    "cedula": cedula,
                    "nombre": nombre,
                    "apellido": apellido
                })

        # Si no hubo coincidencias, ocultamos lista y salimos
        if not coincidencias:
            self.resultados.hide()
            return

        # --------------------------------------------------------------------
        # Llenamos el QListWidget con las coincidencias encontradas
        # --------------------------------------------------------------------
        for persona in coincidencias:

            # Texto que se mostrará en la lista desplegable
            item = f'{persona["cedula"]} - {persona["nombre"]} {persona["apellido"]}'

            # Agregamos el item al QListWidget
            self.resultados.addItem(QListWidgetItem(item))

        # Si solo hay una coincidencia exacta por cédula, se oculta la lista
        if len(coincidencias) == 1 and coincidencias[0]["cedula"].lower() == texto:
            self.resultados.hide()
        else:
            # Si hay varias coincidencias, mostramos la lista de sugerencias
            self.mostrar_lista()



    def mostrar_lista(self):
        pos = self.barra_de_busqueda.mapTo(self, QPoint(0, self.barra_de_busqueda.height()))
        self.resultados.move(pos)
        self.resultados.resize(self.barra_de_busqueda.width(), 100)
        self.resultados.show()
        
        
        
        
    def seleccionar_item(self, item):
        cedula = item.text().split(" - ")[0]
        self.barra_de_busqueda.setText(cedula)
        self.aplicar_filtro(cedula)
        self.resultados.hide()
        
    
    def configurar_filtro(self):
        # Crear el filtro proxy (modelo intermedio entre el modelo real y la tabla)
        self.proxy = QSortFilterProxyModel()

        # Permitir búsqueda en todas las columnas
        self.proxy.setFilterKeyColumn(-1)  

        # Hacer el filtrado sin distinguir mayúsculas/minúsculas
        self.proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)

        # Conectar el QLineEdit al filtro
        #self.barra_de_busqueda.textChanged.connect(self.aplicar_filtro)

    
    
    
    def aplicar_filtro(self, texto):
        # Cada vez que escribes algo, el proxy actualizará las filas visibles
        self.proxy.setFilterFixedString(texto)
        self.resultados.hide()

        
        
        
    def habilitar_edicion(self, fila):
        
        
        cedula = modelo.item(fila, 0).text()
            
        empleado = empleado_servicio.obtener_empleado_por_cedula(cedula)    
        
        empleado_id = empleado[0]
        
        try:
            
            permiso_editar_empleado = permiso_servicio.verificar_permiso_usuario(app_configuracion.USUARIO_ID, "ACTUALIZAR EMPLEADOS")
            
            if permiso_editar_empleado:
                self.stacked_widget.setCurrentIndex(8)
                
                pantalla_editar_empleado = self.stacked_widget.widget(8)
                
                pantalla_editar_empleado.editar_datos_empleado(empleado_id)
                
            
        except Exception as e:
            print(F"No lo puede eliminar: {e}")
            QMessageBox.warning(self, "No puede", f"{e}")
            
            
            

    
    
            
            
    def eliminar_empleado_de_la_bd(self, fila):
        
        """
            Este metodo sirve para eliminar al empleado de la base de datos

        """
        cedula = modelo.item(fila, 0).text()
                    
        empleado_id = FuncionSistema.buscar_id_por_cedula(cedula, self.lista_empleados_actual)
        
        empleado = empleado_servicio.obtener_empleado_por_id(empleado_id)  

        
        try:
        
            permiso_eliminar_empleado = permiso_servicio.verificar_permiso_usuario(app_configuracion.USUARIO_ID, "ELIMINAR EMPLEADOS")
            
            if permiso_eliminar_empleado:
                self.msg_box.setWindowTitle("Advertencia")
                self.msg_box.setIcon(QMessageBox.Warning)
                self.msg_box.setText(f"¿Seguro que quiere eliminar a {empleado[1]} {empleado[4]}? ")
                QApplication.beep()
                
                # Mostrar el cuadro de diálogo y esperar respuesta
                self.msg_box.exec_()
                
                # si le da a SI, verificamos primero
                if self.msg_box.clickedButton() == self.boton_si:
            
            
                    try:


                        empleado_servicio.eliminar_empleado(empleado_id)
                        
                        
                    except Exception as e:
                        
                        QMessageBox.critical(self, "Error", f"No se pudo eliminar a {empleado[1]} {empleado[4]}, {e}")
                        FuncionSistema.mostrar_errores_por_excepcion(e, "eliminar_empleado_de_la_bd")   

                    else:
                        
                        QMessageBox.information(self, "Proceso exitoso", f"Se a eliminado a {empleado[1]} {empleado[4]} con exito")
                        self.filtrar_por_tipo_cargo()
            
                elif self.msg_box.clickedButton() == self.boton_no:
                    
                    return
            
        except Exception as e:
            print(F"No lo puede eliminar: {e}")
            QMessageBox.warning(self, "No puede", f"{e}")
            
             
            
            
            
            
    # esta funcion es para que el usuario le de dobleclick a la fila del empleado
    # ponga la cedula en la barra de busqueda    
    def on_double_click(self, index):
         
        # Obtener la fila donde se hizo doble click
        row = index.row()
        
        # Obtener el texto de la primera columna (nombre)
        cedula = modelo.item(row, 0).text()
        
        # Establecer el texto en el QLineEdit
        # iterar cada tupla de la lista
        for empleado in self.lista_empleados_actual:
            
            # si la busqueda de la cedula esta en la posicion 5 de la tupla que es donde esta la cedula
            
            if cedula in empleado:
                
                # id del empleado
                empleado_id = empleado[0]
                
                
                print(f"el empleado es: \n\nNombre:{empleado[1]}\nID:{empleado[0]}")
                
                self.stacked_widget.setCurrentIndex(11)
                
                pantalla_perfil_empleado = self.stacked_widget.widget(11)
                        
                pantalla_perfil_empleado.mostra_info_empleado(empleado_id)
                
                self.barra_de_busqueda.clear()
                
                break
            
            
                    
        
    # esto accede al perfil del empleado desde la barra de busqueda
    def acceder_perfil_empleado(self):
        
        
        
        try:
            # si tiene valor 
            if self.barra_de_busqueda.text().strip():
                
                
                # iterar cada tupla de la lista
                for empleado in self.lista_empleados_actual:
                    
                    #print("\n",empleado)
                    
                    
                    
                    # si la busqueda de la cedula esta en la posicion 5 de la tupla que es donde esta la cedula
                    
                    if self.barra_de_busqueda.text() in empleado:
                        
                        # id del empleado
                        empleado_id = empleado[0]
                        
                        
                        print(f"el empleado es: \n\nNombre:{empleado[1]}\nID:{empleado[0]}")
                        
                        self.stacked_widget.setCurrentIndex(11)
                        
                        pantalla_perfil_empleado = self.stacked_widget.widget(11)
                        
                        pantalla_perfil_empleado.mostra_info_empleado(empleado_id)
                        
                        self.barra_de_busqueda.clear()
                        
                        break
                    
                    
                        
            else:
                #print(f"el empleado es: \nNombre:{empleado[2]}\n ID:{empleado[0]}")
                QMessageBox.critical(self, "Error", "La barra de busqueda esta vacia")

                return
                    
                
        except:
            
            return
        
    
    
    
        
    # Metodo para la busqueda dinamica
    ##########################################################################################################################
    ##########################################################################################################################
    
        
    ################################################################################################################33
    ################################################################################################################33
    
    
    
 
    
    #Metodo para filtrar por tipo de cargo
    def filtrar_por_tipo_cargo(self):
    
        try:
            situacion_selec = self.boton_de_situacion.currentText()
                        
            # me pasa el indice donde esta id en la tupla, el id esta en el indice 0
            tipo_cargo_id = FuncionSistema.buscar_id_por_nombre_del_elemento(self.boton_de_opciones.currentText(), self.lista_tipo_cargo, 0)
            
            # se le manda el id al metodo del servicio
            empleados = detalle_cargo_servicio.obtener_detalles_cargo_por_tipo_cargo_o_especialidad_o_cedula(tipo_cargo_id = tipo_cargo_id, especialidad_id= None, situacion = situacion_selec)
            
            #self.boton_de_situacion
            #print(empleados)
            self.configurar_filtro()
            
            
            # funcion para cargar la tabla segun el cargo
            self.cargar_empleados_en_tabla(tabla= self.tabla_ver_personal,empleados= empleados, indice_cedula= 2, indice_1er_nombre= 3, indice_2do_nombre= 4,
                                            indice_1er_apellido= 6, indice_2do_apellido= 7, indice_estado= 9)

            # actualizar la tabla segun el cargo
            self.actualizar_tabla(tipo_cargo_id= tipo_cargo_id, especialidad_id= None, situacion_selec= situacion_selec, indice_cedula= 2, indice_1er_nombre= 3, indice_2do_nombre= 4,
                                            indice_1er_apellido= 6, indice_2do_apellido= 7, indice_estado= 9)
            
            # si es docente habilita este boton de especialidades
            self.habilitar_boton_especialidades()
            self.barra_de_busqueda.clear()
            
                        #self.label_contador.setText(str(len(empleados)))
        except Exception as e:
            
            modelo.clear()
            self.label_contador.setText("0")
            QMessageBox.information(self, "No hay registros", f"{e}")
            
            FuncionSistema.mostrar_errores_por_excepcion(e, "filrar_por_tipo_cargo")             
                    
    # Metodo para filtrar por especialidad           
    def filtrar_por_especialidad(self):
        
        # guardamos la seleccion
        situacion_selec = self.boton_de_situacion.currentText()
        
        
        
        # buscar en la base de datos el tipo de cargo docente
        for tipo_cargo in self.lista_tipo_cargo:
                
            # si el cargo es docente que me guarde el id
            if "docente" in tipo_cargo[1].lower():
                
                id_cargo_docente = tipo_cargo[0]
                break
            else:
                
                pass
        
        try:
            # comparamos si tiene seleccion y si esta habilitado el boton
            if self.boton_especialidades.currentText() and self.boton_especialidades.isEnabled() and not self.boton_especialidades.currentIndex() == 0:
                
            
                especialidad_id = FuncionSistema.buscar_id_por_nombre_del_elemento(self.boton_especialidades.currentText(), self.lista_especialidades, 0)
                # si es verdadero se le manda el id que esta en el indice 0 de la tupla
                empleados_por_especialidad = detalle_cargo_servicio.obtener_detalles_cargo_por_tipo_cargo_o_especialidad_o_cedula(tipo_cargo_id= id_cargo_docente,especialidad_id= especialidad_id, situacion= situacion_selec)
                
                self.configurar_filtro()
                self.cargar_empleados_en_tabla(tabla= self.tabla_ver_personal, empleados= empleados_por_especialidad, indice_cedula= 2, indice_1er_nombre= 3,
                                            indice_2do_nombre= 4, indice_1er_apellido= 6, indice_2do_apellido= 7, indice_estado= 9)
    
                self.actualizar_tabla(tipo_cargo_id= id_cargo_docente, especialidad_id= especialidad_id, situacion_selec= situacion_selec, indice_cedula= 2, indice_1er_nombre= 3,
                                            indice_2do_nombre= 4, indice_1er_apellido= 6, indice_2do_apellido= 7, indice_estado= 9)
                
                self.barra_de_busqueda.clear()
                #print(f"\n {especialidad_selec} si esta en la tupla {especialidad}")
                
                
                        
            else:
                
                empleados = detalle_cargo_servicio.obtener_detalles_cargo_por_tipo_cargo_o_especialidad_o_cedula(tipo_cargo_id= id_cargo_docente, situacion = situacion_selec)
                self.cargar_empleados_en_tabla(tabla= self.tabla_ver_personal, empleados= empleados, indice_cedula= 2, indice_1er_nombre= 3,
                                                    indice_2do_nombre= 4, indice_1er_apellido= 6, indice_2do_apellido= 7, indice_estado= 9)
            
                self.actualizar_tabla(tipo_cargo_id= id_cargo_docente, situacion_selec= situacion_selec, indice_cedula= 2, indice_1er_nombre= 3,
                                                    indice_2do_nombre= 4, indice_1er_apellido= 6, indice_2do_apellido= 7, indice_estado= 9)
                        
            
        except Exception as e:
            
            modelo.clear()
            self.label_contador.setText("0")
            QMessageBox.information(self, "Error", f"{e}")
        
    # Metodo para habilitar el boton de especialidades    
    def habilitar_boton_especialidades(self):
        
        if self.boton_de_opciones.currentText() == "DOCENTE":
            
            self.boton_especialidades.setEnabled(True)
        
        else:
            self.boton_especialidades.setCurrentIndex(0)
            self.boton_especialidades.setEnabled(False)              



    # Metodo para actualizar la tabla
    def actualizar_tabla(self,  indice_cedula = None, situacion_selec = None, indice_1er_nombre = None, indice_2do_nombre = None, indice_1er_apellido = None, indice_2do_apellido = None, indice_estado = None, tipo_cargo_id = None, especialidad_id = None):
        
            empleados_actualizados = detalle_cargo_servicio.obtener_detalles_cargo_por_tipo_cargo_o_especialidad_o_cedula(tipo_cargo_id=tipo_cargo_id, especialidad_id= especialidad_id, situacion= situacion_selec)
            
            self.cargar_empleados_en_tabla(tabla= self.tabla_ver_personal, empleados= empleados_actualizados, indice_cedula= indice_cedula,
                                           indice_1er_nombre= indice_1er_nombre, indice_2do_nombre= indice_2do_nombre,
                                           indice_1er_apellido= indice_1er_apellido, indice_2do_apellido= indice_2do_apellido, indice_estado= indice_estado)
            
            self.label_contador.setText(str(len(empleados_actualizados)))
            
        

    # Metodo para cargar los empleados en la tabla
    def cargar_empleados_en_tabla(self, tabla, empleados, indice_cedula, indice_1er_nombre, indice_2do_nombre, indice_1er_apellido, indice_2do_apellido, indice_estado):
        columnas = ["Cédula", 
                    "Primer Nombre", 
                    "Segundo Nombre", 
                    "Apellido Paterno", 
                    "Apellido Materno", 
                    "Estado", 
                    "Opciones"]
        
        global modelo
        
        modelo = QStandardItemModel()
        modelo.setHorizontalHeaderLabels(columnas)

        for indice, empleado in enumerate(empleados):
            datos_visibles = [
                empleado[indice_cedula], 
                empleado[indice_1er_nombre], 
                empleado[indice_2do_nombre], 
                empleado[indice_1er_apellido], 
                empleado[indice_2do_apellido], 
                empleado[indice_estado]
            ]

            items = []
            for dato in datos_visibles:
                item = QStandardItem(str(dato) if dato is not None else "")
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                items.append(item)

            modelo.appendRow(items)
            
            # Numerar filas en el encabezado vertical
            header_item = QStandardItem(str(indice + 1))
            header_item.setFlags(Qt.ItemIsEnabled)
            modelo.setVerticalHeaderItem(indice, header_item)

        # AJUSTES DE ALTURA DE FILAS
        for fila in range(modelo.rowCount()):
            tabla.setRowHeight(fila, 40)

        # PROXY --------------------------------------------
        # Crear o configurar el proxy
        if not hasattr(self, 'proxy'):
            self.proxy = QSortFilterProxyModel()
            self.proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)
        
        # Asociar el modelo original al proxy
        self.proxy.setSourceModel(modelo)

        # Establecer que la tabla use el proxy y no el modelo directo
        tabla.setModel(self.proxy)

        # Ahora sí añadimos los botones fila por fila
        for fila in range(modelo.rowCount()):
            widget = QWidget()
            layout = QHBoxLayout(widget)
            boton_editar = QPushButton("Editar")
            boton_editar.setFixedSize(60, 30) 
            boton_editar.setProperty("tipo", "boton_editar")
            boton_editar.setStyleSheet("""
                    QPushButton{
                        font-size:8pt;
                    }
            """) 
            boton_borrar = QPushButton("Borrar")
            boton_borrar.setFixedSize(60, 30)
            boton_borrar.setProperty("tipo", "boton_borrar") 
            boton_borrar.setStyleSheet("""
                    QPushButton{
                        font-size:8pt;
                    }
            """) 

            # Conectar botones - IMPORTANTE: mantener referencia a fila del modelo fuente
            boton_editar.clicked.connect(lambda _, r=fila: self.habilitar_edicion(r))
            boton_borrar.clicked.connect(lambda _, r=fila: self.eliminar_empleado_de_la_bd(r))

            layout.addWidget(boton_editar)
            layout.addWidget(boton_borrar)
            layout.setContentsMargins(3, 3, 3, 3)
            widget.setLayout(layout)

            # Obtener índice en el modelo fuente (última columna "Opciones")
            fuente_index = modelo.index(fila, len(columnas) - 1)
            
            # Convertir al índice del proxy
            proxy_index = self.proxy.mapFromSource(fuente_index)
            
            # Insertar el widget usando el índice convertido del proxy
            tabla.setIndexWidget(proxy_index, widget)
        
            
        
    #Metodos para la tabla de base de datos  
    ################################################################################################################33
    ################################################################################################################33

    
    # Metodo para ir pantalla va a la pantalla de crear nuevo registro
    def ir_a_crear_nuevo_registro(self):
        self.stacked_widget.setCurrentIndex(8)

    # Metodo para ir  a la pantalla de control de llegadaq
    def ir_a_control_de_llegada(self):
        self.stacked_widget.setCurrentIndex(9)
        
    # Metodo para ir  a la pantalla de control de reposos
    def ir_a_control_de_reposos(self):
        self.stacked_widget.setCurrentIndex(10)
        
    


    

