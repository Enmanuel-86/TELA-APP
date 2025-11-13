from PyQt5.QtCore import Qt,QPoint
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (QWidget, QHeaderView,  QHBoxLayout, 
                             QMessageBox, QListWidget, QListWidgetItem, QPushButton)
from PyQt5 import QtGui
import os
from ..elementos_graficos_a_py import Ui_VistaGeneralDelPersonal


##################################
# importaciones de base de datos #
##################################


# repositorios
from repositorios.empleados.empleado_repositorio import EmpleadoRepositorio
from repositorios.empleados.info_laboral_repositorio import InfoLaboralRepositorio
from repositorios.empleados.cargo_empleado_repositorio import CargoEmpleadoRepositorio
from repositorios.empleados.detalle_cargo_repositorio import DetalleCargoRepositorio
from repositorios.empleados.tipo_cargo_repositorio import TipoCargoRepositorio
from repositorios.especialidades.especialidad_repositorio import EspecialidadRepositorio
from repositorios.empleados.historial_enferm_cronicas_repositorio import HistorialEnfermCronicasRepositorio
from repositorios.empleados.info_clinica_empleado_repositorio import InfoClinicaEmpleadoRepositorio



# servicios
from servicios.empleados.empleado_servicio import EmpleadoServicio
from servicios.empleados.info_laboral_servicio import InfoLaboralServicio
from servicios.empleados.detalle_cargo_servicio import DetalleCargoServicio
from servicios.empleados.cargo_empleado_servicio import CargoEmpleadoServicio
from servicios.empleados.tipo_cargo_servicio import TipoCargoServicio
from servicios.especialidades.especialidad_servicio import EspecialidadServicio
from servicios.empleados.historial_enferm_cronicas_servicio import HistorialEnfermCronicasServicio
from servicios.empleados.info_clinica_empleado_servicio import InfoClinicaEmpleadoServicio


##################################
# importaciones de base de datos #
##################################



# instancias de los repositorios

empleado_repositorio = EmpleadoRepositorio()

info_laboral_repositorio = InfoLaboralRepositorio()

cargo_empleado_repositorio = CargoEmpleadoRepositorio()

detalle_cargo_repositorio = DetalleCargoRepositorio()

tipo_cargo_repositorio = TipoCargoRepositorio()

especialidad_repositorio = EspecialidadRepositorio()

histotial_enferm_cronicas_repositorio = HistorialEnfermCronicasRepositorio()

info_clinica_empleado_repositorio = InfoClinicaEmpleadoRepositorio()


# instancia de los servicios

empleado_servicio = EmpleadoServicio(empleado_repositorio)

info_laboral_servicio = InfoLaboralServicio(info_laboral_repositorio)

cargo_empleado_servicio = CargoEmpleadoServicio(cargo_empleado_repositorio)

detalle_cargo_servicio = DetalleCargoServicio(detalle_cargo_repositorio)

tipo_cargo_servicio = TipoCargoServicio(tipo_cargo_repositorio)

especialidad_servicio = EspecialidadServicio(especialidad_repositorio)

histotial_enferm_cronicas_servicio = HistorialEnfermCronicasServicio(histotial_enferm_cronicas_repositorio)

info_clinica_empleado_servicio = InfoClinicaEmpleadoServicio(info_clinica_empleado_repositorio)

##################################
# importaciones de base de datos #
##################################


lista_cargos = cargo_empleado_servicio.obtener_todos_cargos_empleados()
lista_tipo_cargo = tipo_cargo_servicio.obtener_todos_tipos_cargo()


lista_especialidades = especialidad_servicio.obtener_todos_especialidades()

# este es por cargo
#lista_cargo_actual = detalle_cargo_servicio.obtener_todos_detalles_cargo()


