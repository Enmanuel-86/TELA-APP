from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  (QWidget, QPushButton, QListWidgetItem,
                              QHBoxLayout, QLabel, QMessageBox, QApplication)
from PyQt5 import QtGui, QtCore
from datetime import time
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
        
        
        # Message box para usarlos en cualquier lado
        self.msg_box = QMessageBox(self)
        
        # Crear botones personalizados
        self.boton_si = self.msg_box.addButton("Sí", QMessageBox.YesRole)
        self.boton_no = self.msg_box.addButton("No", QMessageBox.NoRole)
        
        
        self.stacked_widget.currentChanged.connect(lambda indice: self.activar_pantalla() if indice == 14 else self.restaurar_botones_de_registrar() )
        
        
        # Conectando señales para añadir elementos a los catalogos
        
        self.boton_registrar_especialidad.clicked.connect(lambda _: self.agregar_nuevo_elemento_al_catalogo(self.input_especialidad, "especialidad", self.lista_especialidades) )
        self.boton_registrar_diagnostico.clicked.connect(lambda _: self.agregar_nuevo_elemento_al_catalogo(self.input_diagnostico, "diagnostico", self.lista_diagnosticos))
        self.boton_registrar_enfermedad.clicked.connect(lambda _: self.agregar_nuevo_elemento_al_catalogo(self.input_enfermedad, "enfermedad_cronica", self.lista_enfermedades))
        self.boton_registrar_cargo_empleado.clicked.connect(lambda _: self.agregar_nuevo_elemento_al_catalogo(self.input_cargo_empleado, "cargo", self.lista_cargo, self.input_codigo_cargo_empleado))
        self.boton_registrar_tipo_cargo_empleado.clicked.connect(lambda _: self.agregar_nuevo_elemento_al_catalogo(self.input_tipo_cargo_empleado, "tipo_cargo", self.lista_tipo_cargo, None, self.input_hora_cargo_empleado))
        self.boton_registrar_funcion_cargo.clicked.connect(lambda _: self.agregar_nuevo_elemento_al_catalogo(self.input_funcion_cargo, "funcion_cargo", self.lista_funcion_cargo))



    def activar_pantalla(self):
        
        """
            ### Este metodo sirve para activar toda la funcion de la pantalla cuando el estamos en ella.
            
            la logica es la siguiente:
            
            - desde main.py nos aseguramos de la posiciones actual de la pantalla en el stackedWidget.
            
            self.stacked_widget.addWidget(self.pantalla_admin_insertar_catalogo) # indice 14
            
            - en este caso como esta pantalla es la 14 solo verificamos con un if si estamos en el indice 14
            - si lo estamos ejecute todo lo que tenga que hacer
            - si no, que no haga nada

        
        """
        
        
        
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
        self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_cargos_empleados, self.lista_cargo, 2)
        self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_tipos_cargos_empleados, self.lista_tipo_cargo)
        self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_funciones_cargo, self.lista_funcion_cargo)
        
        
    

        self.boton_registrar_tipo_cargo_empleado.clicked.connect(lambda: print(f"hora: {self.input_hora_cargo_empleado.time().hour()} \n minuto: {self.input_hora_cargo_empleado.time().minute()}"))        
   
        
    def agregar_nuevo_elemento_al_catalogo(self, qlineedit, nombre_clave_dict:str, lista_catalogo:list, codigo_cargo = None, hora_tipo_cargo = None):
        
        """
            ### Metodo para registrar nuevo elemento al catalogo.
            
            ### Por ahora solo sirve para los catalogos:
            
            - especialidades
            - diagnosticos
            - enfermedades
            - cargos
            - tipo de cargo
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


            
            verificamos si el input/QlineEdit tiene algun valor.
            
            si lo tiene:
            
            - registre el nuevo elemento
            - que limpie el QLineEdit
            - y que actualice la lista
            
            si no tiene valor:
            
            - lanza un aviso de que el campo esta vacio


            En casos especiales como el tipo de cargo y los cargos, como tienen otro campo, en este metodo estan dos valores con valor None, es decir son opcionales
            si a estos se les llega a pasar uno de los QLineEdit del campo adicional de estos catalogos, este accede a un if especial que verifica si este tiene algun valor
            y si lo tiene crea un diccionario a parte y registra el nuevo elemento al catalogo


            
        """
        
        
        
        
        
        
        
        if qlineedit.text().strip():
            
            
            self.msg_box.setWindowTitle("Confirmar acción")
            self.msg_box.setText(f"¿Seguro que quiere agregar esta {nombre_clave_dict}?")
            self.msg_box.setIcon(QMessageBox.Question)

            

            QApplication.beep()
            self.msg_box.exec_()
            
            if self.msg_box.clickedButton() == self.boton_si:
                
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
                        
                        self.actualizar_especialidades()

                        
                        
                        

                    elif nombre_clave_dict.lower() == "diagnostico":
                        
                        diagnostico_servicio.registrar_diagnostico(diccionario_registrar)
                        
                        lista_catalogo = diagnostico_servicio.obtener_todos_diagnosticos()

                    
                        self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_diagnosticos, lista_catalogo)

                        self.actualizar_diagnosticos()
                    
                    elif nombre_clave_dict.lower() == "enfermedad_cronica":
                        
                        enfermedad_cronica_servicio.registrar_enfermedad_cronica(diccionario_registrar)
                        
                        lista_catalogo = enfermedad_cronica_servicio.obtener_todos_enfermedades_cronicas()

                    
                        self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_enfermedades, lista_catalogo)
                        
                        self.actualizar_enfermedades_cronicas()
                    
                    elif nombre_clave_dict.lower() == "funcion_cargo":
                        
                        funcion_cargo_servicio.registrar_funcion_cargo_repositorio(diccionario_registrar)
                        
                        lista_catalogo = funcion_cargo_servicio.obtener_todos_funciones_cargo()

                    
                        self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_funciones_cargo, lista_catalogo)
                        
                        self.actualizar_funciones_de_cargos()
                        
                    # Casos especiales
                    
                    if nombre_clave_dict.lower() == "tipo_cargo" and hora_tipo_cargo != None:
                        
                        
                        tipo_cargo = self.input_tipo_cargo_empleado.text().capitalize()                        
                        
                        hora = hora_tipo_cargo.time().hour()
                        minuto = hora_tipo_cargo.time().minute()
                        
                        campos_tipo_cargo = {
                            "tipo_cargo": tipo_cargo,
                            "horario_llegada": time(hora, minuto)
                        }
                        
                            
                        
                        tipo_cargo_servicio.registrar_tipo_cargo(campos_tipo_cargo)
                        
                        lista_catalogo = tipo_cargo_servicio.obtener_todos_tipos_cargo()

                        self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_tipos_cargos_empleados, lista_catalogo)

                        self.input_hora_cargo_empleado.clear()
                        
                        self.actualizar_tipos_de_cargos()
                        
                    if nombre_clave_dict.lower() == "cargo" and codigo_cargo != None:
                        
                        
                        codigo_cargo = self.input_codigo_cargo_empleado.text().upper()
                        cargo = self.input_cargo_empleado.text().capitalize()                        
                        
                        
                        campos_cargos_empleados = {
                                "codigo_cargo": codigo_cargo,
                                "cargo": cargo
                                }
                        
                            
                        
                        cargo_empleado_servicio.registrar_cargo_empleado(campos_cargos_empleados)
                        
                        lista_catalogo = cargo_empleado_servicio.obtener_todos_cargos_empleados()

                        self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_cargos_empleados, lista_catalogo)

                        self.input_codigo_cargo_empleado.clear()
                    
                        self.actualizar_cargos()
                        
                        
                    qlineedit.clear()


                    self.activar_pantalla()
                    
                    
                except Exception as e:
                    
                    FuncionSistema.mostrar_errores_por_excepcion(e,"agregar_nuevo_elemento_al_catalogo")    
                
                
                else:
                    
                    QMessageBox.information(self, "Proceso exitoso", f"La {nombre_clave_dict} se agrego con exito")
                        
            
            
            elif self.msg_box.clickedButton() == self.boton_no:
                
                qlineedit.clear()
                
            
            
            
        else:
                        
            QMessageBox.warning(self, "Aviso", f"El campo {nombre_clave_dict} esta vacio")        
            
        
        
        
        
        
        
    def actualizar_elemento_del_catalogo(self, qlineedit, id_elemento:int, nombre_clave_dict: str, lista_catalogo:list, codigo_cargo=None, hora_tipo_cargo = None):
        
        """
            ### Este metodo sirve para actualizar/editar el elemento de los siguientes catalogos
            
            - especialidades
            - enfermededades
            - diagnosticos
            - cargos
            - tipo de cargo
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
        
        
        """
            verificamos si el input/QlineEdit tiene algun valor.
            
            si lo tiene:
            
            - edite el nuevo elemento
            - que limpie el QLineEdit
            - y que actualice la lista
            
            si no tiene valor:
            
            - lanza un aviso de que el campo esta vacio
        
        """
        
        if qlineedit.text().strip():
            
            
            self.msg_box.setWindowTitle("Confirmar acción")
            self.msg_box.setText(f"¿Seguro que quiere editar esta {nombre_clave_dict} ?")
            self.msg_box.setIcon(QMessageBox.Question)

            

            QApplication.beep()
            self.msg_box.exec_()
            
            if self.msg_box.clickedButton() == self.boton_si:
            
                
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


                        FuncionSistema.cambiar_estilo_del_boton(self.boton_registrar_especialidad, "boton_anadir")
                        self.boton_registrar_especialidad.clicked.disconnect()                   
                        self.boton_registrar_especialidad.clicked.connect(lambda _: self.agregar_nuevo_elemento_al_catalogo(self.input_especialidad, "especialidad", self.lista_especialidades) )
                        self.actualizar_especialidades()
                        
                    # en el caso de que sea un diagnostico
                    if nombre_clave_dict.lower() == "diagnostico":
                        
                        diagnostico_servicio.actualizar_diagnostico(id_elemento, diccionario_registrar)
                        
                        lista_catalogo = diagnostico_servicio.obtener_todos_diagnosticos()


                        self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_diagnosticos, lista_catalogo)

                        FuncionSistema.cambiar_estilo_del_boton(self.boton_registrar_diagnostico, "boton_anadir")
                        self.boton_registrar_diagnostico.clicked.disconnect()
                        self.boton_registrar_diagnostico.clicked.connect(lambda _: self.agregar_nuevo_elemento_al_catalogo(self.input_diagnostico, "diagnostico", self.lista_diagnosticos) )
                        self.actualizar_diagnosticos()
                        
                    # en el caso que se una enfermedad cronica
                    if nombre_clave_dict.lower() == "enfermedad_cronica":
                        
                        enfermedad_cronica_servicio.actualizar_enfermedad_cronica(id_elemento, diccionario_registrar)
                        
                        lista_catalogo = enfermedad_cronica_servicio.obtener_todos_enfermedades_cronicas()


                        self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_enfermedades, lista_catalogo)

                        FuncionSistema.cambiar_estilo_del_boton(self.boton_registrar_enfermedad, "boton_anadir")
                        self.boton_registrar_enfermedad.clicked.disconnect()
                        self.boton_registrar_enfermedad.clicked.connect(lambda _: self.agregar_nuevo_elemento_al_catalogo(self.input_enfermedad, "enfermedad_Cronica", self.lista_enfermedades) )
                        self.actualizar_enfermedades_cronicas()
                        
                        
                    # en el caso que se una funcion de cargo
                    if nombre_clave_dict.lower() == "funcion_cargo":
                        
                        funcion_cargo_servicio.actualizar_funcion_cargo(id_elemento, diccionario_registrar)
                        
                        lista_catalogo = funcion_cargo_servicio.obtener_todos_funciones_cargo()

                        self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_funciones_cargo, lista_catalogo)

                        FuncionSistema.cambiar_estilo_del_boton(self.boton_registrar_funcion_cargo, "boton_anadir")
                        self.boton_registrar_funcion_cargo.clicked.disconnect()
                        self.boton_registrar_funcion_cargo.clicked.connect(lambda _: self.agregar_nuevo_elemento_al_catalogo(self.input_funcion_cargo, "funcion_cargo", self.lista_funcion_cargo) )
                        
                        self.actualizar_funciones_de_cargos()
                       
                    
                    if nombre_clave_dict.lower() == "cargo":
                        
                        codigo_cargo = self.input_codigo_cargo_empleado.text().upper()
                        cargo = self.input_cargo_empleado.text().capitalize()                        
                        
                        
                        campos_cargos_empleados = {
                                "codigo_cargo": codigo_cargo,
                                "cargo": cargo
                                }
                        
                            
                        
                        cargo_empleado_servicio.actualizar_cargo_empleado(id_elemento, campos_cargos_empleados)
                        
                        lista_catalogo = cargo_empleado_servicio.obtener_todos_cargos_empleados()

                        self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_funciones_cargo, lista_catalogo)

                        FuncionSistema.cambiar_estilo_del_boton(self.boton_registrar_cargo_empleado, "boton_anadir")
                        self.boton_registrar_cargo_empleado.clicked.disconnect()
                        self.boton_registrar_cargo_empleado.clicked.connect(lambda _: self.agregar_nuevo_elemento_al_catalogo(self.input_cargo_empleado, "cargo", self.lista_cargo, self.input_codigo_cargo_empleado))
                         
                        self.input_codigo_cargo_empleado.clear()
                        self.input_cargo_empleado.clear()
                        
                        self.actualizar_cargos()
                        
                    if nombre_clave_dict.lower() == "tipo_cargo":
                        
                            
                        tipo_cargo = self.input_tipo_cargo_empleado.text().capitalize()                        
                        
                        hora = hora_tipo_cargo.time().hour()
                        minuto = hora_tipo_cargo.time().minute()
                        
                        campos_tipo_cargo = {
                            "tipo_cargo": tipo_cargo,
                            "horario_llegada": time(hora, minuto)
                        }
                        
                            
                        
                        tipo_cargo_servicio.actualizar_tipo_cargo(id_elemento, campos_tipo_cargo)
                        
                        lista_catalogo = tipo_cargo_servicio.obtener_todos_tipos_cargo()

                        self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_tipos_cargos_empleados, lista_catalogo)

                        FuncionSistema.cambiar_estilo_del_boton(self.boton_registrar_tipo_cargo_empleado, "boton_anadir")
                       
                        self.boton_registrar_tipo_cargo_empleado.clicked.disconnect()
                        
                        self.boton_registrar_tipo_cargo_empleado.clicked.connect(lambda _: self.agregar_nuevo_elemento_al_catalogo(self.input_tipo_cargo_empleado, "tipo_cargo", self.lista_tipo_cargo, None, self.input_hora_cargo_empleado))

                        self.input_tipo_cargo_empleado.clear()
                        self.input_hora_cargo_empleado.setTime(QtCore.QTime(8,0))
                        
                        self.actualizar_tipos_de_cargos()
                        
                    
                    qlineedit.clear()


                    
                    self.activar_pantalla()
                    
                except Exception as e:
                    
                    FuncionSistema.mostrar_errores_por_excepcion(e, "actualizar_elemento_del_catalogo" )
                    
                    
                else:
                    
                    QMessageBox.information(self, "Proceso exitoso", f"se edito con exito la {nombre_clave_dict}")
            
            
            
            
            
            if self.msg_box.clickedButton() == self.boton_no:
                
                qlineedit.clear()
                self.input_codigo_cargo_empleado.clear()
                self.input_cargo_empleado.clear()
                
                self.restaurar_botones_de_registrar()
                
            
                
        else:
                    
            QMessageBox.warning(self, "Aviso", f"El campo {nombre_clave_dict} esta vacio")
                
                
    
    def eliminar_elemento_del_catalogo(self,  id_elemento:int, nombre_clave_dict: str, lista_catalogo:list):
        """
            Este metodo sirve para eliminar el elemento del catalogo seleccionado

            a este metodo se le pasa el:
            
            - id del elemento seleccionado
            - el nombre clave de diccionaro 
            - la lista donde pertenece ese elemento


            a partir del id se elemina el elemento del catalogo con su correspondiente servicio



        """
    
        self.msg_box.setWindowTitle("Confirmar acción")
        self.msg_box.setText(f"¿Seguro que quiere eliminar esta {nombre_clave_dict} ?")
        self.msg_box.setIcon(QMessageBox.Question)

        

        QApplication.beep()
        self.msg_box.exec_()
        
        if self.msg_box.clickedButton() == self.boton_si:
        
            
            try:
                
                    
                
                
                # en el caso de que sea especialidad
                if nombre_clave_dict.lower() == "especialidad":
                    
                    especialidad_servicio.eliminar_especialidad(id_elemento)
                    
                    lista_catalogo = especialidad_servicio.obtener_todos_especialidades()

                    self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_especialidades, lista_catalogo)
                    
                    self.actualizar_especialidades()


                elif nombre_clave_dict.lower() == "diagnostico":
                    
                    diagnostico_servicio.eliminar_diagnostico(id_elemento)
                    
                    lista_catalogo = diagnostico_servicio.obtener_todos_diagnosticos()

                    self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_diagnosticos, lista_catalogo)

                    self.actualizar_diagnosticos()

                elif nombre_clave_dict.lower() == "enfermedad_cronica":
                    
                    enfermedad_cronica_servicio.eliminar_enfermedad_cronica(id_elemento)
                    
                    lista_catalogo = enfermedad_cronica_servicio.obtener_todos_enfermedades_cronicas()

                    self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_enfermedades, lista_catalogo)
  
                    self.actualizar_enfermedades_cronicas()
  
                elif nombre_clave_dict.lower() == "funcion_cargo":
                    
                    funcion_cargo_servicio.eliminar_funcion_cargo(id_elemento)
                    
                    lista_catalogo = funcion_cargo_servicio.obtener_todos_funciones_cargo()

                    self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_funciones_cargo, lista_catalogo)
  
                    self.actualizar_funciones_de_cargos()
                
                
                elif nombre_clave_dict.lower() == "tipo_cargo":
                    
                    tipo_cargo_servicio.eliminar_tipo_cargo(id_elemento)
                    
                    lista_catalogo = tipo_cargo_servicio.obtener_todos_tipos_cargo()

                    self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_tipos_cargos_empleados, lista_catalogo)
                    
                    self.actualizar_tipos_de_cargos()
                    
                elif nombre_clave_dict.lower() == "cargo":
                    
                    cargo_empleado_servicio.eliminar_cargo_empleado(id_elemento)
                    
                    lista_catalogo = cargo_empleado_servicio.obtener_todos_cargos_empleados()

                    self.agregar_elementos_a_las_vistas_previas_catalogo(self.vista_previa_cargos_empleados, lista_catalogo)
  
                    self.actualizar_cargos()
                  
                    
            except Exception as e:
                
                FuncionSistema.mostrar_errores_por_excepcion(e, "eliminar_elemento_del_catalogo" )
                QMessageBox.information(self, "error", f"Error: {e}")
                
                
            else:
                
                QMessageBox.information(self, "Proceso exitoso", f"se elimino con exito la {nombre_clave_dict}")
   
        
        
        elif self.msg_box.clickedButton() == self.boton_no:
            
            
            
            self.restaurar_botones_de_registrar()
            
        
            
        else:
            
            QMessageBox.warning(self, "Aviso", f"El campo {nombre_clave_dict} esta vacio")
            
        
            
            
    def accion_editar_catalogo(self, elemento, qlistwidget, item):
        """
            ### Este Metodo sirve para editar un elemento de un qlistwidget/vista_previa
            
            Este Metodo lo que hace es obtener la informacion del elemento seleccionado del qlistwidget
            
            Este metodo hace lo siguiente:
            
            1. verifica si el elemento se encuentra en una lista, que si la lista de enfermedades, especialidades, diagnostico etc.
            2. al saber a donde pertenece este le da foco al qlineedit del segmento en donde pertenece ese elemento.<br>
               ***ejemplo***: si el elemente pertenece a especialidades, este le da foco al qlineedit de especialidad
            3. le cambia el estilo del icono mas con la palabra añadir por un icono de lapiz con la palabra editar (para que sea mas intuitivo)
            4. se desconecta el metodo que tenia el boton del x segmento y le conecta el metodo de actualizar/editar.<br>
               ***ejemplo***: si el boton registraba ahora actualiza/edita
        
        """
        print(f"[EDITAR] Elemento:", elemento)
        qlistwidget.setCurrentItem(item)  # Hace foco en el elemento
        try:
            
            
            if elemento in self.lista_especialidades:
                
                self.input_especialidad.setText(elemento[1])
                self.input_especialidad.setFocus(True)
                
                FuncionSistema.cambiar_estilo_del_boton(self.boton_registrar_especialidad, "boton_editar")
                
                self.boton_registrar_especialidad.clicked.disconnect()
                self.boton_registrar_especialidad.clicked.connect(lambda: self.actualizar_elemento_del_catalogo(self.input_especialidad, elemento[0], "especialidad", self.lista_especialidades))
            
            
            elif elemento in self.lista_diagnosticos:
                
                self.input_diagnostico.setText(elemento[1])
                self.input_diagnostico.setFocus(True)
                
                FuncionSistema.cambiar_estilo_del_boton(self.boton_registrar_diagnostico, "boton_editar")
                self.boton_registrar_diagnostico.clicked.disconnect()
                self.boton_registrar_diagnostico.clicked.connect(lambda: self.actualizar_elemento_del_catalogo(self.input_diagnostico, elemento[0], "diagnostico", self.lista_diagnosticos))
            
            
            elif elemento in self.lista_enfermedades:
                
                self.input_enfermedad.setText(elemento[1])
                self.input_enfermedad.setFocus(True)
                
                FuncionSistema.cambiar_estilo_del_boton(self.boton_registrar_enfermedad, "boton_editar")
                self.boton_registrar_enfermedad.clicked.disconnect()
                self.boton_registrar_enfermedad.clicked.connect(lambda: self.actualizar_elemento_del_catalogo(self.input_enfermedad, elemento[0], "enfermedad_cronica", self.lista_enfermedades))
            
            
            elif elemento in self.lista_funcion_cargo:
                
                self.input_funcion_cargo.setText(elemento[1])
                self.input_funcion_cargo.setFocus(True)
                
                FuncionSistema.cambiar_estilo_del_boton(self.boton_registrar_funcion_cargo, "boton_editar")
                self.boton_registrar_funcion_cargo.clicked.disconnect()
                self.boton_registrar_funcion_cargo.clicked.connect(lambda: self.actualizar_elemento_del_catalogo(self.input_funcion_cargo, elemento[0], "funcion_cargo", self.lista_funcion_cargo))
            
            
            elif elemento in self.lista_cargo:
                
                self.input_codigo_cargo_empleado.setText(elemento[1])
                self.input_cargo_empleado.setText(elemento[2])
                
                self.input_codigo_cargo_empleado.setFocus(True)
                
                
                FuncionSistema.cambiar_estilo_del_boton(self.boton_registrar_cargo_empleado, "boton_editar")
                self.boton_registrar_cargo_empleado.clicked.disconnect()
                self.boton_registrar_cargo_empleado.clicked.connect(lambda: self.actualizar_elemento_del_catalogo(self.input_cargo_empleado, elemento[0], "cargo", self.lista_cargo, self.input_codigo_cargo_empleado))
            
            
            
            elif elemento in self.lista_tipo_cargo:
                
                self.input_tipo_cargo_empleado.setText(elemento[1])
                
                self.input_tipo_cargo_empleado.setFocus(True)
                
                
                FuncionSistema.cambiar_estilo_del_boton(self.boton_registrar_tipo_cargo_empleado, "boton_editar")
                self.boton_registrar_tipo_cargo_empleado.clicked.disconnect()
                self.boton_registrar_tipo_cargo_empleado.clicked.connect(lambda: self.actualizar_elemento_del_catalogo(self.input_tipo_cargo_empleado, elemento[0], "tipo_cargo", self.lista_tipo_cargo, None,self.input_hora_cargo_empleado))
            
            
            
            
        except Exception as e:
            
            QMessageBox.information(self, "aviso", f"paso algo malo {e}")   


    def accion_borrar_catalogo(self, elemento, qlistwidget, item):
        """Prueba del botón borrar"""
        print(f"[BORRAR] Elemento:", elemento)
        qlistwidget.setCurrentItem(item)  # Hace foco en el elemento
        
        
        
        try:
            
            
            if elemento in self.lista_especialidades:
                
                self.eliminar_elemento_del_catalogo(elemento[0], "especialidad", self.lista_especialidades)
            
            
            
            elif elemento in self.lista_diagnosticos:
                
                self.eliminar_elemento_del_catalogo(elemento[0], "diagnostico", self.lista_diagnosticos)
                
                
                
            elif elemento in self.lista_enfermedades:
                
                self.eliminar_elemento_del_catalogo(elemento[0], "enfermedad_cronica", self.lista_enfermedades)
            
            
            
            elif elemento in self.lista_funcion_cargo:
                
        
                self.eliminar_elemento_del_catalogo(elemento[0], "funcion_cargo", self.lista_funcion_cargo)
                
            
            
            elif elemento in self.lista_tipo_cargo:
                
        
                self.eliminar_elemento_del_catalogo(elemento[0], "tipo_cargo", self.lista_tipo_cargo)
                
                
                
            elif elemento in self.lista_cargo:
                
        
                self.eliminar_elemento_del_catalogo(elemento[0], "cargo", self.lista_cargo)
                
                
             
            
            

            
        except Exception as e:
            
            QMessageBox.information(self, "aviso", f"paso algo malo {e}") 



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
            boton_editar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            boton_editar.setFixedSize(40, 30)
            boton_editar.setProperty("tipo", "boton_editar")
            
            # Capturamos las variables actuales en la lambda
            boton_editar.clicked.connect(lambda _, elem=elemento_catalogo, item=item: self.accion_editar_catalogo(elem, nombre_qlistwidget, item))
            row_layout.addWidget(boton_editar)

            # --- Botón Borrar ---
            boton_borrar = QPushButton()
            boton_borrar.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), "..", "recursos_de_imagenes", "iconos_de_interfaz", "borrar.png")))
            boton_borrar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            boton_borrar.setFixedSize(40, 30)
            boton_borrar.setProperty("tipo", "boton_borrar")
            
            boton_borrar.clicked.connect(lambda _, elem=elemento_catalogo, item=item: self.accion_borrar_catalogo(elem, nombre_qlistwidget, item))
            row_layout.addWidget(boton_borrar)

            # Asignar el widget al QListWidgetItem
            item.setSizeHint(widget.sizeHint())
            nombre_qlistwidget.setItemWidget(item, widget)



    
        
            
    def restaurar_botones_de_registrar(self):
        
        
        """
            ### Este Metodo es para dejar los botones de registrar nuevo elemento con su configuracion inicial despues de cancelar la edicion o la eliminacion del elemento
        
        
        """
        
        try:
            
            botones = (self.boton_registrar_especialidad, self.boton_registrar_cargo_empleado, self.boton_registrar_diagnostico, 
                       self.boton_registrar_enfermedad, self.boton_registrar_tipo_cargo_empleado, 
                       self.boton_registrar_funcion_cargo)
            
            for boton in botones:
                
                FuncionSistema.cambiar_estilo_del_boton(boton, "boton_anadir")
                
                
            self.desconectar_botones()

            
            # Conectando señales para añadir elementos a los catalogos
        
            self.boton_registrar_especialidad.clicked.connect(lambda _: self.agregar_nuevo_elemento_al_catalogo(self.input_especialidad, "especialidad", self.lista_especialidades) )
            self.boton_registrar_diagnostico.clicked.connect(lambda _: self.agregar_nuevo_elemento_al_catalogo(self.input_diagnostico, "diagnostico", self.lista_diagnosticos))
            self.boton_registrar_enfermedad.clicked.connect(lambda _: self.agregar_nuevo_elemento_al_catalogo(self.input_enfermedad, "enfermedad_cronica", self.lista_enfermedades))
            self.boton_registrar_funcion_cargo.clicked.connect(lambda _: self.agregar_nuevo_elemento_al_catalogo(self.input_funcion_cargo, "funcion_cargo", self.lista_funcion_cargo))

                
            
            
        except Exception as e:
            
            FuncionSistema.mostrar_errores_por_excepcion(e,"restaurar_botones_de_registrar")
            
            
    def desconectar_botones(self):
        
        self.boton_registrar_especialidad.clicked.disconnect()
        self.boton_registrar_diagnostico.clicked.disconnect()
        self.boton_registrar_enfermedad.clicked.disconnect()
        self.boton_registrar_funcion_cargo.clicked.disconnect()


    def actualizar_especialidades(self):
        """
            Este metodo sirve para actualizar las especialidades en las pantallas qe utilicen esta lista catalogo

        """
        self.lista_especialidades = especialidad_servicio.obtener_todos_especialidades()
        
        # asignamos las pantallas a las variables
        pantalla_vista_general_alumnos = self.stacked_widget.widget(2)
        pantalla_formulario_alumno = self.stacked_widget.widget(3)
        pantalla_asistencia_alumno = self.stacked_widget.widget(4)
        pantalla_generar_informes = self.stacked_widget.widget(5)
        pantalla_vista_general_personal = self.stacked_widget.widget(7)
        pantalla_formulario_empleado = self.stacked_widget.widget(8)
        
        # Agrupamos las pantalla en un lista
        # esta tupla contiene todos  los combobox con "Seleccionar aqui" en la primera opcion
        lista_seleccionar_aqui = (pantalla_formulario_alumno.boton_de_especialidad, 
                                  pantalla_formulario_empleado.boton_de_especialidad, 
                                  pantalla_asistencia_alumno.boton_especialidades,
                                  pantalla_generar_informes.boton_especialidades)
        
        # Aqui iteramos la lista de los combobox
        for combobox_especialidad in lista_seleccionar_aqui:
            FuncionSistema.cargar_elementos_para_el_combobox(self.lista_especialidades, combobox_especialidad, 1, 1)
        
        
        """
            Estos son dos casos particulares, el primero es que la vista general del alumno filtra de golpe y lanza una excepcion, el sistema no se corrompe,
            pero es desgradable para el usuario que cuando edite o agregue automaticamente le salga un mensaje de que no hay alumnos en x especialida nueva.
            
            el segundo la vista general del personal, no hay problemas, solo hay que agregar la palabra "Todos" a la primera opcion del combobox
        """
        pantalla_vista_general_alumnos.actualizar_combobox_especialidades()
        FuncionSistema.cargar_elementos_para_el_combobox(self.lista_especialidades, pantalla_vista_general_personal.boton_especialidades, 1, 0, "Todos")
        
    def actualizar_enfermedades_cronicas(self):
        """
            Este metodo sirve para actualizar las enfermedades cronicas en las pantallas qe utilicen esta lista catalogo
        """
        self.lista_enfermedades = enfermedad_cronica_servicio.obtener_todos_enfermedades_cronicas()
        
        # asignamos las pantallas a las variables
        pantalla_formulario_empleado = self.stacked_widget.widget(8)
        
        FuncionSistema.cargar_elementos_para_el_combobox(self.lista_enfermedades, pantalla_formulario_empleado.boton_enfermedades, 1, 1)
        
        
        
    def actualizar_diagnosticos(self):
        """
            Este metodo sirve para actualizar los diagnosticos en las pantallas qe utilicen esta lista catalogo
        """
        self.lista_diagnosticos = diagnostico_servicio.obtener_todos_diagnosticos()
        
        # asignamos las pantallas a las variables
        pantalla_formulario_alumno = self.stacked_widget.widget(3)
        pantalla_formulario_empleado = self.stacked_widget.widget(8)
        
        # agrupamos los combobox en una lista
        lista_combobox = (pantalla_formulario_alumno.boton_diagnostico,
                          pantalla_formulario_empleado.boton_diagnostico)
        
        for combobox_diagnostico in lista_combobox:
            FuncionSistema.cargar_elementos_para_el_combobox(self.lista_diagnosticos, combobox_diagnostico, 1, 1)
            
        
    def actualizar_cargos(self):
        """
            Este metodo sirve para actualizar los cargos en las pantallas qe utilicen esta lista catalogo
        """
        self.lista_cargo = cargo_empleado_servicio.obtener_todos_cargos_empleados()
        
        pantalla_formulario_empleado = self.stacked_widget.widget(8)
                
        FuncionSistema.cargar_elementos_para_el_combobox(self.lista_cargo, pantalla_formulario_empleado.boton_de_cargos, 2, 1)

       
    def actualizar_funciones_de_cargos(self):
        """
            Este metodo sirve para actualizar las funciones de cargos en las pantallas qe utilicen esta lista catalogo
        """
        self.lista_funcion_cargo = funcion_cargo_servicio.obtener_todos_funciones_cargo()
        
        pantalla_formulario_empleado = self.stacked_widget.widget(8)
                
        FuncionSistema.cargar_elementos_para_el_combobox(self.lista_funcion_cargo, pantalla_formulario_empleado.boton_funcion_cargos, 1, 1)

    
    def actualizar_tipos_de_cargos(self):
        """
            Este metodo sirve para actualizar los tipos de cargos en las pantallas qe utilicen esta lista catalogo
        """
        self.lista_tipo_cargo = tipo_cargo_servicio.obtener_todos_tipos_cargo()
        
        pantalla_vista_general_personal = self.stacked_widget.widget(7)
        pantalla_formulario_empleado = self.stacked_widget.widget(8)
                
        FuncionSistema.cargar_elementos_para_el_combobox(self.lista_tipo_cargo, pantalla_formulario_empleado.boton_tipo_de_cargo, 1, 1)

        """
            Aqui es un caso especial ya que lanza una excepcion cuando el combobox se actualiza, este lanza la excepcion es porque el combobox
            automaticamente filtrar por el currentChanged, asi que el metodo que esta aqui de la propia pantalla lo que hace es desconectar el boton,
            actualizarlo y volverlo a conectar a su funcion/metodo que usa
        """
        pantalla_vista_general_personal.actualizar_tipo_de_cargo()
        
        
        