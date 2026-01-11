from PyQt5.QtCore import Qt,QPoint, QSortFilterProxyModel
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (QWidget, QHeaderView,  QVBoxLayout, 
                             QPushButton , QHBoxLayout,QMessageBox, QListWidget, QListWidgetItem, QLabel, QApplication)
from PyQt5 import QtGui, QtCore
import os
from ..elementos_graficos_a_py import Ui_VistaGeneralDeAlumnos
from ..utilidades.base_de_datos import especialidad_servicio
from ..utilidades.funciones_sistema import FuncionSistema

##################################
# importaciones de base de datos #
##################################

# Repositorios

from repositorios.alumnos.alumno_repositorio import AlumnoRepositorio
from repositorios.alumnos.inscripcion_repositorio import InscripcionRepositorio
from repositorios.alumnos.info_bancaria_alumno_repositorio import InfoBancarioAlumnoRepositorio
from repositorios.alumnos.info_clinica_alumno_repositorio import InfoClinicaAlumnoRepositorio
from repositorios.alumnos.inscripcion_repositorio import InscripcionRepositorio
from repositorios.alumnos.representante_repositorio import RepresentanteRepositorio

# Servicios

from servicios.alumnos.alumno_servicio import AlumnoServicio
from servicios.alumnos.inscripcion_servicio import InscripcionServicio
from servicios.alumnos.info_bancaria_alumno_servicio import InfoBancariaAlumnoServicio
from servicios.alumnos.info_clinica_alumno_servicio import InfoClinicaAlumnoServicio
from servicios.alumnos.inscripcion_servicio import InscripcionServicio
from servicios.alumnos.representante_servicio import RepresentanteServicio



# Instanacias Repositorios


alumnos_repositorio = AlumnoRepositorio()

inscripcion_repositorio = InscripcionRepositorio()

info_bancaria_alumno_repositorio = InfoBancarioAlumnoRepositorio()

info_clinica_alumno_repositorio = InfoClinicaAlumnoRepositorio()

representante_repositorio = RepresentanteRepositorio()

# Instancia Servicios


alumnos_servicio = AlumnoServicio(alumnos_repositorio)

inscripcion_servicio = InscripcionServicio(inscripcion_repositorio)

info_bancaria_alumno_servicio = InfoBancariaAlumnoServicio(info_bancaria_alumno_repositorio)

info_clinica_alumno_servicio = InfoClinicaAlumnoServicio(info_clinica_alumno_repositorio)

representante_servicio = RepresentanteServicio(representante_repositorio)

##################################
# importaciones de base de datos #
##################################




#lista_alumnos = alumnos_servicio.obtener_todos_alumnos()

#botones_opciones = QWidget()
#boton_borrar = QPushButton("Borrar", botones_opciones)
#boton_editar = QPushButton("Editar", botones_opciones)

