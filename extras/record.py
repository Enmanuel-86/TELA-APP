
menu = input("Mensaje de la suerte, ingrese un numero del 1 al 3: ")


match menu:
    
    case "1":
        
        print("vivo")
        
        
    case "2":
        
        print("Muerto")
        

    case "3":
        
        print("Hola")
        
    case _:
        
        print("numero fuera del rango")