import traceback
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import (QPropertyAnimation, QEasingCurve, QFile, QTextStream, QTime)
from PyQt5.QtGui import QIcon, QPixmap
from datetime import datetime
from PIL import Image
from typing import Optional
from openpyxl.utils import range_boundaries
import platform
import os
import io
from itertools import zip_longest

"""
Este archivo contiene todas las funciones que suelen repetirse, esto ayuda a evitar copiar y pegar
codigo que ya esta escrito. Con esto solo llamamos la funcion, pasamos parametro y listo
"""

class FuncionesDelSistema:
    def __init__(self):
        
        # Variables axuliares
        self.estado_sidebar = True
        
        self.id_usuario = None
        
    # Metodo para bloquear los botones del side bar
    def bloquear_botones_sidebar(self, indice_stackedwidget: int, pantallas_importantes: tuple, botones_sidebar: tuple) -> None:
        
        """
            Este metodo sirve especificamente para boloquear los botones del sidebar cuando estan en una pantalla importante.
            
            Lo que hace este metodo como tal es verificar si el indice actual del stackedwideget es igual al de una de las pantallas
            que son importantes, si es una pantalla importante se bloquean los botones del sidebar para evitar errores de insersion de datos
            
            **Ejemplo**
            
            lista_pantallas_importantes = (1,8,0,6) # los indices de las pantallas que se consideren importantes que se deje comentado en el main.py
            
            El el indice actual del **stackedwidger** es uno de los indices de la **lista_pantallas_importantes**
            
            si lo es bloquea los botones
            
            si no lo es deja los botones habilitados, o si estan deshabilitados habilitalos
        
        """
        
        if indice_stackedwidget in pantallas_importantes:
            
            for boton in botones_sidebar:
                
                boton.setDisabled(True)
                
        else:
            
            for boton in botones_sidebar:
                
                boton.setEnabled(True)
                
                
                
                
    # Metodo para salir al login con el sidebar
    def salir_al_login_con_sidebar(self, stacked_widget, sidebar):
        
        """
            Este metodo es para salir al login usando el boton de "salir" que esta en el sidebar,
            este metodo lo que hace es arreglar el tamaño el siderbar y hacer que vuelva a su estado inicial.
            
            **Su estado inicial seria que:**
            
            - Su tamaño es de 190px de ancho por defecto, ya que si nos vamos al login sin hacer eso, el sidebar se vera mal
            - La variable self.estado_sidebar vuelve a tener el valor de True, lo que hace que se reproduzca la animacion de minimizar
            
        """
        
        
        
        self.moverse_de_pantalla(stacked_widget, 0)
        
        sidebar.setFixedWidth(190)
        
        self.estado_sidebar = True
    
    
    
    
    
    # Metodo para moverse entre pantallas
    def moverse_de_pantalla(self, stacked_widget , indice: int) -> None:
        """
        
            Este metodo sirve para moverse de pantalla, se le pasa la variable donde se tiene el QStackedWidget y el indice de la pantalla a donde queremos ir.
        
            Como estamos trabajando con stackedWidget este metodo funciona asi:
            
            boton.clicked.connect(lambda: moverse_de_pantalla(self.stacked_widget, 3 ) # nos dirige a la pantalla de formulario alumno
            
        """
        try:
            stacked_widget.setCurrentIndex(indice)
            
        except Exception as e:
            
            self.mostrar_errores_por_excepcion(e, "moverse_de_pantalla")
            
            
            
            
    # Metodo para buscar el id por la cedula del estudiante o empleado
    def buscar_id_por_cedula(self, cedula: str, lista_personas_actual: list) -> int:
        
        """
            Este metodo sirve para buscar el id segun la cedula del estudiante o empleado.
            
            Se busca la cedula ya que es un numero que normalmente no se repite.
            
            Con el ID del estudiante o empleado podemos utilizar varias funciones que estan hechas en la base de datos
            a partir del ID
            
            Normalmente la lista que suelta la base de datos se ve asi
            
            
            recorremos cada tupla y preguntamos si la cedula que nos pasaron esta, retornamos el ID de la persona
            
            
            **Ejemplo**
            
            lista_empleados = [ (1, 'DOUGLAS', 'JOSE', None, 'MARQUEZ', 'BETANCOURT', '17536256', '1983-05-17', 42, 'Activo', 'M', 1),
                                (2, 'ENMANUEL', 'JESÚS', None, 'GARCIA', 'RAMOS', '5017497', '1956-10-10', 69, 'Activo', 'M', 1),
                                (3, 'ROSMARY', 'DEL VALLE', None, 'SALAS', 'JIMENEZ', '18128319', '1986-10-28', 38, 'Activo', 'F', 0),
                                (4, 'JOSE', 'ALEJANDRO', None, 'SALAS', 'JIMENEZ', '16788123', '1985-10-28', 39, 'Activo', 'F', 0), 
                                (5, 'JOSE', 'ALEJANDRO', None, 'SALAS', 'JIMENEZ', '26788123', '1985-10-28', 39, 'Activo', 'F', 0)]
            
            cedula = "18128319"
            
            
            id_empleado = buscar_id_por_cedula(cedula, lista_empleados) # Tiene como valor 3
            
            
            
            
        """
        
        try:
            
            # cada persona es una tupla como se ve en el comentario anterior
            for persona in lista_personas_actual:
            
                # preguntamos si la cedula esta en la tupla recorrida
                if cedula in persona:
                    
                    # Normalmente el indice en donde se encuentra el id en la tupla es en la posicion 0
                    id_persona = persona[0]
                    
                    # retornamos el id encontrado
                    return id_persona
                
                
                
                    
            
            
        
        
        except Exception as e:
            
            self.mostrar_errores_por_excepcion(e, "buscar_id_por_cedula")
        
        
        
        
    # Metodo para cargar catalogo en los combobox
    def cargar_elementos_para_el_combobox(self, lista_catalogo: list, boton_desplegable, indice_nombre_elemento:int, anadir_seleccionar_aqui: int = 0, texto_personalizdo:str=None) -> None:
        """
            Este metodo sirve para cargar los elementos de una lista a un combobox o actualizar el combobox, indicandole:
            
            - La lista con los elementos a añadir
            - El boton desplegable (el QCombobox)
            - El indice donde se encuetra el nombre del elemento
            - Si se quiere colocar en el boton la palabra (Seleccionar aqui) es opcional para algunos casos y esta se
            basa en colocar 0 y 1, 0 si no se quiere colocar esa palabra o 1 si desea que aparezca
            
            **Ejemplo**
            
            lista_catologo = [(1, nombre_item_1), (2, nombre_item_2), (3, nombre_item_3), etc.....]
            
            boton_desplegable = QCombobox()
            
            funciones_comunes.cargar_elementos_para_el_combobox(lista_catalogo, boton_desplegable, 1, 1)  
            
            
            _____________________
            | seleccione aqui u | (al deplegar el boton)
            _____________________
            * nombre_item_1     *
            * nombre_item_2     *
            * nombre_item_3     *
            * nombre_item_n     *
            
            
            Si se quiere actualizar porque hay un nuevo elemento en la base de datos, solo se vuelve a llamar la funcion
            
        
        """
        try:    
            
            boton_desplegable.clear()
            
            if anadir_seleccionar_aqui == 1:
                # agregamos la palabra seleccionar aqui
                boton_desplegable.addItem("Seleccione aqui")
                
                
            elif anadir_seleccionar_aqui == 0:
                
                if texto_personalizdo != None:
                
                    boton_desplegable.addItem(texto_personalizdo)
            
            elif anadir_seleccionar_aqui > 1:
                
                print("Numero fuera del rango establecido")
                
            
                
            # Iteramos cada elemento de la lista
            for elemento_iterado in lista_catalogo:
                
                # le indicamos con el indice que pedimos que vaya agregando el nombre del elemento
                boton_desplegable.addItem(elemento_iterado[indice_nombre_elemento])
                
            boton_desplegable.setCurrentIndex(0)
        
        except Exception as e:
            
            self.mostrar_errores_por_excepcion(e, "Cargar elementos para el combobox")
            
    
    def obtener_id_del_elemento_del_combobox(self, boton_seleccionado, lista_elementos: list, indice_nombre_del_elemento: int, indice_id_del_elemento:int, seleccionar_aqui: bool = False ) -> int :
            
        """
            Este metodo sirve buscar el id del elemento seleccionado en el combobox
            
            En este metodo se le pasa:
            
            - El combobox donde se selecciono el elemento
            - La lista de elementos que se uso para cargar el combobox
            - El indice donde se encuentra el nombre del elemento en la lista
            - El indice donde se encuentra el id del elemento en la lista
            - Si el combobox tiene la palabra "seleccionar aqui" en la posicion 0, se le pasa True si la tiene, si no se le pasa False
            
            Este metodo funciona asi:
            
            1. el usuario selecciona un elemento del combobox
            2. se obtiene el texto del elemento seleccionado
            3. se recorre la lista de elementos (la misma que se uso para cargar el combobox)
            4. se compara el texto seleccionado con el nombre de cada elemento en la lista
            5. cuando se encuentra una coincidencia, se obtiene el id correspondiente de ese elemento
            6. se retorna el id encontrado
            
            **Ejemplo**

            >>> lista_especialidades = [(1, 'Medicina General'), (2, 'Enfermeria'), (3, 'Odontologia')]
            
            >>> boton_seleccionado = QCombobox() # con 'Enfermeria' seleccionado
            
            >>> id_especialidad = buscar_id_de_la_lista_del_combobox(boton_seleccionado, lista_especialidades, 1, 0)
        
        """    
        # Obtener el texto seleccionado del combobox
        seleccion = boton_seleccionado.currentText()

        
        # si el combobox tiene "seleccionar aqui", omitimos la primera posicion
        if seleccionar_aqui == True:
            
            # si la seleccion no es vacia y no es "seleccionar aqui"
            if  seleccion and not boton_seleccionado.currentIndex() == 0:
                
                # iteramos la lista de elementos
                for elemento in lista_elementos:
                    
                    # comparamos el texto seleccionado con el nombre del elemento en la lista
                    if seleccion.lower() == elemento[indice_nombre_del_elemento].lower():
                        
                        # obtenemos el id del elemento correspondiente
                        id_del_elemento = elemento[indice_id_del_elemento]  
                        
                        # aseguramos que el id sea un entero
                        id_del_elemento = int(id_del_elemento)
                        
                        # retornamos el id encontrado
                        return id_del_elemento
                    
        # si el combobox no tiene "seleccionar aqui", solo buscamos el id normal
        elif seleccionar_aqui == False:
            
            # si hay una seleccion del combobox
            if  seleccion:
                
                # iteramos la lista de elementos
                for elemento in lista_elementos:
                    
                    # comparamos el texto seleccionado con el nombre del elemento en la lista
                    if seleccion.lower() == elemento[indice_nombre_del_elemento].lower():
                        
                        # obtenemos el id del elemento correspondiente
                        id_del_elemento = elemento[indice_id_del_elemento]  
                        
                        # aseguramos que el id sea un entero
                        id_del_elemento = int(id_del_elemento)
                        
                        # retornamos el id encontrado
                        return id_del_elemento
        
    def buscar_id_por_nombre_del_elemento(self, nombre_elemeto:str, lista_de_elementos:list, indice_id:int = 0):
        
        """
            ### Este metodo sirve para buscar el id del elemento que pertenezca a un catalogo.
            
            **Ejemplo**
            
            si tenemos una variable que contiene una especialidad y queremos obtener su id para realizar una operacion usamos el metodo asi:
            
            >>> lista_especialidades = [(1, "artesania"), (2, "ceramica"), (3, "carpinteria")]
            
            >>> mi_especialidad = "artesania"
            
            >>> id_especialidad = FuncionSistema.buscar_id_por_nombre_del_elemento(nombre_elemeto = mi_especialidad, lista_de_elementos = lista_especialidades) # retorna 1
            
            normalmente el indice del id es 0 pero puedes colocar el indice en donde se encuentre el id
            
            
        """     
         
        
        try:
            
            for elemento in lista_de_elementos:
                
                if nombre_elemeto in elemento:
                    
                    return elemento[indice_id]
                
                else:
                    
                    pass
                
        except Exception as e:
            
            self.mostrar_errores_por_excepcion(e, "buscar_id_por_nombre_del_elemento")
        else:
            
            print("buscar_id_por_nombre_del_elemento: se encontro el id con exito")
            
    
    # Metodos para limpiar los inputs 
    def limpiar_inputs_de_qt(self, lista_qlineedits_y_qlabel: tuple, lista_qradiobuttons: tuple = (), lista_qcombobox: tuple = ()) -> None:
        
        """
            ### Este metodo sirve para limpiar los inputs mas relevante como los:
            
            * QLineEdit
            * QLabel
            * QRadioButton
            * QListWidget
            * QComboBox

            * lista normales de python
            
            
            Para usar la funcion solo haga una lista agrupando todos los QLabel y QLineEdit en una lista y los QRadioButton en otra.
            
            Ya que los QLabel y QLineEdit para limpiarse ambos usan .clear() y los QRadioButton no.
            
            
            
            **Ejemplo**
            
            
            lista_qlabel_qlineedit = [input_1, input_2, input_3, label_4, ......]
            
            lista_qradiobutton = [radiobuton_1, radiobuton_2, ........]
            
            limpiar_inputs_de_qt(lista_qlabel_qlineedit, lista_qradiobutton) 
            
            ### Limpia los inputs (usarlo para salir de una pantalla o terminar una tarea)
            
            
            Tambien este metodo sirve para restablecer los combobox a su indice 0 es decir, si el combobox tiene "seleccionar aqui" lo devuelve a esa posicion
            
            
        
        
        """
        
        
        try:
            # Limpiamos los QlineEdits
            for qlineedit_o_qlabel in lista_qlineedits_y_qlabel:
                qlineedit_o_qlabel.clear()
                #qlineedit_o_qlabel.setEnabled(True)
                
            # Limpiamos los RadioButtons
            
            if len(lista_qradiobuttons) > 0: 
                
                for radiobutton in lista_qradiobuttons:
                    
                    radiobutton.setAutoExclusive(False)
                    radiobutton.setChecked(False)
                    radiobutton.setAutoExclusive(True)
                    
                    
            if len(lista_qcombobox) > 0:
                
                for combobox in lista_qcombobox:
                    
                    combobox.setCurrentIndex(0)
                    
            
            

        except Exception as e:
            
            self.mostrar_errores_por_excepcion(e, "Limpiar_inputs_de_qt")
            
            
        else:
            
            print("Todo se limpio correctamente")
        
    
    
    
    
    
    
    
    # Metodo para muestrar los errores en X linea y x funcion
    def mostrar_errores_por_excepcion(self, e, nombre_func: str):
        """
            Esta funcion lo que hace es mostrar los errores por excepcion por consola, especificando la excepcion
            la linea y en donde pasa el error.
            
            **Ejemplo de lo que mostraria por consola si hay algun error**
            
            
            ------------------------------------------------------------------------------------

            Error en la línea: 25

            Error en la funcion: moverse_de_pantalla

            Traceback completo:
            Traceback (most recent call last):
            File "c:/Users/user/TELA-APP/recursos_graficos_y_logicos/pantallas_de_la_aplicacion/funciones_comunes.py", line 25, in moverse_de_pantalla   
                pantalla.setCurrentIndex(indice)
            AttributeError: 'int' object has no attribute 'setCurrentIndex'

            ------------------------------------------------------------------------------------
        
        """
        
        # Obtener el traceback completo como string
        error_traceback = traceback.format_exc()
    
        # Mostrar en consola (para depuración)
        print("------------------------------------------------------------------------------------")
        print("\nError en la línea:", traceback.extract_tb(e.__traceback__)[-1].lineno)
        print(f"\nError en la funcion: {nombre_func}\n")
        print("Traceback completo:\n", error_traceback)
        print("------------------------------------------------------------------------------------")



    # Metodo para minizar el side bar/barra lateral
    def cambiar_tamano_side_bar(self, side_bar, frame_botones_temas):
        
        """
            Este metodo minizar el sidebar a un 200 de ancho y tambien al minizarce este oculta el frame que tiene los botones con los temas
        
        """
        
        # Configurar la animación
        self.animacion = QPropertyAnimation(side_bar, b"minimumWidth")
        self.animacion.setDuration(400)  # 500 milisegundos
        self.animacion.setEasingCurve(QEasingCurve.InOutCubic)
        
        # Segunda animación para el ancho máximo
        self.animacion2 = QPropertyAnimation(side_bar, b"maximumWidth")
        self.animacion2.setDuration(400)
        self.animacion2.setEasingCurve(QEasingCurve.InOutCubic)
        
        
        if self.estado_sidebar == True:
            
            # Animación para minimizar (190 → 50)
            self.animacion.setStartValue(190)
            self.animacion.setEndValue(50)
            self.animacion2.setStartValue(190)
            self.animacion2.setEndValue(50)
            self.minimizado = True
            #side_bar.setFixedWidth(55)
            
            frame_botones_temas.hide()
            self.estado_sidebar  = False
            
            

        elif self.estado_sidebar == False:
            
            
            # Animación para maximizar (50 → 100)
            self.animacion.setStartValue(50)
            self.animacion.setEndValue(190)
            self.animacion2.setStartValue(50)
            self.animacion2.setEndValue(190)
            self.minimizado = False
            
            
            #side_bar.setFixedWidth(190)
            frame_botones_temas.show()
            self.estado_sidebar = True
            
            
        # Iniciar ambas animaciones
        self.animacion.start()
        self.animacion2.start()
            
            
            
    # Metodos para cambiar de estilos/TEMAS
    def cargar_estilos(self, app, ruta_archivo):
        """
            ### Este metodo sirve para cargar las hojas de estilo al sistema
            
            como todos los elementos de la pantalla tienen propiedades dinamicas, podemos usar hojas de estilos en archivos.qss para poder usarlo en el sistema
            
            Lo que se tiene que hacer es pasarle dos parametro:
            
            1. la variable que instacia toda la aplicacion.
            2. la rutra del archivo.qss (procurar que la hoja de estilo este en el archivo.qrc).
            
            **Ejemplo**
            
            
            si es para que los botones cambie entre estilos:
            ### Main.py
                
                
                ###
                if __name__ == "__main__":
                    app = QApplication(sys.argv)
                    window = MainWindow() # variable que instacia la aplicacion
                    FuncionSistema.cargar_estilos(window, ':/hojas_de_estilo/estilos/estilo_oscuro.qss')
                    window.show()
                    window.showMaximized()
                    sys.exit(app.exec_())
                    
            si es para que los botones cambie entre estilos:
            ### Desde donde tengas los botones
                
                ### 
                self.boton_tema_claro.clicked.connect(lambda: FuncionSistema.cargar_estilos(self, ':/hojas_de_estilo/estilos/estilo_default.qss'))
                self.boton_tema_oscuro.clicked.connect(lambda: FuncionSistema.cargar_estilos(self, ':/hojas_de_estilo/estilos/estilo_oscuro.qss'))
                
        """
        try:
            archivo = QFile(ruta_archivo)
            if archivo.open(QFile.ReadOnly | QFile.Text):
                stream = QTextStream(archivo)
                
                # Limpiamos primero el estilo
                app.setStyleSheet("")
                
                # asignamos el estilo
                app.setStyleSheet(stream.readAll())
                
                archivo.close()
        except Exception as e:
            print(f"Error al cargar estilos: {e}")




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

            
            
           
            
    def ver_cursor_posicion_cero(self, lista_qlineedit:list):
        
        """
            Este metodo sirve para que el cursor del qlineedit este en la posicion 0, es decir que el texto que esta en el qlineedit
            se vea desde el principio del lado izquierdo.
            
            Metodo para ver lo QlineEdits(los inputs) se vean desde su posicion cero (ojo no hablo de ninguna posicion
            de alguna lista o tupla) hablo de esto:
              * El texto que tiene en el QlineEdit "avenida fuerzas armadas, calle 2, residencia 1 etc"               
              pero en la interfaz se ve "adas, calle 2, residencia 1 etc" y hay que ponerle la posicion 0 para que se vea:
              "avenida fuerzas armadas, calle 2"
        
        """
        
        # iteramos cada input para darle la posicion 0
        for qlineedit in lista_qlineedit:
            
            qlineedit.setCursorPosition(0)
            
            
            
        
        
       
    def comprobar_si_hay_valor(self, variable):
        
        """
        ### Metodo para comprobar si la variable tiene un valor para mostrar en pantalla
        
        Este metodo sirve en el caso de mostrar una informacion en pantalla teniendo en cuenta que la base de datos puede retornar o un valor o none
        
        ***Ejemplo***
        
        Si es None retornamos a "No tiene"
        
        Si tiene algun valor retornamos el valor de la variable
        
        
        
        alumnos = [ 
                    Manuel,    # 1er nombre
                    Alejandro, # 2do nombre
                    Perez,     # 1er apellido
                    None,      # 2do apellido
                    102031203  # cedula
                    ]
                    
                    
        mostrar_datos_en_pantalla(alumnos) # resultado: muestra todos los campos y el que esta en None lo muestra como "No tiene"
        
        
        esto se hace para no confundirlo con un error
        
        
        
    
        """
        
        if variable == None:
                
            return "No tiene"
                
        else:
            
            return variable
        
        
        
        
    def abrir_carpeta_contenedora_de_archivos(self, ruta_carpeta: str) -> None:
        
        """
            ### Este metodo sirve para abrir la carpeta contenedora de los archivos generados por el sistema en el explorador de archivos del sistema operativo:
            
            - Windows
            - Linux (No hay version de linux)
        
        """
        
        try:
            
            if not os.path.exists(ruta_carpeta):
                QMessageBox.warning(self, "Error", f"No se encontró la carpeta:\n{ruta_carpeta}")
                return
            
            
            # 4. Abrir la carpeta
            if platform.system() == "Windows":
                os.startfile(ruta_carpeta)
            elif platform.system() == "Darwin":  # macOS
                os.system(f'open "{ruta_carpeta}"')
            else:  # Linux
                os.system(f'xdg-open "{ruta_carpeta}"')
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al abrir la carpeta:\n{str(e)}")  
            
            
    def cambiar_estilo_del_boton(self, qpushbutton, tipo:str = "boton_anadir") -> None:
        """
            ### Este metodo sirve para cambiar de estilo a los botones de registrar elementos catalogo.
            
            lo que hace es cambirle es el texto si el parametro tipo es:
            
            - "boton_anadir" le da el estilo por defecto
            - "boton_editar" le cambia el texto por editar, le cambia el fondo a amarillo y le cambia el icono de mas o un lapiz
            
            Lo que hace este metodo es cambiarle la propiedad dinamica para que tome el estilo segun la hoja de estilo usada
            
            ***Ejemplo***
            
            boton_registrar = QPushButton()
            
            self.cambiar_estilo_del_boton(boton_registrar, "boton_editar") # estilo de editar
            
            
        """
        
        
    
        try:
            
            
            
            
            if tipo == "boton_anadir":
                
                qpushbutton.setText(" Anadir")
                qpushbutton.setProperty("tipo", tipo)
                
                
            elif tipo == "boton_editar":
            
                qpushbutton.setText(" Editar")
                qpushbutton.setProperty("tipo", tipo)
            
            
            
            qpushbutton.style().unpolish(qpushbutton)
            qpushbutton.style().polish(qpushbutton)
            

        except Exception as e:
            
            self.mostrar_errores_por_excepcion(e, "cambiar_estilo_del_boton")
    
    
    def cargar_foto_perfil_en_la_interfaz(self, ruta_foto_perfil, widget_foto):
        
        """
            ### Este metodo sirve para cargar la FOTO DE PERFIL EN LA INTERFAZ, es decir, cargar la imagen en el widget que se le tenga que colocar la imagen

            ***Ejemplo***
            ruta_de_la_foto = b'RIFF.)\x00\x00WEBPVP8 ")\x00\x00\x10m\x00\x9d\x01*\x8c\x00\x8c\x00\x00\x00\x00%\xb0\x02\x9d7i\xf9_\xe37K\x04\xee\xef\x7f\x8e\xff\xae\x9f\xe3>Li/\xcf ... (30114 characters truncated) ... x99\xdc\x91\x1b\xc1zM\x05\xbf\xaf\x06I\xfd\xe3q\xfd\xfb\xa5\nb5\xca\xea\xf12G\x10`[\x94GF\x0b\x02\xa5p\x1b=$\x11\r\xc3\xe4\x19\x03\xe5z{\x7f\xb7@\x00
            
            label = QLabel()
            
            FuncionSistema.cargar_foto_perfil_en_la_interfaz(ruta_de_la_foto, label) # esto da como resultado la foto colocada en el label
            
            
        """
        try:
            if not ruta_foto_perfil == None:
                pixmap = QPixmap()  # 1. Crear objeto QPixmap vacío
                pixmap.loadFromData(ruta_foto_perfil)  # 2. Cargar datos

                # Verificar si se cargó correctamente
                if not pixmap.isNull():
                    widget_foto.setPixmap(pixmap)
                    
                else:
                    print("Error: No se pudo cargar la imagen desde bytes")
                
            else: 
                pass
    
        except Exception as e:
            self.mostrar_errores_por_excepcion(e, "cargar_foto_perfil_en_la_interfaz")
            
        else:
            
            print("la imagen cargo bien")
    
    def cargar_foto_perfil(self, ruta_foto_perfil: str = None) -> Optional[bytes]:
        """
        Función para cargar la foto de perfil
        
        :param ruta_foto_perfil: La primera posición de la tupla que obtengo al usar **QFileDialog.getOpenFileName()**
        :type ruta_foto_perfil: str
        :return: La foto convertida en **bytes** para guardarla en la base de datos y leerla usando **QPixmap().loadFromData(QByteArray(foto_en_bytes))** obteniendo la foto original ya optimizada, en caso de no cargar una foto se retorna un **None**
        :rtype: bytes o None
        """
        
        if (ruta_foto_perfil):
            try:
                # OPTIMIZACIÓN (Pillow) - Recortamos a cuadrado primero
                imagen = Image.open(ruta_foto_perfil)
                
                # Crear un cuadrado perfecto (Crop al centro)
                ancho, alto = imagen.size
                min_dim = min(ancho, alto)
                izquierda = (ancho - min_dim) / 2
                superior = (alto - min_dim) / 2
                derecha = (ancho + min_dim) / 2
                inferior = (alto + min_dim) / 2
                imagen = imagen.crop((izquierda, superior, derecha, inferior))
                
                # Redimensionar la imágen
                imagen.thumbnail((140, 140))
                
                # Creo un archivo virtual en la memoria RAM (para no guardar la imágen en el disco duro)
                buffer = io.BytesIO()
                
                # Guardo la imágen en mi archivo virtual (temporalmente) convirtiendola formato .WebP
                imagen.save(buffer, format="WEBP", quality=100)
                
                # Obtengo una cadena de ceros y unos (bytes) y así poder utilizar esto para guardarlo en la base de
                # datos y leerlo a la hora de mostrar la foto de perfil
                foto_en_bytes = buffer.getvalue()
                
                return foto_en_bytes
            except Exception as error:
                raise error
            
        return None
    
    def aplicar_borde_a_rango(self, hoja, rango, borde):
        min_col, min_row, max_col, max_row = range_boundaries(rango)
        for fila in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                hoja.cell(row=fila, column=col).border = borde
        
    def habilitar_o_deshabilitar_widget_de_qt(self, tupla_de_widegts_qt: tuple ,opcion: bool):
        """
            ### Este metodo sirve mas que todo para habilitar o deshabilitar una gran cantidad de widget de qt, como:
            - QLineEdits
            - QRadioButtons
            - QLabels
            - QListWidget
            - QPushButton
            
            Pasandole como argumento una tupla con los widgets y un valor boleano (True o False)
            
            ***Ejemplo***
            
            lista_widget = (label, button, lineedit)
            
            habilitar_0_deshabilitar_widget_de_qt(lista_widget, True) # habilita los widgets
            
            #### True los habilita
            #### False los deshabilita
        """    
        try:
            for widget in tupla_de_widegts_qt:
                widget.setEnabled(opcion)
        
        except Exception as e:
            self.mostrar_errores_por_excepcion(e, "habilitar_0_deshabilitar_widget_de_qt")
    

