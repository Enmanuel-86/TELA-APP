import traceback


"""
Este archivo contiene todas las funciones que suelen repetirse, esto ayuda a evitar copiar y pegar
codigo que ya esta escrito. Con esto solo llamamos la funcion, pasamos parametro y listo
"""

class FuncionesComunes:
    
    
    # Metodo para moverse entre pantallas
    def moverse_de_pantalla(self, pantalla , indice: int) -> None:
        """
        
            Este metodo sirve para moverse de pantalla, se la pantalla y el indice.
        
            Como estamos trabajando con stackedWidget este metodo funciona asi:
            
            boton.clicked.connect(lambda: moverse_de_pantalla(self.stacked_widget, 3 )
            
        """
        try:
            pantalla.setCurrentIndex(indice)
            
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


lista_prueba = [(1, 'DOUGLAS', 'JOSE', None, 'MARQUEZ', 'BETANCOURT', '17536256', '1983-05-17', 42, 'Activo', 'M', 1),
                (2, 'ENMANUEL', 'JESÚS', None, 'GARCIA', 'RAMOS', '5017497', '1956-10-10', 69, 'Activo', 'M', 1),
                (3, 'ROSMARY', 'DEL VALLE', None, 'SALAS', 'JIMENEZ', '18128319', '1986-10-28', 38, 'Activo', 'F', 0),
                (4, 'JOSE', 'ALEJANDRO', None, 'SALAS', 'JIMENEZ', '16788123', '1985-10-28', 39, 'Activo', 'F', 0), 
                (5, 'JOSE', 'ALEJANDRO', None, 'SALAS', 'JIMENEZ', '26788123', '1985-10-28', 39, 'Activo', 'F', 0)]

funciones_comunes = FuncionesComunes()

print(funciones_comunes.buscar_id_por_cedula("175362562", lista_prueba))
print(funciones_comunes.cargar_elementos_para_el_combobox())
