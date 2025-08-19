# Esto en caso de que no lo tengas, porque esto es necesario para ciertos parámetros que son de tipo date
from datetime import date

# Importas la excepción personalizada que creé para así poder mostrar en una ventana de error el mensaje que puse
# dependiendo del método que ejecutes
from excepciones.base_datos_error import BaseDatosError

#1. Importas la clase de configuración de USUARIO_ID que se le va a pasar el USUARIO_ID_AUTENTICADO si la sesión
# inicia correctamente
from configuraciones.configuracion import actualizar_usuario_id, app_configuracion

#2. Importas el repositorio y luego su respectivo servicio
from repositorios.usuarios.usuario_repositorio import UsuarioRepositorio
from repositorios.empleados.empleado_repositorio import EmpleadoRepositorio
from repositorios.usuarios.permiso_repositorio import PermisoRepositorio
from repositorios.empleados.historial_enferm_cronicas_repositorio import HistorialEnfermCronicasRepositorio
from repositorios.empleados.info_clinica_empleado_repositorio import InfoClinicaEmpleadoRepositorio
from repositorios.empleados.info_laboral_repositorio import InfoLaboralRepositorio
from repositorios.empleados.detalle_cargo_repositorio import DetalleCargoRepositorio

from servicios.usuarios.usuario_servicio import UsuarioServicio
from servicios.empleados.empleado_servicio import EmpleadoServicio
from servicios.usuarios.permiso_servicio import PermisoServicio
from servicios.empleados.historial_enferm_cronicas_servicio import HistorialEnfermCronicasServicio
from servicios.empleados.info_clinica_empleado_servicio import InfoClinicaEmpleadoServicio
from servicios.empleados.info_laboral_servicio import InfoLaboralServicio
from servicios.empleados.detalle_cargo_servicio import DetalleCargoServicio

#3. Creas una instancia de el repositorio que importaste
usuario_repositorio = UsuarioRepositorio()
empleado_repositorio = EmpleadoRepositorio()
permiso_repositorio = PermisoRepositorio()
historial_enferm_cronicas_repositorio = HistorialEnfermCronicasRepositorio()
info_clinica_empleado_repositorio = InfoClinicaEmpleadoRepositorio()
info_laboral_repositorio = InfoLaboralRepositorio()
detalle_cargo_repositorio = DetalleCargoRepositorio()

#4. Creas una instancia del servicio correspondiente al repositorio que le vas a inyectar
usuario_servicio = UsuarioServicio(usuario_repositorio)
empleado_servicio = EmpleadoServicio(empleado_repositorio)
permiso_servicio = PermisoServicio(permiso_repositorio)
historial_enferm_cronicas_servicio = HistorialEnfermCronicasServicio(historial_enferm_cronicas_repositorio)
info_clinica_empleado_servicio = InfoClinicaEmpleadoServicio(info_clinica_empleado_repositorio)
info_laboral_servicio = InfoLaboralServicio(info_laboral_repositorio)
detalle_cargo_servicio = DetalleCargoServicio(detalle_cargo_repositorio)

# Info del usuario DIRECTOR. Nombre de usuario: douglas345. Clave de usuario: 1234
nombre_usuario = input("- Ingrese su nombre de usuario: ")
clave_usuario = input("- Ingrese su clave de usuario: ")

# Acá retornará el ID del usuario en caso de que el nombre de usuario y la clave sean correctos, de lo contrario
# retornará una excepción que yo creé con un mensaje que debes mostrar con una ventana emergente

try:
    USUARIO_ID_AUTENTICADO = usuario_servicio.autenticar_usuario(nombre_usuario, clave_usuario)
except BaseDatosError as error:
    print(f"{error}")
