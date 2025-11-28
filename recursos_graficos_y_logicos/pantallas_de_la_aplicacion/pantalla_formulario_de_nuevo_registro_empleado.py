from datetime import datetime
from PyQt5.QtCore import QRegExp, QDate
from PyQt5.QtGui import QRegExpValidator, QIntValidator
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QIcon
import traceback
import os
from PyQt5.QtWidgets import (QWidget, QCalendarWidget, QFrame,
                             QStackedWidget, QMessageBox,QListWidgetItem,
                             QLabel, QHBoxLayout,
                             QPushButton, QApplication)

from ..elementos_graficos_a_py import Ui_PantallaFormularioEmpleado
from ..utilidades.funciones_sistema import FuncionSistema


##################################
# importaciones de base de datos #
##################################



# repositorios
from repositorios.empleados.empleado_repositorio import EmpleadoRepositorio
from repositorios.empleados.enfermedad_cronica_repositorio import EnfermedadCronicaRepositorio
from repositorios.empleados.info_laboral_repositorio import InfoLaboralRepositorio
from repositorios.diagnosticos.diagnostico_repositorio import DiagnosticoRepositorio
from repositorios.empleados.tipo_cargo_repositorio import TipoCargoRepositorio
from repositorios.empleados.cargo_empleado_repositorio import CargoEmpleadoRepositorio
from repositorios.empleados.funcion_cargo_repositorio import FuncionCargoRepositorio
from repositorios.empleados.detalle_cargo_repositorio import DetalleCargoRepositorio
from repositorios.especialidades.especialidad_repositorio import EspecialidadRepositorio
from repositorios.empleados.info_clinica_empleado_repositorio import InfoClinicaEmpleadoRepositorio
from repositorios.empleados.historial_enferm_cronicas_repositorio import HistorialEnfermCronicasRepositorio




# servicios
from servicios.empleados.empleado_servicio import EmpleadoServicio
from servicios.empleados.enfermedad_cronica_servicio import EnfermedadCronicaServicio
from servicios.empleados.info_laboral_servicio import InfoLaboralServicio
from servicios.diagnosticos.diagnostico_servicio import DiagnosticoServicio
from servicios.empleados.tipo_cargo_servicio import TipoCargoServicio
from servicios.empleados.cargo_empleado_servicio import CargoEmpleadoServicio
from servicios.empleados.funcion_cargo_servicio import FuncionCargoServicio
from servicios.empleados.detalle_cargo_servicio import DetalleCargoServicio
from servicios.especialidades.especialidad_servicio import EspecialidadServicio
from servicios.empleados.info_clinica_empleado_servicio import InfoClinicaEmpleadoServicio
from servicios.empleados.historial_enferm_cronicas_servicio import HistorialEnfermCronicasServicio


##################################
# importaciones de base de datos #
##################################

# instancias de los repositorios
empleado_repositorio = EmpleadoRepositorio()

info_laboral_repositorio = InfoLaboralRepositorio()

tipo_cargo_repositorio = TipoCargoRepositorio()

cargo_empleado_repositorio = CargoEmpleadoRepositorio()

enfermedad_cronica_repositorio = EnfermedadCronicaRepositorio()

diagnostico_repositorio = DiagnosticoRepositorio()

funcion_cargo_repositorio = FuncionCargoRepositorio()

detalle_cargo_repositorio = DetalleCargoRepositorio()

especialidad_repositorio = EspecialidadRepositorio()

info_clinica_empleado_repositorio = InfoClinicaEmpleadoRepositorio()

historial_enferm_cronicas_repositorio = HistorialEnfermCronicasRepositorio()


# instancia de los servicios
empleado_servicio = EmpleadoServicio(empleado_repositorio)

info_laboral_servicio = InfoLaboralServicio(info_laboral_repositorio)

tipo_cargo_servicio = TipoCargoServicio(tipo_cargo_repositorio)

cargo_empleado_servicio = CargoEmpleadoServicio(cargo_empleado_repositorio)

enfermedad_cronica_servicio = EnfermedadCronicaServicio(enfermedad_cronica_repositorio)

diagnostico_servicio = DiagnosticoServicio(diagnostico_repositorio)

funcion_cargo_servicio = FuncionCargoServicio(funcion_cargo_repositorio)

detalle_cargo_servicio = DetalleCargoServicio(detalle_cargo_repositorio)

especialidad_servicio = EspecialidadServicio(especialidad_repositorio)

info_clinica_empleado_servicio = InfoClinicaEmpleadoServicio(info_clinica_empleado_repositorio)

historial_enferm_cronicas_servicio = HistorialEnfermCronicasServicio(historial_enferm_cronicas_repositorio)

# listas de datos segun la tabla
#lista_enfermedades = enfermedad_cronica_servicio.obtener_todos_enfermedades_cronicas()
#lista_diagnostico = diagnostico_servicio.obtener_todos_diagnosticos()

lista_cargo = cargo_empleado_servicio.obtener_todos_cargos_empleados()
lista_tipo_cargo = tipo_cargo_servicio.obtener_todos_tipos_cargo()
lista_funcion_cargo = funcion_cargo_servicio.obtener_todos_funciones_cargo()
lista_especialidades = especialidad_servicio.obtener_todos_especialidades()

