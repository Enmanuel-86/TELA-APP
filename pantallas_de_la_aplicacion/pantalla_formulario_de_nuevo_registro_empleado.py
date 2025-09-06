from datetime import datetime
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QIntValidator
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QIcon
import traceback
import os
from PyQt5.QtWidgets import (QWidget, QCalendarWidget, QFrame,
                             QStackedWidget, QMessageBox,QListWidgetItem,
                             QLabel, QHBoxLayout,
                             QPushButton, QApplication)

from elementos_graficos_a_py import Ui_PantallaFormularioEmpleado


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
        
        # Inicialización de variables 
        self.calendario = None  # Usa 'calendario' en todo el código
        self.current_label = None

        
        ## Rutas relativas para las imagenes ##
        self.boton_de_regreso.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "flecha_izquierda_2.png")))
        self.foto_anadir_personal.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "registro_personal.png")))
        self.boton_para_agregar_fecha.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "calendario.png")))
        self.boton_fecha_de_ingreso_tela.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "calendario.png")))
        self.boton_anadir_diagnostico.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "circulo_mas.png")))
        self.boton_anadir_enfermedad.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "circulo_mas.png")))
        self.boton_para_agregar_fecha_de_ingreso_del_minis.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "calendario.png")))

        ###############################################################################################################
        # Detalles para los inputs info basica #
        ## aqui ponemos que el campo de cedula solo pida numeros ##
        self.input_cedula.setValidator(QRegExpValidator(QRegExp("[0-9]{12}")))


        ###############################################################################################################
        # Detalles para los inputs info medidas #
        
        self.input_talla_de_pantalon.setValidator(QIntValidator())
        self.input_talla_de_zapatos.setValidator(QIntValidator())
        
        ###############################################################################################################
        # Detalles para los input info contactos #
        
        self.input_numero_de_telefono.setMaxLength(12)
        
        
        
        ###############################################################################################################
        # Detalles para info medica #
        
        # lista de las base de datos
        self.lista_diagnostico = diagnostico_servicio.obtener_todos_diagnosticos()       
        self.lista_enfermedades = enfermedad_cronica_servicio.obtener_todos_enfermedades_cronicas()



        # cargar catalogo de enfermedades
        self.cargar_lista_para_el_combobox(self.lista_enfermedades, self.boton_enfermedades, 1)
         
        # cargar catalogo de diagnosticos
        self.cargar_lista_para_el_combobox(self.lista_diagnostico ,self.boton_diagnostico, 1)

        # listas carrito
        self.lista_de_enfermedades = []
        self.lista_de_diagnosticos = []

        

        self.boton_anadir_enfermedad.clicked.connect(self.anadir_enfermedad)
        self.boton_anadir_diagnostico.clicked.connect(self.anadir_diagnostico)

        ###############################################################################################################
        # Detalles para detalles de cargo
        today = datetime.now()
        dia_de_hoy = today.strftime("%Y-%m-%d")
        self.label_mostrar_fecha_de_ingreso_tela.setText(dia_de_hoy)
        self.input_labores_que_realiza.clear()
        
        # Cargamos al boton la lista de los cargos
        self.cargar_lista_para_el_combobox(lista_cargo, self.boton_de_cargos, 2)

        # Cargando al boton la lista de tipo de cargo
        self.cargar_lista_para_el_combobox(lista_tipo_cargo, self.boton_tipo_de_cargo, 1)

        # Cargando al boton la lista de funcion de cargo
        self.cargar_lista_para_el_combobox(lista_funcion_cargo, self.boton_funcion_cargos, 1)

        # Cargamos al boton la lista de especialidades
        self.cargar_lista_para_el_combobox(lista_especialidades, self.boton_de_especialidad, 1)
        
        self.boton_de_especialidad.setEnabled(False)
        
        self.boton_tipo_de_cargo.currentIndexChanged.connect(self.habilitar_boton_especialidades)





        
        
        ###############################################################################################################
        ## Boton de siguiente para ir cambiando las preguntas ##
        self.boton_finalizar.clicked.connect(self.guardar_informacion_empleado)
        
        self.boton_para_agregar_fecha.clicked.connect(lambda: self.mostrar_calendario(self.label_mostrar_fecha))
        
        
        

        ## Boton de regreso para retroceder a la pregunta previa o salir del formulario ##
        self.boton_de_regreso.clicked.connect(self.salir_del_formulario_empleado)
        
        # Conexión CORRECTA del botón (usa lambda sin llamar a la función)
        self.boton_fecha_de_ingreso_tela.clicked.connect(
            lambda: self.mostrar_calendario(self.label_mostrar_fecha_de_ingreso_tela)
        )
        self.boton_para_agregar_fecha_de_ingreso_del_minis.clicked.connect(
            lambda: self.mostrar_calendario(self.label_mostrar_fecha_de_ingreso_del_minis)
        )
        
        
        ### Esto es de prueba, esto asigna un valor a los input
        
        """
        self.input_primer_nombre.setText("Ligia")
        self.input_apellido_paterno.setText("Garcia")
        self.input_cedula.setText("24345231")
        self.input_sexo_femenino.setChecked(True)
        self.input_si.setChecked(True)
        self.label_mostrar_fecha.setText("2000-03-02")
        
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
    
    
    ## Metodo para mostrar el calendario ##
    def mostrar_calendario(self, label_destino):
        
        ## Metodo para colocar la fecha a un label  ##
        def seleccionar_fecha(date):
            """Actualiza el label con la fecha seleccionada y cierra el calendario."""
            if self.current_label:
                fecha_formateada = date.toString("yyyy-MM-dd")
                fecha_date = datetime.strptime(fecha_formateada, "%Y-%m-%d").date()
                self.current_label.setText(f"{fecha_date}")
                #print(type(fecha_date))
                self.calendario.close()  # Cerrar el calendario (¡nombre correcto!)


        
        
        
        
        """Muestra el calendario y asigna el label objetivo."""
        if not self.calendario:
            # Crear el calendario solo una vez
            self.calendario = QCalendarWidget(self)
            self.calendario.setGridVisible(True)
            self.calendario.clicked.connect(seleccionar_fecha)
            self.calendario.setWindowTitle("Seleccione una fecha")
            self.calendario.setFixedSize(400, 300)

        self.current_label = label_destino  # Guardar el label a actualizar
        self.calendario.move(
            (self.width() - self.calendario.width()) // 2,
            (self.height() - self.calendario.height()) // 2
        )
        self.calendario.show()

    
    ## Metodo para añadir una enfermedad al "carrito"
    def anadir_enfermedad(self):

        enfermedad = None
        
            
        if self.boton_enfermedades.currentText() and not self.boton_enfermedades.currentIndex() == 0:
            
            enfermedad = self.boton_enfermedades.currentText()
            self.lista_de_enfermedades.append(enfermedad)
        
            
        elif self.input_otra_enfermedad.text():
            
            enfermedad = self.input_otra_enfermedad.text()
            self.lista_de_enfermedades.append(enfermedad)
            
            nueva_enfermedad = {"enfermedad_cronica": enfermedad.capitalize()}
            
            enfermedad_cronica_servicio.registrar_enfermedad_cronica(nueva_enfermedad)
            
            #self.boton_enfermedades.addItem(enfermedad)
            
            
            print(self.lista_enfermedades)
            
        
        else:
            return
        
        


    ## Metodo para añadir un diagnostico al "carrito"
    def anadir_diagnostico(self):

        diagnostico = None
        
        # si el combo box tiene texto y no el indice del mismo no el 0
        if self.boton_diagnostico.currentText() and not self.boton_diagnostico.currentIndex() == 0:
            
            diagnostico = self.boton_diagnostico.currentText()
            
            self.lista_de_diagnosticos.append(diagnostico)

            self.agregar_elementos_a_la_vista_previa(self.ver_lista_diagnostico, self.lista_de_diagnosticos, self.boton_diagnostico, diagnostico)

        
            
        elif self.input_otro_diagnostico.text().strip():
            
            diagnostico = self.input_otro_diagnostico.text().strip()
            self.lista_de_diagnosticos.append(diagnostico)
            self.agregar_elementos_a_la_vista_previa(self.ver_lista_diagnostico, self.lista_de_diagnosticos, self.boton_diagnostico ,diagnostico)

        
            nuevo_diagnostico = {"diagnostico": diagnostico}
            
            diagnostico_servicio.registrar_diagnostico(nuevo_diagnostico)
            
            #self.boton_diagnostico.addItem(diagnostico)
            
            
            
            #print(lista_diagnostico)
        
        else:
            return
        
    
       
        

       
        
        # Limpiar el QLineEdit después de añadir
        self.input_otro_diagnostico.clear()
        self.boton_diagnostico.setCurrentIndex(0)
        print(self.lista_de_diagnosticos)


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
    def buscar_id_de_la_lista_del_combobox(self, boton_seleccionado, lista_elementos, indice_nombre_del_elemento, indice_id_del_elemento):
            
        seleccion = boton_seleccionado.currentText()

        
        
        if  seleccion and not boton_seleccionado.currentIndex() == 0:
            
            for elemento in lista_elementos:
                
                if seleccion.upper() == elemento[indice_nombre_del_elemento] or seleccion.lower() == elemento[indice_nombre_del_elemento] or seleccion.capitalize() == elemento[indice_nombre_del_elemento]:
                    
                    id_del_elemento = elemento[indice_id_del_elemento]  
                    
                    id_del_elemento = int(id_del_elemento)
                    
                    return id_del_elemento
                    
                        
                else:
                    pass   

        
        else:
            
            
            pass

    
    # Metodo para agregar elementos a la vista previa de los diagnosticos
    def fecha_de_str_a_date(self, fecha_string):
        
        # Convertir el string a objeto date
        try:
            fecha_date = datetime.strptime(fecha_string, "%Y-%m-%d").date()
            
            return fecha_date
            #print(type(fecha_nacimiento))
        except ValueError as e:
            print(f"Error al convertir la fecha: {e}")
    
    # Metodo para mostrar errores de la base de datos 
    def mostrar_errores_antes_de_guardar(self, errores):
        
        error_msg = "Lista de errores:\n"
        error_msg += "\n".join(f"- {field.capitalize()}" for field in errores)
        QMessageBox.critical(self, "Errores", error_msg)
        print("\n".join(errores))
        return
    
    
    ## Metodo para guardar todas las preguntas en la bd ##
    def guardar_informacion_empleado(self):

        

        global primer_nombre, segundo_nombre, apellido_paterno, tiene_hijos_menores, talla_camisa, sexo, talla_pantalon, fecha_nacimiento, apellido_materno, municipio, estado_reside, num_telefono, enferm_cronica_id, correo_electronico, diagnostico_id, funcion_cargo, institucion_labora, direccion_residencia, talla_zapatos, cod_depend_cobra, campos_info_clinica_empleado, campos_historial_enferm_cronicas, cedula


        
            
        try:    
            
            # info basica
            fecha_nacimiento = 0

            primer_nombre = self.input_primer_nombre.text()
            segundo_nombre = self.input_segundo_nombre.text()
            apellido_paterno = self.input_apellido_paterno.text()
            apellido_materno = self.input_apellido_materno.text()
            cedula = self.input_cedula.text()
            
            fecha_nacimiento = self.fecha_de_str_a_date(self.label_mostrar_fecha.text())


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
                primer_nombre, segundo_nombre,
                apellido_paterno, apellido_materno,
                cedula, fecha_nacimiento
            )

            if errores_info_basica:
                self.area_de_scroll.verticalScrollBar().setValue(100)
                self.mostrar_errores_antes_de_guardar(errores_info_basica)
                return
                
                



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
            

            num_telefono = self.input_numero_de_telefono.text()
            correo_electronico = self.input_correo_electronico.text()

            errores_info_contacto = empleado_servicio.validar_info_contacto_empleado(num_telefono, correo_electronico)

            if errores_info_contacto:
                self.area_de_scroll.verticalScrollBar().setValue(700)
                self.mostrar_errores_antes_de_guardar(errores_info_contacto)
                return



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








            ## "info detalle del cargo" que verifique si falta un campo requerido  ##
            ## y que muestre un mensaje que de registro exitoso y que se vaya a la pantalla de vista previa del personal  ##
            
            
            

            #cargo_id = None
            #funcion_cargo_id = None
            #tipo_cargo_id = None
            
            labores_cargo = self.input_labores_que_realiza.text()

            fecha_ingreso_institucion = None  # Por defecto se establece la fecha actual

            fecha_ingreso_ministerio = self.fecha_de_str_a_date(self.label_mostrar_fecha_de_ingreso_del_minis.text())
            

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
        
        
            
            
            if especialidad_id == None:
                
                # buscamos el id de la especialidad que esta en la lista del boton 
                especialidad_id = self.buscar_id_de_la_lista_del_combobox(self.boton_de_especialidad, lista_especialidades, 1, 0)

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


            print(f" cargo: {cargo_id}\n funcion de cargo: {funcion_cargo_id}\n tipo de cargo: {tipo_cargo_id}\n especialidad: {especialidad_id}")



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
                    "correo_electronico": correo_electronico,
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
                if self.lista_de_diagnosticos:
                    
                    # se itera cada diagnostico
                    for diagnostico in self.lista_de_diagnosticos:
                        
                        for id_diagnostico, nombre_diagnostico in self.lista_diagnostico:
                            
                            
                            if diagnostico == nombre_diagnostico:
                                
                                diagnostico_id = id_diagnostico
                                
                                campos_info_clinica_empleado["diagnostico_id"] = diagnostico_id
                            
                                info_clinica_empleado_servicio.registrar_info_clinica_empleado(campos_info_clinica_empleado)

                    
                else:
                    pass
                    
                    
                
                        
                    
                if self.lista_de_enfermedades:
                    
                    for enfermedad in self.lista_de_enfermedades:
                        
                            for id_enfermedad, nombre_enfermedad in self.lista_enfermedades:
                                
                                if enfermedad == nombre_enfermedad:
                                    
                                    enferm_cronica_id = id_enfermedad
                                    
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


                pantalla_tabla = self.stacked_widget.widget(2)
                
                pantalla_tabla.actualizar_tabla(tipo_cargo_id= 1, especialidad_id= None, indice_cedula= 1, indice_1er_nombre= 2, indice_2do_nombre= 3,
                                                   indice_1er_apellido= 4, indice_2do_apellido= 5, indice_estado= 7)
                pantalla_tabla.actualizar_lista_busqueda()
                pantalla_tabla.boton_de_opciones.setCurrentIndex(0)
            
                self.stacked_widget.setCurrentIndex(2)


                ## Borrar todo lo que esta en el formulario 1 info basica ##
                self.input_primer_nombre.clear()
                self.input_segundo_nombre.clear()
                self.input_apellido_paterno.clear()
                self.input_apellido_materno.clear()
                self.input_cedula.clear()
                self.label_mostrar_fecha.clear()
                # Desactivar temporalmente la auto-exclusividad
                self.input_sexo_masculino.setAutoExclusive(False)
                self.input_sexo_femenino.setAutoExclusive(False)

                # Desmarcar ambos
                self.input_sexo_masculino.setChecked(False)
                self.input_sexo_femenino.setChecked(False)

                # Reactivar la auto-exclusividad (comportamiento normal)
                self.input_sexo_masculino.setAutoExclusive(True)
                self.input_sexo_femenino.setAutoExclusive(True)

                # Desactivar temporalmente la auto-exclusividad
                self.input_si.setAutoExclusive(False)
                self.input_no.setAutoExclusive(False)

                # Desmarcar ambos
                self.input_si.setChecked(False)
                self.input_no.setChecked(False)

                # Reactivar la auto-exclusividad (comportamiento normal)
                self.input_si.setAutoExclusive(True)
                self.input_no.setAutoExclusive(True)

                ## Borrar todo lo del formulario 2 info medidas ##

                self.input_talla_de_camisa.clear()
                self.input_talla_de_zapatos.clear()
                self.input_talla_de_pantalon.clear()


                ## Borrar todo lo del formulario 4 info geografica  ##

                self.input_municipio.clear()
                self.input_estado_residente.clear()
                self.input_direccion_residencia.clear()

                ## Borrar todo lo del formulario 5 info de contacto  ##

                self.input_numero_de_telefono.clear()
                self.input_correo_electronico.clear()

                ## Borrar todo lo del formulario 7 info del cargo ##

                self.input_institucion_donde_laboral.clear()
                self.input_codigo_por_donde_cobra.clear()



            except Exception as e:

                QMessageBox.information(self, "No se pudo", f"{str(e)}")
                return
                #self.cambio.setCurrentIndex(0)
                #self.stacked_widget.setCurrentIndex(2)

            else:
                
                print("registro exitoso")
                
        except Exception as e:
            
            # Obtener el traceback completo como string
            error_traceback = traceback.format_exc()
        
            # Mostrar en consola (para depuración)
            print("\n\nError en la línea:", traceback.extract_tb(e.__traceback__)[-1].lineno)
            print("Traceback completo:\n", error_traceback)
            
            print(f"error en un segmento: {e}")
            
        else:
            
            print("libre de errores")
     


    




    ## Metodos para  salir del formulario ##
    def salir_del_formulario_empleado(self):

        
        ##  Creamos una ventana emergente para preguntar si de verdad se quiere salir ##
        QApplication.beep()
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirmar salida")
        msg_box.setText("¿Seguro que quiere salir sin registrar?")
        msg_box.setIcon(QMessageBox.Question)

        # Crear botones personalizados
        boton_si = msg_box.addButton("Sí", QMessageBox.YesRole)
        boton_no = msg_box.addButton("No", QMessageBox.NoRole)

        # Mostrar el cuadro de diálogo y esperar respuesta
        msg_box.exec_()

        # Determinar qué botón fue presionado

        # si el boton pulsado es "si" se regresa y borra todo el registro
        if msg_box.clickedButton() == boton_si:
            
            self.limpiar_diagnosticos()
            self.limpiar_enfermedades()
            ## Borrar todo lo que esta en el formulario 1 info basica ##
            self.input_primer_nombre.clear()
            self.input_segundo_nombre.clear()
            self.input_apellido_paterno.clear()
            self.input_apellido_materno.clear()
            self.input_cedula.clear()
            self.label_mostrar_fecha.clear()
            # Desactivar temporalmente la auto-exclusividad
            self.input_sexo_masculino.setAutoExclusive(False)
            self.input_sexo_femenino.setAutoExclusive(False)

            # Desmarcar ambos
            self.input_sexo_masculino.setChecked(False)
            self.input_sexo_femenino.setChecked(False)

            # Reactivar la auto-exclusividad (comportamiento normal)
            self.input_sexo_masculino.setAutoExclusive(True)
            self.input_sexo_femenino.setAutoExclusive(True)

            # Desactivar temporalmente la auto-exclusividad
            self.input_si.setAutoExclusive(False)
            self.input_no.setAutoExclusive(False)

            # Desmarcar ambos
            self.input_si.setChecked(False)
            self.input_no.setChecked(False)

            # Reactivar la auto-exclusividad (comportamiento normal)
            self.input_si.setAutoExclusive(True)
            self.input_no.setAutoExclusive(True)

            ## Borrar todo info medidas ##

            self.input_talla_de_camisa.clear()
            self.input_talla_de_zapatos.clear()
            self.input_talla_de_pantalon.clear()



        

            ## Borrar todo lo del formulario 4 info geografica  ##

            self.input_municipio.clear()
            self.input_estado_residente.clear()
            self.input_direccion_residencia.clear()

            ## Borrar todo  info de contacto  ##

            self.input_numero_de_telefono.clear()
            self.input_correo_electronico.clear()

        

            ##  info del cargo ##

            self.input_institucion_donde_laboral.clear()
            self.input_codigo_por_donde_cobra.clear()

            self.stacked_widget.setCurrentIndex(2)

        ## si el boton "no" es pulsadoo, no pasa nada #3
        elif msg_box.clickedButton() == boton_no:
            pass











########################################################################################################################






