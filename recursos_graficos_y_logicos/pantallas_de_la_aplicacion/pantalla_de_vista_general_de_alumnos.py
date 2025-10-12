from PySide2.QtCore import Qt,QPoint
from PySide2.QtGui import QIcon, QStandardItemModel, QStandardItem
from PySide2.QtWidgets import (QWidget, QHeaderView, QStyledItemDelegate, QVBoxLayout, 
                             QPushButton , QHBoxLayout,QMessageBox, QListWidget, QListWidgetItem, QLabel)
from PySide2 import QtGui, QtCore
import os
from ..elementos_graficos_a_py import Ui_VistaGeneralDeAlumnos, Ui_VentanaMostrarDiagnosticoRegistrado



##################################
# importaciones de base de datos #
##################################

# Repositorios

from repositorios.especialidades.especialidad_repositorio import EspecialidadRepositorio
from repositorios.alumnos.alumno_repositorio import AlumnoRepositorio
from repositorios.alumnos.inscripcion_repositorio import InscripcionRepositorio
from repositorios.alumnos.info_bancaria_alumno_repositorio import InfoBancarioAlumnoRepositorio
from repositorios.alumnos.info_clinica_alumno_repositorio import InfoClinicaAlumnoRepositorio
from repositorios.alumnos.inscripcion_repositorio import InscripcionRepositorio

# Servicios

from servicios.especialidades.especialidad_servicio import EspecialidadServicio
from servicios.alumnos.alumno_servicio import AlumnoServicio
from servicios.alumnos.inscripcion_servicio import InscripcionServicio
from servicios.alumnos.info_bancaria_alumno_servicio import InfoBancariaAlumnoServicio
from servicios.alumnos.info_clinica_alumno_servicio import InfoClinicaAlumnoServicio
from servicios.alumnos.inscripcion_servicio import InscripcionServicio



# Instanacias Repositorios

especialidad_repositorio = EspecialidadRepositorio()

alumnos_repositorio = AlumnoRepositorio()

inscripcion_repositorio = InscripcionRepositorio()

info_bancaria_alumno_repositorio = InfoBancarioAlumnoRepositorio()

info_clinica_alumno_repositorio = InfoClinicaAlumnoRepositorio()



# Instancia Servicios

especialidad_servicio = EspecialidadServicio(especialidad_repositorio)

alumnos_servicio = AlumnoServicio(alumnos_repositorio)

inscripcion_servicio = InscripcionServicio(inscripcion_repositorio)

info_bancaria_alumno_servicio = InfoBancariaAlumnoServicio(info_bancaria_alumno_repositorio)

info_clinica_alumno_servicio = InfoClinicaAlumnoServicio(info_clinica_alumno_repositorio)



##################################
# importaciones de base de datos #
##################################


lista_especialidades = especialidad_servicio.obtener_todos_especialidades()

#lista_alumnos = alumnos_servicio.obtener_todos_alumnos()

#botones_opciones = QWidget()
#boton_borrar = QPushButton("Borrar", botones_opciones)
#boton_editar = QPushButton("Editar", botones_opciones)