class PantallaDeFormularioNuevoRegistroEmpleado(QWidget, Ui_PantallaFormularioEmpleado):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.setupUi(self)
        
        # se crea messagebox
        self.msg_box = QMessageBox(self)
        self.boton_si = self.msg_box.addButton("Sí", QMessageBox.YesRole)
        self.boton_no = self.msg_box.addButton("No", QMessageBox.NoRole)
        
        
        # Se que se tratan de tuplas, pero las nombre LISTA para que fuera rapido de asociar
        
        # AQui estan las listas carrito y los qlistwidget ya que pueden usar tambien el .clear()
        self.lista_qlineedit = (
                                self.input_primer_nombre, self.input_segundo_nombre, self.input_tercer_nombre, self.input_apellido_paterno,
                                self.input_apellido_materno, self.input_cedula, self.input_talla_de_camisa, self.input_talla_de_pantalon,
                                self.input_talla_de_zapatos, self.input_estado_residente, self.input_municipio, self.input_direccion_residencia,
                                self.input_numero_de_telefono, self.input_numero_de_telefono_adicional, self.input_correo_electronico, self.input_correo_electronico_adicional,
                                self.input_otra_enfermedad, self.input_otro_diagnostico, self.ver_lista_diagnostico, self.ver_lista_enfermedades,
                                self.input_codigo_por_donde_cobra, self.input_institucion_donde_laboral, self.input_titulo_del_cargo, self.input_labores_que_realiza,
                                self.ver_lista_diagnostico, self.ver_lista_enfermedades
                                )
        
        
        self.lista_qradiobutton = (
                                    self.input_sexo_femenino, self.input_sexo_masculino, self.input_si, self.input_no
                                )
        

        self.lista_qcombobox = ( self.boton_enfermedades, self.boton_diagnostico, self.boton_de_especialidad, self.boton_de_cargos,
                                self.boton_funcion_cargos, self.boton_tipo_de_cargo
                                )
        
        # lista de las base de datos
        self.lista_diagnostico = diagnostico_servicio.obtener_todos_diagnosticos()       
        self.lista_enfermedades_cronicas = enfermedad_cronica_servicio.obtener_todos_enfermedades_cronicas()

        # listas carrito
        self.lista_carrito_enfermedades = []
        self.lista_carrito_diagnosticos = []

        
        
        # Detalles para detalles de cargo
        self.dateedit_fecha_ingreso_tela.setDate(QtCore.QDate.currentDate()) # esto le coloca la fecha actual
        

        
        self.boton_de_especialidad.setEnabled(False)
        
    
        # Conectar Botones a los metodos
        self.boton_anadir_enfermedad.clicked.connect(self.anadir_enfermedad)
        self.boton_anadir_diagnostico.clicked.connect(self.anadir_diagnostico)
        self.boton_tipo_de_cargo.currentIndexChanged.connect(self.habilitar_boton_especialidades)    
        
        ## Boton para registrar toda la informacion a la base de datos##
        self.boton_finalizar.clicked.connect(self.guardar_informacion_empleado)

        ## Boton de regreso para retroceder a la pregunta previa o salir del formulario ##
        self.boton_de_regreso.clicked.connect(self.salir_del_formulario_empleado)
        


        # Cargar catalogos a los combobox
        
        # cargar catalogo de enfermedades
        FuncionSistema.cargar_elementos_para_el_combobox(self.lista_enfermedades_cronicas, self.boton_enfermedades, 1, 1)
        
        # cargar catalogo de diagnosticos
        FuncionSistema.cargar_elementos_para_el_combobox(self.lista_diagnostico ,self.boton_diagnostico, 1, 1)
        
        # Cargamos al boton la lista de los cargos
        FuncionSistema.cargar_elementos_para_el_combobox(lista_cargo, self.boton_de_cargos, 2, 1)

        # Cargando al boton la lista de tipo de cargo
        FuncionSistema.cargar_elementos_para_el_combobox(lista_tipo_cargo, self.boton_tipo_de_cargo, 1, 1)

        # Cargando al boton la lista de funcion de cargo
        FuncionSistema.cargar_elementos_para_el_combobox(lista_funcion_cargo, self.boton_funcion_cargos, 1, 1)

        # Cargamos al boton la lista de especialidades
        FuncionSistema.cargar_elementos_para_el_combobox(lista_especialidades, self.boton_de_especialidad, 1, 1)

        

        
        ### Esto es de prueba, esto asigna un valor a los input
        
        
        """
        self.input_primer_nombre.setText("Marla")
        self.input_apellido_paterno.setText("Garcia")
        self.input_cedula.setText("24345231")
        self.input_sexo_femenino.setChecked(True)
        self.input_si.setChecked(True)
        
        self.input_talla_de_camisa.setText("s")
        self.input_talla_de_pantalon.setText("23")
        self.input_talla_de_zapatos.setText("25")
        
        
        self.input_estado_residente.setText("Anzoategui")
        self.input_municipio.setText("Bolivar")
        self.input_direccion_residencia.setText("Calle 19")
        
        self.input_numero_de_telefono.setText("04120293022")
        self.input_correo_electronico.setText("lgii@gmail.com")
        
        self.input_codigo_por_donde_cobra.setText("123123123")
        self.input_institucion_donde_laboral.setText("Escuela de tal")
        
        
        """
        
        
    
    def habilitar_boton_especialidades(self):
        
        if not self.boton_tipo_de_cargo.currentText() == "DOCENTE":
        
            self.boton_de_especialidad.setEnabled(False)

        
        else:
            self.boton_de_especialidad.setEnabled(True)
    
    

    
    ## Metodo para añadir una enfermedad al "carrito"
    def anadir_enfermedad(self):

        """
            Este metodo sirve para agregar las enfermedades al carrito de enfermedades.
            
            este metodo funciona asi:
            
            Si el combobox de las enfermedades tiene texto y no esta en la posicion 0 
            - Primero declaramos una lista vacia
            - a esa lista le agregamos el nombre de la enfermedad segun el combobox
            - luego buscamos y agregamos el id de esa enfermedad
            - luego la lista se transforma en tupla
            - y por ultimo mandamos esto a el qlistwidget para que lo muestre por pantalla
            
            Si el QlineEdit otra enfermedad tiene texto
            - registramos la enfermedad
            - se hace el mismo proceso descrito anteriormente
            
        
        
        """
        
        
        carrito_enfermedad = []
            
        if self.boton_enfermedades.currentText() and not self.boton_enfermedades.currentIndex() == 0:
            
            # Nombre de la enfermedad
            enfermedad = self.boton_enfermedades.currentText()
            
            # Id de la enfermedad
            enfermedad_id = self.buscar_id_de_la_lista_del_combobox(self.boton_enfermedades, self.lista_enfermedades_cronicas, 1, 0)
            
            # Se añade los elementos a la lista "Carrito pequeño"
            carrito_enfermedad.append(enfermedad_id)
            carrito_enfermedad.append(enfermedad)
            
            # lo transformamos en tupla
            carrito_enfermedad = tuple(carrito_enfermedad)
            
            # Lo agregamos al carrito que se utilizara para el final
            self.lista_carrito_enfermedades.append(carrito_enfermedad)
            
            # esto es lo que se mostrara en el qlistwidget
            texto_mostrar = carrito_enfermedad[1]
            
            # se agrega en el qlistwidget
            self.agregar_elementos_a_la_vista_previa(self.ver_lista_enfermedades, self.lista_carrito_enfermedades, self.boton_enfermedades, texto_mostrar)
        
            
        elif self.input_otra_enfermedad.text() :
            
            # Registra
            enfermedad = self.input_otra_enfermedad.text().strip().capitalize()
            nueva_enfermedad = {"enfermedad_cronica": enfermedad.capitalize()}
            enfermedad_cronica_servicio.registrar_enfermedad_cronica(nueva_enfermedad) 
            
            # actualiza la lista
            self.lista_enfermedades_cronicas = enfermedad_cronica_servicio.obtener_todos_enfermedades_cronicas()
            
            # Actualiza la lista catalogo
            enfermedad_id = self.buscar_id_de_la_lista_del_combobox(self.boton_enfermedades, self.lista_enfermedades_cronicas, 1, 0, self.input_otra_enfermedad)
            
            carrito_enfermedad.append(enfermedad_id)
            carrito_enfermedad.append(enfermedad)
            
            carrito_enfermedad = tuple(carrito_enfermedad)
            
            self.lista_carrito_enfermedades.append(carrito_enfermedad)
            
            texto_mostrar = carrito_enfermedad[1]
            
            self.agregar_elementos_a_la_vista_previa(self.ver_lista_enfermedades, self.lista_carrito_enfermedades, self.boton_enfermedades, texto_mostrar)
        


        
        else:
            return
        
        # Actualizamos el combobox, limpiandolo y dandole la lista nueva
        self.boton_enfermedades.clear()
        
        self.lista_enfermedades_cronicas = enfermedad_cronica_servicio.obtener_todos_enfermedades_cronicas()
        
        FuncionSistema.cargar_elementos_para_el_combobox(self.lista_enfermedades_cronicas, self.boton_enfermedades, 1, 1)



        # Limpiar el QLineEdit después de añadir
        self.input_otra_enfermedad.clear()
        self.boton_enfermedades.setCurrentIndex(0)
        print(self.lista_carrito_enfermedades)





    ## Metodo para añadir un diagnostico al "carrito"
    def anadir_diagnostico(self):

        """
            Este metodo sirve para agregar los diagnosticos al carrito de diagnosticos.
            
            este metodo funciona asi:
            
            Si el combobox de los diagnosticos tiene texto y no esta en la posicion 0 
            - Primero declaramos una lista vacia
            - a esa lista le agregamos el nombre del diagnostico segun el combobox
            - luego buscamos y agregamos el id de ese diagnostico
            - luego la lista se transforma en tupla
            - y por ultimo mandamos esto a el qlistwidget para que lo muestre por pantalla
            
            Si el QlineEdit otra diagnostico tiene texto
            - registramos el diagnostico
            - se hace el mismo proceso descrito anteriormente
            
        
        
        """
        
        carrito_diagnostico = []
        
        
        # si el combo box tiene texto y no el indice del mismo no el 0
        if self.boton_diagnostico.currentText() and not self.boton_diagnostico.currentIndex() == 0:
            
            # Nombre del diagnostico
            diagnostico = self.boton_diagnostico.currentText()
            
            # Id del diagnostico
            diagnostico_id = self.buscar_id_de_la_lista_del_combobox(self.boton_diagnostico, self.lista_diagnostico, 1, 0)
            
            # se añaden al carrito temporal
            carrito_diagnostico.append(diagnostico_id)
            carrito_diagnostico.append(diagnostico)
            
            # se transforma en tupla
            carrito_diagnostico = tuple(carrito_diagnostico)
            
            # Lo añadimos al carrito que nos servira para el final
            self.lista_carrito_diagnosticos.append(carrito_diagnostico)

            # Esto es lo que se va a mostrar en pantalla
            texto_mostrar = carrito_diagnostico[1]
            
            # Lo agregamos al qlistwidget
            self.agregar_elementos_a_la_vista_previa(self.ver_lista_diagnostico, self.lista_carrito_diagnosticos, self.boton_diagnostico, texto_mostrar)

        
            
        elif self.input_otro_diagnostico.text().strip():
            
            # Se registra
            diagnostico = self.input_otro_diagnostico.text().strip().capitalize()
            nuevo_diagnostico = {"diagnostico": diagnostico}
            diagnostico_servicio.registrar_diagnostico(nuevo_diagnostico)
            
            # 
            self.lista_diagnostico = diagnostico_servicio.obtener_todos_diagnosticos()
            
            diagnostico_id = self.buscar_id_de_la_lista_del_combobox(self.boton_diagnostico, self.lista_diagnostico, 1, 0, self.input_otro_diagnostico)
            
            carrito_diagnostico.append(diagnostico_id)
            carrito_diagnostico.append(diagnostico)
            
            carrito_diagnostico = tuple(carrito_diagnostico)
            
            self.lista_carrito_diagnosticos.append(carrito_diagnostico)

            texto_mostrar = carrito_diagnostico[1]
            
            self.agregar_elementos_a_la_vista_previa(self.ver_lista_diagnostico, self.lista_carrito_diagnosticos, self.boton_diagnostico, texto_mostrar)

        
            
   
        
        else:
            return
        
    
       
        

       
        
        # Limpiar el QLineEdit después de añadir
        self.boton_diagnostico.clear()
        
        self.lista_diagnostico = diagnostico_servicio.obtener_todos_diagnosticos()
        
        FuncionSistema.cargar_elementos_para_el_combobox(self.lista_diagnostico ,self.boton_diagnostico, 1, 1)

        # Limpiar el QLineEdit después de añadir
        self.input_otro_diagnostico.clear()
        self.boton_diagnostico.setCurrentIndex(0)




    # Metodo para agregar elementos a la vista previa
    def agregar_elementos_a_la_vista_previa(self, nombre_qlistwidget, nombre_lista, enfoca_input = None, texto_a_mostrar=None):
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
        delete_button = QPushButton()
        delete_button.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "borrar.png")))
        delete_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        delete_button.setFixedSize(40,40)
        delete_button.setStyleSheet("""
                                    
                                    QPushButton{
                                        background:red;
                                        border-radius:20px;
                                        icon-size:28px;
                                    
                                    }
                                    
                                    QPushButton:hover{
                                        
                                        background:#9e0000
                                        
                                        
                                    }
                                    
                                    
                                    """)
        
        delete_button.clicked.connect(lambda: self.borrar_elementos_a_la_vista_previa(nombre_qlistwidget, nombre_lista, enfoca_input, item))
        row_layout.addWidget(delete_button)

        # Asignar el widget al QListWidgetItem
        item.setSizeHint(widget.sizeHint())
        nombre_qlistwidget.setItemWidget(item, widget)

    
    

    # Metodo para borrar elemento a la vista previa
    def borrar_elementos_a_la_vista_previa(self, nombre_qlistwidget, nombre_lista, enfoca_input,  item):
        
        
        # Logica para borrar el registro del diagnostico de la lista
        
        # indice del listwidget
        indice_vista_previa = nombre_qlistwidget.row(item)
        
        # borramos el elemento de la lista segun el indice del listwidget
        del nombre_lista[indice_vista_previa]
        
        # darle foco al input del segmento
        # esto lo hice porque al borrar toda la lista de X segmento, esta se subia al arriba del todo del formulario
        
        
        enfoca_input.setFocus()
        
        
        
        
        
        
        ##########################################################################
        # Obtener la fila del item y eliminarlo
        row = nombre_qlistwidget.row(item)
        nombre_qlistwidget.takeItem(row)
    
        print(f"lista actualizada: {nombre_lista}")
    



    ## Metodo para cargar la lista en los botones desplegables de cargo, tipo cargo, funcion de cargo y especialidad
    ## para las enfermedades y diagnostico ya sirve
    def cargar_lista_para_el_combobox(self, lista_catalogo, boton_desplegable, indice_nombre_elemento:int):
        
        try:    
            boton_desplegable.addItem("Seleccione aqui")
                
        
            
            for elemento_iterado in lista_catalogo:
                
                boton_desplegable.addItem(elemento_iterado[indice_nombre_elemento])
        
        except Exception as e:
            
            print(f"Ocurrio un error: {e}")
            
        #else: 
            
            #print(f"\nLa lista para el/los boton cargo correctamente")
        
        
    # Metodo para buscar el id que esta en la tupla de la lista que arroja la base de datos
    def buscar_id_de_la_lista_del_combobox(self, boton_seleccionado, lista_elementos, indice_nombre_del_elemento, indice_id_del_elemento, qlineedit_elemento_nuevo= None):
            
        seleccion = boton_seleccionado.currentText()

        
        
        if  seleccion and not boton_seleccionado.currentIndex() == 0:
            
            for elemento in lista_elementos:
                
                if seleccion.lower() == elemento[indice_nombre_del_elemento].lower():
                    
                    id_del_elemento = elemento[indice_id_del_elemento]  
                    
                    id_del_elemento = int(id_del_elemento)
                    
                    return id_del_elemento
                    
                        
        if not qlineedit_elemento_nuevo == None:
            
            if boton_seleccionado.currentIndex() == 0 and qlineedit_elemento_nuevo.text().strip():
                
                
                for elemento in lista_elementos:
                    
                    if qlineedit_elemento_nuevo.text().lower() == elemento[indice_nombre_del_elemento].lower():
                        
                        id_del_elemento = elemento[indice_id_del_elemento]  
                        
                        id_del_elemento = int(id_del_elemento)
                        
                        return id_del_elemento
                
            
            
            
            
                            
                        
        
        
        

    
    # Método para cambiar de str a date (solo usar para las fechas)
    def fecha_de_str_a_date(self, fecha_string):
        # Convertir el string a objeto date
        try:
            # Primero eliminar espacios y normalizar el formato
            fecha_limpia = fecha_string.replace(" ", "")  # Eliminar espacios
            fecha_limpia = fecha_limpia.replace("/", "-")  # Reemplazar / por -
            
            # Si el formato original era "2000/04/02" ahora será "2000-04-02"
            # Verificar que tenga el formato correcto para datetime
            fecha_date = datetime.strptime(fecha_limpia, "%Y-%m-%d").date()
            
            return fecha_date
    
        except ValueError as e:
            print(f"Error al convertir la fecha: {e}")
            return None  
    
    # Metodo para mostrar errores de la base de datos 
    def mostrar_errores_antes_de_guardar(self, errores):
        
        error_msg = "Lista de errores:\n"
        error_msg += "\n".join(f"- {field.capitalize()}" for field in errores)
        QMessageBox.critical(self, "Errores", error_msg)
        print("\n".join(errores))
        return
    
    
    # Metodo para comprobar si la input tiene texto o valor
    # si es SI: guarda el valor
    # si es NO: guarda NONE
    def comprobar_si_hay_valor(self, elemento_a_comprobar):
        
        if elemento_a_comprobar.text().strip():
            
            return elemento_a_comprobar.text().strip().capitalize()
        
        else:
            
            return None
    
    
    ## Metodo para guardar todas las preguntas en la bd ##
    def guardar_informacion_empleado(self):

        

        
            
        try:    
            
            # info basica
            

            primer_nombre = self.input_primer_nombre.text().capitalize()
            segundo_nombre = self.comprobar_si_hay_valor(self.input_segundo_nombre)
            tercer_nombre = self.comprobar_si_hay_valor(self.input_tercer_nombre)
            apellido_paterno = self.input_apellido_paterno.text().capitalize()
            apellido_materno = self.comprobar_si_hay_valor(self.input_apellido_materno)
            cedula = self.input_cedula.text().capitalize()
            
            fecha_nacimiento = self.fecha_de_str_a_date(self.dateedit_fecha_nacimiento.text())


            if self.input_sexo_masculino.isChecked():
                sexo = "M"

            elif self.input_sexo_femenino.isChecked():
                sexo = "F"
                
            else:
                sexo = None


            if self.input_si.isChecked():
                tiene_hijos_menores = 1

            elif self.input_no.isChecked():
                tiene_hijos_menores = 0

            #print(f"tiene hijos: {tiene_hijos_menores}\n sexo: {sexo}, fecha{type(fecha_nacimiento)}")



            errores_info_basica = empleado_servicio.validar_info_basica_empleado(
                primer_nombre, segundo_nombre, tercer_nombre,
                apellido_paterno, apellido_materno,
                cedula, fecha_nacimiento
            )

            if errores_info_basica:
                self.area_de_scroll.verticalScrollBar().setValue(100)
                self.mostrar_errores_antes_de_guardar(errores_info_basica)
                return
            
            else:   
                



                ## "Info medidas" que verifique si falta un campo requerido  ##

                talla_camisa =  self.input_talla_de_camisa.text().upper()
                talla_pantalon = self.input_talla_de_pantalon.text()
                talla_zapatos = self.input_talla_de_zapatos.text()

                if not(talla_pantalon):
                    talla_pantalon = None
                else:
                    talla_pantalon = int(talla_pantalon)
                    
                if not(talla_zapatos):
                    talla_zapatos = None
                else:
                    talla_zapatos = int(talla_zapatos)
                        
                    

                errores_medidas = empleado_servicio.validar_medidas_empleado(talla_camisa, talla_pantalon, talla_zapatos)

                if errores_medidas:
                    self.area_de_scroll.verticalScrollBar().setValue(300)
                    self.mostrar_errores_antes_de_guardar(errores_medidas)
                    return
                
                else:
                    
                
                
                

                    ## info cgeografica" que verifique si falta un campo requerido  ##
                    

                    estado_reside = self.input_estado_residente.text()
                    municipio = self.input_municipio.text()
                    direccion_residencia = self.input_direccion_residencia.text()

                    errores_info_geografica = empleado_servicio.validar_info_geografica_empleado(
                        estado_reside, municipio,
                        direccion_residencia
                    )

                    if errores_info_geografica:
                        
                        self.area_de_scroll.verticalScrollBar().setValue(500)
                        self.mostrar_errores_antes_de_guardar(errores_info_geografica)
                        return
                        

                    ## "info contactos" que verifique si falta un campo requerido  ##
                    

                    num_telefono = self.input_numero_de_telefono.text().strip()
                    num_telefono_adicional = self.comprobar_si_hay_valor(self.input_numero_de_telefono_adicional)
                    
                    correo_electronico = self.input_correo_electronico.text().strip()
                    correo_electronico_adicional = self.comprobar_si_hay_valor(self.input_correo_electronico_adicional)

                    errores_info_contacto = empleado_servicio.validar_info_contacto_empleado(num_telefono, num_telefono_adicional, correo_electronico, correo_electronico_adicional)

                    if errores_info_contacto:
                        #print(f"tlf 1: {num_telefono}| tlf 2 : {num_telefono_adicional}")
                        #print(f"correo 1: {correo_electronico} | correo 2: {correo_electronico_adicional}")
                        self.area_de_scroll.verticalScrollBar().setValue(700)
                        self.mostrar_errores_antes_de_guardar(errores_info_contacto)
                        return

                    else:

                        ## "info medica" que verifique si falta un campo requerido  ##
                        
                        # Info medica es opcional

                        


                        ## "info laboral" que verifique si falta un campo requerido  ##
                        
                        cod_depend_cobra = self.input_codigo_por_donde_cobra.text()
                        institucion_labora = self.input_institucion_donde_laboral.text()


                        errores_info_laboral = info_laboral_servicio.validar_campos_info_laboral(
                            cod_depend_cobra, institucion_labora
                        )

                        if errores_info_laboral:
                            self.area_de_scroll.verticalScrollBar().setValue(1500)
                            self.mostrar_errores_antes_de_guardar(errores_info_laboral)
                            return
                        
                        else:


                            ## "info detalle del cargo" que verifique si falta un campo requerido  ##
                            ## y que muestre un mensaje que de registro exitoso y que se vaya a la pantalla de vista previa del personal  ##
                            
                            
                            

                            #cargo_id = None
                            #funcion_cargo_id = None
                            #tipo_cargo_id = None
                            
                            labores_cargo = self.input_labores_que_realiza.text()

                            fecha_ingreso_institucion = self.fecha_de_str_a_date(self.dateedit_fecha_ingreso_tela.text())  # Por defecto se establece la fecha actual

                            fecha_ingreso_ministerio = self.fecha_de_str_a_date(self.dateedit_fecha_ingreso_ministerio.text())
                            

                            situacion = None  # Por defecto es Activo

                            titulo_cargo = self.input_titulo_del_cargo.text()
                            
                            especialidad_id = None

                            #cargo_id, funcion_cargo_id, tipo_cargo_id, especialidad_id = 1,1,1,1
                            #funcion_cargo_id, tipo_cargo_id, especialidad_id = 1,1,1

                            # buscamos el id de la lista cargo del boton seleccionado
                            cargo_id = self.buscar_id_de_la_lista_del_combobox(self.boton_de_cargos, lista_cargo, 2, 0)

                            # buscamos el id de la lista de la funcion del cargo del boton seleccionado
                            funcion_cargo_id = self.buscar_id_de_la_lista_del_combobox(self.boton_funcion_cargos, lista_funcion_cargo, 1, 0)

                            # buscamos el id en la lista del tipo de cargo del boton seleccionado 
                            tipo_cargo_id = self.buscar_id_de_la_lista_del_combobox(self.boton_tipo_de_cargo, lista_tipo_cargo, 1, 0)
                        
                        
                            
                            
                            if self.boton_tipo_de_cargo.currentText().lower() == "docente" and not self.boton_de_especialidad.currentIndex() == 0:
            
                                if especialidad_id == None:
                                    
                                    # buscamos el id de la especialidad que esta en la lista del boton 
                                    especialidad_id = self.buscar_id_de_la_lista_del_combobox(self.boton_de_especialidad, lista_especialidades, 1, 0)

                            
                            elif self.boton_tipo_de_cargo.currentText().lower() == "docente" and  self.boton_de_especialidad.currentIndex() == 0:
                                
                                QMessageBox.warning(self, "Aviso", "Si es docente eliga una especialidad")
                                return
                                
                            else:
                                especialidad_id = None
                                
                                

                            
                                
                            #print(f"\nID del cargo: {cargo_id}tipo de variable: {type(cargo_id)}",)
                            #print(f"\nID del funcion de cargo: {funcion_cargo_id} tipo de variable: {type(funcion_cargo_id)}",)
                            #print(f"\nID del tipo de cargo: {tipo_cargo_id} tipo de variable: {type(tipo_cargo_id)}",)
                            #print(f"\nID del especialidad: {especialidad_id} tipo de variable: {type(especialidad_id)}",)   
                    


                            errores_detalle_cargo = detalle_cargo_servicio.validar_detalles_cargo(
                                cargo_id, funcion_cargo_id,
                                tipo_cargo_id, titulo_cargo,
                                labores_cargo, fecha_ingreso_ministerio
                            )

                            if errores_detalle_cargo:
                                self.mostrar_errores_antes_de_guardar(errores_detalle_cargo)
                                return

                            
                            
                            else:
                                
                                

                                self.msg_box.setWindowTitle("Confirmar registro")
                                self.msg_box.setText("¿Seguro que quiere registrar a este empleado?")
                                self.msg_box.setIcon(QMessageBox.Question)
                                QApplication.beep()

                                # Mostrar el cuadro de diálogo y esperar respuesta
                                self.msg_box.exec_()


                                if self.msg_box.clickedButton() == self.boton_si:
                                    try:
                                        # esto es para ver si los datos se guardan y mostrarlos por consola
                                        """
                                        print("-------nuevo empleado--------")
                                        print(f"Primer Nombre:{primer_nombre} {type(primer_nombre)}\nSegundo nombre: {segundo_nombre} {type(segundo_nombre)}")
                                        print(f"Apellido Paterno: {apellido_paterno} {type(apellido_paterno)}\n Apellido Materno: {apellido_materno} {type(apellido_materno)}")
                                        print(f"Sexo: {sexo} {type(sexo)}\nTiene hijos: {tiene_hijos_menores} {type(tiene_hijos_menores)}")
                                        print(f"Fecha de nacimiento: {fecha_nacimiento} {type(fecha_nacimiento)}")
                                        print(f"Talla camisa: {talla_camisa} {type(talla_camisa)}\nTalla pantalon: {talla_pantalon}\nTalla zapatos: {talla_zapatos} {type(talla_zapatos)}")
                                        print(f"Estado: {estado_reside} {type(estado_reside)}\nMunicipio: {municipio} {type(municipio)}\n Direccion: {direccion_residencia} {type(direccion_residencia)} ")
                                        print(f"Telefono: {num_telefono} {type(num_telefono)}\nCorreo: {correo_electronico} {type(correo_electronico)}")
                                        print(f'Enfermedad:{enferm_cronica_id} {type(enferm_cronica_id)}\nDiagnotico:{diagnostico_id} {type(diagnostico_id)}')
                                        print(f"Codigo por donde cobra: {cod_depend_cobra} {type(cod_depend_cobra)}\nInstitucion por donde labora: {institucion_labora} {type(institucion_labora)} ")
                                        print(f"Cargo: {cargo_id} {type(cargo_id)}\nFuncion del cargo: {funcion_cargo_id} {type(funcion_cargo_id)}\nTipo de cargo: {tipo_cargo_id} {type(tipo_cargo_id)} ")
                                        print(f"Titulo: {titulo_cargo} {type(titulo_cargo)}\n Labores que realiza: {labores_cargo} {type(labores_cargo)}")
                                        print(f"fecha de ingreso del ministerio: {fecha_ingreso_ministerio} {type(fecha_ingreso_ministerio)}\nFecha de ingreso al tela: {fecha_ingreso_institucion} {type(fecha_ingreso_institucion)}")

                                        """

                                        campos_empleado = {
                                            "cedula": cedula,
                                            "primer_nombre": primer_nombre,
                                            "segundo_nombre": segundo_nombre,
                                            "tercer_nombre": tercer_nombre,
                                            "apellido_paterno": apellido_paterno,
                                            "apellido_materno": apellido_materno,
                                            "fecha_nacimiento": fecha_nacimiento,
                                            "sexo": sexo,
                                            "tiene_hijos_menores": tiene_hijos_menores,
                                            "fecha_ingreso_institucion": fecha_ingreso_institucion,
                                            "fecha_ingreso_ministerio": fecha_ingreso_ministerio,
                                            "talla_camisa": talla_camisa,
                                            "talla_pantalon": talla_pantalon,
                                            "talla_zapatos": talla_zapatos,
                                            "num_telefono": num_telefono,
                                            "num_telefono_adicional": num_telefono_adicional,
                                            "correo_electronico": correo_electronico,
                                            "correo_electronico_adicional": correo_electronico_adicional,
                                            "estado_reside": estado_reside,
                                            "municipio": municipio,
                                            "direccion_residencia": direccion_residencia,
                                            "situacion": situacion
                                        }

                                        # Acá va a retornar el empleado_id para asociarlo a las demás tablas cuyos campos
                                        # se llenaron en el formulario
                                        empleado_id = empleado_servicio.registrar_empleado(campos_empleado)

                                        # Acá con esto es para más adelante comprobar que si
                                        # Si la lista de diagnosticos o la lista de enfermedades crónicas
                                        # no está vacía entonces se hace el proceso de asociar el empleado con sus enfermedades o discapacidades
                                        # en caso de que alguna esté vacía entonces ese registro en concreto (por ejemplo, si la de discapaciades
                                        # está vacía) no se hace
                                        
                                        campos_info_clinica_empleado = {
                                            "empleado_id": empleado_id,
                                            "diagnostico_id": None
                                        }
                                        
                                        # declaramos el diccionario
                                        campos_historial_enferm_cronicas = {
                                                "empleado_id": empleado_id,
                                                "enferm_cronica_id": None
                                            }
                                        
                                        
                                        
                                        
                                        # se ve si la lista esta llena
                                        if self.lista_carrito_diagnosticos:
                                            
                                            # se itera cada diagnostico
                                            for diagnostico in self.lista_carrito_diagnosticos:
                                                
                                                diagnostico_id = diagnostico[0]
                                                        
                                                campos_info_clinica_empleado["diagnostico_id"] = diagnostico_id
                                            
                                                info_clinica_empleado_servicio.registrar_info_clinica_empleado(campos_info_clinica_empleado)

                                            
                                        
                                        
                                                
                                            
                                        if self.lista_carrito_enfermedades:
                                            
                                            for enfermedad in self.lista_carrito_enfermedades:
                                                
                                                    
                                                    
                                                enferm_cronica_id = enfermedad[0]
                                                
                                                campos_historial_enferm_cronicas["enferm_cronica_id"] = enferm_cronica_id
                                                
                                                historial_enferm_cronicas_servicio.registrar_historial_enferm_cronica(campos_historial_enferm_cronicas)

                                                            
                                        else:
                                            
                                            pass
                                                                
                                            
                                        

                                        campos_info_laboral = {
                                            "empleado_id": empleado_id,
                                            "cod_depend_cobra": cod_depend_cobra,
                                            "institucion_labora": institucion_labora
                                        }

                                        campos_detalle_cargo = {
                                            "empleado_id": empleado_id,
                                            "cargo_id": cargo_id,
                                            "funcion_cargo_id": funcion_cargo_id,
                                            "especialidad_id": especialidad_id,
                                            "tipo_cargo_id": tipo_cargo_id,
                                            "titulo_cargo": titulo_cargo,
                                            "labores_cargo": labores_cargo
                                        }

                                        info_laboral_servicio.registrar_info_laboral(campos_info_laboral)
                                        detalle_cargo_servicio.registrar_detalle_cargo(campos_detalle_cargo)

                                        QMessageBox.information(self, "Bien hecho", "Registro exitoso")


                                        pantalla_tabla = self.stacked_widget.widget(7)
                                        
                                        pantalla_tabla.actualizar_tabla(tipo_cargo_id= 1, especialidad_id= None, indice_cedula= 1, indice_1er_nombre= 2, indice_2do_nombre= 3,
                                                                        indice_1er_apellido=5, indice_2do_apellido= 6, indice_estado= 8)
                                        
                                        pantalla_tabla.actualizar_lista_busqueda()
                                        
                                        pantalla_tabla.boton_de_opciones.setCurrentIndex(0)
                                    
                                        self.stacked_widget.setCurrentIndex(7)


                                        FuncionSistema.limpiar_inputs_de_qt(self.lista_qlineedit, self.lista_qradiobutton, self.lista_qcombobox)
                                        
                                        
                                        self.dateedit_fecha_nacimiento.setDate(QtCore.QDate(2000, 1, 1))
                                        self.dateedit_fecha_ingreso_ministerio.setDate(QtCore.QDate(2000, 1, 1))



                                    except Exception as e:

                                        QMessageBox.information(self, "No se pudo", f"{str(e)}")
                                        return
                                        #self.cambio.setCurrentIndex(0)
                                        #self.stacked_widget.setCurrentIndex(2)

                                    else:
                                        
                                        print("registro exitoso")

                                if self.msg_box.clickedButton() == self.boton_no:
                                    
                                    print("registro cancelado")
                                    return
                                
                                
                                
        except Exception as e:
            
            # Obtener el traceback completo como string
            error_traceback = traceback.format_exc()
        
            # Mostrar en consola (para depuración)
            print("\n\nError en la línea:", traceback.extract_tb(e.__traceback__)[-1].lineno)
            print("Traceback completo:\n", error_traceback)
            
            print(f"error en la funcion guardar_informacion_empleado: {e}")
            
        else:
            
            print("libre de errores")
     


    
    def editar_datos_empleado(self, empleado_id):
        """
            Este metodo sirve para editar la informacion del empleado en cuestion, se reutiliza esta pantalla es para aprobechar mejor todas las funciones y metodos que ya estan
        
        
        """
        
        self.boton_finalizar.clicked.disconnect()
        self.boton_finalizar.clicked.connect(lambda: self.confirmar_edicion_datos_empleados(empleado_id))
        

        info_basica = empleado_servicio.obtener_empleado_por_id(empleado_id)
        
        # Info basica
        self.input_primer_nombre.setText(info_basica[1])
        self.input_segundo_nombre.setText(info_basica[2])
        self.input_tercer_nombre.setText("" if info_basica[3] == None else info_basica[3])
        self.input_apellido_paterno.setText(info_basica[4])
        self.input_apellido_materno.setText(info_basica[5])
        self.input_cedula.setText(info_basica[6])
        
        self.dateedit_fecha_nacimiento.setDate(QDate.fromString(info_basica[7], 'yyyy-dd-MM'))



        if info_basica[10] == 'M':
            
            self.input_sexo_masculino.setChecked(True)
        
        
        elif info_basica[10] == 'F':
            
            self.input_sexo_femenino.setChecked(True)
            
            
            
            
        if info_basica[11] == 0:
            
            self.input_no.setChecked(True)
        
        if info_basica[11] == 1:
            
            self.input_si.setChecked(True)
        
        
        
        
        # Info medidas
        
        info_medidas = empleado_servicio.obtener_medidas_empleado(empleado_id)
        
        self.input_talla_de_camisa.setText(info_medidas[1])
        self.input_talla_de_pantalon.setText(str(info_medidas[2]))
        self.input_talla_de_zapatos.setText(str(info_medidas[3]))
        
        
        # Info geografica
        
        info_geografica = empleado_servicio.obtener_info_geografica_empleado(empleado_id)
        
        self.input_estado_residente.setText(info_geografica[1])
        self.input_municipio.setText(info_geografica[2])
        self.input_direccion_residencia.setText(info_geografica[3])
        
        
        
        # Info contacto
        
        info_contacto = empleado_servicio.obtener_info_contacto_empleado(empleado_id)
            
            
            
        self.input_numero_de_telefono.setText(info_contacto[1])
        
        self.input_numero_de_telefono_adicional.setText("" if info_contacto[2] == None else info_contacto[2])
        
        self.input_correo_electronico.setText(info_contacto[3])
        
        self.input_correo_electronico_adicional.setText("" if info_contacto[4] == None else info_contacto[4])
        



        
        
        
        
        # Info laboral
        
        info_laboral = info_laboral_servicio.obtener_info_laboral_por_empleado_id(empleado_id)
        
        if info_laboral != None:
            
            self.input_codigo_por_donde_cobra.setText(info_laboral[4])
            self.input_institucion_donde_laboral.setText(info_laboral[5])
            
        else:
            
            pass
            
        # detalles del cargo
        
        info_detalles_cargo = detalle_cargo_servicio.obtener_detalles_cargo(empleado_id)
        #(2, '100000C', 'BACHILLER CONTRATADO', 'SUB-DIRECTOR ENCARGADO', 'ADMINISTRATIVO', 'BACHILLER', 'Hacer tal cosa', '2025-09-06', '2007-07-19', 18, None)
        
        #print("Informacion detalles del cargo ",info_detalles_cargo)
        self.boton_de_cargos.setCurrentText(info_detalles_cargo[2])
        self.boton_funcion_cargos.setCurrentText(info_detalles_cargo[3])
        self.boton_tipo_de_cargo.setCurrentText(info_detalles_cargo[4])
        
        
        if info_detalles_cargo[4].lower() == "docente":
            
            self.boton_de_especialidad.setCurrentText(info_detalles_cargo[10])
            
        else: 
            
            pass
        
        self.input_titulo_del_cargo.setText(info_detalles_cargo[5])
        self.input_labores_que_realiza.setText(info_detalles_cargo[6])
        
        self.dateedit_fecha_ingreso_tela.setDate(QDate.fromString(info_detalles_cargo[7], 'yyyy-dd-MM'))
        self.dateedit_fecha_ingreso_ministerio.setDate(QDate.fromString(info_detalles_cargo[8], 'yyyy-dd-MM'))
        
        
            # Se coloca esto aqui de manera provicional, ya que hay un error cuando el empleado no tiene ni diagnostico ni enfermedad
        # no retorna ni un none o algo por el estilo, da un error
        
        
        
        try:
            # enfermedades
            
            self.lista_carrito_enfermedades = historial_enferm_cronicas_servicio.obtener_historial_enferm_cronica_por_empleado_id(empleado_id)

            #[(1, 1, 'Artritis'), (2, 1, 'Diabetes')]
            
            if self.lista_carrito_enfermedades:
            
                for enfermedad in self.lista_carrito_enfermedades:
                
                    self.agregar_elementos_a_la_vista_previa(self.ver_lista_enfermedades, self.lista_carrito_enfermedades, self.boton_enfermedades, enfermedad[2])
            
            else:

                pass
            
        except Exception as e:
            
            print("No tiene enfermedades")
            
        else:
            
            print("si tiene enfermedades") 
            
            
        try:
        
            # diagnosticos
            
            self.lista_carrito_diagnosticos = info_clinica_empleado_servicio.obtener_info_clinica_por_empleado_id(empleado_id)
            
            
            if self.lista_carrito_diagnosticos:
                
                for diagnostico in self.lista_carrito_diagnosticos:
                    
                    self.agregar_elementos_a_la_vista_previa(self.ver_lista_diagnostico, self.lista_carrito_diagnosticos, self.boton_diagnostico, diagnostico[2])
            
            else:

                pass
        
        
        except Exception as e:
            
            print("No tiene diagnosticos")
            
        else:
            
            print("Si tiene diagnostico")
        
        
        
    def confirmar_edicion_datos_empleados(self, empleado_id:int):
        
        
        """
        
            Este metodo sirve para confirmar todos los cambios que se hagan a la hora de editar
        
        """
        
        try:
            
            # info basica
                

            primer_nombre = self.input_primer_nombre.text().capitalize()
            segundo_nombre = self.comprobar_si_hay_valor(self.input_segundo_nombre)
            tercer_nombre = self.comprobar_si_hay_valor(self.input_tercer_nombre)
            apellido_paterno = self.input_apellido_paterno.text().capitalize()
            apellido_materno = self.comprobar_si_hay_valor(self.input_apellido_materno)
            cedula = self.input_cedula.text().capitalize()
            
            fecha_nacimiento = self.fecha_de_str_a_date(self.dateedit_fecha_nacimiento.text())


            if self.input_sexo_masculino.isChecked():
                sexo = "M"

            elif self.input_sexo_femenino.isChecked():
                sexo = "F"
                
            else:
                sexo = None


            if self.input_si.isChecked():
                tiene_hijos_menores = 1

            elif self.input_no.isChecked():
                tiene_hijos_menores = 0


            errores_info_basica = empleado_servicio.validar_info_basica_empleado(
                primer_nombre, segundo_nombre, tercer_nombre,
                apellido_paterno, apellido_materno,
                cedula, fecha_nacimiento, empleado_id
            )


            if errores_info_basica:
                self.area_de_scroll.verticalScrollBar().setValue(100)
                self.mostrar_errores_antes_de_guardar(errores_info_basica)
                return
            
            else:   
                

                    
                ## "Info medidas" que verifique si falta un campo requerido  ##

                talla_camisa =  self.input_talla_de_camisa.text().upper()
                talla_pantalon = self.input_talla_de_pantalon.text()
                talla_zapatos = self.input_talla_de_zapatos.text()

                if not(talla_pantalon):
                    talla_pantalon = None
                else:
                    talla_pantalon = int(talla_pantalon)
                    
                if not(talla_zapatos):
                    talla_zapatos = None
                else:
                    talla_zapatos = int(talla_zapatos)
                        
                        
                errores_medidas = empleado_servicio.validar_medidas_empleado(talla_camisa, talla_pantalon, talla_zapatos)

                if errores_medidas:
                    self.area_de_scroll.verticalScrollBar().setValue(300)
                    self.mostrar_errores_antes_de_guardar(errores_medidas)
                    return
                
                else:
                

                    ## info cgeografica" que verifique si falta un campo requerido  ##
                    

                    estado_reside = self.input_estado_residente.text()
                    municipio = self.input_municipio.text()
                    direccion_residencia = self.input_direccion_residencia.text()

                    errores_info_geografica = empleado_servicio.validar_info_geografica_empleado(
                                estado_reside, municipio,
                                direccion_residencia
                            )

                    if errores_info_geografica:
                        
                        self.area_de_scroll.verticalScrollBar().setValue(500)
                        self.mostrar_errores_antes_de_guardar(errores_info_geografica)
                        return

                    else:
                        
                    
                        ## "info contactos" que verifique si falta un campo requerido  ##
            
                        num_telefono = self.input_numero_de_telefono.text().strip()
                        num_telefono_adicional = self.comprobar_si_hay_valor(self.input_numero_de_telefono_adicional)
                        
                        correo_electronico = self.input_correo_electronico.text().strip()
                        correo_electronico_adicional = self.comprobar_si_hay_valor(self.input_correo_electronico_adicional)

                        errores_info_contacto = empleado_servicio.validar_info_contacto_empleado(num_telefono, num_telefono_adicional, 
                                                                                                correo_electronico, correo_electronico_adicional, empleado_id)

                        if errores_info_contacto:
                            #print(f"tlf 1: {num_telefono}| tlf 2 : {num_telefono_adicional}")
                            #print(f"correo 1: {correo_electronico} | correo 2: {correo_electronico_adicional}")
                            self.area_de_scroll.verticalScrollBar().setValue(700)
                            self.mostrar_errores_antes_de_guardar(errores_info_contacto)
                            return

                        else:



                            ## "info laboral" que verifique si falta un campo requerido  ##
                            
                            cod_depend_cobra = self.input_codigo_por_donde_cobra.text()
                            institucion_labora = self.input_institucion_donde_laboral.text()


                            errores_info_laboral = info_laboral_servicio.validar_campos_info_laboral(
                                            cod_depend_cobra, institucion_labora
                                        )

                            if errores_info_laboral:
                                self.area_de_scroll.verticalScrollBar().setValue(1500)
                                self.mostrar_errores_antes_de_guardar(errores_info_laboral)
                                return
                            
                            else:



                                ## "info detalle del cargo" que verifique si falta un campo requerido  ##
                                ## y que muestre un mensaje que de registro exitoso y que se vaya a la pantalla de vista previa del personal  ##

                                fecha_ingreso_institucion = self.fecha_de_str_a_date(self.dateedit_fecha_ingreso_tela.text())  # Por defecto se establece la fecha actual

                                fecha_ingreso_ministerio = self.fecha_de_str_a_date(self.dateedit_fecha_ingreso_ministerio.text())
                                

                                situacion = "Activo"  # Por defecto es Activo

                                titulo_cargo = self.input_titulo_del_cargo.text()
                                
                                labores_cargo = self.input_labores_que_realiza.text()
                                
                                
                                #cargo_id, funcion_cargo_id, tipo_cargo_id, especialidad_id = 1,1,1,1
                                #funcion_cargo_id, tipo_cargo_id, especialidad_id = 1,1,1

                                # buscamos el id de la lista cargo del boton seleccionado
                                cargo_id = self.buscar_id_de_la_lista_del_combobox(self.boton_de_cargos, lista_cargo, 2, 0)

                                # buscamos el id de la lista de la funcion del cargo del boton seleccionado
                                funcion_cargo_id = self.buscar_id_de_la_lista_del_combobox(self.boton_funcion_cargos, lista_funcion_cargo, 1, 0)

                                # buscamos el id en la lista del tipo de cargo del boton seleccionado 
                                tipo_cargo_id = self.buscar_id_de_la_lista_del_combobox(self.boton_tipo_de_cargo, lista_tipo_cargo, 1, 0)
                            
                                
                                #especialidad_id = None
                                
                                # si esta habilitado
                                if self.boton_de_especialidad.isEnabled() and not self.boton_de_especialidad.currentIndex() == 0: 
                                                
                                    if self.boton_tipo_de_cargo.currentText().lower() == "docente":
                                    
                                        
                                        especialidad_id = self.buscar_id_de_la_lista_del_combobox(self.boton_de_especialidad, lista_especialidades,1, 0)
                                        print(especialidad_id)
                                    
                                    elif self.boton_tipo_de_cargo.currentText().lower() == "docente" and  self.boton_de_especialidad.currentIndex() == 0:
                                        
                                        QMessageBox.warning(self, "Aviso", "Si es docente eliga una especialidad")
                                        return
                                else:
                                    
                                    
                                    especialidad_id = None
                                    
                                    
                                
                                errores_detalle_cargo = detalle_cargo_servicio.validar_detalles_cargo(
                                                    cargo_id, funcion_cargo_id,
                                                    tipo_cargo_id, titulo_cargo,
                                                    labores_cargo, fecha_ingreso_ministerio
                                                )

                                if errores_detalle_cargo:
                                    self.mostrar_errores_antes_de_guardar(errores_detalle_cargo)
                                    return

                                
                                
                                else:
                                    
                                    self.msg_box.setWindowTitle("Confirmar edición")
                                    self.msg_box.setText("¿Seguro que quiere editar la información del empleado?")
                                    self.msg_box.setIcon(QMessageBox.Question)
                                    QApplication.beep()

                                    # Mostrar el cuadro de diálogo y esperar respuesta
                                    self.msg_box.exec_()  
                                    
                                    if self.msg_box.clickedButton() == self.boton_si:
                                        
                                        try:
                                            # esto es para ver si los datos se guardan y mostrarlos por consola
                                            

                                            campos_empleado = {
                                                "cedula": cedula,
                                                "primer_nombre": primer_nombre,
                                                "segundo_nombre": segundo_nombre,
                                                "tercer_nombre": tercer_nombre,
                                                "apellido_paterno": apellido_paterno,
                                                "apellido_materno": apellido_materno,
                                                "fecha_nacimiento": fecha_nacimiento,
                                                "sexo": sexo,
                                                "tiene_hijos_menores": tiene_hijos_menores,
                                                "fecha_ingreso_institucion": fecha_ingreso_institucion,
                                                "fecha_ingreso_ministerio": fecha_ingreso_ministerio,
                                                "talla_camisa": talla_camisa,
                                                "talla_pantalon": talla_pantalon,
                                                "talla_zapatos": talla_zapatos,
                                                "num_telefono": num_telefono,
                                                "num_telefono_adicional": num_telefono_adicional,
                                                "correo_electronico": correo_electronico,
                                                "correo_electronico_adicional": correo_electronico_adicional,
                                                "estado_reside": estado_reside,
                                                "municipio": municipio,
                                                "direccion_residencia": direccion_residencia,
                                                "situacion": situacion
                                            }

                                            
                                            # Actualizamos los datos de info basica del empleado
                                            empleado_servicio.actualizar_empleado(empleado_id, campos_empleado)

                                            
                                            
                                            campos_info_laboral = {
                                                "cod_depend_cobra": cod_depend_cobra,
                                                "institucion_labora": institucion_labora
                                            }
                                            
                                            info_laboral_servicio.actualizar_info_laboral(empleado_id, campos_info_laboral)

                                            campos_detalle_cargo = {
                                                "cargo_id": cargo_id,
                                                "funcion_cargo_id": funcion_cargo_id,
                                                "especialidad_id": especialidad_id,
                                                "tipo_cargo_id": tipo_cargo_id,
                                                "titulo_cargo": titulo_cargo,
                                                "labores_cargo": labores_cargo
                                            }
                                            

                                            
                                            detalle_cargo_servicio.actualizar_detalle_cargo(empleado_id, campos_detalle_cargo)

                                            
                                            
                                            
                                            
                                            # Acá con esto es para más adelante comprobar que si
                                            # Si la lista de diagnosticos o la lista de enfermedades crónicas
                                            # no está vacía entonces se hace el proceso de asociar el empleado con sus enfermedades o discapacidades
                                            # en caso de que alguna esté vacía entonces ese registro en concreto (por ejemplo, si la de discapaciades
                                            # está vacía) no se hace
                                            """
                                            
                                                
                                            campos_info_clinica_empleado = {
                                                "diagnostico_id": None
                                            }
                                            
                                            # declaramos el diccionario
                                            campos_historial_enferm_cronicas = {
                                                    "enferm_cronica_id": None
                                                }
                                            
                                            
                                            
                                            
                                            # se ve si la lista esta llena
                                            if self.lista_carrito_diagnosticos:
                                                
                                                # se itera cada diagnostico
                                                for diagnostico in self.lista_carrito_diagnosticos:
                                                    
                                                    diagnostico_id = diagnostico[0]
                                                            
                                                    campos_info_clinica_empleado["diagnostico_id"] = diagnostico_id
                                                
                                                    info_clinica_empleado_servicio.actualizar_info_clinica(empleado_id, campos_info_clinica_empleado)

                                                
                                            
                                            
                                                    
                                                
                                            if self.lista_carrito_enfermedades:
                                                
                                                for enfermedad in self.lista_carrito_enfermedades:
                                                    
                                                        
                                                        
                                                    enferm_cronica_id = enfermedad[0]
                                                    
                                                    campos_historial_enferm_cronicas["enferm_cronica_id"] = enferm_cronica_id
                                                    
                                                    historial_enferm_cronicas_servicio.actualizar_historial_enferm_cronica(empleado_id, campos_historial_enferm_cronicas)

                                                                
                                            else:
                                                
                                                pass
                                                                    
                                                
                                            
                                            
                                            """
                                            


                                            pantalla_tabla = self.stacked_widget.widget(7)
                                            
                                            pantalla_tabla.actualizar_tabla(tipo_cargo_id= 1, especialidad_id= None, indice_cedula= 1, indice_1er_nombre= 2, indice_2do_nombre= 3,
                                                                            indice_1er_apellido=5, indice_2do_apellido= 6, indice_estado= 8)
                                            
                                            pantalla_tabla.actualizar_lista_busqueda()
                                            
                                            pantalla_tabla.boton_de_opciones.setCurrentIndex(0)
                                        
                                            


                                            FuncionSistema.limpiar_inputs_de_qt(self.lista_qlineedit, self.lista_qradiobutton, self.lista_qcombobox)
                                            
                                            
                                            self.dateedit_fecha_nacimiento.setDate(QtCore.QDate(2000, 1, 1))
                                            self.dateedit_fecha_ingreso_ministerio.setDate(QtCore.QDate(2000, 1, 1))



                                        except Exception as e:

                                            QMessageBox.information(self, "No se pudo", f"{str(e)}")
                                            return
                                            

                                        else:
                                            
                                            print("registro exitoso")
                                        
                                        
                                    if self.msg_box.clickedButton() == self.boton_no:
                                        
                                        return


                                
        except Exception as e:
            
            FuncionSistema.mostrar_errores_por_excepcion(e, "Confirmar_edidcion_empleados")
            
        
        else:
            
            QMessageBox.information(self, "Proceso exitoso", "Se realizo la edicion correctamente")
            self.stacked_widget.setCurrentIndex(7)
    
                            
        
        

    ## Metodos para  salir del formulario ##
    def salir_del_formulario_empleado(self):

        
        ##  Creamos una ventana emergente para preguntar si de verdad se quiere salir ##
        
        
        self.msg_box.setWindowTitle("Confirmar salida")
        self.msg_box.setText("¿Seguro que quiere salir sin registrar?")
        self.msg_box.setIcon(QMessageBox.Question)
        QApplication.beep()

        # Mostrar el cuadro de diálogo y esperar respuesta
        self.msg_box.exec_()

        # Determinar qué botón fue presionado

        # si el boton pulsado es "si" se regresa y borra todo el registro
        if self.msg_box.clickedButton() == self.boton_si:
            
            FuncionSistema.limpiar_inputs_de_qt(self.lista_qlineedit, self.lista_qradiobutton, self.lista_qcombobox)
            

            self.dateedit_fecha_nacimiento.setDate(QtCore.QDate(2000, 1, 1))
            self.dateedit_fecha_ingreso_ministerio.setDate(QtCore.QDate(2000, 1, 1))


            self.stacked_widget.setCurrentIndex(7)

        ## si el boton "no" es pulsadoo, no pasa nada #3
        elif self.msg_box.clickedButton() == self.boton_no:
            pass











########################################################################################################################






