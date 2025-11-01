from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  QWidget, QPushButton, QListWidgetItem, QHBoxLayout, QLabel
from PyQt5 import QtGui, QtCore
import os
from ..elementos_graficos_a_py import Ui_PantallaInsertarCatalogoBD
from ..utilidades.funciones_sistema import FuncionSistema

##################################
# importaciones de base de datos #
##################################

# Repositorios

from repositorios.alumnos.alumno_repositorio import AlumnoRepositorio
from repositorios.diagnosticos.diagnostico_repositorio import DiagnosticoRepositorio
from repositorios.especialidades.especialidad_repositorio import EspecialidadRepositorio
from repositorios.empleados.tipo_cargo_repositorio import TipoCargoRepositorio
from repositorios.empleados.cargo_empleado_repositorio import CargoEmpleadoRepositorio
from repositorios.empleados.funcion_cargo_repositorio import FuncionCargoRepositorio
from repositorios.empleados.enfermedad_cronica_repositorio import EnfermedadCronicaRepositorio


# Servicio

from servicios.alumnos.alumno_servicio import AlumnoServicio
from servicios.diagnosticos.diagnostico_servicio import DiagnosticoServicio
from servicios.especialidades.especialidad_servicio import EspecialidadServicio
from servicios.empleados.tipo_cargo_servicio import TipoCargoServicio
from servicios.empleados.cargo_empleado_servicio import CargoEmpleadoServicio
from servicios.empleados.funcion_cargo_servicio import FuncionCargoServicio
from servicios.empleados.enfermedad_cronica_servicio import EnfermedadCronicaServicio


##################################
# importaciones de base de datos #
##################################

# Instancia de los repositorios

alumno_repositorio = AlumnoRepositorio()

diagnostico_repositorio = DiagnosticoRepositorio()

especialidad_repositorio = EspecialidadRepositorio()

tipo_cargo_repositorio = TipoCargoRepositorio()

cargo_empleado_repositorio = CargoEmpleadoRepositorio()

funcion_cargo_repositorio = FuncionCargoRepositorio()

enfermedad_cronica_repositorio = EnfermedadCronicaRepositorio()


# Intancia de los servicio

alumno_servicio = AlumnoServicio(alumno_repositorio)

diagnostico_servicio = DiagnosticoServicio(diagnostico_repositorio)

especialidad_servicio = EspecialidadServicio(especialidad_repositorio)

tipo_cargo_servicio = TipoCargoServicio(tipo_cargo_repositorio)

cargo_empleado_servicio = CargoEmpleadoServicio(cargo_empleado_repositorio)

funcion_cargo_servicio = FuncionCargoServicio(funcion_cargo_repositorio)


enfermedad_cronica_servicio = EnfermedadCronicaServicio(enfermedad_cronica_repositorio)