lista_prueba = [(1, 'DOUGLAS', 'JOSE', None, 'MARQUEZ', 'BETANCOURT', '17536256', '1983-05-17', 42, 'Activo', 'M', 1),
                (2, 'ENMANUEL', 'JESÚS', None, 'GARCIA', 'RAMOS', '5017497', '1956-10-10', 69, 'Activo', 'M', 1),
                (3, 'ROSMARY', 'DEL VALLE', None, 'SALAS', 'JIMENEZ', '18128319', '1986-10-28', 38, 'Activo', 'F', 0),
                (4, 'JOSE', 'ALEJANDRO', None, 'SALAS', 'JIMENEZ', '16788123', '1985-10-28', 39, 'Activo', 'F', 0), 
                (5, 'JOSE', 'ALEJANDRO', None, 'SALAS', 'JIMENEZ', '26788123', '1985-10-28', 39, 'Activo', 'F', 0)]

FuncionSistema = FuncionesDelSistema()


#lista_especialidades = [(1, "artesania"), (2, "ceramica"), (3, "carpinteria")]
            
mi_especialidad = "carpinteria"

#print(FuncionSistema.buscar_id_por_nombre_del_elemento(nombre_elemeto = mi_especialidad, lista_de_elementos = lista_especialidades))

#print(FuncionSistema.buscar_id_por_cedula("5017497", lista_prueba))
#print(funciones_comunes.cargar_elementos_para_el_combobox())


#funciones_comunes.limpiar_inputs_de_qt(lista_qlineedits_y_qlabel= [("12"), (123)])
