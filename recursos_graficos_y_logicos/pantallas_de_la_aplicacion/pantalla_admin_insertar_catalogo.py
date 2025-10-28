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


# Servicio

from servicios.alumnos.alumno_servicio import AlumnoServicio
from servicios.diagnosticos.diagnostico_servicio import DiagnosticoServicio
from servicios.especialidades.especialidad_servicio import EspecialidadServicio


##################################
# importaciones de base de datos #
##################################

# Instancia de los repositorios

alumno_repositorio = AlumnoRepositorio()

diagnostico_repositorio = DiagnosticoRepositorio()

especialidad_repositorio = EspecialidadRepositorio()




# Intancia de los servicio

alumno_servicio = AlumnoServicio(alumno_repositorio)

diagnostico_servicio = DiagnosticoServicio(diagnostico_repositorio)

especialidad_servicio = EspecialidadServicio(especialidad_repositorio)


lista_diagnosticos = diagnostico_servicio.obtener_todos_diagnosticos()
lista_especialidades = especialidad_servicio.obtener_todos_especialidades()


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
        
        
        
        
        
        self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_diagnosticos, lista_diagnosticos)
        
        self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_especialidades, lista_especialidades)

        
        
   # Metodo para agregar diagnostico a la vista previa
    def agregar_elementos_a_las_vistas_previas_catalogo(self, nombre_qlistwidget, lista_catalogo):
        
        i = 1
        for elemento_catalogo in lista_catalogo:
            
            
            
            texto_a_mostrar = f"{i}) " + elemento_catalogo[1]
            
            i += 1
            
            # Crear un QListWidgetItem
            item = QListWidgetItem()
            nombre_qlistwidget.addItem(item)
            
            

            # Crear un widget personalizado para la fila
            widget = QWidget()
            
            widget.setStyleSheet("""
                                    QWidget{
                                        
                                        border:none;
                                        padding:0px;
                                        
                                        
                                    }
            
            
            """)
            
            row_layout = QHBoxLayout()
            
            #row_layout.setSpacing(0)
            
            widget.setLayout(row_layout)

            # Label para el texto
            label = QLabel(texto_a_mostrar if texto_a_mostrar else f"Elemento {self.list_widget.count() + 1}")
            label.setStyleSheet("""
                                
                                QLabel{
                                    
                                    background:none;
                                    font-family: 'Arial';
                                    font-size: 12pt;
                                    padding:0px;
                                    
                                    
                                }
                                
                                """)
            
            row_layout.addWidget(label)
            
            
            # Botón para eliminar
            boton_editar = QPushButton()
            boton_editar.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "editar.png")))
            boton_editar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            boton_editar.setFixedSize(40,40)
            boton_editar.setStyleSheet("""
                                        
                                        QPushButton{
                                            background: yellow;
                                            border-radius:12px;
                                            icon-size:28px;
                                            border:1px solid black;
                                        }
                                        
                                        QPushButton:hover{
                                            
                                            background:#acacac
                                            
                                            
                                        }
                                        
                                        
                                        """)

            # Botón para eliminar
            boton_borrar = QPushButton()
            boton_borrar.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "borrar.png")))
            boton_borrar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            boton_borrar.setFixedSize(40,40)
            boton_borrar.setStyleSheet("""
                                        
                                        QPushButton{
                                            background:red;
                                            border-radius:12px;
                                            icon-size:28px;
                                            border:1px solid black;
                                        }
                                        
                                        QPushButton:hover{
                                            
                                            background:#acacac
                                            
                                            
                                        }
                                        
                                        
                                        """)
            
            row_layout.addWidget(boton_editar)
            row_layout.addWidget(boton_borrar)
            
            
    
        
            # Asignar el widget al QListWidgetItem
            item.setSizeHint(widget.sizeHint())
            nombre_qlistwidget.setItemWidget(item, widget)
