from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  (QWidget, QPushButton, QListWidgetItem,
                              QHBoxLayout, QLabel, QMessageBox)
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
        
        
        self.stacked_widget.currentChanged.connect(lambda indice: self.activar_pantalla(indice))

    def activar_pantalla(self, indice_pantalla):
        
        """
            ### Este metodo sirve para activar toda la funcion de la pantalla cuando el estamos en ella.
            
            la logica es la siguiente:
            
            - desde main.py nos aseguramos de la posiciones actual de la pantalla en el stackedWidget.
            
            self.stacked_widget.addWidget(self.pantalla_admin_insertar_catalogo) # indice 14
            
            - en este caso como esta pantalla es la 14 solo verificamos con un if si estamos en el indice 14
            - si lo estamos ejecute todo lo que tenga que hacer
            - si no, que no haga nada

        
        """
        
        if indice_pantalla == 14:
        
            # Listas catalogo
            self.lista_cargo = cargo_empleado_servicio.obtener_todos_cargos_empleados()
            self.lista_tipo_cargo = tipo_cargo_servicio.obtener_todos_tipos_cargo()
            self.lista_funcion_cargo = funcion_cargo_servicio.obtener_todos_funciones_cargo()
            self.lista_diagnosticos = diagnostico_servicio.obtener_todos_diagnosticos()
            self.lista_especialidades = especialidad_servicio.obtener_todos_especialidades()
            self.lista_enfermedades = enfermedad_cronica_servicio.obtener_todos_enfermedades_cronicas()
            
            
            # Cargando listas catalogos a los QListwidget
            self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_especialidades, self.lista_especialidades)
            self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_diagnosticos, self.lista_diagnosticos)
            self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_enfermedades, self.lista_enfermedades)
            self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_funciones_cargo, self.lista_funcion_cargo)
            self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_cargos_empleados, self.lista_cargo, 2)


            # Conectando señales para añadir elementos a los catalogos
            
            self.boton_registrar_especialidad.clicked.connect(lambda _: self.agregar_nuevo_elemento_al_catalogo(self.input_especialidad, "especialidad", self.lista_especialidades) )
            self.boton_registrar_diagnostico.clicked.connect(lambda _: self.agregar_nuevo_elemento_al_catalogo(self.input_diagnostico, "diagnostico", self.lista_diagnosticos))
            self.boton_registrar_enfermedad.clicked.connect(lambda _: self.agregar_nuevo_elemento_al_catalogo(self.input_enfermedad, "enfermedad_cronica", self.lista_enfermedades))
            self.boton_registrar_funcion_cargo.clicked.connect(lambda _: self.agregar_nuevo_elemento_al_catalogo(self.input_funcion_cargo, "funcion_cargo", self.lista_funcion_cargo))

        
        else:
            
            return None
        
    def agregar_nuevo_elemento_al_catalogo(self, qlineedit, nombre_clave_dict:str, lista_catalogo:list):
        
        """
            ### Metodo para registrar nuevo elemento al catalogo.
            
            ### Por ahora solo sirve para los catalogos:
            
            - especialidades
            - diagnosticos
            - enfermedades
            - funcion de cargo
        
            ya que comparten la misma estructura de:
            
            Lista_n = [(int, "str"), (int, "str")]
            
            
            ***Ejemplo***
            
            lista_diagnosticos = [(1, "diagnostico 1"), (2, "diagnostico 2")]
            
            input_diagnostico = QLineEdit()
            
            
            self.agregar_nuevo_elemento_al_catalogo(input_diagnostico, "diagnostico", lista_diagnostico) # esto da como resultado la insercion de un nuevo elemento
            
            
            
            - se pide el QLineEdit para poder tomar el texto
            - se le indica un nombre_clave_dict en este caso diagnostico ya que el metodo de la base de datos tiene la siguiente estructura

            registrar_diagnostico{ "diagnostico": "nuevo_diagnostico"}  # en este caso el texto del QLineEdit

              y lo que hace el metodo es variar el nombre clave del diccionario por el de enfermedades, diagnostico y especialidades
                
            - se pide la lista para que la refresque y con esta misma usamos de nuevo el metodo de agregar_elemento_a_la_vista_previa para actualizar el QListWidget
            
            
            
        """
        
        """
            verificamos si el input/QlineEdit tiene algun valor.
            
            si lo tiene:
            
            - registre el nuevo elemento
            - que limpie el QLineEdit
            - y que actualice la lista
            
            si no tiene valor:
            
            - lanza un aviso de que el campo esta vacio
        
        """
        if qlineedit.text().strip():
            try:
                
                    
                # diccionario para registrar el nuevo elemento
                diccionario_registrar = {
                    nombre_clave_dict: qlineedit.text().strip().capitalize()
                }
                
                # en el caso de que sea especialidad
                if nombre_clave_dict.lower() == "especialidad":
                    
                    especialidad_servicio.registrar_especialidad(diccionario_registrar)
                    
                    lista_catalogo = especialidad_servicio.obtener_todos_especialidades()

                
                    self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_especialidades, lista_catalogo)

                    
                    
                    

                elif nombre_clave_dict.lower() == "diagnostico":
                    
                    diagnostico_servicio.registrar_diagnostico(diccionario_registrar)
                    
                    lista_catalogo = diagnostico_servicio.obtener_todos_diagnosticos()

                
                    self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_diagnosticos, lista_catalogo)

                
                elif nombre_clave_dict.lower() == "enfermedad_cronica":
                    
                    enfermedad_cronica_servicio.registrar_enfermedad_cronica(diccionario_registrar)
                    
                    lista_catalogo = enfermedad_cronica_servicio.obtener_todos_enfermedades_cronicas()

                
                    self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_enfermedades, lista_catalogo)
                    
                
                
                elif nombre_clave_dict.lower() == "funcion_cargo":
                    
                    funcion_cargo_servicio.registrar_funcion_cargo_repositorio(diccionario_registrar)
                    
                    lista_catalogo = funcion_cargo_servicio.obtener_todos_funciones_cargo()

                
                    self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_funciones_cargo, lista_catalogo)
                    
                qlineedit.clear()


                
                
            except Exception as e:
                
                FuncionSistema.mostrar_errores_por_excepcion(e,"agregar_nuevo_elemento_al_catalogo")    
            
            
            else:
                
                QMessageBox.information(self, "Proceso exitoso", f"La {nombre_clave_dict} se agrego con exito")
                
        else:
                    
            QMessageBox.warning(self, "Aviso", f"El campo {nombre_clave_dict} esta vacio")        
        
    def actualizar_elemento_del_catalogo(self, qlineedit, id_elemento:int, nombre_clave_dict: str, lista_catalogo:list):
        
        """
            ### Este metodo sirve para actualizar/editar el elemento de los siguientes catalogos
            
            - especialidades
            - enfermededades
            - diagnosticos
            - funcion de cargo
            
            
            Este metodo sigue la misma estructura del metodo agregar_nuevo_elemento_al_catalogo(), solo que la diferencia que se pide el id del elemento catalogo
            
            ***Ejemplo***
            
            lista_diagnosticos = [(1, "diagnostico 1"), (2, "diagnostico 2")]
            
            input_diagnostico = QLineEdit()
            
            
            self.actualizar_elemento_del_catalogo(input_diagnostico, id_elemento, "diagnostico", lista_diagnostico) # esto da como resultado la insercion de un nuevo elemento
            
            
            
            - se le coloca texto del elemento catalogo a el QLineEdit para poder tomar el texto
            - se le indica un nombre_clave_dict en este caso diagnostico ya que el metodo de la base de datos tiene la siguiente estructura

            registrar_diagnostico{ "diagnostico": "nuevo_diagnostico"}  # en este caso el texto del QLineEdit

              y lo que hace el metodo es variar el nombre clave del diccionario por el de enfermedades, diagnostico y especialidades
                
            - se pide la lista para que la refresque y con esta misma usamos de nuevo el metodo de agregar_elemento_a_la_vista_previa para actualizar el QListWidget
            
        
        
        
        """
        
        if qlineedit.text().strip():
            
            try:
                
                    
                # diccionario para registrar el nuevo elemento
                diccionario_registrar = {
                    nombre_clave_dict: qlineedit.text().strip().capitalize()
                }
                
                # en el caso de que sea especialidad
                if nombre_clave_dict.lower() == "especialidad":
                    
                    especialidad_servicio.actualizar_especialidad(id_elemento, diccionario_registrar)
                    
                    lista_catalogo = especialidad_servicio.obtener_todos_especialidades()


                    self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_especialidades, lista_catalogo)

                    
                    self.boton_registrar_especialidad.clicked.disconnect()
                    
                    self.boton_registrar_especialidad.clicked.connect(lambda _: self.agregar_nuevo_elemento_al_catalogo(self.input_especialidad, "especialidad", self.lista_especialidades) )
                    
                
                # en el caso de que sea especialidad
                if nombre_clave_dict.lower() == "diagnostico":
                    
                    diagnostico_servicio.actualizar_diagnostico(id_elemento, diccionario_registrar)
                    
                    lista_catalogo = diagnostico_servicio.obtener_todos_diagnosticos()


                    self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_diagnosticos, lista_catalogo)

                    
                    self.boton_registrar_diagnostico.clicked.disconnect()
                    self.boton_registrar_diagnostico.clicked.connect(lambda _: self.agregar_nuevo_elemento_al_catalogo(self.input_diagnostico, "diagnostico", self.lista_diagnosticos) )
                    
                
                if nombre_clave_dict.lower() == "enfermedad_cronica":
                    
                    enfermedad_cronica_servicio.actualizar_enfermedad_cronica(id_elemento, diccionario_registrar)
                    
                    lista_catalogo = enfermedad_cronica_servicio.obtener_todos_enfermedades_cronicas()


                    self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_enfermedades, lista_catalogo)

                    
                    self.boton_registrar_enfermedad.clicked.disconnect()
                    self.boton_registrar_enfermedad.clicked.connect(lambda _: self.agregar_nuevo_elemento_al_catalogo(self.input_enfermedad, "enfermedad_Cronica", self.lista_enfermedades) )
                    
                
                if nombre_clave_dict.lower() == "funcion_cargo":
                    
                    funcion_cargo_servicio.actualizar_funcion_cargo(id_elemento, diccionario_registrar)
                    
                    lista_catalogo = funcion_cargo_servicio.obtener_todos_funciones_cargo()


                    self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_funciones_cargo, lista_catalogo)

                    
                    self.boton_registrar_funcion_cargo.clicked.disconnect()
                    self.boton_registrar_funcion_cargo.clicked.connect(lambda _: self.agregar_nuevo_elemento_al_catalogo(self.input_funcion_cargo, "funcion_cargo", self.lista_funcion_cargo) )
                    
                
                
                    
                qlineedit.clear()


                
            
            except Exception as e:
                
                FuncionSistema.mostrar_errores_por_excepcion(e, "actualizar_elemento_del_catalogo" )
                
                
            else:
                
                QMessageBox.information(self, "Proceso exitoso", f"se edito con exito la {nombre_clave_dict}")
                
        else:
                    
            QMessageBox.warning(self, "Aviso", f"El campo {nombre_clave_dict} esta vacio")
                
                
            
    def accion_editar_catalogo(self, elemento, qlistwidget, item):
        """
            Prueba del botón editar
        
        """
        print(f"[EDITAR] Elemento:", elemento)
        qlistwidget.setCurrentItem(item)  # Hace foco en el elemento
        try:
            
            
            if elemento in self.lista_especialidades:
                
                self.input_especialidad.setText(elemento[1])
                self.input_especialidad.setFocus(True)
                
                self.boton_registrar_especialidad.clicked.disconnect()
                self.boton_registrar_especialidad.clicked.connect(lambda: self.actualizar_elemento_del_catalogo(self.input_especialidad, elemento[0], "especialidad", self.lista_especialidades))
            
            
            elif elemento in self.lista_diagnosticos:
                
                self.input_diagnostico.setText(elemento[1])
                self.input_diagnostico.setFocus(True)
                
                self.boton_registrar_diagnostico.clicked.disconnect()
                self.boton_registrar_diagnostico.clicked.connect(lambda: self.actualizar_elemento_del_catalogo(self.input_diagnostico, elemento[0], "diagnostico", self.lista_diagnosticos))
            
            
            elif elemento in self.lista_enfermedades:
                
                self.input_enfermedad.setText(elemento[1])
                self.input_enfermedad.setFocus(True)
                
                self.boton_registrar_enfermedad.clicked.disconnect()
                self.boton_registrar_enfermedad.clicked.connect(lambda: self.actualizar_elemento_del_catalogo(self.input_enfermedad, elemento[0], "enfermedad_cronica", self.lista_enfermedades))
            
            
            elif elemento in self.lista_funcion_cargo:
                
                self.input_funcion_cargo.setText(elemento[1])
                self.input_funcion_cargo.setFocus(True)
                
                self.boton_registrar_funcion_cargo.clicked.disconnect()
                self.boton_registrar_funcion_cargo.clicked.connect(lambda: self.actualizar_elemento_del_catalogo(self.input_funcion_cargo, elemento[0], "funcion_cargo", self.lista_funcion_cargo))
            
            
            
        except Exception as e:
            
            QMessageBox.information(self, "aviso", f"paso algo malo {e}")   


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