## pantalla para ver el registro del personal
class PantallaDeVistaGeneralDelPersonal(QWidget, Ui_VistaGeneralDelPersonal):
    def __init__(self, stacked_widget):
        super().__init__()

        

        
        self.stacked_widget = stacked_widget
        
        
        self.setupUi(self)
        
        #(1, '17536256', 'DOUGLAS', 'JOSE', None, 'MARQUEZ', 'BETANCOURT', 'ADMINISTRATIVO', 'Activo'), (2, '5017497', 'ENMANUEL', 'JESÚS', None, 'GARCIA', 'RAMOS', 'ADMINISTRATIVO', 'Activo')
        self.actualizar_tabla(tipo_cargo_id= 1, especialidad_id= None, indice_cedula= 1, indice_1er_nombre= 2, indice_2do_nombre= 3,
                                                   indice_1er_apellido=5, indice_2do_apellido= 6, indice_estado= 8 )
        ## Ruta relativa de las imagenes ##
        self.boton_buscar.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz","lupa_blanca.png")))
        self.boton_control_de_llegada.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz","control_de_llegada.png")))
        self.boton_control_de_reposos.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "control_de_reposos.png")))
        self.boton_crear_nuevo_registro.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz","nuevo_registro.png")))
        self.imagen_contador.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz","icono_de_usuario.png")))



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
        self.tabla_ver_personal.verticalHeader().setMinimumWidth(40)
        self.tabla_ver_personal.verticalHeader().setDefaultAlignment(Qt.AlignCenter)

        #esto me da el valor de la cedula al darle click a la persona que quiero
        self.tabla_ver_personal.clicked.connect(lambda index: print(index.sibling(index.row(), 0).data()))

        # Opcional: desactivar clic en el encabezado vertical
        self.tabla_ver_personal.verticalHeader().setSectionsClickable(True)

        # Activar filas alternadas y aplicar estilo si quieres
        #self.tabla_ver_personal.setAlternatingRowColors(True)


        # Estilo de encabezados
        self.tabla_ver_personal.horizontalHeader().setStyleSheet("""

            QHeaderView{
                        
                        background:#ffffff;    
                        border-radius:0px;
                        border:none;
                    }
                    


            QHeaderView::section {
                background-color: #008e3e;
                color: white;
                padding: 0px;
                font: 75 14pt "Arial";
                
            
            }
        """)

        self.tabla_ver_personal.verticalHeader().setStyleSheet("""
                    
                    QHeaderView{
                        
                        background:#ffffff;    
                        border-radius:0px;
                        border:none;
                    }
                    
                    QHeaderView::section {
                        background-color: #ffffff;
                        font: 75 14pt "Arial";



                    }
                """)


        self.tabla_ver_personal.setStyleSheet("""
                            QTableView {
                                
                                gridline-color: 5px black;
                                border-radius:0px;
                                background-color:white;
                                font: 75 14pt "Arial";
                                margin:10px;
                            }
                        
                            QHeaderView::section {
                                
                                font-weight: bold;  
                            }
                        """)
        
        



        # conectar botones a los metodos para ir a las otras pantallas
        self.boton_crear_nuevo_registro.clicked.connect(self.ir_a_crear_nuevo_registro)
        self.boton_control_de_llegada.clicked.connect(self.ir_a_control_de_llegada)
        self.boton_control_de_reposos.clicked.connect(self.ir_a_control_de_reposos)
        self.boton_buscar.clicked.connect(self.acceder_perfil_empleado)
        

        ## logica de Base de datos para mostrar a los empleados
        
        self.boton_de_opciones.currentIndexChanged.connect(self.filtrar_por_tipo_cargo)
        
        self.boton_especialidades.currentIndexChanged.connect(self.filtrar_por_especialidad)
        
        # cargar catalogo de los tipos de cargos
        self.cargar_tipos_cargos()
        
        # cargar catalogos de las especialidades
        self.cargar_especialidades()
        
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
        self.resultados.setStyleSheet("background-color: white; border: 1px solid gray;border-radius:0px; padding:10px;")
        self.resultados.itemClicked.connect(self.seleccionar_item)
        self.resultados.hide() 
    
    ##########################################################################################################################
    ##########################################################################################################################
    # Metodo para la busqueda dinamica
    
    
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
            if texto in persona[6] or texto in persona[1].lower()
        ]

        if not coincidencias:
            self.resultados.hide()
            return

        for persona in coincidencias:
            item = f'{persona[6]} - {persona[1]} {persona[4]}'
            self.resultados.addItem(QListWidgetItem(item))

        # Ocultar si hay una coincidencia exacta por cédula
        if len(coincidencias) == 1 and coincidencias[0][1] == texto:
            self.resultados.hide()
        else:
            self.mostrar_lista()




    def mostrar_lista(self):
        pos = self.barra_de_busqueda.mapTo(self, QPoint(0, self.barra_de_busqueda.height()))
        self.resultados.move(pos)
        self.resultados.resize(self.barra_de_busqueda.width(), 100)
        self.resultados.show()
        
        
        
        
    def seleccionar_item(self, item):
        cedula = item.text().split(" - ")[0]
        self.barra_de_busqueda.setText(cedula)
        self.resultados.hide()
        
        
    
    def eliminar_empleado(self, fila):
        
        pass
        
        
        
        
    def habilitar_edicion(self, fila):
        
        try:
            #cedula = modelo.item(fila, 0).text()
            
            #empleado_id = self.buscar_id_empleado(cedula)
            
            self.stacked_widget.setCurrentIndex(8)
            
            
            #self.mostra_info_empleado(empleado_id)
            
            
            

            
        except Exception as e:
            print(f"Algo paso: {e}")
            
    
            

    
    
        
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
    
    
    #Metodos para la tabla de base de datos
    
    # Metodo para buscar al empleado por su id
    def buscar_id_empleado(self, cedula):
        
        for empleado in self.lista_empleados_actual:
            
            if cedula in empleado:
                
                empleado_id = empleado[0]
                
                return empleado_id
                
                
            
            else:
                
                pass
    
    
    def cargar_tipos_cargos(self):
        
        
        for tipo_cargo in lista_tipo_cargo:
            
            self.boton_de_opciones.addItem(tipo_cargo[1])
            
            
            
    #Metodo para cargar la lista de especialidades
    def cargar_especialidades(self):
        
        self.boton_especialidades.addItem("Seleccione aqui")
        #print(lista_especialidades)
        for especialidad in lista_especialidades:
            
            self.boton_especialidades.addItem(especialidad[1])
    
    
    #Metodo para filtrar por tipo de cargo
    def filtrar_por_tipo_cargo(self):
    
        tipo_cargo_selec = self.boton_de_opciones.currentText()
        
        # si el boton esta pulsado
        if self.boton_de_opciones.currentText() :
            
            # print("\n",self.boton_de_opciones.currentText())
            
            # aqui se obtiene el id del tipo de cargo que esta en el combobox boton_de_opciones
            for tipo_cargo in lista_tipo_cargo:
                
                # si la seleccion esta en el catalogo
                if tipo_cargo_selec in tipo_cargo:
                    
                    # me pasa el indice donde esta id en la tupla, el id esta en el indice 0
                    tipo_cargo_id = tipo_cargo[0]
                    
                    # se le manda el id al metodo del servicio
                    empleados = detalle_cargo_servicio.obtener_detalles_cargo_por_tipo_cargo_o_especialidad_o_cedula(tipo_cargo_id = tipo_cargo_id, especialidad_id= None)
                    
                    # funcion para cargar la tabla segun el cargo
                    self.cargar_empleados_en_tabla(tabla= self.tabla_ver_personal,empleados= empleados, indice_cedula= 1, indice_1er_nombre= 2, indice_2do_nombre= 3,
                                                   indice_1er_apellido= 5, indice_2do_apellido= 6, indice_estado= 8)

                    # actualizar la tabla segun el cargo
                    self.actualizar_tabla(tipo_cargo_id= tipo_cargo_id, especialidad_id= None, indice_cedula= 1, indice_1er_nombre= 2, indice_2do_nombre= 3,
                                                   indice_1er_apellido= 5, indice_2do_apellido= 6, indice_estado= 8)
                    
                    # si es docente habilita este boton de especialidades
                    self.habilitar_boton_especialidades()
                    
                    #self.label_contador.setText(str(len(empleados)))
                    
                    
    # Metodo para filtrar por especialidad           
    def filtrar_por_especialidad(self):
        
        # guardamos la seleccion
        especialidad_selec = self.boton_especialidades.currentText()
        
        
        
        # buscar en la base de datos el tipo de cargo docente
        for tipo_cargo in lista_tipo_cargo:
                
            # si el cargo es docente que me guarde el id
            if "docente" in tipo_cargo[1].lower():
                
                id_cargo_docente = tipo_cargo[0]
                break
            else:
                
                pass
        
        try:
            # comparamos si tiene seleccion y si esta habilitado el boton
            if self.boton_especialidades.currentText() and self.boton_especialidades.isEnabled() and not self.boton_especialidades.currentIndex() == 0:
                
                # iteramos cada tupla de la lista
                for especialidad in lista_especialidades:
                    
                    # comparamos si la especialidad seleecionada esta en la tupla ejemplo:
                    # "ceramicas" esta en (1,"ceramica")? si es verdadero realiza las instrucciones
                    # si no es verdadero como este caso
                    # "ceramica" esta en (3,"hoteleria")? si no esta el va cambiando de tupla hasta conseguir la indicada
                    if especialidad_selec in especialidad:
                        
                        
                        especialidad_id = especialidad[0]
                        # si es verdadero se le manda el id que esta en el indice 0 de la tupla
                        empleados_por_especialidad = detalle_cargo_servicio.obtener_detalles_cargo_por_tipo_cargo_o_especialidad_o_cedula(tipo_cargo_id= id_cargo_docente,especialidad_id= especialidad_id)
                        
                        
                        self.cargar_empleados_en_tabla(tabla= self.tabla_ver_personal, empleados= empleados_por_especialidad, indice_cedula= 2, indice_1er_nombre= 3,
                                                    indice_2do_nombre= 4, indice_1er_apellido= 6, indice_2do_apellido= 7, indice_estado= 9)
            
                        self.actualizar_tabla(tipo_cargo_id= id_cargo_docente, especialidad_id= especialidad_id, indice_cedula= 2, indice_1er_nombre= 3,
                                                    indice_2do_nombre= 4, indice_1er_apellido= 6, indice_2do_apellido= 7, indice_estado= 9)
                        
                        
                        #print(f"\n {especialidad_selec} si esta en la tupla {especialidad}")
                        
                        break
                    else:
                        
                        #print(f"{especialidad_selec} no esta en la tupla {especialidad}")
                        
                        pass
                        
            else:
                
                pass
            
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
    def actualizar_tabla(self,  indice_cedula = None, indice_1er_nombre = None, indice_2do_nombre = None, indice_1er_apellido = None, indice_2do_apellido = None, indice_estado = None, tipo_cargo_id = None, especialidad_id = None):
        
            empleados_actualizados = detalle_cargo_servicio.obtener_detalles_cargo_por_tipo_cargo_o_especialidad_o_cedula(tipo_cargo_id=tipo_cargo_id, especialidad_id= especialidad_id)
            self.cargar_empleados_en_tabla(tabla= self.tabla_ver_personal, empleados= empleados_actualizados, indice_cedula= indice_cedula,
                                           indice_1er_nombre= indice_1er_nombre, indice_2do_nombre= indice_2do_nombre,
                                           indice_1er_apellido= indice_1er_apellido, indice_2do_apellido= indice_2do_apellido, indice_estado= indice_estado)
            
            self.label_contador.setText(str(len(empleados_actualizados)))
            
        

    # Metodo para cargar los empleados en la tabla
    def cargar_empleados_en_tabla(self, tabla, empleados, indice_cedula, indice_1er_nombre, indice_2do_nombre, indice_1er_apellido, indice_2do_apellido, indice_estado):
        columnas = ["Cédula", "Primer Nombre", "Segundo Nombre", "Apellido Paterno", "Apellido Materno", "Estado", "Opciones"]
        
        global modelo
        
        modelo = QStandardItemModel()
        modelo.setHorizontalHeaderLabels(columnas)

        for indice, empleado in enumerate(empleados):
            #datos_visibles = [empleado[1], empleado[2], empleado[3], empleado[4], empleado[5], empleado[7]]
            
            datos_visibles = [empleado[indice_cedula], empleado[indice_1er_nombre], empleado[indice_2do_nombre], empleado[indice_1er_apellido], empleado[indice_2do_apellido], empleado[indice_estado]]

            items = []

            
            
            for dato in datos_visibles:
                item = QStandardItem(str(dato) if dato is not None else "")
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                items.append(item)

            modelo.appendRow(items)
            
            for fila in range(modelo.rowCount()):
                tabla.setRowHeight(fila, 40)

            # Numerar filas en el encabezado vertical
            header_item = QStandardItem(str(indice + 1))
            header_item.setFlags(Qt.ItemIsEnabled)
            modelo.setVerticalHeaderItem(indice, header_item)

        # Muy importante: asignar modelo primero
        tabla.setModel(modelo)

        #  Ahora sí añadimos los botones fila por fila
        for fila in range(modelo.rowCount()):
            widget = QWidget()
            layout = QHBoxLayout(widget)
            boton_editar = QPushButton("Editar")
            boton_editar.setFixedSize(60, 30) 
            boton_borrar = QPushButton("Borrar")
            boton_borrar.setFixedSize(60, 30) 
            
            
            boton_editar.setStyleSheet("""
                                        QPushButton{

                                        
                                            
                                            background-color: rgb(244, 131, 2);
                                            
                                            color: rgb(255, 255, 255);
                                        }
                                        
                                        QPushButton:hover{
                                            
                                            background-color: rgb(191, 64, 0);
                                        }

                                    """)
            
            boton_borrar.setStyleSheet("""
                                        QPushButton{

                                        
                                        
                                        background-color: rgb(255, 0, 0);
                                        
                                        color: rgb(255, 255, 255);
                                    }
                                    
                                    QPushButton:hover{
                                    
                                        background-color: rgb(147, 0, 0);
                                    }
                                    
                                    """)
            
            boton_borrar.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), "..","recursos_de_imagenes", "iconos_de_interfaz","borrar.png")))
            boton_editar.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), "..","recursos_de_imagenes", "iconos_de_interfaz","editar.png")))


            # Conectar botones
            boton_editar.clicked.connect(lambda _, r=fila: self.habilitar_edicion(r))
            #btn_delete.clicked.connect(lambda _, r=fila: self.borrar_alumno(r))

            layout.addWidget(boton_editar)
            layout.addWidget(boton_borrar)
            layout.setContentsMargins(3, 3, 3, 3)
            widget.setLayout(layout)

            index = modelo.index(fila, len(columnas) - 1)  # última columna ("Opciones")
            tabla.setIndexWidget(index, widget)
        
    
        
        
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
        
    


    

