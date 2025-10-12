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
        
        
    # Metodo para cargar catalogo en los combobox
    def cargar_elementos_para_el_combobox(self, lista_catalogo, boton_desplegable, indice_nombre_elemento:int, anadir_seleccionar_aqui: int = 0) -> None:
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




funciones_comunes = FuncionesComunes()