else:
    actualizar_usuario_id(USUARIO_ID_AUTENTICADO)
    



    print("------------------------------------------------")
    print("     SELECCIONA A DONDE SE QUIERE IR")
    print("\n1. Registrar a un empleado.")
    print("2. Consultar la info de todos los empleados.")
    print("------------------------------------------------")
    opcion = input("\n- Elige una opcion: ")
    
    # Antes de acceder a una parte de la app como registrar a un empleado, se verifica si el usuario
    # autenticado tiene el permiso requerido, sino, retorna la excepción personalizada con el mensaje
    permiso_crear_empleados = permiso_servicio.verificar_permiso_usuario(USUARIO_ID_AUTENTICADO, "CREAR EMPLEADOS")
    permiso_consultar_empleados = permiso_servicio.verificar_permiso_usuario(USUARIO_ID_AUTENTICADO, "CONSULTAR EMPLEADOS")
    
    if (opcion == "1" and permiso_crear_empleados):
        
        #Supongamos que estas en el formulario para registrar un empleado
        #Guardamos lo que son los valores de cada parte del formulario
        
        #Campos de información básica
        primer_nombre = ""
        segundo_nombre = None
        apellido_paterno = "CHACÓN"
        apellido_materno = None
        cedula = "30932925"
        fecha_nacimiento = date(2004, 10, 11)
        sexo = None # Por defecto es M si es NULL
        tiene_hijos_menores = None # Por defecto es 0 (No)
        
        errores_info_basica = empleado_servicio.validar_info_basica_empleado(
            primer_nombre, segundo_nombre,
            apellido_paterno, apellido_materno,
            cedula, fecha_nacimiento
        )
        
        if errores_info_basica:
            print("\n".join(errores_info_basica))
        else:
            print("- Primera parte sin errores.")
            #Campos de medidas de empleados
            talla_camisa = "S"
            talla_pantalon = 30
            talla_zapatos = 45
            
            errores_medidas = empleado_servicio.validar_medidas_empleado(talla_camisa, talla_pantalon, talla_zapatos)
            
            if errores_medidas:
                print("\n".join(errores_medidas))
            else:
                print("- Segunda parte sin errores.")
                #Campos de info geográfica
                estado_reside = "ANZOÁTEGUI"
                municipio = "SIMÓN BOLÍVAR"
                direccion_residencia = "BOYACÁ 2"
                
                errores_info_geografica = empleado_servicio.validar_info_geografica_empleado(
                    estado_reside, municipio,
                    direccion_residencia
                )
                
                if errores_info_geografica:
                    print("\n".join(errores_info_geografica))
                else:
                    print("- Tercera parte sin errores.")
                    #Campos de info de contacto
                    num_telefono = None # Por defecto No tiene
                    correo_electronico = "alonsochacon441@gmail.com"
                    
                    errores_info_contacto = empleado_servicio.validar_info_contacto_empleado(num_telefono, correo_electronico)
                    
                    if errores_info_contacto:
                        print("\n".join(errores_info_contacto))
                    else:
                        print("- Cuarta parte sin errores.")
                        #Campos de historial de enfermedades crónicas y discapacidades
                        
                        # Acá te toca ir haciendo lo del bucle for y eso para trabajar por separado la lista
                        # de enfermedades crónicas y la lista de diagnósticos, para este ejemplo pondré que escogió uno de cada uno 
                        # (No se realizan validaciones porque estas cosas son opcionales)
                        enferm_cronica_id = 1
                        diagnostico_id = 1
                        
                        print("- Quinta parte sin errores.")
                        
                        #Campos de info laboral
                        cod_depend_cobra = "123456789"
                        institucion_labora = "TEV TRONCONAL 3"
                        
                        errores_info_laboral = info_laboral_servicio.validar_campos_info_laboral(
                            cod_depend_cobra, institucion_labora
                        )
                        
                        if errores_info_laboral:
                            print("\n".join(errores_info_laboral))
                        else:
                            print("- Sexta parte sin errores.")
                            # Campos de detalles del cargo
                            
                            #Acá te encargas de que el listado al seleccionar un elemento de cada catálogo
                            # se retorne el ID asociado para poder utilizarlo al registrarlo
                            cargo_id = 1
                            funcion_cargo_id = 1
                            titulo_cargo = "LINCENCIADO EN TAL COSA"
                            tipo_cargo_id = 1
                            
                            #Si selecciona una especialidad, no creo que deba escribir la labor del cargo 
                            #(hay que ver después)
                            especialidad_id = None 
                            
                            labores_cargo = "ADMINISTRAR TAL COSA"
                            fecha_ingreso_ministerio = date(2025, 1, 10)
                            fecha_ingreso_institucion = None # Por defecto se establece la fecha actual
                            
                            situacion  = None # Por defecto es Activo
                            
                            errores_detalle_cargo = detalle_cargo_servicio.validar_detalles_cargo(
                                cargo_id, funcion_cargo_id,
                                tipo_cargo_id, titulo_cargo,
                                labores_cargo, fecha_ingreso_ministerio
                            )
                            
                            if errores_detalle_cargo:
                                print("\n".join(errores_detalle_cargo))
                            else:
                                print("- Registro de empleado finalizado con éxito sin errores")
                                
                                # Acá se le pasan los valores al diccionario que se usará para el método
                                # registrar de los repositorios
                                
                                #Las claves del diccionario tanta para registrar como para actualizar campos
                                # tienen que tener exactamente los mismos nombres de este ejemplo
                                # porque así están escritos en la base de datos
                                
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
                            
                            #Acá va a retornar el empleado_id para asociarlo a las demás tablas cuyos campos
                            # se llenaron en el formulario
                            empleado_id = empleado_servicio.registrar_empleado(campos_empleado)
                            
                            # Acá con esto es para más adelante comprobar que si
                            # Si la lista de diagnosticos o la lista de enfermedades crónicas
                            # no está vacía entonces se hace el proceso de asociar el empleado con sus enfermedades o discapacidades
                            # en caso de que alguna esté vacía entonces ese registro en concreto (por ejemplo, si la de discapaciades
                            # está vacía) no se hace
                            if (diagnostico_id):
                                campos_info_clinica_empleado = {
                                    "empleado_id": empleado_id,
                                    "diagnostico_id": diagnostico_id
                                }
                            
                            if (enferm_cronica_id):
                                campos_historial_enferm_cronicas = {
                                    "empleado_id": empleado_id,
                                    "enferm_cronica_id": enferm_cronica_id
                                }
                            
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
                            
                            
                            info_clinica_empleado_servicio.registrar_info_clinica_empleado(campos_info_clinica_empleado)
                            historial_enferm_cronicas_servicio.registrar_historial_enferm_cronica(campos_historial_enferm_cronicas)
                            info_laboral_servicio.registrar_info_laboral(campos_info_laboral)
                            detalle_cargo_servicio.registrar_detalle_cargo(campos_detalle_cargo)
    elif (opcion == "2" and permiso_consultar_empleados):
        print("CÉDULA   PRIMER NOMBRE   APELLIDO PATERNO     TIPO DE CARGO    SITUACIÓN")
        #El segundo parámetro del método del servicio de detalle cargo es opcional y es el de la cédula del empleado
        # (en caso de que necesite buscar un empleado específico pasarle el segundo parámetro, por defecto muestra por tipo de cargo)
        empleados = detalle_cargo_servicio.obtener_detalles_cargo_por_tipo_cargo_o_cedula(1)
        if (type(empleados) == list):
            for empleado in empleados:
                print(f"{empleado[1]}   {empleado[2]}        {empleado[4]}            {empleado[6]}       {empleado[7]}")
        else:
            print(f"{empleados[1]}   {empleados[2]}        {empleados[4]}            {empleados[6]}       {empleados[7]}")