class PantallaDeVistaGeneralDeAlumnos(QWidget, Ui_VistaGeneralDeAlumnos):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.setupUi(self)
        
        

        ## Ruta relativa de las imagenes ##
        self.boton_de_regreso.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz","flecha_izquierda_2.png")))
        self.boton_buscar.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz","lupa_blanca.png")))
        self.boton_generar_informe.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz","generar_informe.png")))
        self.boton_asistencia_alumnos.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz","control_de_llegada.png")))
        self.boton_crear_nuevo_registro.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz","nuevo_registro.png")))
        self.imagen_contador.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "icono_de_usuario.png")))

        
        
        
        
        self.actualizar_lista_busqueda()
        
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

        #esto me da el valor de la cedula al darle click a la persona que quiero
        self.tabla_ver_alumnos.clicked.connect(lambda index: print(index.sibling(index.row(), 2).data()))

        # Opcional: desactivar clic en el encabezado vertical
        self.tabla_ver_alumnos.verticalHeader().setSectionsClickable(True)

        # Activar filas alternadas y aplicar estilo si quieres
        #self.tabla_ver_alumnos.setAlternatingRowColors(True)
        
        

        # Estilo de encabezados
        self.tabla_ver_alumnos.horizontalHeader().setStyleSheet("""

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

        self.tabla_ver_alumnos.verticalHeader().setStyleSheet("""
                    
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


        self.tabla_ver_alumnos.setStyleSheet("""
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
        
        
        
        #self.ventana_diagnostico = VentanaMostrarDiagnostico() 
        
        self.boton_especialidades.currentIndexChanged.connect(self.filtrar_por_especialidad)
        
        # Conectar señal de doble click
        self.tabla_ver_alumnos.doubleClicked.connect(self.on_double_click)
        
        self.barra_de_busqueda.textChanged.connect(self.filtrar_resultados)
        
        # Carga las especialidades al boton deplegable
        self.cargar_especialidades()
        

        self.boton_de_regreso.clicked.connect(self.volver_pantalla_opciones)

        self.boton_crear_nuevo_registro.clicked.connect(self.ir_crear_nuevo_registro)
        
        self.boton_buscar.clicked.connect(self.acceder_al_perfil_alumno)
        
        self.boton_asistencia_alumnos.clicked.connect(self.ir_asistencia_alumno)
        
        self.boton_generar_informe.clicked.connect(self.ir_a_generar_informes_y_reportes)
        
        
        
        # Lista de coincidencias
        self.resultados = QListWidget(self)
        self.resultados.setFocusPolicy(Qt.NoFocus)
        self.resultados.setMouseTracking(True)
        self.resultados.setStyleSheet("background-color: white; border: 1px solid gray;border-radius:0px; padding:10px;")
        self.resultados.itemClicked.connect(self.seleccionar_item)
        self.resultados.hide() 
     
     
     
     
     
     
     
     
     
     
     
    ################################################################################################################################ 
    ################################################################################################################################

    # Metodos para la busqueda dianamica
    
    def actualizar_lista_busqueda(self):

        self.lista_alumnos_actual = alumnos_servicio.obtener_todos_alumnos()
    
    
    
    
    def filtrar_resultados(self, texto):
        texto = texto.strip().lower()
        self.resultados.clear()

        if not texto:
            self.resultados.hide()
            return
        

        
        coincidencias = [
            persona for persona in self.lista_alumnos_actual
            if texto in persona[1] or texto in persona[2].lower()
        ]

        if not coincidencias:
            self.resultados.hide()
            return

        for persona in coincidencias:
            item = f'{persona[1]} - {persona[2]} {persona[5]}'
            self.resultados.addItem(QListWidgetItem(item))

        # Ocultar si hay una coincidencia exacta por cédula
        if len(coincidencias) == 1 and coincidencias[0][2] == texto:
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
        
        
        
        
    # esta funcion es para que el usuario le de dobleclick a la fila del empleado
    # para que lo lleve a la pantalla de perfil del alumno
    def on_double_click(self, index):
         
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
                    self.stacked_widget.setCurrentIndex(11)
                    
                    self.mostrar_la_info_alumno(alumno_id= alumno[0])
                    
                    self.barra_de_busqueda.clear()
                    
                    break
            
            
        except Exception as e:
            
            print("Error en la funcion on_double_click", f"{e}")
    

    ################################################################################################################    
    ################################################################################################################
    
    
    
    
    
    
    

    # Metodo para cargar las especialidades en el boton de especialidades   
    def cargar_especialidades(self):
        
        #print(lista_especialidades)
        for especialidad in lista_especialidades:
            
            self.boton_especialidades.addItem(especialidad[1])
    
    
    # Metodo para filtrar por especialidad
    def filtrar_por_especialidad(self):
        
        especialidad_selec = self.boton_especialidades.currentText()
        
        try:
        
            # si el boton es pulsado
            if self.boton_especialidades.currentText():
                
                # Iteramos todas las especialidades, ejemplo (1,"ceramica")
                for especialidad in lista_especialidades:
                    
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
            QMessageBox.information(self, "Error", f"{e}")
            
            print("Error en la funcion filtrar_por_especialidad", f"{e}")
    
    
    
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
                alumno[5], alumno[1], alumno[2],
                alumno[3], alumno[9] 
            ]

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

        #  Muy importante: asignar modelo primero
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
            #btn_edit.clicked.connect(lambda _, r=fila: self.editar_alumno(r))
            #btn_delete.clicked.connect(lambda _, r=fila: self.borrar_alumno(r))

            layout.addWidget(boton_editar)
            layout.addWidget(boton_borrar)
            layout.setContentsMargins(3, 3, 3, 3)
            widget.setLayout(layout)

            index = modelo.index(fila, len(columnas) - 1)  # última columna ("Opciones")
            tabla.setIndexWidget(index, widget)
        
    
    
    # Metodo para actualizar la tabla
    def actualizar_tabla(self, especialidad_id = None):
        
            alumnos_actuales = inscripcion_servicio.obtener_inscripcion_por_especialidad(especialidad_id)
            self.cargar_alumnos_en_tabla(self.tabla_ver_alumnos, alumnos_actuales)
            self.label_contador.setText(str(len(alumnos_actuales)))
            
        



##########################################################################################################################

    # Metodo para acceder a la información del alumno
    def acceder_al_perfil_alumno(self):
        
        
        try:
            
            if self.barra_de_busqueda.text().strip():
                
                for alumno in self.lista_alumnos_actual:
                    
                    
                    if self.barra_de_busqueda.text() == alumno[1]:
                        
                        alumno_id = alumno[0]
                        
                        print(f"\nel alumno es: \nNombre:{alumno[2]}\nID:{alumno[0]}")
                        
                        
                        self.stacked_widget.setCurrentIndex(11)
                        
                        self.mostrar_la_info_alumno(alumno_id= alumno_id)
                        
                        self.barra_de_busqueda.clear()
                        
                        break
                
                
                
            else:
                
                QMessageBox.critical(self, "Error ", "La barra de busqueda esta vacia")

                return
            
                
        except:
            
            QMessageBox.critical(self, "Error en la funcion acceder_al_perfil_alumno", "Cédula no encontrada")
            return
        

    # Metodo para acceder a la informacion del alumno
    def mostrar_la_info_alumno(self, alumno_id: int):
        
        global pantalla_perfil_alumno
        
        pantalla_perfil_alumno = self.stacked_widget.widget(11)
    
    
        if pantalla_perfil_alumno.lista_cuentas_alumno.count() == 0:
            
            pantalla_perfil_alumno.lista_cuentas_alumno.addItem("No tiene cuentas bancarias registradas")
            
        
        
        # cargamos todos la infomacion del alumno
        info_basica = alumnos_servicio.obtener_alumno_por_id(alumno_id)
        
        datos_representante = alumnos_servicio.obtener_datos_representante(alumno_id)
        
        
        info_academica = alumnos_servicio.obtener_info_academica_alumno(alumno_id)
        
        info_clinica = info_clinica_alumno_servicio.obtener_info_clinica_por_alumno_id(alumno_id)
        
        info_inscripcion = inscripcion_servicio.obtener_inscripcion_por_id(alumno_id)
        
        
        try:
            
            
            # info basica
            pantalla_perfil_alumno.input_mostrar_cedula.setText(info_basica[1])
            pantalla_perfil_alumno.input_mostrar_primer_nombre.setText(info_basica[2])
            
            segundo_nombre = self.comprobar_si_hay_valor(info_basica[3])
            pantalla_perfil_alumno.input_mostrar_segundo_nombre.setText(segundo_nombre)
            
            
            tercer_nombre = self.comprobar_si_hay_valor(info_basica[4])
            pantalla_perfil_alumno.input_mostrar_tercer_nombre.setText(tercer_nombre)
            
            
            pantalla_perfil_alumno.input_mostrar_apellido_paterno.setText(info_basica[5])
            
            apellido_materno = self.comprobar_si_hay_valor(info_basica[6])
            pantalla_perfil_alumno.input_mostrar_apellido_materno.setText(apellido_materno)
            pantalla_perfil_alumno.input_mostrar_fecha_nacimiento.setText(info_basica[7])
            pantalla_perfil_alumno.input_mostrar_edad.setText(str(info_basica[8]))
            pantalla_perfil_alumno.input_mostrar_lugar_nacimiento.setText(info_basica[9])
            
            pantalla_perfil_alumno.label_mostrar_estado.setText(info_basica[14])
            
            
            if info_basica[10] == 'F':
                    
                pantalla_perfil_alumno.label_imagen_del_alumno.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "..", "recursos_de_imagenes", "estudiante_f.png")))
                
                pantalla_perfil_alumno.input_sexo_femenino.setChecked(True)
                pantalla_perfil_alumno.input_sexo_masculino.setChecked(False)
                
                
            elif info_basica[10] == 'M':
                
                
                pantalla_perfil_alumno.label_imagen_del_alumno.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "..", "recursos_de_imagenes", "estudiante_m.png")))
                pantalla_perfil_alumno.input_sexo_masculino.setChecked(True)
                pantalla_perfil_alumno.input_sexo_femenino.setChecked(False)
        
        
        
            if info_basica[11] == 1:
                
                pantalla_perfil_alumno.input_si_cma.setChecked(True)
                pantalla_perfil_alumno.input_no_cma.setChecked(False)
                
            elif info_basica[11] == 0:
                
                pantalla_perfil_alumno.input_no_cma.setChecked(True)
                pantalla_perfil_alumno.input_si_cma.setChecked(False)
                
                
                
            if info_basica[12] == 1:
                
                pantalla_perfil_alumno.input_si_imt.setChecked(True)
                pantalla_perfil_alumno.input_no_imt.setChecked(False)
                
            elif info_basica[12] == 0:
                
                pantalla_perfil_alumno.input_no_imt.setChecked(True)
                pantalla_perfil_alumno.input_si_imt.setChecked(False)
                
        except Exception as e:
            
            print(f"Algo malo paso en la info basica: {e}")  
            
            
        
        try:    
            # Datos del representante
                
            
            
            pantalla_perfil_alumno.input_mostrar_nombre.setText(datos_representante[3])
            pantalla_perfil_alumno.input_mostrar_apellido.setText(datos_representante[4])   
            pantalla_perfil_alumno.input_mostrar_relacion_alumno.setText(info_inscripcion[10])
            pantalla_perfil_alumno.input_mostrar_cedula_representante.setText(datos_representante[2])
            
            pantalla_perfil_alumno.input_mostrar_direccion_residencial.setText(datos_representante[5])
            pantalla_perfil_alumno.input_mostrar_numero_telefono.setText(datos_representante[6])
            
            if datos_representante[7] == None:
                pantalla_perfil_alumno.input_mostrar_numero_telefono_adicional.setText("No tiene")
            
            else:
                pantalla_perfil_alumno.input_mostrar_numero_telefono_adicional.setText(datos_representante[7])
            
            pantalla_perfil_alumno.input_mostrar_carga_familiar.setText(str(datos_representante[8]))   
            pantalla_perfil_alumno.input_mostrar_estado_civil.setText(datos_representante[9])
            
        except Exception as e:
            print(f"Algo paso en datos del representante: {e}")
            
            
        
        
        try: 
        
            # Info bancaria del alumno
            info_bancaria = info_bancaria_alumno_servicio.obtener_info_bancaria_por_alumno_id(alumno_id)
            
            if info_bancaria:
                
                print("tiene cuenta en el banco")
                print(info_bancaria)
                pantalla_perfil_alumno.lista_cuentas_alumno.clear()
                self.agregar_elementos_a_la_vista_previa_cuentas_alumno(pantalla_perfil_alumno.lista_cuentas_alumno, info_bancaria)
                
                
            
        except Exception as e:
            
            print(f"Algo paso en info bancaria: {e}")
    
            
            
        
        
        
        
        try:
            
            
            # info escolaridad
            
            pantalla_perfil_alumno.input_mostrar_escolaridad.setText(info_academica[1])
            pantalla_perfil_alumno.input_mostrar_procedencia.setText(info_academica[2])
            
            
        except Exception as e:
            print(f"Algo paso en escolaridad: {e}")
            
            
            
        try:
            
            
            # info clinica
            self.agregar_elementos_a_la_vista_previa_diagnostico_alumno(pantalla_perfil_alumno.lista_diagnostico_alumno, info_clinica)
            
        except Exception as e:
            print(f"Algo paso en info clinia: {e}")
            
            
        try:
            
            
            # info inscripcion
            pantalla_perfil_alumno.input_mostrar_especialidad.setText(info_inscripcion[4])
            pantalla_perfil_alumno.input_mostrar_matricula.setText(info_inscripcion[5])
            pantalla_perfil_alumno.input_mostrar_fecha_ingreso.setText(str(info_inscripcion[6]))
            pantalla_perfil_alumno.input_mostrar_tiempo.setText("1 año")
            
            
            
        except Exception as e:
            print(f"Algo paso en info inscripcion: {e}")
            
            

    
        
    # Metodo para agregar diagnostico a la vista previa
    def agregar_elementos_a_la_vista_previa_cuentas_alumno(self, nombre_qlistwidget, nombre_lista):
        
        
        for cuenta in nombre_lista:
            
            texto_a_mostrar = cuenta[2] + " " + cuenta[3] 
    
            # Crear un QListWidgetItem
            item = QListWidgetItem()
            nombre_qlistwidget.addItem(item)
            
            

            # Crear un widget personalizado para la fila
            widget = QWidget()
            row_layout = QHBoxLayout()
            widget.setLayout(row_layout)

            # Label para el texto
            label = QLabel(texto_a_mostrar if texto_a_mostrar else f"Elemento {self.list_widget.count() + 1}")
            label.setStyleSheet("""
                                
                                QLabel{
                                    
                                    background:none;
                                    font-family: 'Arial';
                                    font-size: 14pt;
                                    
                                    
                                }
                                
                                """)
            row_layout.addWidget(label)

            # Asignar el widget al QListWidgetItem
            item.setSizeHint(widget.sizeHint())
            nombre_qlistwidget.setItemWidget(item, widget)
            
            
        
    # Metodo para agregar diagnostico a la vista previa
    def agregar_elementos_a_la_vista_previa_diagnostico_alumno(self, nombre_qlistwidget, nombre_lista):
        
        i = 1
        for diagnostico in nombre_lista:
            
            
            
            texto_a_mostrar = f"{i}) " + diagnostico[2]
            
            i += 1
            
            # Crear un QListWidgetItem
            item = QListWidgetItem()
            nombre_qlistwidget.addItem(item)
            
            

            # Crear un widget personalizado para la fila
            widget = QWidget()
            row_layout = QHBoxLayout()
            widget.setLayout(row_layout)

            # Label para el texto
            label = QLabel(texto_a_mostrar if texto_a_mostrar else f"Elemento {self.list_widget.count() + 1}")
            label.setStyleSheet("""
                                
                                QLabel{
                                    
                                    background:none;
                                    font-family: 'Arial';
                                    font-size: 14pt;
                                    
                                    
                                }
                                
                                """)
            row_layout.addWidget(label)

            # Botón para eliminar
            boton_ver = QPushButton()
            boton_ver.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "ver_contraseña.png")))
            boton_ver.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            boton_ver.setFixedSize(40,40)
            boton_ver.setStyleSheet("""
                                        
                                        QPushButton{
                                            background:#ffffff;
                                            border-radius:12px;
                                            icon-size:28px;
                                            border:1px solid black;
                                        }
                                        
                                        QPushButton:hover{
                                            
                                            background:#acacac
                                            
                                            
                                        }
                                        
                                        
                                        """)
            
            row_layout.addWidget(boton_ver)
            
            boton_ver.clicked.connect(
            lambda  item=item, lista=nombre_lista: self.ver_diagnostico_seleccionado(nombre_qlistwidget, lista, item)
        )
        
            # Asignar el widget al QListWidgetItem
            item.setSizeHint(widget.sizeHint())
            nombre_qlistwidget.setItemWidget(item, widget)


        

    # Metodo para borrar diagnostico a la vista previa
    def ver_diagnostico_seleccionado(self, nombre_qlistwidget, nombre_lista,  item):
        
        
        # Logica para borrar el registro del diagnostico de la lista
        
        # indice del listwidget
        indice_vista_previa = nombre_qlistwidget.row(item)
        
        info_clinica_id = nombre_lista[indice_vista_previa][0]
        
        print(f"Indice del diagnostico: {info_clinica_id}")
        
        try:
        
            diagnostico = info_clinica_alumno_servicio.obtener_info_clinica_alumno_por_id(info_clinica_id)
            
            if pantalla_perfil_alumno.dockWidget_diagnostico.show():
                
                pantalla_perfil_alumno.dockWidget_diagnostico.hide()
                
            elif pantalla_perfil_alumno.dockWidget_diagnostico.hide():
                
                pantalla_perfil_alumno.dockWidget_diagnostico.show()
                
            
            
            pantalla_perfil_alumno.mostrar(f"Diagnóstico N° {indice_vista_previa + 1}",diagnostico[2],str(diagnostico[3]),diagnostico[4],diagnostico[5],str(diagnostico[6]),diagnostico[7])
        
        except Exception as e:
            
            print(f"algo paso: {e}")
        
        
        
    # Metodo para comprobar y hay valor por asignar en la variable o se asigna None
    # Este metodo sirve para comprobar esos valores que pueden ser None
    def comprobar_si_hay_valor(self, elemento_lista):
        
        if elemento_lista == None:
                
            return "No tiene"
                
        else:
            
            return elemento_lista
            




    


    # Metodo para ir a la pantalla para registrar un alumno
    def ir_crear_nuevo_registro(self):
        self.stacked_widget.setCurrentIndex(6)
        
    # Metodo para ir a la pantalla de asistenca de alumnos
    def ir_asistencia_alumno(self):
        
        self.stacked_widget.setCurrentIndex(13)
        
        
    def ir_a_generar_informes_y_reportes(self):
    
        self.stacked_widget.setCurrentIndex(14)
        

    # Metodo para volver a la pantalla anterior
    def volver_pantalla_opciones(self):
        self.stacked_widget.setCurrentIndex(1)

    
    
    # metodo para volver a la pantalla anterior admin
    def volver_pantalla_opciones_admin(self):
        
            self.stacked_widget.setCurrentIndex(7)
            
            
            
            
""""            
            
    # Clase de la ventana para mostrar el x diagnostico
    class VentanaMostrarDiagnostico(QWidget, Ui_VentanaMostrarDiagnosticoRegistrado):
        def __init__(self):
            super().__init__()
            
            self.setupUi(self) 
            
            self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
            self.setWindowModality(Qt.ApplicationModal)
"""