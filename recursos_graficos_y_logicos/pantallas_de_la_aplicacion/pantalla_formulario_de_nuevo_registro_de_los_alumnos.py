from datetime import datetime, date
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate
import traceback
import os
from PyQt5.QtWidgets import (QWidget, QCalendarWidget, QListWidgetItem,
                             QStackedWidget, QMessageBox,
                             QLabel, QHBoxLayout,
                             QPushButton, QApplication)
from ..elementos_graficos_a_py import Ui_FormularioNuevoRegistroAlumnos
from ..utilidades.funciones_sistema import FuncionSistema
                                     
##################################
# importaciones de base de datos #
##################################

# Repositorios

from repositorios.alumnos.alumno_repositorio import AlumnoRepositorio
from repositorios.diagnosticos.diagnostico_repositorio import DiagnosticoRepositorio
from repositorios.alumnos.representante_repositorio import RepresentanteRepositorio
from repositorios.especialidades.especialidad_repositorio import EspecialidadRepositorio
from repositorios.alumnos.medidas_alumno_repositorio import MedidasAlumnoRepositorio
from repositorios.alumnos.info_clinica_alumno_repositorio import InfoClinicaAlumnoRepositorio
from repositorios.alumnos.info_bancaria_alumno_repositorio import InfoBancarioAlumnoRepositorio
from repositorios.alumnos.inscripcion_repositorio import InscripcionRepositorio

# Servicio

from servicios.alumnos.alumno_servicio import AlumnoServicio
from servicios.diagnosticos.diagnostico_servicio import DiagnosticoServicio
from servicios.alumnos.representante_servicio import RepresentanteServicio
from servicios.especialidades.especialidad_servicio import EspecialidadServicio
from servicios.alumnos.medidas_alumno_servicio import MedidasAlumnoServicio
from servicios.alumnos.info_clinica_alumno_servicio import InfoClinicaAlumnoServicio
from servicios.alumnos.info_bancaria_alumno_servicio import InfoBancariaAlumnoServicio
from servicios.alumnos.inscripcion_servicio import InscripcionServicio

##################################
# importaciones de base de datos #
##################################

# Instancia de los repositorios

alumno_repositorio = AlumnoRepositorio()

diagnostico_repositorio = DiagnosticoRepositorio()

representante_repositorio = RepresentanteRepositorio()

especialidad_repositorio = EspecialidadRepositorio()

medidas_alumno_repositorio = MedidasAlumnoRepositorio()

info_clinica_alumno_repositorio = InfoClinicaAlumnoRepositorio()

info_bancaria_alumno_repositorio = InfoBancarioAlumnoRepositorio()

inscripcion_repositorio = InscripcionRepositorio()

# Intancia de los servicio

alumno_servicio = AlumnoServicio(alumno_repositorio)

diagnostico_servicio = DiagnosticoServicio(diagnostico_repositorio)

representante_servicio = RepresentanteServicio(representante_repositorio)

especialidad_servicio = EspecialidadServicio(especialidad_repositorio)

medidas_alumno_servicio = MedidasAlumnoServicio(medidas_alumno_repositorio)

info_clinica_alumno_servicio = InfoClinicaAlumnoServicio(info_clinica_alumno_repositorio)

info_bancaria_alumno_servicio = InfoBancariaAlumnoServicio(info_bancaria_alumno_repositorio)

inscripcion_servicio = InscripcionServicio(inscripcion_repositorio)

# Lista de la bd





# Obtener el año actual
año_actual = datetime.now().year



