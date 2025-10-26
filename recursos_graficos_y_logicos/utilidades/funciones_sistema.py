import traceback
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve


"""
Este archivo contiene todas las funciones que suelen repetirse, esto ayuda a evitar copiar y pegar
codigo que ya esta escrito. Con esto solo llamamos la funcion, pasamos parametro y listo
"""

class FuncionesDelSistema:
    def __init__(self):
        
        # Variables axuliares
        self.estado_sidebar = True
        
        
        
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
        
            Este metodo sirve para moverse de pantalla, se la pantalla y el indice.
        
            Como estamos trabajando con stackedWidget este metodo funciona asi:
            
            boton.clicked.connect(lambda: moverse_de_pantalla(self.stacked_widget, 3 )
            
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
                
                
                
                # Si no hay coincidencias, que siga buscando o que de por si no haga nada    
                else:
                    
                    return
                    
            
            
        
        
        except Exception as e:
            
            self.mostrar_errores_por_excepcion(e, "buscar_id_por_cedula")
        
        
    # Metodo para cargar catalogo en los combobox
    def cargar_elementos_para_el_combobox(self, lista_catalogo: list, boton_desplegable, indice_nombre_elemento:int, anadir_seleccionar_aqui: int = 0) -> None:
        """
            Este metodo sirve para cargar los elementos de una lista a un combobox, indicandole:
            
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
            
        
        """
        try:    
            
            
            
            if anadir_seleccionar_aqui == 1:
                # agregamos la palabra seleccionar aqui
                boton_desplegable.addItem("Seleccione aqui")
                
                
            elif anadir_seleccionar_aqui == 0:
                
                pass
            
            elif anadir_seleccionar_aqui > 1:
                
                print("Numero fuera del rango establecido")
                
            
                
            # Iteramos cada elemento de la lista
            for elemento_iterado in lista_catalogo:
                
                # le indicamos con el indice que pedimos que vaya agregando el nombre del elemento
                boton_desplegable.addItem(elemento_iterado[indice_nombre_elemento])
        
        except Exception as e:
            
            self.mostrar_errores_por_excepcion(e, "Cargar elementos para el combobox")
            
        else: 
            
            print(f"\nLa lista para el/los boton cargo correctamente")
    
    
    
    # Metodos para limpiar los inputs 
    def limpiar_inputs_de_qt(self, lista_qlineedits_y_qlabel: list, lista_qradiobuttons: list = []) -> None:
        
        """
            ### Este metodo sirve para limpiar los inputs mas relevante como los:
            
            * QLineEdit
            * QLabel
            * QRadioButton
            
            
            Para usar la funcion solo haga una lista agrupando todos los QLabel y QLineEdit en una lista y los QRadioButton en otra.
            
            Ya que los QLabel y QLineEdit para limpiarse ambos usan .clear() y los QRadioButton no.
            
            
            
            **Ejemplo**
            
            lista_qlabel_qlineedit = [input_1, input_2, input_3, ......]
            
            lista_qradiobutton = [radiobuton_1, radiobuton_2, ........]
            
            limpiar_inputs_de_qt(lista_qlabel_qlineedit, lista_qradiobutton) 
            
            ### Limpia los inputs (usarlo para salir de una pantalla o terminar una tarea)
            
            
            
            
            
        
        
        """
        
        
        try:
            # Limpiamos los QlineEdits
            for qlineedit_o_qlabel in lista_qlineedits_y_qlabel:
                qlineedit_o_qlabel.clear()
                #qlineedit_o_qlabel.setEnabled(True)
                
            # Limpiamos los RadioButtons
            
            if len(lista_qradiobuttons) >= 0: 
                
                for radiobutton in lista_qradiobuttons:
                    
                    radiobutton.setAutoExclusive(False)
                    radiobutton.setChecked(False)
                    radiobutton.setAutoExclusive(True)
                
            

        except Exception as e:
            
            self.mostrar_errores_por_excepcion(e, "Limpiar_inputs_de_qt")
            
            
        else:
            
            print("Todo se limpio correctamente")
        
    
    
    
    
    
    
    
    # Metodo para muestrar los errores en X linea y x funcion
    def mostrar_errores_por_excepcion(self, e, nombre_func: str):
        """
            Esta funcion lo que hace es mostrar los errores por excepcion por consola, especificando la excepcion
            la linea y en donde pasa el error
            
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
    def cambiar_tamano_side_bar(self, side_bar):
        
        """
            Este metodo minizar el sidebar a un 200 de ancho
        
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
            
            self.estado_sidebar  = False
            
            

        elif self.estado_sidebar == False:
            
            
            # Animación para maximizar (50 → 100)
            self.animacion.setStartValue(50)
            self.animacion.setEndValue(190)
            self.animacion2.setStartValue(50)
            self.animacion2.setEndValue(190)
            self.minimizado = False
            
            
            #side_bar.setFixedWidth(190)
            
            self.estado_sidebar = True
            
            
        # Iniciar ambas animaciones
        self.animacion.start()
        self.animacion2.start()
            
            
            
           
            
            
            
            
            
        
        
       
        
        
        
        
lista_prueba = [(1, 'DOUGLAS', 'JOSE', None, 'MARQUEZ', 'BETANCOURT', '17536256', '1983-05-17', 42, 'Activo', 'M', 1),
                (2, 'ENMANUEL', 'JESÚS', None, 'GARCIA', 'RAMOS', '5017497', '1956-10-10', 69, 'Activo', 'M', 1),
                (3, 'ROSMARY', 'DEL VALLE', None, 'SALAS', 'JIMENEZ', '18128319', '1986-10-28', 38, 'Activo', 'F', 0),
                (4, 'JOSE', 'ALEJANDRO', None, 'SALAS', 'JIMENEZ', '16788123', '1985-10-28', 39, 'Activo', 'F', 0), 
                (5, 'JOSE', 'ALEJANDRO', None, 'SALAS', 'JIMENEZ', '26788123', '1985-10-28', 39, 'Activo', 'F', 0)]

FuncionSistema = FuncionesDelSistema()

#print(funciones_comunes.buscar_id_por_cedula("175362562", lista_prueba))
#print(funciones_comunes.cargar_elementos_para_el_combobox())


#funciones_comunes.limpiar_inputs_de_qt(lista_qlineedits_y_qlabel= [("12"), (123)])