class PantallaDeVistaGeneralDeAlumnos(QWidget, Ui_VistaGeneralDeAlumnos):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.setupUi(self)
        
        self.configurar_filtro()
                
        self.msg_box = QMessageBox(self)
        
        # Crear botones personalizados
        self.boton_si = self.msg_box.addButton("Sí", QMessageBox.YesRole)
        self.boton_no = self.msg_box.addButton("No", QMessageBox.NoRole)
        
        # Estableciendo estilo de la tabla
            
        #self.tabla_ver_alumnos.setColumnWidth(6, 300) 

        self.tabla_ver_alumnos.horizontalHeader().setVisible(True)
        self.tabla_ver_alumnos.horizontalHeader().setMinimumHeight(50)
        self.tabla_ver_alumnos.horizontalHeader().setMinimumWidth(10)
        self.tabla_ver_alumnos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_ver_alumnos.horizontalHeader().setSectionsClickable(False)
        
        self.tabla_ver_alumnos.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tabla_ver_alumnos.verticalHeader().setVisible(True)
        self.tabla_ver_alumnos.verticalHeader().setMinimumWidth(40)
        self.tabla_ver_alumnos.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.tabla_ver_alumnos.verticalHeader().setFixedWidth(20)

        #esto me da el valor de la cedula al darle click a la persona que quiero
        self.tabla_ver_alumnos.clicked.connect(lambda index: print(index.sibling(index.row(), 2).data()))

        # Opcional: desactivar clic en el encabezado vertical
        self.tabla_ver_alumnos.verticalHeader().setSectionsClickable(True)

        # Activar filas alternadas y aplicar estilo si quieres
        #self.tabla_ver_alumnos.setAlternatingRowColors(True)
        

        
    
        # conexion de botones
        self.boton_crear_nuevo_registro.clicked.connect(lambda _: self.ir_crear_nuevo_registro())
        self.boton_buscar.clicked.connect(lambda _: self.aplicar_filtro(self.barra_de_busqueda.text()))
        self.boton_asistencia_alumnos.clicked.connect(lambda _: self.ir_asistencia_alumno())
        self.boton_especialidades.currentIndexChanged.connect(self.filtrar_por_especialidad)
        self.boton_entidades.currentIndexChanged.connect(lambda: self.filtrar_por_ente_seleccionado())
        self.tabla_ver_alumnos.doubleClicked.connect(self.acceder_al_prefil_del_alumno_desde_la_tabla)
        self.barra_de_busqueda.textChanged.connect(lambda texto: self.filtrar_resultados(texto) if not texto == "" else self.filtrar_por_ente_seleccionado())
        self.barra_de_busqueda.returnPressed.connect(lambda: self.aplicar_filtro(self.barra_de_busqueda.text()) )
        self.barra_de_busqueda.textChanged.connect(lambda texto: self.resultados.hide() if texto == "" else None )
        
        self.lista_especialidades = especialidad_servicio.obtener_todos_especialidades()
        self.lista_alumnos_actual = alumnos_servicio.obtener_todos_alumnos()
        
        
        
        
        
        
        
        # Carga las especialidades al boton deplegable
        FuncionSistema.cargar_elementos_para_el_combobox(self.lista_especialidades, self.boton_especialidades, 1)
        
        
            
        
        
        # Lista de coincidencias
        self.resultados = QListWidget(self)
        self.resultados.setFocusPolicy(Qt.NoFocus)
        self.resultados.setMouseTracking(True)
        self.resultados.setStyleSheet("padding:10px;")
        self.resultados.itemClicked.connect(self.seleccionar_item)
        self.resultados.hide() 
        
        
  
    def actualizar_combobox_especialidades(self):
        
        self.lista_especialidades = especialidad_servicio.obtener_todos_especialidades()
        FuncionSistema.cargar_elementos_para_el_combobox(self.lista_especialidades, self.boton_especialidades, 1)
            
            
            
            
        
        
        
        
        
        
        
        
        
     
    ################################################################################################################################ 
    ################################################################################################################################


    
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

            if self.boton_entidades.currentIndex() == 0: # si es alumno
                # Obtenemos el índice del proxy
                index_proxy = self.proxy.index(fila, 0)

                # Convertimos el índice del proxy al índice original del modelo
                index_modelo = self.proxy.mapToSource(index_proxy)

                # Obtenemos la cédula desde la columna 1 del modelo
                cedula = modelo.index(index_modelo.row(), 1).data()

                # Obtenemos nombre desde la columna 2
                nombre = modelo.index(index_modelo.row(), 2).data()

                # Obtenemos apellido desde la columna 3
                apellido = modelo.index(index_modelo.row(), 3).data()

                # Convertimos todo a minúsculas para comparar
                cedula_lower = str(cedula).lower()
                nombre_lower = str(nombre).lower()
                apellido_lower = str(apellido).lower()
                
                
            if self.boton_entidades.currentIndex() == 1: # si es representante
                # Obtenemos el índice del proxy
                index_proxy = self.proxy.index(fila, 0)

                # Convertimos el índice del proxy al índice original del modelo
                index_modelo = self.proxy.mapToSource(index_proxy)

                # Obtenemos la cédula desde la columna 1 del modelo
                cedula = modelo.index(index_modelo.row(), 0).data()

                # Obtenemos nombre desde la columna 2
                nombre = modelo.index(index_modelo.row(), 1).data()

                # Obtenemos apellido desde la columna 3
                apellido = modelo.index(index_modelo.row(), 2).data()

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
        
        
        
        
    # esta funcion es para que el usuario le de dobleclick a la fila del empleado
    # para que lo lleve a la pantalla de perfil del alumno
    def acceder_al_prefil_del_alumno_desde_la_tabla(self, index):
        
        """
            Este Metodo sirve para acceder al perfil del alumno desde la tabla que se muestra en pantalla
            
            Tomamos la fila y si hace el doble click este accede al perfil del alumno
        """
         
        # Obtener la fila donde se hizo doble click
        row = index.row()
        
        # Obtener el texto de la primera columna (nombre)
        cedula = modelo.item(row, 1).text()
        
        try:
            
            # buscamo el id del alumno para acceder a su perfil
            # iteramos cada alumno en la lista de alumnos
            for alumno in self.lista_alumnos_actual:
                
                # comparamos la cedula de cada que esta en la lista para ver si es igual para obtener su id
                if cedula == alumno[1]:
                    
                    # luego nos vamos a la pantalla del perfil del alumno
                    self.stacked_widget.setCurrentIndex(6)
                    self.barra_de_busqueda.clear()
                    pantalla_perfil_alumno = self.stacked_widget.widget(6)
                    pantalla_perfil_alumno.mostrar_la_info_alumno(alumno_id= alumno[0])
                    
                    
                    
                    break
            
            
        except Exception as e:
            
            print("Error en la funcion acceder_al_prefil_del_alumno_desde_la_tabla", f"{e}")
    

    ################################################################################################################    
    ################################################################################################################
    
    def filtrar_en_la_barra_de_busqueda(self):
        
        """
        
        """
        
        if self.barra_de_busqueda.text() and self.boton_entidades.currentIndex() == 0: # si es alumno
        
            self.filtrar_por_especialidad()
            
        elif self.barra_de_busqueda.text() and self.boton_entidades.currentIndex() == 1: # si es representante
            
            self.filtrar_por_ente_seleccionado()
            
            
            
    
    def filtrar_por_ente_seleccionado(self):
        """
            Este metodo sirve para filtrar segun el ente seleccionado alumno o representante, para ver su informacion con mas detalles y editarlo
        """
    
        if self.boton_entidades.currentIndex() == 0: # si es alumno
            
            self.boton_especialidades.setEnabled(True)
            self.label_titulo_contador.setText("N° Estudiantes")
            self.barra_de_busqueda.clear()
            self.configurar_filtro()
            self.filtrar_por_especialidad()
            
        elif self.boton_entidades.currentIndex() == 1: # si es representante
            
            self.boton_especialidades.setEnabled(False)
            self.barra_de_busqueda.clear()
            self.configurar_filtro()
            lista_representates = representante_servicio.obtener_todos_representantes()
            self.cargar_representantes_en_tabla(self.tabla_ver_alumnos, lista_representates)
            self.label_contador.setText(str(len(lista_representates)))
            self.label_titulo_contador.setText("N° Representantes")
            print("representantes")
    

    
    # Metodo para filtrar por especialidad
    def filtrar_por_especialidad(self):
        
        especialidad_selec = self.boton_especialidades.currentText()
        
        try:
        
            # si el boton es pulsado
            if self.boton_especialidades.currentText():
                
                # Iteramos todas las especialidades, ejemplo (1,"ceramica")
                for especialidad in self.lista_especialidades:
                    
                    # si el boton esta en X especialidad entonces
                    if especialidad_selec in especialidad:
                        
                        #obtenemos el id de la especialidad
                        especialidad_id = especialidad[0]
                        
                        alumnos_especialidad = inscripcion_servicio.obtener_inscripcion_por_especialidad(especialidad_id = especialidad_id)
                        
                        
                        
                        self.cargar_alumnos_en_tabla(self.tabla_ver_alumnos, alumnos_especialidad)
                        
                                                
                        self.actualizar_tabla(especialidad_id)
                        
                        break
                        
                    
                    
        except Exception as e:
            
            modelo.clear()
            self.label_contador.setText("0")
            QMessageBox.information(self, "No hay registros", f"{e}")
            
            FuncionSistema.mostrar_errores_por_excepcion(e, "filrar_por_especialidad")
    
    
    
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

        
    
    def cargar_representantes_en_tabla(self, tabla, representantes):
        columnas = [
            "Cédula", "Nombre", "Paterno",
            "Estado Civil", "Opciones"
        ]

        global modelo
        modelo = QStandardItemModel()
        modelo.setHorizontalHeaderLabels(columnas)

        # Primero cargamos los datos
        for indice, representante in enumerate(representantes):
            datos_visibles = [
            representante[1],  # Cedula
            representante[2],  # Nombre
            representante[3],  # Apellido
            representante[8],  # Estado civil
            
            ]


            items = []
            for dato in datos_visibles:
                item = QStandardItem(str(dato) if dato is not None else "")
                # Evita edición del usuario
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                items.append(item)

            # Agregar la fila completa
            modelo.appendRow(items)
            
            
            for fila in range(modelo.rowCount()):
                tabla.setRowHeight(fila, 40)

            # Numerar filas en el encabezado vertical
            header_item = QStandardItem(str(indice + 1))
            header_item.setFlags(Qt.ItemIsEnabled)
            modelo.setVerticalHeaderItem(indice, header_item)

        #  Muy importante: asignar modelo primero
        tabla.setModel(modelo)
        
        
        # PROXY --------------------------------------------
        # Asociar el modelo original al proxy
        self.proxy.setSourceModel(modelo)

        # Establecer que la tabla use el proxy y no el modelo directo
        tabla.setModel(self.proxy)


        #  Ahora sí añadimos los botones fila por fila
        for fila in range(modelo.rowCount()):
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
            #boton_borrar = QPushButton("Borrar")
            #boton_borrar.setFixedSize(60, 30) 
            #boton_borrar.setProperty("tipo", "boton_borrar")
            #boton_borrar.setStyleSheet("""
            #        QPushButton{
            #            font-size:8pt;
            #        }
            #""") 
            

            # Conectar botones
            #boton_editar.clicked.connect(lambda _, fila=fila: self.habilitar_edicion_alumno(fila))
            #boton_borrar.clicked.connect(lambda _, fila=fila: self.eliminar_alumno_de_la_bd(fila))

            layout.addWidget(boton_editar)
            #layout.addWidget(boton_borrar)
            layout.setContentsMargins(3, 3, 3, 3)
            widget.setLayout(layout)

            index = modelo.index(fila, len(columnas) - 1)  # última columna ("Opciones")
            tabla.setIndexWidget(index, widget)
       

            # Insertar el widget usando el índice convertido para el proxy
            proxy_index = self.proxy.mapFromSource(index)

            tabla.setIndexWidget(proxy_index, widget)
        
        
    
    # Método para cargar los alumnos en la tabla
    def cargar_alumnos_en_tabla(self, tabla, alumnos):
        columnas = [
            "Matricula", "Cédula", "Primer Nombre", "Apellido Paterno",
            "Situación", "Opciones"
        ]

        global modelo
        modelo = QStandardItemModel()
        modelo.setHorizontalHeaderLabels(columnas)

        # Primero cargamos los datos
        for indice, alumno in enumerate(alumnos):
            datos_visibles = [
            alumno[5],  # Matricula
            alumno[1],  # Cedula
            alumno[2],  # Primer Nombre
            alumno[3],  # Apellido
            alumno[9]   # Situacion
            ]


            items = []
            for dato in datos_visibles:
                item = QStandardItem(str(dato) if dato is not None else "")
                # Evita edición del usuario
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                items.append(item)

            # Agregar la fila completa
            modelo.appendRow(items)
            
            
            for fila in range(modelo.rowCount()):
                tabla.setRowHeight(fila, 40)

            # Numerar filas en el encabezado vertical
            header_item = QStandardItem(str(indice + 1))
            header_item.setFlags(Qt.ItemIsEnabled)
            modelo.setVerticalHeaderItem(indice, header_item)

        #  Muy importante: asignar modelo primero
        tabla.setModel(modelo)
        
        
        # PROXY --------------------------------------------
        # Asociar el modelo original al proxy
        self.proxy.setSourceModel(modelo)

        # Establecer que la tabla use el proxy y no el modelo directo
        tabla.setModel(self.proxy)


        #  Ahora sí añadimos los botones fila por fila
        for fila in range(modelo.rowCount()):
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
            boton_editar.clicked.connect(lambda _, fila=fila: self.habilitar_edicion_alumno(fila))
            boton_borrar.clicked.connect(lambda _, fila=fila: self.eliminar_alumno_de_la_bd(fila))

            layout.addWidget(boton_editar)
            layout.addWidget(boton_borrar)
            layout.setContentsMargins(3, 3, 3, 3)
            widget.setLayout(layout)

            index = modelo.index(fila, len(columnas) - 1)  # última columna ("Opciones")
            tabla.setIndexWidget(index, widget)
       

            # Insertar el widget usando el índice convertido para el proxy
            proxy_index = self.proxy.mapFromSource(index)

            tabla.setIndexWidget(proxy_index, widget)
        
        
   