class PantallaDeFormularioNuevoRegistroAlumnos(QWidget, Ui_FormularioNuevoRegistroAlumnos):
    def __init__(self, stacked_widget):
        super().__init__()


        self.stacked_widget = stacked_widget
        self.setupUi(self)
        
        ## Rutas relativas para las imagenes ##
        
        self.boton_de_regreso.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "flecha_izquierda_2.png")))
        self.boton_ayuda.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "signo_de_interrogacion.png")))
        self.boton_buscar_cedula_representante.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "lupa_de_busqueda.png")))
        self.boton_anadir_diagnostico.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "circulo_mas.png")))
        self.foto_anadir_alumno.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "registro_alumnos.png")))
        self.boton_anadir_otro_diagnostico.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "mas.png")))
        

        # lista de inputs para usarlo en el metodo de limpiar inputs,
        # en esta lista solo estan los inputs QLineEdit, QLabel y QListWidget
        self.lista_de_inputs = (
                                self.input_primer_nombre, self.input_segundo_nombre, self.input_apellido_paterno, self.input_apellido_materno,
                                self.input_cedula, self.input_relacion_con_representante, self.input_lugar_de_nacimiento,
                                self.input_situacion, self.input_escolaridad, self.input_procendencia, self.input_buscar_por_cedula,self.input_nombre_del_representante, 
                                self.input_apellido_del_representante, self.input_numero_de_telefono, self.input_estado_civil, self.input_carga_familiar, self.input_direccion_residencia,
                                self.input_talla_camisa, self.input_talla_pantalon, self.input_talla_zapatos, self.input_peso, self.input_estatura,
                                self.input_tipo_de_cuenta, self.input_numero_de_cuenta, self.vista_previa_cuentas_bancarias, self.input_otro_diagnostico,
                                self.input_medicacion, self.input_medico_tratante,  self.input_certificado_discapacidad,
                                self.vista_previa_diagnostico
                                )
        
        # esta lista es exclusiva de radiobuttons, aqui no hay ningun QLabel, QLineedit, nada de eso
        self.lista_de_radiobuttons = (
                                      self.input_sexo_masculino, self.input_sexo_femenino, self.input_cma_si, self.input_cma_no,
                                      self.input_imt_si, self.input_imt_no
                                        )
        
        
        # Se cargar la lista catalogo
        self.lista_especialidades = especialidad_servicio.obtener_todos_especialidades()
        self.lista_diagnostico = diagnostico_servicio.obtener_todos_diagnosticos()   
        
        
        # Message box para usarlos en cualquier lado
        self.msg_box = QMessageBox(self)
        
        # Crear botones personalizados
        self.boton_si = self.msg_box.addButton("Sí", QMessageBox.YesRole)
        self.boton_no = self.msg_box.addButton("No", QMessageBox.NoRole)


        
        
        # esta variable es para almacenar el id del representate para el registro del alumno
        self.representante_id = None
        self.representante_registrado = False
        self.comprobacion = False

        self.diagnostio_id = None

        
        # lista vacia para agrupar los diagnosticos de manera temporal
        
        self.lista_carrito_diagnosticos = []
        self.lista_carrito_cuentas_bancarias = []
        
        
        # periodo escolar
        self.label_mostrar_periodo_escolar.setText(str(año_actual) + "-" + str(año_actual + 1))
        
        
       
        
        # cargar catalogo de diagnosticos
        FuncionSistema.cargar_elementos_para_el_combobox(self.lista_diagnostico ,self.boton_diagnostico, 1,1)
        
        # cargar catalogos de las especialidades
        FuncionSistema.cargar_elementos_para_el_combobox(self.lista_especialidades, self.boton_de_especialidad, 1,1)
        
        
        
        today = datetime.now()
        dia_de_hoy = today.strftime("%Y-%m-%d")
        
        self.dateedit_fecha_ingreso_tela.setDate(QDate.currentDate())
        self.dateedit_fecha_ingreso_especialidad.setDate(QDate.currentDate())
        
        
        self.boton_buscar_cedula_representante.clicked.connect(self.comprobar_representante_registrado)
        
        self.boton_anadir_cuenta_banco.clicked.connect(self.anadir_cuentas_bancarias_alumno)
        
        self.boton_anadir_diagnostico.clicked.connect(self.anadir_diagnosticos_alumno_a_lista)
        
        self.boton_anadir_otro_diagnostico.clicked.connect(self.anadir_otro_diagnotico_diferente)
        
        self.boton_finalizar.clicked.connect(self.guardar_informacion_alumno)
        
        self.boton_de_regreso.clicked.connect(self.salir_del_formulario_alumno)
        
        
        # esto es para hacer pruebas  para no ingresar datos a cada rato
        # NOTA: lo pueden cambiar
        
        # Datos insertados desde los inputs
        # si no los va a usar comentelos con """"""
        
        """
        
        # info alumno
        
        self.input_primer_nombre.setText("jario")
        
        self.input_segundo_nombre.setText("Jose")
        self.input_apellido_paterno.setText("Merida")
        self.input_apellido_materno.setText("Lopez")
        self.input_cedula.setText("40199022")
        self.input_relacion_con_representante.setText("hijo")
        self.input_sexo_masculino.setChecked(True)
        
        self.input_cma_no.setChecked(True)
        self.input_imt_si.setChecked(True)
        self.input_lugar_de_nacimiento.setText("barcelona")
        self.input_situacion.setText("Inicial")
        
        # info representante no los voy a colocar, es para comprobar si se asocian al alumno
        
        # info cuenta de banco, como es opcional no los voy a llenar por aqui
        
        
        # info medidas
        self.input_talla_camisa.setText("M")
        self.input_talla_pantalon.setText("32")
        self.input_talla_zapatos.setText("32")
        self.input_peso.setText("60")
        self.input_estatura.setText("170")
        
        # info escolaridad
        
        self.input_escolaridad.setText("Ninguna")
        self.input_procendencia.setText("U E Escuela de arte")
        
    
    
    
        
        """
        
        
    def actualizar_listas_catalogo(self):
        
        """
            Este metodo es para actualizar las listas de los catalogos y a su vez actualizar los comboboxes
            
            este metodo se utilizara unicamente en la pantalla de registrar elementos catalogos
            
            actualiza los combobox ya que son las listas que se usan para cargar los comboboxes
        
        """    
    
        self.lista_especialidades = especialidad_servicio.obtener_todos_especialidades()
        self.lista_diagnostico = diagnostico_servicio.obtener_todos_diagnosticos()
        
        
        self.boton_de_especialidad.clear()
        self.boton_diagnostico.clear()
        
        # cargar catalogo de diagnosticos
        FuncionSistema.cargar_elementos_para_el_combobox(self.lista_diagnostico ,self.boton_diagnostico, 1,1)
        
        # cargar catalogos de las especialidades
        FuncionSistema.cargar_elementos_para_el_combobox(self.lista_especialidades, self.boton_de_especialidad, 1,1)
          
            
            
    

            
    # Metodo para buscar el id que esta en la tupla de la lista que arroja la base de datos
    def buscar_id_de_la_lista_del_combobox(self, boton_seleccionado, lista_elementos, indice_nombre_del_elemento, indice_id_del_elemento):
            
        seleccion = boton_seleccionado.currentText()

        
        
        if  seleccion and not boton_seleccionado.currentIndex() == 0:
            
            for elemento in lista_elementos:
                
                if seleccion == elemento[indice_nombre_del_elemento]:
                    
                    id_del_elemento = elemento[indice_id_del_elemento]  
                    
                    id_del_elemento = int(id_del_elemento)
                    
                    return id_del_elemento
                    
                        
                else:
                    pass   

        
        else:
            
            
            pass

            
            
    
        
        
    # Metodo para comprobar que el representante esta registrado o no, para evitar redundancia/no repetir los datos
    def comprobar_representante_registrado(self):
        
        """
            Este metodo sirve para comprobar si el representante esta registrado en la base de datos usando su cedula
            
            Si esta registrado: Se asocia con el alumno con quien se va a registrar
            
            Si no esta registrado: Se registra el representante
        
        """
        
        cedula_representante = self.input_buscar_por_cedula.text().strip()
        
        
        try:
            
            # comprobamos si el input de cedula tiene valor/texto
            if cedula_representante:
                
                # si lo tiene, que busque al representante
                # si el representante esta registrado
                if representante_servicio.obtener_representante_por_cedula(cedula_representante):
                    
                    # este booleano es para comprobar mejor que ya esta el representante
                    self.representante_registrado = True
                    
                    datos_representante = representante_servicio.obtener_representante_por_cedula(cedula_representante)
                    
                    # obtenemos todos los datos 
                    nombre_representante = datos_representante[2]
                    apellido_representante = datos_representante[3]
                    num_telefono_representante = datos_representante[5]
                    
                    
                    if datos_representante[6] == None:
                        self.input_numero_de_telefono_adicional.setText("No posee")
                    else:
                        self.input_numero_de_telefono_adicional.setText(datos_representante[6])
                    
                    
                    carga_familiar_representante = datos_representante[7]
                    carga_familiar_representante = str(carga_familiar_representante)
                    direccion_residencia_representante = datos_representante[4]
                    estado_civil_representante = datos_representante[8]
                    
                    representante_id_retornado = datos_representante[0]
                    
                    # guardamos el ID del representante en una variable para usar lo a parte
                    self.representante_id = representante_id_retornado
                    
                    print(self.representante_id)
                    
                    # mostramos los datos en los campos
                    self.input_nombre_del_representante.setText(nombre_representante)
                    self.input_apellido_del_representante.setText(apellido_representante)
                    self.input_numero_de_telefono.setText(num_telefono_representante)
                    self.input_carga_familiar.setText(carga_familiar_representante)
                    self.input_direccion_residencia.setText(direccion_residencia_representante)
                    self.input_estado_civil.setText(estado_civil_representante)
                    
                    # deshabilitamos los campos
                    self.input_nombre_del_representante.setDisabled(True)
                    self.input_apellido_del_representante.setDisabled(True)
                    self.input_carga_familiar.setDisabled(True)
                    self.input_direccion_residencia.setDisabled(True)
                    self.input_numero_de_telefono.setDisabled(True)
                    self.input_numero_de_telefono_adicional.setDisabled(True)
                    self.input_estado_civil.setDisabled(True)
                    
                    # mostramos mensaje en pantalla
                    QMessageBox.information(self, "Aviso", "este representante ya esta registrado")                    
                
                
                # si no esta el representante que registre uno nuevo
                else:
                    
                    self.representante_registrado = False
                    
                    # habilitamos los campos
                    self.input_nombre_del_representante.setEnabled(True)
                    self.input_apellido_del_representante.setEnabled(True)
                    self.input_carga_familiar.setEnabled(True)
                    self.input_direccion_residencia.setEnabled(True)
                    self.input_numero_de_telefono.setEnabled(True)
                    self.input_numero_de_telefono_adicional.setEnabled(True)
                    self.input_estado_civil.setEnabled(True)
                    
                    # limpiamos los campos
                    self.input_nombre_del_representante.clear()
                    self.input_apellido_del_representante.clear()
                    self.input_carga_familiar.clear()
                    self.input_direccion_residencia.clear()
                    self.input_numero_de_telefono.clear()
                    self.input_numero_de_telefono_adicional.clear()
                    self.input_estado_civil.clear()
                    
                    # mostramos el mensaje
                    QMessageBox.information(self, "Alerta", "Este representante no esta registrado, por favor\nllene los datos de este segmento")
            
            else:
                
                QMessageBox.information(self, "Alerta", "El campo ( cedula del representante ) esta vacio")

                
            self.comprobacion = True    

            return self.comprobacion
        
        except Exception as e:
            
            self.mostrar_errores_por_excepcion(e)
    
    


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
        
    
    # Metodo para agregar otro diagnostico que no esta en la lista catalogo de los diagnosticos
    def anadir_otro_diagnotico_diferente(self):
        
        try :
            
            if self.input_otro_diagnostico.text().strip():
                
                diagnostico = self.input_otro_diagnostico.text().strip()
                
                nuevo_diagnostico = {"diagnostico": diagnostico}
                
                diagnostico_servicio.registrar_diagnostico(nuevo_diagnostico)
                
                
                self.boton_diagnostico.clear()
                
                self.input_otro_diagnostico.clear()
                
                self.lista_diagnostico = diagnostico_servicio.obtener_todos_diagnosticos()
                
                FuncionSistema.cargar_elementos_para_el_combobox(self.lista_diagnostico, self.boton_diagnostico, 1, 1)
                
                self.boton_diagnostico.setCurrentIndex(0)
                
                
                
            else:
                
                QMessageBox.warning(self, "Aviso", "Si va a añadir otro diagnostico, por favor coloque el nombre del diangostico en el campo (otro diagnostico)")
        
        except Exception as e:
            
            print("error")
        
        
    # Metodo para añadir los diagnosticos del alumno en el  "carrito"
    def anadir_diagnosticos_alumno_a_lista(self):
        
        lista_diagnostico = []
        
        # la lista debe estar llena asi
        # [id_diagnostico, nombre_diagnostico, medico_tratante, fecha_diagnotico, fecha_vencimiento_certificado, medicacion, observacion_adicional]
        #        0                  1                 2                3                        4                     5             6
        
        try:
            
            if not self.boton_diagnostico.currentIndex() == 0 and not self.input_otro_diagnostico.text().strip():
                
                # Guardamos el diagnostico en la lista de diagnostico registrados
                if self.boton_diagnostico.currentText() and not self.input_otro_diagnostico.text():
                    
                    diagnostico_id = self.buscar_id_de_la_lista_del_combobox(self.boton_diagnostico, self.lista_diagnostico, 1, 0)
                    
                else:
                    pass
                    
                    
                    
                
                medico_tratante = self.input_medico_tratante.text()
                
                
                
                fecha_diagnostico = self.fecha_de_str_a_date(self.dateedit_fecha_diagnostico.text().strip())
                
                
                fecha_vencimiento_certif = self.fecha_de_str_a_date(self.dateedit_fecha_vencimiento_certificado.text())
                
                print(fecha_diagnostico, type(fecha_diagnostico))
                
                if self.input_medicacion.text().strip():
                    
                    medicacion = self.input_medicacion.text().strip()
                    
                else: 
                    
                    medicacion = None
                    
                certificacion_discap = self.input_certificado_discapacidad.text().strip()
                
                
                
                if  self.input_observacion_adicional.text().strip():
                    
                    observacion_adicional = self.input_observacion_adicional.text().strip()
                    
                else:
                    
                    observacion_adicional = None
                
                    
                
                
                
                
                campos_info_clinica_alumno = {
                                    "alumno_id": None,
                                    "diagnostico_id": diagnostico_id,
                                    "fecha_diagnostico": fecha_diagnostico,
                                    "medico_tratante": medico_tratante,
                                    "certificacion_discap": certificacion_discap,
                                    "fecha_vencimiento_certif": fecha_vencimiento_certif,
                                    "medicacion": medicacion,
                                    "observacion_adicional": observacion_adicional
                                }
                                
    
                # comprobamos si no hay errores al añadir elementos al diccionario
                errores_info_clinica_alumno = info_clinica_alumno_servicio.valdidar_campos_info_clinica_alumno(
                                    campos_info_clinica_alumno.get("diagnostico_id"),
                                    campos_info_clinica_alumno.get("fecha_diagnostico"),
                                    campos_info_clinica_alumno.get("medico_tratante"),
                                    campos_info_clinica_alumno.get("certificacion_discap"),
                                    campos_info_clinica_alumno.get("fecha_vencimiento_certif"),
                                    campos_info_clinica_alumno.get("medicacion"),
                                    campos_info_clinica_alumno.get("observacion_adicional")
                                )
                                    
                # Mostrar errores
                if errores_info_clinica_alumno:
                    
                    self.mostrar_errores_antes_de_guardar(errores_info_clinica_alumno, "Información clinica del alumno")

                    return
                
                else:
                    
                    # agregamos todos los elementos a la lista
                    lista_diagnostico.append(diagnostico_id)
                    lista_diagnostico.append(self.boton_diagnostico.currentText())
                    lista_diagnostico.append(medico_tratante)
                    lista_diagnostico.append(fecha_diagnostico)
                    lista_diagnostico.append(fecha_vencimiento_certif)
                    lista_diagnostico.append(medicacion)
                    lista_diagnostico.append(certificacion_discap)
                    lista_diagnostico.append(observacion_adicional)
                    
                    
                    # usamos el metodo para que se vea en la vista previa de cuantos
                    # diagnostico tiene el alumno
                    self.agregar_elementos_a_la_vista_previa(self.vista_previa_diagnostico , self.lista_carrito_diagnosticos, lista_diagnostico[1])
                    
                    lista_diagnostico = tuple(lista_diagnostico)
                    
                    
                    
                    self.lista_carrito_diagnosticos.append(lista_diagnostico)
                    
                    print(f"Lista de diagnostico: {self.lista_carrito_diagnosticos}")
                    
                    
                    #  limpia los inputs
                    self.boton_diagnostico.setCurrentIndex(0)
                    self.input_otro_diagnostico.clear()
                    self.input_medico_tratante.clear()
                    self.input_medicacion.clear()
                    self.input_certificado_discapacidad.clear()
                    self.dateedit_fecha_diagnostico.setDate(QtCore.QDate(2000, 1, 1))
                    self.dateedit_fecha_vencimiento_certificado.setDate(QtCore.QDate(2000, 1, 1))
                    self.input_observacion_adicional.clear()
                    
                    

            
            else:
                QMessageBox.warning(self, "Atento", "Si va a añadir un diagnostico, seleccione un diagnostico")  
                
            
        except Exception as e:
            
            FuncionSistema.mostrar_errores_por_excepcion(e, "añadir_diagnostico_alumno_a_lista")
    
    
    
    # Metodo para añadir cuentas bancarias del alumno
    def anadir_cuentas_bancarias_alumno(self):
        
        # una lista vacia para agregarla a otra lista que va a tener todas las cuentas
        cuenta = []
        
        try:
            # si los campos de la cuenta bancaria de alumno tiene texto entonces...
            if self.input_tipo_de_cuenta.text().strip() and self.input_numero_de_cuenta.text().strip():
                
                tipo_cuenta = self.input_tipo_de_cuenta.text().strip()
                num_cuenta = self.input_numero_de_cuenta.text().strip()
                
                
                
                
                
                
                campos_info_bancaria_alumno = {
                                "alumno_id": None,
                                "tipo_cuenta": tipo_cuenta,
                                "num_cuenta": num_cuenta
                            }
                        
                errores_info_bancaria_alumno = info_bancaria_alumno_servicio.validar_campos_info_bancaria_alumno(
                    campos_info_bancaria_alumno.get("tipo_cuenta"),
                    campos_info_bancaria_alumno.get("num_cuenta")
                )
                
                # mostramos los errores
                if errores_info_bancaria_alumno:
                    
                    self.mostrar_errores_antes_de_guardar(errores_info_bancaria_alumno, "Información Bancaria del alumno")
                    return
                
                else:
                    # agregamos los elementos a la lista
                    cuenta.append(tipo_cuenta)
                    
                    cuenta.append(num_cuenta)
                    
                    # agregamos la lista de cuenta a la lista donde van a estar todas las cuentas de banco
                    cuenta = tuple(cuenta)
                    
                    self.lista_carrito_cuentas_bancarias.append(cuenta)
                    
                    mostrar_texto = cuenta[0] + " " + cuenta [1]
                    
                    # Mandamos los datos a la funcion que los agrega a la vista previa
                    self.agregar_elementos_a_la_vista_previa(self.vista_previa_cuentas_bancarias, self.lista_carrito_cuentas_bancarias, mostrar_texto)
                
                    # limpiamos los inputs
                    self.input_tipo_de_cuenta.clear()
                    self.input_numero_de_cuenta.clear()
                    
                    
                    print(f"Lista de cuentas: {self.lista_carrito_cuentas_bancarias}")
                
                
            else :
                
                QMessageBox.warning(self, "Aviso", "Si va a añadir una cuenta, los dos campos deben estar llenos")
            
            
            
        except Exception as e:
            FuncionSistema.mostrar_errores_por_excepcion(e, "anadir_cuentas_bancarias_alumno")
            print("Error en la funcion añadir cuentas bancarias del alumno")
            
    

    # Metodo para agregar diagnostico a la vista previa
    def agregar_elementos_a_la_vista_previa(self, nombre_qlistwidget, nombre_lista, texto_a_mostrar=None, editando:bool = False):
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
        boton_eliminar = QPushButton()
        boton_eliminar.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), ".." ,"recursos_de_imagenes", "iconos_de_interfaz", "borrar.png")))
        boton_eliminar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        boton_eliminar.setFixedSize(40,40)
        boton_eliminar.setStyleSheet("""
                                    
                                    QPushButton{
                                        background:red;
                                        border-radius:0px;
                                        icon-size:28px;
                                    
                                    }
                                    
                                    QPushButton:hover{
                                        
                                        background:#9e0000
                                        
                                        
                                    }
                                    
                                    
                                    """)
        
        boton_eliminar.clicked.connect(lambda: self.borrar_elementos_a_la_vista_previa(nombre_qlistwidget, nombre_lista, item))
        row_layout.addWidget(boton_eliminar)

        if editando:
            # Botón para editar
            boton_editar = QPushButton()
            boton_editar.setIcon(QIcon.fromTheme(os.path.join(os.path.dirname(__file__), "..", "recursos_de_imagenes", "iconos_de_interfaz", "editar.png")))
            boton_editar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            boton_editar.setFixedSize(40, 40)
            boton_editar.setStyleSheet("""
                QPushButton {
                    background-color: rgb(244, 131, 2);
                    color: white;
                }
                QPushButton:hover {
                    background-color: rgb(191, 64, 0);
                }
            """)
            
            boton_editar.clicked.connect(lambda _, item=item, lista=nombre_lista:self.ver_elemento_de_la_lista_seleccionada(nombre_qlistwidget, lista, item))
            row_layout.addWidget(boton_editar)
            
        # Asignar el widget al QListWidgetItem
        item.setSizeHint(widget.sizeHint())
        nombre_qlistwidget.setItemWidget(item, widget)

    
    

    # Metodo para borrar diagnostico a la vista previa
    def borrar_elementos_a_la_vista_previa(self, nombre_qlistwidget, nombre_lista,  item):
        
        
        # Logica para borrar el registro del diagnostico de la lista
        
        # indice del listwidget
        indice_vista_previa = nombre_qlistwidget.row(item)
        
        # borramos el elemento de la lista segun el indice del listwidget
        del nombre_lista[indice_vista_previa]
        
        # darle foco al input del segmento
        # esto lo hice porque al borrar toda la lista de X segmento, esta se subia al arriba del todo del formulario
        
        ##########################################################################
        # Obtener la fila del item y eliminarlo
        row = nombre_qlistwidget.row(item)
        nombre_qlistwidget.takeItem(row)
    
        print(f"lista actualizada: {nombre_lista}")
    
    
    # Metodo para mostrar errores de la base de datos 
    def mostrar_errores_antes_de_guardar(self, errores, nombre_segmento):
        
        error_msg = "Lista de errores:\n"
        error_msg += "\n".join(f"- {field.capitalize()}" for field in errores)
        QMessageBox.critical(self, f"Errores en {nombre_segmento}", error_msg)
        print("\n".join(errores))
        return
    
    
    




    # recordar Borrar todos los inputs al salir
    def salir_del_formulario_alumno(self):

        
        ##  Creamos una ventana emergente para preguntar si de verdad se quiere salir ##
        QApplication.beep()
       
        self.msg_box.setWindowTitle("Confirmar salida")
        self.msg_box.setText("¿Seguro que quiere salir sin registrar?")
        self.msg_box.setIcon(QMessageBox.Question)

        

        # Mostrar el cuadro de diálogo y esperar respuesta
        self.msg_box.exec_()
        
        # si el boton pulsado es "si" se regresa y borra todo el registro
        if self.msg_box.clickedButton() == self.boton_si:
            
        
            self.stacked_widget.setCurrentIndex(2)
            FuncionSistema.limpiar_inputs_de_qt(self.lista_de_inputs, self.lista_de_radiobuttons)
        
        ## si el boton "no" es pulsadoo, no pasa nada #3
        elif self.msg_box.clickedButton() == self.boton_no:
            pass


    # Metodo para tranformar str a int o float
    # esto es para los variables como (peso, estatura, talla_zapatos, talla_pantalon)
    def de_str_a_int_o_float(self, nombre_variable,  input_para_la_variable, tipo_de_dato):
        
        if not input_para_la_variable.text().strip():
            
            nombre_variable = None
            
            return nombre_variable
        
        else:
            
            nombre_variable = input_para_la_variable.text().strip()
            
            nombre_variable = tipo_de_dato(nombre_variable)
        
            return nombre_variable
        
 
    def ver_elemento_de_la_lista_seleccionada(self,  nombre_qlistwidget, nombre_lista, item):
        
        """
            Este metodo sirve para poder ver los elementos que se ven en la lista previa (QListWidget), segun de cual se elija
            
            por ejemplo si se elige un elemento de la vista previa de las cuentas bancarias de los alumno, se va a ver la infomacion del elemento seleccionado
            lo mismo para los diagnosticos
        """       
        
        if nombre_qlistwidget == self.vista_previa_diagnostico:
            self.ver_diagnostico_seleccionado(nombre_qlistwidget, nombre_lista, item)
            
        elif nombre_qlistwidget == self.vista_previa_cuentas_bancarias:
            
            self.ver_cuenta_bancaria_seleccionada(nombre_qlistwidget, nombre_lista, item)
        
    
    def ver_cuenta_bancaria_seleccionada(self, nombre_qlistwidget, nombre_lista, item):
        
        """
            Este metodo sirve para ver la cuenta de banco seleccionda
        """
        
        indice_vista_previa = nombre_qlistwidget.row(item)
        
        cuenta_bancaria_id = nombre_lista[indice_vista_previa][0]
        
        cuentas_bancarias = nombre_lista
        
        
        for cuenta_bancaria in cuentas_bancarias:
            
            if cuenta_bancaria[0] == cuenta_bancaria_id:
                
                self.input_tipo_de_cuenta.setText(cuenta_bancaria[2])
                self.input_numero_de_cuenta.setText(cuenta_bancaria[3])
                
                self.boton_anadir_cuenta_banco.clicked.disconnect()
                FuncionSistema.cambiar_estilo_del_boton(self.boton_anadir_cuenta_banco, "editar")
                self.boton_anadir_cuenta_banco.clicked.connect(lambda: self.editar_cuenta_banaria_seleccionada(nombre_lista, cuenta_bancaria_id))

                break
            
    def editar_cuenta_banaria_seleccionada(self, nombre_lista, cuenta_bancaria_id):
        
        """
            Este metodo sirve para editar la cuenta de banco seleccionado y funciona asi:
            
            1. con un for iterando todas las cuentas de banco del alumno e ir comparando si es igual que la cuenta de banco que selecciono para poder editar la informacion
            2. si es igual transformamos la tupla que contiene la cuenta de banco seleccionada en una lista para poder editar la informacion y luego de editar la transformamos en una tupla nuevamente
            
        
        """
        cuentas_bancarias = nombre_lista
        ##  Creamos una ventana emergente para preguntar si de verdad se quiere salir ##
        QApplication.beep()
        
        self.msg_box.setWindowTitle("Confirmar edicion de la cuenta de banco")
        self.msg_box.setText("¿Seguro que quiere editar esta cuenta bancaria?")
        self.msg_box.setIcon(QMessageBox.Question)

        

        # Mostrar el cuadro de diálogo y esperar respuesta
        self.msg_box.exec_()
        
        
        if self.msg_box.clickedButton() == self.boton_si:
            
            for i, _ in enumerate(cuentas_bancarias):
                
                if cuentas_bancarias[i][0] == cuenta_bancaria_id: 
                    print(f"antes: {cuentas_bancarias}")
                    
                    cuentas_bancarias[i] = list(cuentas_bancarias[i])
                    
                    cuentas_bancarias[i][2] = self.input_tipo_de_cuenta.text()
                    cuentas_bancarias[i][3] = self.input_numero_de_cuenta.text()

                    cuentas_bancarias[i] = tuple(cuentas_bancarias[i])
                    
                    print(f"Ahora: {cuentas_bancarias}")
                    
                    self.input_tipo_de_cuenta.clear()
                    self.input_numero_de_cuenta.clear()
                    
                    self.boton_anadir_cuenta_banco.clicked.disconnect()
                    self.boton_anadir_cuenta_banco.clicked.connect(lambda: self.anadir_cuentas_bancarias_alumno())
                    FuncionSistema.cambiar_estilo_del_boton(self.boton_anadir_cuenta_banco, "añadir")
                    
                    self.vista_previa_cuentas_bancarias.clear()
                    
                    for cuenta_bancaria in cuentas_bancarias:
                        
                        texto_mostrar = cuenta_bancaria[2] + " " +cuenta_bancaria[3]
                        self.agregar_elementos_a_la_vista_previa(self.vista_previa_cuentas_bancarias, cuentas_bancarias,texto_mostrar, True )
                            
                    break
                
        elif self.msg_box.clickedButton() == self.boton_no:
            
            self.boton_anadir_cuenta_banco.clicked.disconnect()
            self.boton_anadir_cuenta_banco.clicked.connect(lambda: self.anadir_cuentas_bancarias_alumno())
            FuncionSistema.cambiar_estilo_del_boton(self.boton_anadir_cuenta_banco, "añadir")
        
    def ver_diagnostico_seleccionado(self, nombre_qlistwidget, nombre_lista, item):
        
        """
            Este metodo sirve para ver la infomacion que tiene el diagnostico para editarlo.
            
            Este metodo funciona asi:
            
            1. Tomamos el indice del qlistwidget para saber que elemento vamos a modificar
            2. con el indice del qlistwidget lo usamos en la lista de info_clinica del alumno para acceder al id del diagnostico
            3. conectamos el boton de añadir diagnostico a otro metodo que es para confirmar la edicion de los elementos del diagnostico seleccionado
            4. con un for iteramos cada diagnostico
            5. dentro del for hay un if que compara si el diagnostico iterado tiene el mismo valor que la variable info_clinica_id
            6. si es verdadero mostramos los datos en pantalla de dicho diagnostico, si es falso no pasa nada
        
        """
        
        #info_clinica = info_clinica_alumno_servicio.obtener_info_clinica_por_alumno_id(alumno_id)
        
        # Este es el indice del QListWidget
        indice_vista_previa = nombre_qlistwidget.row(item)
        
        # accedemos al nombre del diagnostico
        info_clinica_id = nombre_lista[indice_vista_previa][0]
        #print(f"indice del qlistwidget: {indice_vista_previa}")
        #print(f"Indice del diagnostico: {info_clinica_id}")
        
        
        

        info_clinica = nombre_lista # le coloco en otra variable es para que sea mas entendible
        
        self.boton_anadir_diagnostico.clicked.disconnect()
        self.boton_anadir_diagnostico.clicked.connect(lambda: self.editar_diagnostico_seleccionado(nombre_lista, info_clinica_id))
        FuncionSistema.cambiar_estilo_del_boton(self.boton_anadir_diagnostico, "editar")
        try: 
            
            for i, _ in enumerate(info_clinica):
                
                if info_clinica[i][0] == info_clinica_id:

                    #[(1, 1, 'Sindrome de down', datetime.date(2012, 10, 11), 'Dr Alejandro', 'D-0321121', datetime.date(2015, 8, 14), 'No tiene', None)]
                    
                    self.boton_diagnostico.setCurrentText(info_clinica[i][2])
                    self.dateedit_fecha_diagnostico.setDate(info_clinica[i][3])
                    self.input_medico_tratante.setText(info_clinica[i][4])
                    self.input_certificado_discapacidad.setText(info_clinica[i][5])
                    self.dateedit_fecha_vencimiento_certificado.setDate(info_clinica[i][6])
                    self.input_medicacion.setText("" if not info_clinica[i][7] else info_clinica[i][7])
                    self.input_observacion_adicional.setText("" if info_clinica[i][8] == None else info_clinica[i][8])
                    
                    break
        
        except:
            print(f"ID: {info_clinica[i][0]}, Diagnostico: {nombre_lista[indice_vista_previa][2]} no cargo correctamente")
            
        else:
            
            print(f"ID: {info_clinica[i][0]}, Diagnostico: {nombre_lista[indice_vista_previa][2]} cargado correctamente")
     
    
    def editar_diagnostico_seleccionado(self, nombre_lista, info_clinica_id):
        
        """
            Este metodo sirve para editar el diagnostico seleccionado del alumno

            Este metodo funciona asi:
            
            1. iteramos cada diagnostico otra vez para comparar si el diagnostico tiene el mismo valor que info_clinica_id
            2. si es verdadero editamos, si es falso no pasaria nada
            
        """       
       
        info_clinica = nombre_lista 
        
        ##  Creamos una ventana emergente para preguntar si de verdad se quiere salir ##
        QApplication.beep()
        
        self.msg_box.setWindowTitle("Confirmar edicion de diagnostico")
        self.msg_box.setText("¿Seguro que quiere editar este diagnostico?")
        self.msg_box.setIcon(QMessageBox.Question)

        

        # Mostrar el cuadro de diálogo y esperar respuesta
        self.msg_box.exec_()
        
        # si el boton pulsado es "si" se regresa y borra todo el registro
        if self.msg_box.clickedButton() == self.boton_si:
            
        
            for i, _ in enumerate(info_clinica):
            
            
                if info_clinica[i][0] == info_clinica_id:

                    #[(1, 1, 'Sindrome de down', datetime.date(2012, 10, 11), 'Dr Alejandro', 'D-0321121', datetime.date(2015, 8, 14), 'No tiene', None)]
                    print(f"antes: {info_clinica}")
                    info_clinica[i] = list(info_clinica[i])
                    
                    info_clinica[i][2] = self.boton_diagnostico.currentText().strip()
                    info_clinica[i][3] = date(self.dateedit_fecha_diagnostico.date().year(),
                                                    self.dateedit_fecha_diagnostico.date().month(),
                                                    self.dateedit_fecha_diagnostico.date().day())
                    info_clinica[i][4] = self.input_medico_tratante.text().strip()
                    info_clinica[i][5] = self.input_certificado_discapacidad.text().strip()
                    info_clinica[i][6] = date(self.dateedit_fecha_vencimiento_certificado.date().year(),
                                                self.dateedit_fecha_vencimiento_certificado.date().month(),
                                                self.dateedit_fecha_vencimiento_certificado.date().day())
                    info_clinica[i][7] = self.input_medicacion.text().strip()
                    info_clinica[i][8] = None if not self.input_observacion_adicional.text().strip() else self.input_observacion_adicional.text().strip()
                    
                    info_clinica[i] = tuple(info_clinica[i])
                    print(f"\ndespues: {info_clinica}")
                    
                    
                    self.boton_diagnostico.setCurrentIndex(0)
                    #self.dateedit_fecha_diagnostico.clear()
                    self.input_medico_tratante.clear()
                    self.input_certificado_discapacidad.clear()
                    #self.dateedit_fecha_vencimiento_certificado.clear()
                    self.input_medicacion.clear()
                    self.input_observacion_adicional.clear()
                    
                    FuncionSistema.cambiar_estilo_del_boton(self.boton_anadir_diagnostico, "añadir")
                    self.boton_anadir_diagnostico.clicked.disconnect()
                    self.boton_anadir_diagnostico.clicked.connect(lambda: self.anadir_diagnosticos_alumno_a_lista())
                    
                    self.vista_previa_diagnostico.clear()
                    for diagnostico in info_clinica:
                        
                        self.agregar_elementos_a_la_vista_previa(self.vista_previa_diagnostico, info_clinica, diagnostico[2], True)
                            
                    
                    #print(nombre_lista)
                    
                    break
        
        ## si el boton "no" es pulsadoo, no pasa nada #3
        elif self.msg_box.clickedButton() == self.boton_no:
            
            FuncionSistema.cambiar_estilo_del_boton(self.boton_anadir_diagnostico, "añadir")
            self.boton_anadir_diagnostico.clicked.disconnect()
            self.boton_anadir_diagnostico.clicked.connect(lambda: self.anadir_diagnosticos_alumno_a_lista())
            
            self.boton_diagnostico.setCurrentIndex(0)
            #self.dateedit_fecha_diagnostico.clear()
            self.input_medico_tratante.clear()
            self.input_certificado_discapacidad.clear()
            #self.dateedit_fecha_vencimiento_certificado.clear()
            self.input_medicacion.clear()
            self.input_observacion_adicional.clear()


        
            
            
              
    # Metodo para guardar todos los datos del Alumno en la BD
    # hasta los momentos nada (vamos a realizar todas las funciones, )
    def guardar_informacion_alumno(self):
        
        try:
            
            ################################################################################################
            # Primera parte
            # Informacion del alumno
            
            # vamos guardando los valores de los inputs en las varibles
            
            primer_nombre = self.input_primer_nombre.text().strip().capitalize()
            segundo_nombre = FuncionSistema.comprobar_si_hay_valor(self.input_segundo_nombre.text().strip().capitalize())
            tercer_nombre = FuncionSistema.comprobar_si_hay_valor(self.input_tercer_nombre.text().strip().capitalize())
            
            
            
            apellido_paterno = self.input_apellido_paterno.text().strip().capitalize()
            apellido_materno = FuncionSistema.comprobar_si_hay_valor(self.input_apellido_materno.text().strip().capitalize())
            cedula = self.input_cedula.text().strip()
            relacion_con_rep = self.input_relacion_con_representante.text().strip().capitalize()
            situacion = self.input_situacion.text().strip().capitalize()
            
            fecha_ingreso_institucion = self.fecha_de_str_a_date(self.dateedit_fecha_ingreso_tela.text())
            
            
            if self.input_sexo_masculino.isChecked():
                
                sexo = "M"
                
            elif self.input_sexo_femenino.isChecked():
                
                sexo = "F"
                
            else:
                
                sexo = None
            
            campos_datos_alumno_1 = {
                "primer_nombre": primer_nombre,
                "segundo_nombre": segundo_nombre,
                "tercer_nombre": tercer_nombre,
                "apellido_paterno": apellido_paterno,
                "apellido_materno": apellido_materno,
                "cedula": cedula,
                "relacion_con_rep": relacion_con_rep,
                "sexo": sexo,
                "situacion": situacion,
                "fecha_ingreso_institucion": fecha_ingreso_institucion
                }
            
            errores_primera_info_alumno = alumno_servicio.validar_campos_primera_info_alumno(
                    campos_datos_alumno_1.get("cedula"),
                    campos_datos_alumno_1.get("primer_nombre"),
                    campos_datos_alumno_1.get("segundo_nombre"),
                    campos_datos_alumno_1.get("tercer_nombre"),
                    campos_datos_alumno_1.get("apellido_paterno"),
                    campos_datos_alumno_1.get("apellido_materno"),
                    campos_datos_alumno_1.get("relacion_con_rep"),
                    campos_datos_alumno_1.get("fecha_ingreso_institucion")
                )
            
            # verificamos que no hay errores
            if errores_primera_info_alumno:
                
                self.mostrar_errores_antes_de_guardar(errores_primera_info_alumno, "Información del alumno")
                return
            
            else:
                # esto es para depuracion, es para ver si todo esta correcto
                #print("\nAlumno")
                #print(f"Nombres: {primer_nombre}, {segundo_nombre}")
                #print(f"Apellidos: {apellido_paterno}, {apellido_materno}")
                #print(f"Relacion con el representante: {relacion_con_rep}")
                
                # Primera parte sin errores
                
                ############################################################################################3
                
                # segunda parte
                # Info alumno parte 2
                
                # vamos guardando los valores de los inputs en las varibles
                
                cma = None
                imt = None
                
                if self.input_cma_si.isChecked():
                    
                    cma = True
                    
                elif self.input_cma_no.isChecked():
                    
                    cma = False
                    
                
                else:
                    
                    cma = None
                    
                    
                if self.input_imt_si.isChecked():
                    imt = True
                    
                elif self.input_imt_no.isChecked():
                    imt = False
                    
                else:
                    
                    imt = None
                
                
                    
                fecha_nacimiento = self.fecha_de_str_a_date(self.dateedit_fecha_nacimiento.text())
                    
                
                
                lugar_nacimiento = self.input_lugar_de_nacimiento.text()
                
                campos_datos_alumno_2 = {
                    "cma": cma,
                    "imt": imt,
                    "fecha_nacimiento": fecha_nacimiento,
                    "lugar_nacimiento": lugar_nacimiento
                    }
                
                errores_segunda_info_alumno = alumno_servicio.validar_campos_segunda_info_alumno(
                campos_datos_alumno_2.get("fecha_nacimiento"),
                campos_datos_alumno_2.get("lugar_nacimiento")
                )
                
                
                # comprobamos si no hay errores
                # si los hay que muestre el mensaje en la pantalla
                if errores_segunda_info_alumno:
                
                    self.mostrar_errores_antes_de_guardar(errores_segunda_info_alumno, "Información del alumno")
                    return
                
                else:
                    
                    # esto es para depuracion, es para ver si todo esta correcto
                    #print("\nAlumno parte 2")
                    #print(f"cma: {cma}")
                    #print(f"imt: {imt}")
                    #print(f"fecha de nacimiento {fecha_nacimiento}")
                    #print(f"lugar de nacimiento: {lugar_nacimiento}")
                    
                    # segunda parte sin errores
                    
                    ########################################################################################3
                    
                    
                    # tercera parte
                    
                    
                    # Info academica
            
                    escolaridad = self.input_escolaridad.text().strip()
                    procedencia = self.input_procendencia.text().strip()
                    
                    campos_info_academica = {
                                "escolaridad": escolaridad,
                                "procedencia": procedencia
                            }
                                    
                    errores_info_academica = alumno_servicio.validar_info_academica(
                        campos_info_academica.get("escolaridad"),
                        campos_info_academica.get("procedencia")
                    )
                    
                    # comprobamos si no hay errores
                    if errores_info_academica:
                        self.mostrar_errores_antes_de_guardar(errores_info_academica, "Información académica")
                        return
                    
                    else:
                        
                        # esto es para depuracion, es para ver si todo esta correcto
                        #print("\nInfo Académica Alumno")
                        #print(f"procedencia: {procedencia} ")
                        #print(f"escolaridad: {escolaridad} ")
                        
                        # Tercera parte sin erroes
                        
                    
                        #######################################################################################################
                        
                        # Cuarta parte
                        
                        # info representante
                    
                    
                        # Primero comprobamos si el usuario comprobo que el representante existe o no
                        
                        # comprobacion
                        if not self.comprobacion:
                            
                            QMessageBox.warning(self, "Aviso", "Tiene que comprobar si el representante esta registrado o no")
                            return
                        
                        # si hizo la comprobacion, puede seguir con lo demas 
                        else:  
                            
                            
                            # si el representante esta registrado
                            if self.representante_registrado:
                                
                                # solo quiero el id del representante
                                representante_id = self.representante_id
                                
                                
                                # Quinta parte
                                
                                # proceso para asociar a el representate con el alumno
                                
                                # Recordar que para crear este diccionario y poder crear un registro en tb_alumnos
                                # Tienes que tener los campos de su info básica e info académica para poder
                                # crear registros en las tablas tb_medidas_alumnos, tb_info_bancaria_alumnos, tb_info_clinica_alumnos
                                campos_alumno = {
                                    "representante_id": representante_id,
                                    "cedula": campos_datos_alumno_1.get("cedula"),
                                    "primer_nombre": campos_datos_alumno_1.get("primer_nombre"),
                                    "segundo_nombre": campos_datos_alumno_1.get("segundo_nombre"),
                                    "tercer_nombre": campos_datos_alumno_1.get("tercer_nombre"),
                                    "apellido_paterno": campos_datos_alumno_1.get("apellido_paterno"),
                                    "apellido_materno": campos_datos_alumno_1.get("apellido_materno"),
                                    "fecha_nacimiento": campos_datos_alumno_2.get("fecha_nacimiento"),
                                    "lugar_nacimiento": campos_datos_alumno_2.get("lugar_nacimiento"),
                                    "sexo": campos_datos_alumno_1.get("sexo"),
                                    "cma": campos_datos_alumno_2.get("cma"),
                                    "imt": campos_datos_alumno_2.get("imt"),
                                    "relacion_con_rep": campos_datos_alumno_1.get("relacion_con_rep"),
                                    "escolaridad": campos_info_academica.get("escolaridad"),
                                    "procedencia": campos_info_academica.get("procedencia"),
                                    "situacion": campos_datos_alumno_1.get("situacion")
                                }
                                
                                # Acá guardo el alumno_id que retorno al crear un registro en la tabla tb_alumnos
                                # y lo uso para asociarlo a las demás tablas        
                                alumno_id = alumno_servicio.registrar_alumno(campos_alumno)
                                
                                print(alumno_id)
                                
                                
                                
                                ###########################################################################
                                
                                # sexta parte
                                # Info medidas del alumno
                                
                                # vamos guardando los valores de los inputs en las varibles
                                estatura = None
                                peso = None
                                talla_camisa = self.input_talla_camisa.text().strip()
                                talla_pantalon = None
                                talla_zapatos = None
                                
                                estatura = self.de_str_a_int_o_float(estatura, self.input_estatura, float)
                                peso = self.de_str_a_int_o_float(peso, self.input_peso, float)
                                talla_pantalon = self.de_str_a_int_o_float(talla_pantalon, self.input_talla_pantalon, int)
                                talla_zapatos = self.de_str_a_int_o_float(talla_zapatos, self.input_talla_zapatos, int)
                                
                                
                                
                                campos_medidas_alumno = {
                                    "alumno_id": alumno_id,
                                    "estatura": estatura,
                                    "peso": peso,
                                    "talla_camisa": talla_camisa.upper(),
                                    "talla_pantalon": talla_pantalon,
                                    "talla_zapatos": talla_zapatos
                                }
                            
                                errores_medidas_alumnos = medidas_alumno_servicio.validar_campos_medidas_alumnos(
                                    campos_medidas_alumno.get("estatura"),
                                    campos_medidas_alumno.get("peso"),
                                    campos_medidas_alumno.get("talla_camisa"),
                                    campos_medidas_alumno.get("talla_pantalon"),
                                    campos_medidas_alumno.get("talla_zapatos")
                                )

                                # comprobamos que no haigan errores
                                if errores_medidas_alumnos:
                                    
                                    self.mostrar_errores_antes_de_guardar(errores_medidas_alumnos, "Información medidas del alumnos")
                                    return
                                
                                else:
                                    
                                    # esto es para debugear y ver si todo esta correcto
                                    
                                    #print("\nMedidas del Alumno")
                                    #print(f"ID Alumno: {alumno_id}")
                                    #print(f"Estatura: {estatura}, {type(estatura)}")
                                    #print(f"Peso: {peso}, {type(peso)}")
                                    #print(f"Talla de camisa: {talla_camisa}, {type(talla_camisa)}")
                                    #print(f"Talla de pantalon: {talla_pantalon}, {type(talla_pantalon)}")
                                    #print(f"Talla de zapatos: {talla_zapatos}, {type(talla_zapatos)}")
                                    
                                    
                                    # sexta parte sin erroes
                                    
                                    #####################################################################################
                                    
                                    # Septima parte
                                    
                                    
                                    # cuentas del alumno y diagnostico del alumno
                                    
                                    # comprobamos si la lista de diagnostico por lo menos tenga un diagnostico registrado
                                    
                                    if not self.lista_carrito_diagnosticos:
                                        
                                        # si no tiene un registro que le muestre un mensaje de que no a registrado un diagnostico para el alumno
                                        QMessageBox.warning(self, "Aviso", f"El alumno {primer_nombre} {apellido_paterno}, no tiene diagnosticos registrados")
                                    
                                    
                                    
                                    # si un o unos diagnostico entonces que siga 
                                    else: 
                                        
                                    
                                        # aqui no va la logica ya que esta en otra funcion
                                        # mas a bajo tiene que registra todo lo que tenga el carrito de cada parte
                                        
                                        ######################################################################################
                                        
                                        # Novena parte 
                                        
                                        # Info especialida / info inscripcion
                                        
                                        
                                        # Incripcion 
                                
                                        especialidad_id = self.buscar_id_de_la_lista_del_combobox(self.boton_de_especialidad, self.lista_especialidades, 1, 0)
                                        periodo_escolar = str(año_actual) + "-" + str(año_actual + 1)
                                        
                                        
                                        
                                        fecha_inscripcion = self.fecha_de_str_a_date(self.dateedit_fecha_ingreso_especialidad.text())
                                        
                                        campos_inscripcion = {
                                                            "num_matricula": None, #Esto es None para que internamente se modifique este valor por el que se va a generar automáticamente
                                                            "alumno_id": alumno_id,
                                                            "especialidad_id": especialidad_id,
                                                            "fecha_inscripcion": fecha_inscripcion,
                                                            "periodo_escolar": periodo_escolar
                                                        }
                                                        
                                        errores_inscripcion = inscripcion_servicio.valdiar_campos_inscripcion(
                                            campos_inscripcion.get("especialidad_id"),
                                            campos_inscripcion.get("fecha_inscripcion"),
                                            campos_inscripcion.get("periodo_escolar")
                                        )
                                        
                                        # comprobamos errores
                                        if errores_inscripcion:
                                            self.mostrar_errores_antes_de_guardar(errores_inscripcion, "Especialidad por inscribir")
                                            return
                                        
                                        else:
                                            
                                            # esto es para debugaer y ver si todo esta correcto
                                            
                                            #print("\nIncripcion alumno")
                                            #print(f"ID alumno: {alumno_id}")
                                            #print(f"ID Especialidad: {especialidad_id}, {type(especialidad_id)}")
                                            #print(f"Fecha de inscripcion: {fecha_inscripcion}, {type(fecha_inscripcion)}")
                                            #print(f"Periodo escolar: {periodo_escolar}")
                                            
                                            # novena parte si errores
                                            
                                            
                                            try:
                                                
                                                QApplication.beep()
                                                self.msg_box.setWindowTitle("Confirmar registro")
                                                self.msg_box.setText("¿Seguro que quiere hacer este registro?")
                                                self.msg_box.setIcon(QMessageBox.Question)

                                                # Mostrar el cuadro de diálogo y esperar respuesta
                                                self.msg_box.exec_()
                                                
                                                # si el boton pulsado es "si" guarda todo
                                                if self.msg_box.clickedButton() == self.boton_si:
                                                    
                                                    medidas_alumno_servicio.registrar_medidas_alumno(campos_medidas_alumno)
                                
                                                    # logica para agregar todas las cuentas que estan en la lista al diccionario
                                                    campos_info_bancaria_alumno = {
                                                                        "alumno_id": alumno_id,
                                                                        "tipo_cuenta": None,
                                                                        "num_cuenta": None
                                                                    }
                                                    
                                                    # si la lista de cuentas de banco esta llena
                                                    if self.lista_carrito_cuentas_bancarias:
                                                        
                                                        # quiero que itere cada tupla y me de los valores y los registre
                                                        for cuenta_n in self.lista_carrito_cuentas_bancarias:
                                                            
                                                            campos_info_bancaria_alumno["alumno_id"] = alumno_id
                                                            campos_info_bancaria_alumno["tipo_cuenta"] = cuenta_n[0]
                                                            campos_info_bancaria_alumno["num_cuenta"] = cuenta_n[1]
                                                    
                                                            info_bancaria_alumno_servicio.registrar_info_bancaria_alumno(campos_info_bancaria_alumno)
                                                            
                                                    else:
                                                        
                                                        pass
                                                    
                                                    
                                                    campos_info_clinica_alumno = {
                                                                            "alumno_id": alumno_id,
                                                                            "diagnostico_id": None,
                                                                            "fecha_diagnostico": None,
                                                                            "medico_tratante": None,
                                                                            "certificacion_discap": None,
                                                                            "fecha_vencimiento_certif": None,
                                                                            "medicacion": None
                                                                        }
                                                    
                                                    # si hay diagnosticos en el "carrito" de diagnosticos
                                                    if self.lista_carrito_diagnosticos:
                                                        
                                                        for diagnostico in self.lista_carrito_diagnosticos:
                                                            
                                                            
                                                            campos_info_clinica_alumno["alumno_id"] = alumno_id
                                                            campos_info_clinica_alumno["diagnostico_id"] = diagnostico[0]
                                                            campos_info_clinica_alumno["medico_tratante"] = diagnostico[2]
                                                            campos_info_clinica_alumno["fecha_diagnostico"] = diagnostico[3]
                                                            campos_info_clinica_alumno["fecha_vencimiento_certif"] = diagnostico[4]
                                                            campos_info_clinica_alumno["medicacion"] = diagnostico[5]
                                                            campos_info_clinica_alumno["certificacion_discap"] = diagnostico[6]
                                                            
                                                                        
                                                            info_clinica_alumno_servicio.registrar_info_clinica_alumno(campos_info_clinica_alumno)
                                                            
                                                            
                                                            
                                                    else:
                                                        
                                                        QMessageBox.warning(self, "Aviso", f"El joven {self.input_primer_nombre.text()} {self.input_apellido_paterno.text()}, no tiene diagnosticos registrados")
                                                                
                                                        
                                                    inscripcion_servicio.registrar_inscripcion(campos_inscripcion)
                                                    
                                                    QMessageBox.information(self, "Bien hecho", "Registro exitoso")
                                                
                                                    # Parte final si esta registrado el representante
                                                            
                                                    # Limpiar todos los inputs
                                                    self.limpiar_los_valores_de_los_inputs(self.lista_de_inputs, self.lista_de_radiobuttons)
                                                    
                                                    pantalla_tabla_alumnos = self.stacked_widget.widget(2)
        
                                                    pantalla_tabla_alumnos.actualizar_tabla(1)
                                                    pantalla_tabla_alumnos.actualizar_lista_busqueda()
                                                    
                                                    pantalla_tabla_alumnos.boton_especialidades.setCurrentIndex(0)
                                                
                                                    self.stacked_widget.setCurrentIndex(2)
                                                    
                                                ## si el boton "no" es pulsadoo, no hace nada
                                                elif self.msg_box.clickedButton() == self.boton_no:
                                                    return
                                                
                                            except Exception as e:
                                                
                                                print("No se puedo guardar la informacion del alumno correctamente cuando el representante esta registrado")
                                                return
                            
                            
                            
                                
                                
                            ## si el representante no esta registrado
                            else:
                                
                                # vamos guardando los valores de los inputs en las varibles 
                                cedula_representante = self.input_buscar_por_cedula.text().strip()
                                nombre = self.input_nombre_del_representante.text().strip().capitalize()
                                apellido = self.input_apellido_del_representante.text().strip().capitalize()
                                direccion_residencia = self.input_direccion_residencia.text().strip()
                                num_telefono = self.input_numero_de_telefono.text().strip()
                                
                                if self.input_numero_de_telefono_adicional.text().strip():
                                    num_telefono_adicional = self.input_numero_de_telefono_adicional.text().strip()
                                else:
                                    num_telefono_adicional = None
                                
                                estado_civil = self.input_estado_civil.text().strip().capitalize()
                                carga_familiar = None
                                carga_familiar = self.de_str_a_int_o_float(carga_familiar, self.input_carga_familiar, int)
                                
                                
                                campos_representante = {
                                    "cedula": cedula_representante,
                                    "nombre": nombre,
                                    "apellido": apellido,
                                    "direccion_residencia": direccion_residencia,
                                    "num_telefono": num_telefono,
                                    "num_telefono_adicional": num_telefono_adicional,
                                    "carga_familiar": carga_familiar,
                                    "estado_civil": estado_civil
                                }
                                
                                errores_datos_representante = representante_servicio.validar_campos_representante(
                                campos_representante.get("cedula"),
                                campos_representante.get("nombre"),
                                campos_representante.get("apellido"),
                                campos_representante.get("direccion_residencia"),
                                campos_representante.get("num_telefono"),
                                campos_representante.get("num_telefono_adicional"),
                                campos_representante.get("carga_familiar"),
                                campos_representante.get("estado_civil")
                                )
                                
                                # guardamos el id del representante que se acaba de registrar
                                representante_id_retornado = representante_servicio.registrar_representante(campos_representante)
                            
                                # el id del representante lo pasamos a esta variable
                                representante_id = representante_id_retornado
                            
                                # comprobar si hay errores
                                if errores_datos_representante:
                                
                                    self.mostrar_errores_antes_de_guardar(errores_datos_representante, "Información del representante")
                                    return
                                
                                else:
                                    
                                    # esto es para depuracion, es para ver si todo esta correcto
                                    #print("\nRepresentante")
                                    #print(f"ID Representante: {representante_id}")
                                    #print(f"Nombre: {nombre}")
                                    #print(f"Apellido: {apellido}")
                                    #print(f"Direccion de residencia: {direccion_residencia}")
                                    #print(f"Carga familiar: {carga_familiar} {type(carga_familiar)}")
                                    #print(f"Estado civil: {estado_civil}")
                                    
                                    # cuarta parte sin errores
                                    
                                    
                                    ###################################################################
                                    
                                    # Quinta parte
                                    
                                    # proceso para asociar a el representate con el alumno
                                    
                                    # Recordar que para crear este diccionario y poder crear un registro en tb_alumnos
                                    # Tienes que tener los campos de su info básica e info académica para poder
                                    # crear registros en las tablas tb_medidas_alumnos, tb_info_bancaria_alumnos, tb_info_clinica_alumnos
                                    campos_alumno = {
                                        "representante_id": representante_id,
                                        "cedula": campos_datos_alumno_1.get("cedula"),
                                        "primer_nombre": campos_datos_alumno_1.get("primer_nombre"),
                                        "segundo_nombre": campos_datos_alumno_1.get("segundo_nombre"),
                                        "apellido_paterno": campos_datos_alumno_1.get("apellido_paterno"),
                                        "apellido_materno": campos_datos_alumno_1.get("apellido_materno"),
                                        "fecha_nacimiento": campos_datos_alumno_2.get("fecha_nacimiento"),
                                        "lugar_nacimiento": campos_datos_alumno_2.get("lugar_nacimiento"),
                                        "sexo": campos_datos_alumno_1.get("sexo"),
                                        "cma": campos_datos_alumno_2.get("cma"),
                                        "imt": campos_datos_alumno_2.get("imt"),
                                        "relacion_con_rep": campos_datos_alumno_1.get("relacion_con_rep"),
                                        "escolaridad": campos_info_academica.get("escolaridad"),
                                        "procedencia": campos_info_academica.get("procedencia"),
                                        "situacion": campos_datos_alumno_1.get("situacion")
                                    }
                                    
                                    # Acá guardo el alumno_id que retorno al crear un registro en la tabla tb_alumnos
                                    # y lo uso para asociarlo a las demás tablas        
                                    alumno_id = alumno_servicio.registrar_alumno(campos_alumno)
                                    
                                    print(alumno_id)
                                    
                                    
                                    
                                    ###########################################################################
                                    
                                    # sexta parte
                                    # Info medidas del alumno
                                    
                                    # vamos guardando los valores de los inputs en las varibles
                                    estatura = None
                                    peso = None
                                    talla_camisa = self.input_talla_camisa.text().strip()
                                    talla_pantalon = None
                                    talla_zapatos = None
                                    
                                    estatura = self.de_str_a_int_o_float(estatura, self.input_estatura, float)
                                    peso = self.de_str_a_int_o_float(peso, self.input_peso, float)
                                    talla_pantalon = self.de_str_a_int_o_float(talla_pantalon, self.input_talla_pantalon, int)
                                    talla_zapatos = self.de_str_a_int_o_float(talla_zapatos, self.input_talla_zapatos, int)
                                    
                                    
                                    
                                    campos_medidas_alumno = {
                                        "alumno_id": alumno_id,
                                        "estatura": estatura,
                                        "peso": peso,
                                        "talla_camisa": talla_camisa.upper(),
                                        "talla_pantalon": talla_pantalon,
                                        "talla_zapatos": talla_zapatos
                                    }
                                
                                    errores_medidas_alumnos = medidas_alumno_servicio.validar_campos_medidas_alumnos(
                                        campos_medidas_alumno.get("estatura"),
                                        campos_medidas_alumno.get("peso"),
                                        campos_medidas_alumno.get("talla_camisa"),
                                        campos_medidas_alumno.get("talla_pantalon"),
                                        campos_medidas_alumno.get("talla_zapatos")
                                    )

                                    # comprobamos que no haigan errores
                                    if errores_medidas_alumnos:
                                        
                                        self.mostrar_errores_antes_de_guardar(errores_medidas_alumnos, "Información medidas del alumnos")
                                        return
                                    
                                    else:
                                        
                                        # esto es para debugear y ver si todo esta correcto
                                        
                                        #print("\nMedidas del Alumno")
                                        #print(f"ID Alumno: {alumno_id}")
                                        #print(f"Estatura: {estatura}, {type(estatura)}")
                                        #print(f"Peso: {peso}, {type(peso)}")
                                        #print(f"Talla de camisa: {talla_camisa}, {type(talla_camisa)}")
                                        #print(f"Talla de pantalon: {talla_pantalon}, {type(talla_pantalon)}")
                                        #print(f"Talla de zapatos: {talla_zapatos}, {type(talla_zapatos)}")
                                        
                                        
                                        # sexta parte sin erroes
                                        
                                        #####################################################################################
                                        
                                        # Septima parte
                                        
                                        
                                        # cuentas del alumno y diagnostico del alumno
                                        
                                        # comprobamos si la lista de diagnostico por lo menos tenga un diagnostico registrado
                                        
                                        if not self.lista_carrito_diagnosticos:
                                            
                                            # si no tiene un registro que le muestre un mensaje de que no a registrado un diagnostico para el alumno
                                            QMessageBox.warning(self, "Aviso", f"El alumno {primer_nombre} {apellido_paterno}, no tiene diagnosticos registrados")
                                        
                                        
                                        
                                        # si un o unos diagnostico entonces que siga 
                                        else: 
                                            
                                        
                                            # aqui no va la logica ya que esta en otra funcion
                                            # mas a bajo tiene que registra todo lo que tenga el carrito de cada parte
                                            
                                            ######################################################################################
                                            
                                            # Novena parte 
                                            
                                            # Info especialida / info inscripcion
                                            
                                            
                                            # Incripcion 
                                    
                                            especialidad_id = self.buscar_id_de_la_lista_del_combobox(self.boton_de_especialidad, self.lista_especialidades, 1, 0)
                                            periodo_escolar = str(año_actual) + "-" + str(año_actual + 1)
                                            
                                            
                                            fecha_inscripcion = self.fecha_de_str_a_date(self.dateedit_fecha_ingreso_especialidad.text())
                                            
                                            campos_inscripcion = {
                                                                "num_matricula": None, #Esto es None para que internamente se modifique este valor por el que se va a generar automáticamente
                                                                "alumno_id": alumno_id,
                                                                "especialidad_id": especialidad_id,
                                                                "fecha_inscripcion": fecha_inscripcion,
                                                                "periodo_escolar": periodo_escolar
                                                            }
                                                            
                                            errores_inscripcion = inscripcion_servicio.valdiar_campos_inscripcion(
                                                campos_inscripcion.get("especialidad_id"),
                                                campos_inscripcion.get("fecha_inscripcion"),
                                                campos_inscripcion.get("periodo_escolar")
                                            )
                                            
                                            # comprobamos errores
                                            if errores_inscripcion:
                                                self.mostrar_errores_antes_de_guardar(errores_inscripcion, "Especialidad por inscribir")
                                                return
                                            
                                            else:
                                                
                                                # esto es para debugaer y ver si todo esta correcto
                                                
                                                #print("\nIncripcion alumno")
                                                #print(f"ID alumno: {alumno_id}")
                                                #print(f"ID Especialidad: {especialidad_id}, {type(especialidad_id)}")
                                                #print(f"Fecha de inscripcion: {fecha_inscripcion}, {type(fecha_inscripcion)}")
                                                #print(f"Periodo escolar: {periodo_escolar}")
                                                
                                                # novena parte si errores
                                                
                                                
                                                try:
                                                    
                                                    QApplication.beep()
                                                    self.msg_box.setWindowTitle("Confirmar registro")
                                                    self.msg_box.setText("¿Seguro que quiere hacer este registro?")
                                                    self.msg_box.setIcon(QMessageBox.Question)

                                                    # Mostrar el cuadro de diálogo y esperar respuesta
                                                    self.msg_box.exec_()
                                                    
                                                    # si el boton pulsado es "si" guarda todo
                                                    if self.msg_box.clickedButton() == self.boton_si:
                                                        
                                                        medidas_alumno_servicio.registrar_medidas_alumno(campos_medidas_alumno)
                                    
                                                        # logica para agregar todas las cuentas que estan en la lista al diccionario
                                                        campos_info_bancaria_alumno = {
                                                                            "alumno_id": alumno_id,
                                                                            "tipo_cuenta": None,
                                                                            "num_cuenta": None
                                                                        }
                                                        
                                                        # si la lista de cuentas de banco esta llena
                                                        if self.lista_carrito_cuentas_bancarias:
                                                            
                                                            # quiero que itere cada tupla y me de los valores y los registre
                                                            for cuenta_n in self.lista_carrito_cuentas_bancarias:
                                                                
                                                                campos_info_bancaria_alumno["alumno_id"] = alumno_id
                                                                campos_info_bancaria_alumno["tipo_cuenta"] = cuenta_n[0]
                                                                campos_info_bancaria_alumno["num_cuenta"] = cuenta_n[1]
                                                        
                                                                info_bancaria_alumno_servicio.registrar_info_bancaria_alumno(campos_info_bancaria_alumno)
                                                                
                                                        else:
                                                            
                                                            pass
                                                        
                                                        
                                                        campos_info_clinica_alumno = {
                                                                                "alumno_id": alumno_id,
                                                                                "diagnostico_id": None,
                                                                                "fecha_diagnostico": None,
                                                                                "medico_tratante": None,
                                                                                "certificacion_discap": None,
                                                                                "fecha_vencimiento_certif": None,
                                                                                "medicacion": None
                                                                            }
                                                        
                                                        # si hay diagnosticos en el "carrito" de diagnosticos
                                                        if self.lista_carrito_diagnosticos:
                                                            
                                                            for diagnostico in self.lista_carrito_diagnosticos:
                                                                
                                                                
                                                                campos_info_clinica_alumno["alumno_id"] = alumno_id
                                                                campos_info_clinica_alumno["diagnostico_id"] = diagnostico[0]
                                                                campos_info_clinica_alumno["medico_tratante"] = diagnostico[2]
                                                                campos_info_clinica_alumno["fecha_diagnostico"] = diagnostico[3]
                                                                campos_info_clinica_alumno["fecha_vencimiento_certif"] = diagnostico[4]
                                                                campos_info_clinica_alumno["medicacion"] = diagnostico[5]
                                                                campos_info_clinica_alumno["certificacion_discap"] = diagnostico[6]
                                                                
                                                                            
                                                                info_clinica_alumno_servicio.registrar_info_clinica_alumno(campos_info_clinica_alumno)
                                                                
                                                            
                                                            
                                                        else:
                                                            
                                                            QMessageBox.warning(self, "Aviso", f"El joven {self.input_primer_nombre.text()} {self.input_apellido_paterno.text()}, no tiene diagnosticos registrados")
                                                                    
                                                            
                                                        inscripcion_servicio.registrar_inscripcion(campos_inscripcion)
                                                        
                                                        
                                                        QMessageBox.information(self, "Bien hecho", "Registro exitoso")
                                                    
                                                    
                                                    
                                                    
                                                    
                                                        # Parte final si No esta registrado el representante
                                                            
                                                        # Limpiar todos los inputs
                                                        self.limpiar_los_valores_de_los_inputs(self.lista_de_inputs, self.lista_de_radiobuttons)
                                                        
                                                        pantalla_tabla_alumnos = self.stacked_widget.widget(2)
            
                                                        pantalla_tabla_alumnos.actualizar_tabla(1)
                                                        pantalla_tabla_alumnos.actualizar_lista_busqueda()
                                                                                                                
                                                        pantalla_tabla_alumnos.boton_especialidades.setCurrentIndex(0)
                                                    
                                                        self.stacked_widget.setCurrentIndex(2)
                                                    
                                                    ## si el boton "no" es pulsadoo, no hace nada
                                                    elif self.msg_box.clickedButton() == self.boton_no:
                                                        return

                                                except Exception as e:
                                                    
                                                    print("Error al tratar de guardar la informacion del alumno")
                                                    return
                                                
                                            
        
        except Exception as e:
            
            FuncionSistema.mostrar_errores_por_excepcion(e, "guardar_informacion_alumno")
            
            
            
    def editar_datos_alumno(self, alumno_id: int):
        
        """
            Este metodo sirve para editar los datos del alumno
            se hace desde la pantalla del formulario de registro del alumno para aprovechar algunos metodos ya prestablecidos
        
        """
        self.boton_finalizar.setText("Editar")
        self.boton_finalizar.clicked.disconnect()
        self.boton_finalizar.clicked.connect(lambda _: self.confirmar_edicion_datos_alumno(alumno_id))
        
        info_basica = alumno_servicio.obtener_alumno_por_id(alumno_id)
        info_inscripcion = inscripcion_servicio.obtener_inscripcion_por_id(alumno_id)
        
        print("--------------------------------------------------------------------")
        print(f"Edicion de los datos del alumno/a: {info_basica[2]} {info_basica[5]}")
        # 1. Información Basica
        try:
             
            #(1, '30466351', 'Ariana', 'G', None, 'Mijares', 'G', '2000-08-21', 25, 'Barcelona', 'F', 1, 1, '2025-09-06', 'Ingresado')
            #(1, '30466351', 'Ariana', 'Mijares', 'Artesanía', 'MAT-1234567', '2025-09-06', 0, '2025-2026', 'Ingresado', 'Padre')
            self.input_cedula.setText(info_basica[1])
            self.input_primer_nombre.setText(info_basica[2])
            self.input_segundo_nombre.setText(info_basica[3])
            self.input_tercer_nombre.setText("" if not info_basica[4] else info_basica[4])
            self.input_apellido_paterno.setText(info_basica[5])
            self.input_apellido_materno.setText("" if not info_basica[6] else info_basica[6])
            self.input_relacion_con_representante.setText(info_inscripcion[10])
            
            self.dateedit_fecha_nacimiento.setDate(QDate.fromString(info_basica[7], 'yyyy-MM-dd'))
            
            self.input_lugar_de_nacimiento.setText(info_basica[9])
            
            if info_basica[10] == 'M':
                self.input_sexo_masculino.setChecked(True)
                
            elif info_basica[10] == 'F':
                
                self.input_sexo_femenino.setChecked(True) 
                
                
            
            if info_basica[11] == 1:
                
                self.input_cma_si.setChecked(True)
                
            elif info_basica[11] == 0:
                
                self.input_cma_no.setChecked(True)
                
            
            if info_basica[12] == 1:
                
                self.input_imt_si.setChecked(True)
                
            elif info_basica[12] == 0:
                
                self.input_imt_no.setChecked(True)
                
                
            self.dateedit_fecha_ingreso_tela.setDate(QDate.fromString(info_basica[13], 'yyyy-MM-dd'))
            
            self.input_situacion.setText(info_basica[14])
                            
        except:
            
            print("Error al cargar la Informacion basica")
            
        else:
            
            print("1. La informacion basica cargo correctamente")
        
        
        # 2. Info academica
        try:
            info_academica = alumno_servicio.obtener_info_academica_alumno(alumno_id)
            
            self.input_escolaridad.setText(info_academica[1])
            self.input_procendencia.setText(info_academica[2])
            
        except:
            
            print("Error al cargar la Informacion academica")
            
        else:
            
            print("2. La informacion academica cargo correctamente")
        
        
        
        
        # 3. Info medidas del alumno
        try:

            # (1, 1, 1.42, 56.9, 'M', 30, 36)
            info_medidas = medidas_alumno_servicio.obtener_medidas_alumno_por_id(alumno_id)
            self.input_estatura.setText("" if not info_medidas[2] else str(info_medidas[2]))
            self.input_peso.setText("" if not info_medidas[3] else str(info_medidas[3]))
            self.input_talla_camisa.setText("" if not info_medidas[4] else str(info_medidas[4]))
            self.input_talla_pantalon.setText("" if not info_medidas[5] else str(info_medidas[5]))
            self.input_talla_zapatos.setText("" if not info_medidas[6] else str(info_medidas[6]))
            
        except:
            
            print("Error al cargar la Informacion de las medidas")
            
        else:
            
            print("3. La informacion medidas del alumno cargo correctamente")



        # 4. Info del representate
        try:
            
            info_representante = alumno_servicio.obtener_datos_representante(alumno_id)
            #print(info_representante)
            #(1, 1, '12345', 'Juan', 'Mijares', 'Av. Juan de Urpín , C/ Rocal nº 21-18, Barcelona', '04142878970', None, 4, 'Casado/a')
            
            self.input_buscar_por_cedula.setText(info_representante[2])
            self.input_nombre_del_representante.setText(info_representante[3])
            self.input_apellido_del_representante.setText(info_representante[4])
            self.input_direccion_residencia.setText(info_representante[5])
            self.input_numero_de_telefono.setText(info_representante[6])
            self.input_numero_de_telefono_adicional.setText("" if info_representante[7] == None else info_representante[7])
            self.input_carga_familiar.setText(str(info_representante[8]))
            self.input_estado_civil.setText(info_representante[9])
            
        except:
            
            print("La informacion del representante no cargo correctamente")
            
        else:
        
            print("4. La informacion del representante cargo correctamente")
        
        
        # 5. info bancaria
        try:
            info_banacaria = info_bancaria_alumno_servicio.obtener_info_bancaria_por_alumno_id(alumno_id)
            
            self.lista_carrito_cuentas_bancarias.clear()
            
            for cuenta_bancaria in info_banacaria:
                
                self.lista_carrito_cuentas_bancarias.append(cuenta_bancaria)
                
                texto_mostrar = cuenta_bancaria[2] + " " + cuenta_bancaria[3]
                
                self.agregar_elementos_a_la_vista_previa(self.vista_previa_cuentas_bancarias, self.lista_carrito_cuentas_bancarias, texto_a_mostrar= texto_mostrar, editando=True)
                
        except:
            
            #FuncionSistema.mostrar_errores_por_excepcion(e, "Informacion bancaria")
            print("No posee informacion bancaria")
            
        else:
            
            print("5. La informacion bancaria del alumno cargo correctamente")
            
            
        # 6. Diagnostico del alumno
        try:
            info_clinica = info_clinica_alumno_servicio.obtener_info_clinica_por_alumno_id(alumno_id)
            #(2, 2, 'Espectro Autista leve', datetime.date(2013, 5, 14), 'Dr Jose', 'D-365515', datetime.date(2016, 11, 15), 'Carbamazepina', None)
            self.lista_carrito_diagnosticos.clear()
            
            for diagnostico in info_clinica:
                
                self.lista_carrito_diagnosticos.append(diagnostico)
                
                self.agregar_elementos_a_la_vista_previa(self.vista_previa_diagnostico, self.lista_carrito_diagnosticos, diagnostico[2], editando= True )
                
        except:
            print("error al cargar los diagnosticos del alumno")
        else:
            
            print("6. Los diagnosticos cargaron correctamente")
            
        
        # 7. Especialidad por inscribir
        try:
            
            #(1, '30466351', 'Ariana', 'Mijares', 'Artesanía', 'MAT-1234567', '2025-09-06', 0, '2025-2026', 'Ingresado', 'Padre')
            
            self.boton_de_especialidad.setCurrentText(info_inscripcion[4])
            self.dateedit_fecha_ingreso_especialidad.setDate(QDate.fromString(info_inscripcion[6], 'yyyy-MM-dd'))
            
            
        except:
            
            print("la especialidad por inscribir no cargo correctamente")
            
        else:
            
            print("7. la especialidad por inscribir cargo correctamente")
            
            
    def confirmar_edicion_datos_alumno(self, alumno_id):
        """
            Este metodo srve para tener todos los datos de los inputs subir o que se edito a la base de datos
        
        """
        
        
            
        try:
            
            ################################################################################################
            # Primera parte
            # Informacion del alumno
            
            # vamos guardando los valores de los inputs en las varibles
            
            primer_nombre = self.input_primer_nombre.text().strip().capitalize()
            segundo_nombre = FuncionSistema.comprobar_si_hay_valor(self.input_segundo_nombre.text().strip().capitalize())
            tercer_nombre = FuncionSistema.comprobar_si_hay_valor(self.input_tercer_nombre.text().strip().capitalize())
            
            
            
            apellido_paterno = self.input_apellido_paterno.text().strip().capitalize()
            apellido_materno = FuncionSistema.comprobar_si_hay_valor(self.input_apellido_materno.text().strip().capitalize())
            cedula = self.input_cedula.text().strip()
            relacion_con_rep = self.input_relacion_con_representante.text().strip().capitalize()
            situacion = self.input_situacion.text().strip().capitalize()
            
            fecha_ingreso_institucion = self.fecha_de_str_a_date(self.dateedit_fecha_ingreso_tela.text())
            
            
            if self.input_sexo_masculino.isChecked():
                
                sexo = "M"
                
            elif self.input_sexo_femenino.isChecked():
                
                sexo = "F"
                
            else:
                
                sexo = None
            
            campos_datos_alumno_1 = {
                "primer_nombre": primer_nombre,
                "segundo_nombre": segundo_nombre,
                "tercer_nombre": tercer_nombre,
                "apellido_paterno": apellido_paterno,
                "apellido_materno": apellido_materno,
                "cedula": cedula,
                "relacion_con_rep": relacion_con_rep,
                "sexo": sexo,
                "situacion": situacion,
                "fecha_ingreso_institucion": fecha_ingreso_institucion
                }
            
            errores_primera_info_alumno = alumno_servicio.validar_campos_primera_info_alumno(
                    campos_datos_alumno_1.get("cedula"),
                    campos_datos_alumno_1.get("primer_nombre"),
                    campos_datos_alumno_1.get("segundo_nombre"),
                    campos_datos_alumno_1.get("tercer_nombre"),
                    campos_datos_alumno_1.get("apellido_paterno"),
                    campos_datos_alumno_1.get("apellido_materno"),
                    campos_datos_alumno_1.get("relacion_con_rep"),
                    campos_datos_alumno_1.get("fecha_ingreso_institucion"),
                    alumno_id
                )
            
            # verificamos que no hay errores
            if errores_primera_info_alumno:
                
                self.mostrar_errores_antes_de_guardar(errores_primera_info_alumno, "Información del alumno")
                return
            
            else:
                # esto es para depuracion, es para ver si todo esta correcto
                #print("\nAlumno")
                #print(f"Nombres: {primer_nombre}, {segundo_nombre}")
                #print(f"Apellidos: {apellido_paterno}, {apellido_materno}")
                #print(f"Relacion con el representante: {relacion_con_rep}")
                
                # Primera parte sin errores
                
                ############################################################################################3
                
                # segunda parte
                # Info alumno parte 2
                
                # vamos guardando los valores de los inputs en las varibles
                
                cma = None
                imt = None
                
                if self.input_cma_si.isChecked():
                    
                    cma = True
                    
                elif self.input_cma_no.isChecked():
                    
                    cma = False
                    
                
                else:
                    
                    cma = None
                    
                    
                if self.input_imt_si.isChecked():
                    imt = True
                    
                elif self.input_imt_no.isChecked():
                    imt = False
                    
                else:
                    
                    imt = None
                
                
                    
                fecha_nacimiento = self.fecha_de_str_a_date(self.dateedit_fecha_nacimiento.text())
                    
                
                
                lugar_nacimiento = self.input_lugar_de_nacimiento.text()
                
                campos_datos_alumno_2 = {
                    "cma": cma,
                    "imt": imt,
                    "fecha_nacimiento": fecha_nacimiento,
                    "lugar_nacimiento": lugar_nacimiento
                    }
                
                errores_segunda_info_alumno = alumno_servicio.validar_campos_segunda_info_alumno(
                campos_datos_alumno_2.get("fecha_nacimiento"),
                campos_datos_alumno_2.get("lugar_nacimiento")
                )
                
                
                # comprobamos si no hay errores
                # si los hay que muestre el mensaje en la pantalla
                if errores_segunda_info_alumno:
                
                    self.mostrar_errores_antes_de_guardar(errores_segunda_info_alumno, "Información del alumno")
                    return
                
                else:
                    
                    # esto es para depuracion, es para ver si todo esta correcto
                    #print("\nAlumno parte 2")
                    #print(f"cma: {cma}")
                    #print(f"imt: {imt}")
                    #print(f"fecha de nacimiento {fecha_nacimiento}")
                    #print(f"lugar de nacimiento: {lugar_nacimiento}")
                    
                    # segunda parte sin errores
                    
                    ########################################################################################3
                    
                    
                    # tercera parte
                    
                    
                    # Info academica
            
                    escolaridad = self.input_escolaridad.text().strip()
                    procedencia = self.input_procendencia.text().strip()
                    
                    campos_info_academica = {
                                "escolaridad": escolaridad,
                                "procedencia": procedencia
                            }
                                    
                    errores_info_academica = alumno_servicio.validar_info_academica(
                        campos_info_academica.get("escolaridad"),
                        campos_info_academica.get("procedencia")
                    )
                    
                    # comprobamos si no hay errores
                    if errores_info_academica:
                        self.mostrar_errores_antes_de_guardar(errores_info_academica, "Información académica")
                        return
                    
                    else:
                        
                        # esto es para depuracion, es para ver si todo esta correcto
                        #print("\nInfo Académica Alumno")
                        #print(f"procedencia: {procedencia} ")
                        #print(f"escolaridad: {escolaridad} ")
                        
                        # Tercera parte sin erroes
                        
                    
                        #######################################################################################################
                        
                        # Cuarta parte
                        
                        # info representante
                    
                    
                        # Primero comprobamos si el usuario comprobo que el representante existe o no
                        
                        # comprobacion
                        if not self.comprobacion:
                            
                            QMessageBox.warning(self, "Aviso", "Tiene que comprobar si el representante esta registrado o no")
                            return
                        
                        # si hizo la comprobacion, puede seguir con lo demas 
                        else:  
                            
                            
                            # si el representante esta registrado
                            if self.representante_registrado:
                                
                                # solo quiero el id del representante
                                representante_id = self.representante_id
                                
                                
                                # Quinta parte
                                
                                # proceso para asociar a el representate con el alumno
                                
                                # Recordar que para crear este diccionario y poder crear un registro en tb_alumnos
                                # Tienes que tener los campos de su info básica e info académica para poder
                                # crear registros en las tablas tb_medidas_alumnos, tb_info_bancaria_alumnos, tb_info_clinica_alumnos
                                campos_alumno = {
                                    "representante_id": representante_id,
                                    "cedula": campos_datos_alumno_1.get("cedula"),
                                    "primer_nombre": campos_datos_alumno_1.get("primer_nombre"),
                                    "segundo_nombre": campos_datos_alumno_1.get("segundo_nombre"),
                                    "tercer_nombre": campos_datos_alumno_1.get("tercer_nombre"),
                                    "apellido_paterno": campos_datos_alumno_1.get("apellido_paterno"),
                                    "apellido_materno": campos_datos_alumno_1.get("apellido_materno"),
                                    "fecha_nacimiento": campos_datos_alumno_2.get("fecha_nacimiento"),
                                    "lugar_nacimiento": campos_datos_alumno_2.get("lugar_nacimiento"),
                                    "sexo": campos_datos_alumno_1.get("sexo"),
                                    "cma": campos_datos_alumno_2.get("cma"),
                                    "imt": campos_datos_alumno_2.get("imt"),
                                    "relacion_con_rep": campos_datos_alumno_1.get("relacion_con_rep"),
                                    "escolaridad": campos_info_academica.get("escolaridad"),
                                    "procedencia": campos_info_academica.get("procedencia"),
                                    "situacion": campos_datos_alumno_1.get("situacion")
                                }
                                
                                # Acá guardo el alumno_id que retorno al crear un registro en la tabla tb_alumnos
                                # y lo uso para asociarlo a las demás tablas        
                                
                                
                                print(alumno_id)
                                
                                
                                
                                ###########################################################################
                                
                                # sexta parte
                                # Info medidas del alumno
                                
                                # vamos guardando los valores de los inputs en las varibles
                                estatura = None
                                peso = None
                                talla_camisa = self.input_talla_camisa.text().strip()
                                talla_pantalon = None
                                talla_zapatos = None
                                
                                estatura = self.de_str_a_int_o_float(estatura, self.input_estatura, float)
                                peso = self.de_str_a_int_o_float(peso, self.input_peso, float)
                                talla_pantalon = self.de_str_a_int_o_float(talla_pantalon, self.input_talla_pantalon, int)
                                talla_zapatos = self.de_str_a_int_o_float(talla_zapatos, self.input_talla_zapatos, int)
                                
                                
                                
                                campos_medidas_alumno = {
                                    "alumno_id": alumno_id,
                                    "estatura": estatura,
                                    "peso": peso,
                                    "talla_camisa": talla_camisa.upper(),
                                    "talla_pantalon": talla_pantalon,
                                    "talla_zapatos": talla_zapatos
                                }
                            
                                errores_medidas_alumnos = medidas_alumno_servicio.validar_campos_medidas_alumnos(
                                    campos_medidas_alumno.get("estatura"),
                                    campos_medidas_alumno.get("peso"),
                                    campos_medidas_alumno.get("talla_camisa"),
                                    campos_medidas_alumno.get("talla_pantalon"),
                                    campos_medidas_alumno.get("talla_zapatos")
                                )

                                # comprobamos que no haigan errores
                                if errores_medidas_alumnos:
                                    
                                    self.mostrar_errores_antes_de_guardar(errores_medidas_alumnos, "Información medidas del alumnos")
                                    return
                                
                                else:
                                    
                                    # esto es para debugear y ver si todo esta correcto
                                    
                                    #print("\nMedidas del Alumno")
                                    #print(f"ID Alumno: {alumno_id}")
                                    #print(f"Estatura: {estatura}, {type(estatura)}")
                                    #print(f"Peso: {peso}, {type(peso)}")
                                    #print(f"Talla de camisa: {talla_camisa}, {type(talla_camisa)}")
                                    #print(f"Talla de pantalon: {talla_pantalon}, {type(talla_pantalon)}")
                                    #print(f"Talla de zapatos: {talla_zapatos}, {type(talla_zapatos)}")
                                    
                                    
                                    # sexta parte sin erroes
                                    
                                    #####################################################################################
                                    
                                    # Septima parte
                                    
                                    
                                    # cuentas del alumno y diagnostico del alumno
                                    
                                    # comprobamos si la lista de diagnostico por lo menos tenga un diagnostico registrado
                                    
                                    if not self.lista_carrito_diagnosticos:
                                        
                                        # si no tiene un registro que le muestre un mensaje de que no a registrado un diagnostico para el alumno
                                        QMessageBox.warning(self, "Aviso", f"El alumno {primer_nombre} {apellido_paterno}, no tiene diagnosticos registrados")
                                    
                                    
                                    
                                    # si un o unos diagnostico entonces que siga 
                                    else: 
                                        
                                    
                                        # aqui no va la logica ya que esta en otra funcion
                                        # mas a bajo tiene que registra todo lo que tenga el carrito de cada parte
                                        
                                        ######################################################################################
                                        
                                        # Novena parte 
                                        
                                        # Info especialida / info inscripcion
                                        
                                        
                                        # Incripcion 
                                
                                        especialidad_id = self.buscar_id_de_la_lista_del_combobox(self.boton_de_especialidad, self.lista_especialidades, 1, 0)
                                        periodo_escolar = str(año_actual) + "-" + str(año_actual + 1)
                                        
                                        
                                        
                                        fecha_inscripcion = self.fecha_de_str_a_date(self.dateedit_fecha_ingreso_especialidad.text())
                                        
                                        campos_inscripcion = {
                                                            "num_matricula": None, #Esto es None para que internamente se modifique este valor por el que se va a generar automáticamente
                                                            "alumno_id": alumno_id,
                                                            "especialidad_id": especialidad_id,
                                                            "fecha_inscripcion": fecha_inscripcion,
                                                            "periodo_escolar": periodo_escolar
                                                        }
                                                        
                                        errores_inscripcion = inscripcion_servicio.valdiar_campos_inscripcion(
                                            campos_inscripcion.get("especialidad_id"),
                                            campos_inscripcion.get("fecha_inscripcion"),
                                            campos_inscripcion.get("periodo_escolar")
                                        )
                                        
                                        # comprobamos errores
                                        if errores_inscripcion:
                                            self.mostrar_errores_antes_de_guardar(errores_inscripcion, "Especialidad por inscribir")
                                            return
                                        
                                        else:
                                            
                                            # esto es para debugaer y ver si todo esta correcto
                                            
                                            #print("\nIncripcion alumno")
                                            #print(f"ID alumno: {alumno_id}")
                                            #print(f"ID Especialidad: {especialidad_id}, {type(especialidad_id)}")
                                            #print(f"Fecha de inscripcion: {fecha_inscripcion}, {type(fecha_inscripcion)}")
                                            #print(f"Periodo escolar: {periodo_escolar}")
                                            
                                            # novena parte si errores
                                            
                                            
                                            try:
                                                
                                                QApplication.beep()
                                                self.msg_box.setWindowTitle("Confirmar registro")
                                                self.msg_box.setText("¿Seguro que quiere hacer este registro?")
                                                self.msg_box.setIcon(QMessageBox.Question)

                                                # Mostrar el cuadro de diálogo y esperar respuesta
                                                self.msg_box.exec_()
                                                
                                                # si el boton pulsado es "si" guarda todo
                                                if self.msg_box.clickedButton() == self.boton_si:
                                                    alumno_servicio.actualizar_alumno(alumno_id, campos_alumno)
                                                    """
                                                    medidas_alumno_servicio.registrar_medidas_alumno(campos_medidas_alumno)
                                
                                                    # logica para agregar todas las cuentas que estan en la lista al diccionario
                                                    campos_info_bancaria_alumno = {
                                                                        "alumno_id": alumno_id,
                                                                        "tipo_cuenta": None,
                                                                        "num_cuenta": None
                                                                    }
                                                    
                                                    # si la lista de cuentas de banco esta llena
                                                    if self.lista_carrito_cuentas_bancarias:
                                                        
                                                        # quiero que itere cada tupla y me de los valores y los registre
                                                        for cuenta_n in self.lista_carrito_cuentas_bancarias:
                                                            
                                                            campos_info_bancaria_alumno["alumno_id"] = alumno_id
                                                            campos_info_bancaria_alumno["tipo_cuenta"] = cuenta_n[0]
                                                            campos_info_bancaria_alumno["num_cuenta"] = cuenta_n[1]
                                                    
                                                            info_bancaria_alumno_servicio.registrar_info_bancaria_alumno(campos_info_bancaria_alumno)
                                                            
                                                    else:
                                                        
                                                        pass
                                                    
                                                    
                                                    campos_info_clinica_alumno = {
                                                                            "alumno_id": alumno_id,
                                                                            "diagnostico_id": None,
                                                                            "fecha_diagnostico": None,
                                                                            "medico_tratante": None,
                                                                            "certificacion_discap": None,
                                                                            "fecha_vencimiento_certif": None,
                                                                            "medicacion": None
                                                                        }
                                                    
                                                    # si hay diagnosticos en el "carrito" de diagnosticos
                                                    if self.lista_carrito_diagnosticos:
                                                        
                                                        for diagnostico in self.lista_carrito_diagnosticos:
                                                            
                                                            
                                                            campos_info_clinica_alumno["alumno_id"] = alumno_id
                                                            campos_info_clinica_alumno["diagnostico_id"] = diagnostico[0]
                                                            campos_info_clinica_alumno["medico_tratante"] = diagnostico[2]
                                                            campos_info_clinica_alumno["fecha_diagnostico"] = diagnostico[3]
                                                            campos_info_clinica_alumno["fecha_vencimiento_certif"] = diagnostico[4]
                                                            campos_info_clinica_alumno["medicacion"] = diagnostico[5]
                                                            campos_info_clinica_alumno["certificacion_discap"] = diagnostico[6]
                                                            
                                                                        
                                                            info_clinica_alumno_servicio.registrar_info_clinica_alumno(campos_info_clinica_alumno)
                                                            
                                                            
                                                            
                                                    else:
                                                        
                                                        QMessageBox.warning(self, "Aviso", f"El joven {self.input_primer_nombre.text()} {self.input_apellido_paterno.text()}, no tiene diagnosticos registrados")
                                                                
                                                    
                                                    """
                                                        
                                                    inscripcion_servicio.actualizar_inscripcion(campos_inscripcion)
                                                    
                                                    QMessageBox.information(self, "Bien hecho", "Registro exitoso")
                                                
                                                    # Parte final si esta registrado el representante
                                                            
                                                    # Limpiar todos los inputs
                                                    self.limpiar_los_valores_de_los_inputs(self.lista_de_inputs, self.lista_de_radiobuttons)
                                                    
                                                    pantalla_tabla_alumnos = self.stacked_widget.widget(2)
        
                                                    pantalla_tabla_alumnos.actualizar_tabla(1)
                                                    pantalla_tabla_alumnos.actualizar_lista_busqueda()
                                                    
                                                    pantalla_tabla_alumnos.boton_especialidades.setCurrentIndex(0)
                                                
                                                    self.stacked_widget.setCurrentIndex(2)
                                                
                                                ## si el boton "no" es pulsadoo, no hace nada
                                                elif self.msg_box.clickedButton() == self.boton_no:
                                                    return
                                                
                                            except Exception as e:
                                                
                                                self.mostrar_errores_por_excepcion(e)
                                                return
                                            
        except Exception as e:
            
            FuncionSistema.mostrar_errores_por_excepcion(e, "confirmar_edicion_datos_alumno")
            
        
        else:
            
            print("No hubo problemas al tomar los datos")