class PantallaAdminInsertarCatalogo(QWidget, Ui_PantallaInsertarCatalogoBD):
    def __init__(self, stacked_widget):
        super().__init__()
        
        self.stacked_widget = stacked_widget
        self.setupUi(self)
        
        
        # Ruta relativa para las imagenes
        self.boton_registrar_cargo_empleado.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz","mas_blanco.png")))
        self.boton_registrar_diagnostico.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz","mas_blanco.png")))
        self.boton_registrar_enfermedad.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz","mas_blanco.png")))
        self.boton_registrar_especialidad.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz","mas_blanco.png")))
        self.boton_registrar_funcion_cargo.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz","mas_blanco.png")))
        
        
        # Listas catalogo
        self.lista_cargo = cargo_empleado_servicio.obtener_todos_cargos_empleados()
        self.lista_tipo_cargo = tipo_cargo_servicio.obtener_todos_tipos_cargo()
        self.lista_funcion_cargo = funcion_cargo_servicio.obtener_todos_funciones_cargo()
        self.lista_diagnosticos = diagnostico_servicio.obtener_todos_diagnosticos()
        self.lista_especialidades = especialidad_servicio.obtener_todos_especialidades()
        self.lista_enfermerdades = enfermedad_cronica_servicio.obtener_todos_enfermedades_cronicas()
        
        
        # Cargando listas catalogos a los QListwidget
        self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_especialidades, self.lista_especialidades)
        self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_diagnosticos, self.lista_diagnosticos)
        self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_enfermedades, self.lista_enfermerdades)
        self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_funciones_cargo, self.lista_funcion_cargo)
        self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_cargos_empleados, self.lista_cargo, 2)


        # Conectando señales para añadir elementos a los catalogos
        
        self.boton_registrar_especialidad.clicked.connect(lambda _: self.agregar_nuevo_elemento_al_catalogo(self.input_especialidad) )
     
    def agregar_nuevo_elemento_al_catalogo(self, campo_nuevo):
        
        
        
        campo_nuevo = {
            
            "especialidad": campo_nuevo.text().strip().upper()
        }
        
        especialidad_servicio.registrar_especialidad(campo_nuevo)
        
        self.lista_especialidades = especialidad_servicio.obtener_todos_especialidades()

       
        self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_especialidades, self.lista_especialidades)

    
    def accion_editar_catalogo(self, elemento, qlistwidget, item):
        """Prueba del botón editar"""
        print(f"[EDITAR] Elemento:", elemento)
        qlistwidget.setCurrentItem(item)  # Hace foco en el elemento


    def accion_borrar_catalogo(self, elemento, qlistwidget, item):
        """Prueba del botón borrar"""
        print(f"[BORRAR] Elemento:", elemento)
        qlistwidget.setCurrentItem(item)  # Hace foco en el elemento



    def agregar_elementos_a_las_vistas_previas_catalogo(self, nombre_qlistwidget, lista_catalogo: list, indice_elemento: int = 1):
        """
        Agrega elementos a un QListWidget, cada uno con botones de editar y borrar.
        """
        nombre_qlistwidget.clear()  # Limpia antes de agregar nuevos elementos
        
        for i, elemento_catalogo in enumerate(lista_catalogo, start=1):
            texto_a_mostrar = f"{i}) " + elemento_catalogo[indice_elemento]

            # Crear un QListWidgetItem
            item = QListWidgetItem()
            nombre_qlistwidget.addItem(item)

            # Crear el widget personalizado
            widget = QWidget()
            widget.setStyleSheet("""
                QWidget {
                    border: none;
                    padding: 0px;
                }
            """)
            row_layout = QHBoxLayout(widget)
            row_layout.setContentsMargins(2, 2, 2, 2)
            row_layout.setSpacing(6)

            # Label
            label = QLabel(texto_a_mostrar)
            label.setStyleSheet("""
                QLabel {
                    background: none;
                    font-family: 'Arial';
                    font-size: 12pt;
                    padding: 0px;
                }
            """)
            row_layout.addWidget(label)

            # --- Botón Editar ---
            boton_editar = QPushButton()
            boton_editar.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), "..", "recursos_de_imagenes", "iconos_de_interfaz", "editar.png")))
            boton_editar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            boton_editar.setFixedSize(40, 30)
            boton_editar.setStyleSheet("""
                QPushButton {
                    background-color: rgb(244, 131, 2);
                    color: white;
                }
                QPushButton:hover {
                    background-color: rgb(191, 64, 0);
                }
            """)
            # Capturamos las variables actuales en la lambda
            boton_editar.clicked.connect(lambda _, elem=elemento_catalogo, item=item: self.accion_editar_catalogo(elem, nombre_qlistwidget, item))
            row_layout.addWidget(boton_editar)

            # --- Botón Borrar ---
            boton_borrar = QPushButton()
            boton_borrar.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), "..", "recursos_de_imagenes", "iconos_de_interfaz", "borrar.png")))
            boton_borrar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            boton_borrar.setFixedSize(40, 30)
            boton_borrar.setStyleSheet("""
                QPushButton {
                    background-color: rgb(255, 0, 0);
                    color: white;
                }
                QPushButton:hover {
                    background-color: rgb(147, 0, 0);
                }
            """)
            boton_borrar.clicked.connect(lambda _, elem=elemento_catalogo, item=item: self.accion_borrar_catalogo(elem, nombre_qlistwidget, item))
            row_layout.addWidget(boton_borrar)

            # Asignar el widget al QListWidgetItem
            item.setSizeHint(widget.sizeHint())
            nombre_qlistwidget.setItemWidget(item, widget)