##########################################################################################################################
    def actualizar_lista_busqueda(self):

        self.lista_alumnos_actual = alumnos_servicio.obtener_todos_alumnos()
        
    
    def actualizar_especialidades(self):

        self.boton_especialidades.clear()
        self.lista_especialidades = especialidad_servicio.obtener_todos_especialidades()
        FuncionSistema.cargar_elementos_para_el_combobox(self.lista_especialidades, self.boton_especialidades, 1)
        

    # Metodo para actualizar la tabla
    def actualizar_tabla(self, especialidad_id = None):
        
            alumnos_actuales = inscripcion_servicio.obtener_inscripcion_por_especialidad(especialidad_id)
            self.cargar_alumnos_en_tabla(self.tabla_ver_alumnos, alumnos_actuales)
            self.label_contador.setText(str(len(alumnos_actuales)))

    

    
    def habilitar_edicion_alumno(self, fila):
        
        """
            Este Metodo sirve para acceder a la pantalla del formulario del alumno pero con la informacion ya registradra
            para asi poder editarla.
            
            
        """
        
        try: 
            
            # Obtener el texto de la primera columna (nombre)
            cedula = modelo.item(fila, 1).text()
            
            alumno_id = FuncionSistema.buscar_id_por_cedula(cedula, self.lista_alumnos_actual)
            
            
            
            pantalla_perfil_alumno = self.stacked_widget.widget(3)
            
            
            
        except Exception as e:
            
            FuncionSistema.mostrar_errores_por_excepcion(e, "habilitar_edicion_alumno")
            
        else:
            
            self.stacked_widget.setCurrentIndex(3)
            
            pantalla_perfil_alumno.editar_datos_alumno(alumno_id)
            
            
        
        
                
    def eliminar_alumno_de_la_bd(self, fila):
        
        """
            Este metodo sirve para eliminar al alumno de la base de datos
        
        """
        cedula = modelo.item(fila, 1).text()
        
        alumno_id = FuncionSistema.buscar_id_por_cedula(cedula, self.lista_alumnos_actual)
        
        alumno = alumnos_servicio.obtener_alumno_por_id(alumno_id)
        print(alumno)
        
        self.msg_box.setWindowTitle("Advertencia")
        self.msg_box.setIcon(QMessageBox.Warning)
        self.msg_box.setText(f"¿Seguro que quiere eliminar a {alumno[2]} {alumno[5]}? ")
        QApplication.beep()
        
        # Mostrar el cuadro de diálogo y esperar respuesta
        self.msg_box.exec_()
        
        # si le da a SI, verificamos primero
        if self.msg_box.clickedButton() == self.boton_si:
            try: 
                                
                alumnos_servicio.eliminar_alumno(alumno_id)
                
                
            except Exception as e:
                
                FuncionSistema.mostrar_errores_por_excepcion(e, "eliminar_alumno_de_la_bd")
                
            else:
                
                QMessageBox.information(self, "Proceso exitoso", f"Se a eliminado a {alumno[2]} {alumno[5]} con exito")
                self.filtrar_por_especialidad()
                
        elif self.msg_box.clickedButton() == self.boton_no: 
            
            return  
            
            


    # Metodo para ir a la pantalla para registrar un alumno
    def ir_crear_nuevo_registro(self):
        self.stacked_widget.setCurrentIndex(3)
        pantalla_perfil_alumno = self.stacked_widget.widget(3)
        
        pantalla_perfil_alumno.boton_finalizar.setText("Guardar")
        
    # Metodo para ir a la pantalla de asistenca de alumnos
    def ir_asistencia_alumno(self):
        
        self.stacked_widget.setCurrentIndex(4)
        

 
    
    
            
            
""""            
            
    # Clase de la ventana para mostrar el x diagnostico
    class VentanaMostrarDiagnostico(QWidget, Ui_VentanaMostrarDiagnosticoRegistrado):
        def __init__(self):
            super().__init__()
            
            self.setupUi(self) 
            
            self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
            self.setWindowModality(Qt.ApplicationModal)
"""