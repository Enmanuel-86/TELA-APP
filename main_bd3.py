from datetime import date
from excepciones.base_datos_error import BaseDatosError
from configuraciones.configuracion import app_configuracion

# Importar los repositorios
from repositorios.usuarios.usuario_repositorio import UsuarioRepositorio
from repositorios.usuarios.permiso_repositorio import PermisoRepositorio

from repositorios.alumnos.representante_repositorio import RepresentanteRepositorio
from repositorios.alumnos.alumno_repositorio import AlumnoRepositorio
from repositorios.alumnos.medidas_alumno_repositorio import MedidasAlumnoRepositorio
from repositorios.alumnos.info_clinica_alumno_repositorio import InfoClinicaAlumnoRepositorio
from repositorios.alumnos.info_bancaria_alumno_repositorio import InfoBancarioAlumnoRepositorio
from repositorios.alumnos.inscripcion_repositorio import InscripcionRepositorio

# Importar los servicios
from servicios.usuarios.usuario_servicio import UsuarioServicio
from servicios.usuarios.permiso_servicio import PermisoServicio

from servicios.alumnos.representante_servicio import RepresentanteServicio
from servicios.alumnos.alumno_servicio import AlumnoServicio
from servicios.alumnos.medidas_alumno_servicio import MedidasAlumnoServicio
from servicios.alumnos.info_clinica_alumno_servicio import InfoClinicaAlumnoServicio
from servicios.alumnos.info_bancaria_alumno_servicio import InfoBancariaAlumnoServicio
from servicios.alumnos.inscripcion_servicio import InscripcionServicio

# Crear los repositorios
usuario_repositorio = UsuarioRepositorio()
permiso_repositorio = PermisoRepositorio()

representante_repositorio = RepresentanteRepositorio()
alumno_repositorio = AlumnoRepositorio()
medidas_alumno_repositorio = MedidasAlumnoRepositorio()
info_clinica_alumno_repositorio = InfoClinicaAlumnoRepositorio()
info_bancaria_alumno_repositorio = InfoBancarioAlumnoRepositorio()
inscripcion_repositorio = InscripcionRepositorio()

# Crear los servicios inyectando los repositorios
usuario_servicio = UsuarioServicio(usuario_repositorio)
permiso_servicio = PermisoServicio(permiso_repositorio)

representante_servicio = RepresentanteServicio(representante_repositorio)
alumno_servicio = AlumnoServicio(alumno_repositorio)
medidas_alumno_servicio = MedidasAlumnoServicio(medidas_alumno_repositorio)
info_clinica_alumno_servicio = InfoClinicaAlumnoServicio(info_clinica_alumno_repositorio)
info_bancaria_alumno_servicio = InfoBancariaAlumnoServicio(info_bancaria_alumno_repositorio)
inscripcion_servicio = InscripcionServicio(inscripcion_repositorio)

# Info del usuario DIRECTOR. Nombre de usuario: douglas345. Clave de usuario: 1234
# Info del usuario SECRETARIO. Nombre de usuario: Enmanuel86. Clave de usuario: 1212

nombre_usuario = input("- Ingrese su nombre de usuario: ")
clave_usuario = input("- Ingrese su clave de usuario: ")

try:
    USUARIO_ID_AUTENTICADO = usuario_servicio.autenticar_usuario(nombre_usuario, clave_usuario)
    app_configuracion.actualizar_usuario_id(USUARIO_ID_AUTENTICADO)
except BaseDatosError as error:
    print(f"{error}")
else:
    
    print("------------------------------------------------")
    print("     SELECCIONA A DONDE SE QUIERE IR")
    print("\n1. Registrar a un alumno.")
    print("2. Consultar la info de todos los alumnos.")
    print("------------------------------------------------")
    opcion = input("\n- Elige una opcion: ")
        
    permiso_registrar_alumnos = permiso_servicio.verificar_permiso_usuario(USUARIO_ID_AUTENTICADO, "CREAR ALUMNOS")
    permiso_consultar_alumnos = permiso_servicio.verificar_permiso_usuario(USUARIO_ID_AUTENTICADO, "CONSULTAR ALUMNOS")
        
    if (opcion == "1" and permiso_registrar_alumnos):
        campos_datos_alumno_1 = {
            "primer_nombre": "Miguel",
            "segundo_nombre": None,
            "apellido_paterno": "Infante",
            "apellido_materno": None,
            "cedula": "31485909",
            "relacion_con_rep": "Padre",
            "sexo": "M",
            "situacion": "Inicial",
            "fecha_ingreso_institucion": date.today()
        }
            
        errores_primera_info_alumno = alumno_servicio.validar_campos_primera_info_alumno(
                campos_datos_alumno_1.get("cedula"),
                campos_datos_alumno_1.get("primer_nombre"),
                campos_datos_alumno_1.get("segundo_nombre"),
                campos_datos_alumno_1.get("apellido_paterno"),
                campos_datos_alumno_1.get("apellido_materno"),
                campos_datos_alumno_1.get("relacion_con_rep"),
                campos_datos_alumno_1.get("fecha_ingreso_institucion")
            )
            
        if errores_primera_info_alumno:
                print("\n".join(errores_primera_info_alumno))
        else:
                print("- Primera parte sin errores.")
                
                campos_datos_alumno_2 = {
                    "cma": 0,
                    "imt": 0,
                    "fecha_nacimiento": date(2004, 1, 26),
                    "lugar_nacimiento": "Barcelona"
                }
                
                errores_segunda_info_alumno = alumno_servicio.validar_campos_segunda_info_alumno(
                    campos_datos_alumno_2.get("fecha_nacimiento"),
                    campos_datos_alumno_2.get("lugar_nacimiento")
                )
                
                if errores_segunda_info_alumno:
                    print("\n".join(errores_segunda_info_alumno))
                else:
                    print("- Segunda parte sin errores.")
                    
                    # Ingreso la cédula en la barra de búsqueda para que en el if verifique si existe el 
                    # registro (ver si es diferente de None)
                    cedula_representante = input("- Ingrese la cédula del representante: ")
                    
                    # Si el registro del representante por la cédula existe, entonces se bloquea los inputs y se muestra los datos
                    # sacados de este método y se extrae del mismo el representante_id para poder crear un registro en tb_alumnos
                    # más adelante con el diccionario campos_alumno
                    if (representante_servicio.obtener_representante_por_cedula(cedula_representante)):
                        print("ESTE REPRESENTANTE ESTÁ REGISTRADO. SUS DATOS SON:")
                        datos_representante = representante_servicio.obtener_representante_por_cedula(cedula_representante)
                        nombre_representante = datos_representante[2]
                        apellido_representante = datos_representante[3]
                        num_telefono_representante = datos_representante[5]
                        carga_familiar_representante = datos_representante[6]
                        direccion_residencia_representante = datos_representante[4]
                        estado_civil_representante = datos_representante[7]
                        
                        representante_id_retornado = datos_representante[0]
                        
                        print(f"- NOMBRE: {nombre_representante}")
                        print(f"- AEPLLIDO: {apellido_representante}")
                        print(f"- NÚMERO DE TELÉFONO: {num_telefono_representante}")
                        print(f"- CARGA FAMILIAR: {carga_familiar_representante}")
                        print(f"- DIRECCIÓN DE RESIDENCIA: {direccion_residencia_representante}")
                        print(f"- ESTADO CIVIL: {estado_civil_representante}")
                        
                        print("\n- Tercera parte sin errores.")
                    else:
                        # En caso de que no exista el registro en tb_representantes, la cédula del input se usa para
                        # ese registro nuevo de representante y los inputs restantes están habilitados para escribir
                        # (supongamos que el empleado escribió en los demás campos porque acá le puse un valor directamente)
                        campos_representante = {
                            "cedula": cedula_representante,
                            "nombre": "JOSÉ",
                            "apellido": "GÓMEZ",
                            "direccion_residencia": "BOYACÁ 2",
                            "num_telefono": "0412123678",
                            "carga_familiar": 4,
                            "estado_civil": None
                        }
                        
                        errores_datos_representante = representante_servicio.validar_campos_representante(
                            campos_representante.get("cedula"),
                            campos_representante.get("nombre"),
                            campos_representante.get("apellido"),
                            campos_representante.get("direccion_residencia"),
                            campos_representante.get("num_telefono"),
                            campos_representante.get("carga_familiar"),
                            campos_representante.get("estado_civil")
                        )
                        
                        if errores_datos_representante:
                            print("\n".join(errores_datos_representante))
                        else:
                            print("- Tercera parte sin errores")
                            representante_id_retornado = representante_servicio.registrar_representante(campos_representante)
                    
                    # En esta línea yo guardo el representante_id ya sea si de un representante registrado
                    # o de un representante nuevo (dependiendo del condicional)
                    representante_id = representante_id_retornado
                    
                    campos_info_academica = {
                        "escolaridad": "6to grado aprobado",
                        "procedencia": "Escuela tal"
                    }
                            
                    errores_info_academica = alumno_servicio.validar_info_academica(
                        campos_info_academica.get("escolaridad"),
                        campos_info_academica.get("procedencia")
                    )
                    
                    if errores_info_academica:
                        print("\n".join(errores_info_academica))
                    else:
                        print("- Cuarta parte sin errores.")

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
                            "fecha_ingreso_institucion": campos_datos_alumno_1.get("fecha_ingreso_institucion"),
                            "relacion_con_rep": campos_datos_alumno_1.get("relacion_con_rep"),
                            "escolaridad": campos_info_academica.get("escolaridad"),
                            "procedencia": campos_info_academica.get("procedencia"),
                            "situacion": campos_datos_alumno_1.get("situacion")
                        }
                        
                        # Acá guardo el alumno_id que retorno al crear un registro en la tabla tb_alumnos
                        # y lo uso para asociarlo a las demás tablas        
                        alumno_id = alumno_servicio.registrar_alumno(campos_alumno)
                    
                        campos_medidas_alumno = {
                            "alumno_id": alumno_id,
                            "estatura": 1.87,
                            "peso": 49.5,
                            "talla_camisa": "M",
                            "talla_pantalon": 30,
                            "talla_zapatos": 46
                        }
                    
                        errores_medidas_alumnos = medidas_alumno_servicio.validar_campos_medidas_alumnos(
                            campos_medidas_alumno.get("estatura"),
                            campos_medidas_alumno.get("peso"),
                            campos_medidas_alumno.get("talla_camisa"),
                            campos_medidas_alumno.get("talla_pantalon"),
                            campos_medidas_alumno.get("talla_zapatos")
                        )
                    
                        if errores_medidas_alumnos:
                            print("\n".join(errores_medidas_alumnos))
                        else:
                            print("- Quinta parte sin errores.")
                            
                            # Acá hacer la misma mecánica que hiciste al agregar diagnósticos y enfermedades
                            # ya que esto es algo opcional y solo se valida el tipo de cuenta y el num_cuenta
                            # al agregar con la mecánica de "carrito"
                            campos_info_bancaria_alumno = {
                                "alumno_id": alumno_id,
                                "tipo_cuenta": "CORRIENTE",
                                "num_cuenta": "086203045067"
                            }
                        
                            errores_info_bancaria_alumno = info_bancaria_alumno_servicio.validar_campos_info_bancaria_alumno(
                                campos_info_bancaria_alumno.get("tipo_cuenta"),
                                campos_info_bancaria_alumno.get("num_cuenta")
                            )
                            
                            if errores_info_bancaria_alumno:
                                print("\n".join(errores_info_bancaria_alumno))
                            else:
                                print("- Sexta parte sin errores.")
                                
                                # Acá lo mismo, la mecánica que hiciste para agregar diagnósticos
                                campos_info_clinica_alumno = {
                                    "alumno_id": alumno_id,
                                    "diagnostico_id": 1,
                                    "fecha_diagnostico": date(2006, 5, 13),
                                    "medico_tratante": "DR. ALEJANDRO",
                                    "certificacion_discap": "D-234796",
                                    "fecha_vencimiento_certif": date(2010, 5, 15),
                                    "medicacion": None,
                                    "observacion_adicional": None
                                }
                                
                                errores_info_clinica_alumno = info_clinica_alumno_servicio.valdidar_campos_info_clinica_alumno(
                                    campos_info_clinica_alumno.get("diagnostico_id"),
                                    campos_info_clinica_alumno.get("fecha_diagnostico"),
                                    campos_info_clinica_alumno.get("medico_tratante"),
                                    campos_info_clinica_alumno.get("certificacion_discap"),
                                    campos_info_clinica_alumno.get("fecha_vencimiento_certif"),
                                    campos_info_clinica_alumno.get("observacion_adicional")
                                )
                                    
                                if errores_info_clinica_alumno:
                                    print("\n".join(errores_info_clinica_alumno))
                                else:
                                    print("- Séptima parte sin errores.")
                                
                                
                                    campos_inscripcion = {
                                        "num_matricula": None, #Esto es None para que internamente se modifique este valor por el que se va a generar automáticamente
                                        "alumno_id": alumno_id,
                                        "especialidad_id": 1,
                                        "fecha_inscripcion": date.today(),
                                        "periodo_escolar": "2025-2026"
                                    }
                                    
                                    errores_inscripcion = inscripcion_servicio.valdiar_campos_inscripcion(
                                        campos_inscripcion.get("especialidad_id"),
                                        campos_inscripcion.get("fecha_inscripcion"),
                                        campos_inscripcion.get("periodo_escolar")
                                    )
                                    
                                    if errores_inscripcion:
                                        print("\n".join(errores_inscripcion))
                                    else:
                                        print("- Octava parte sin errores.")
                                        
                                        # Acá se registra lo demás pasándole los diccionarios
                                        medidas_alumno_servicio.registrar_medidas_alumno(campos_medidas_alumno)
                                        info_bancaria_alumno_servicio.registrar_info_bancaria_alumno(campos_info_bancaria_alumno)
                                        info_clinica_alumno_servicio.registrar_info_clinica_alumno(campos_info_clinica_alumno)
                                        inscripcion_servicio.registrar_inscripcion(campos_inscripcion)
    elif ((opcion == "2") and (permiso_consultar_alumnos)):
        try:
                todos_alumnos_inscritos = inscripcion_servicio.obtener_inscripcion_por_especialidad_o_cedula(1, "30466351")
                print(f"ESPECIALIDAD   MATRICULA    CÉDULA  PRIMER NOMBRE   APELLIDO PATERNO    FECHA DE INGRESO    SITUACIÓN")
                if (type(todos_alumnos_inscritos) == list):
                    for registro in todos_alumnos_inscritos:
                        print(f"{registro[3]}   {registro[4]}   {registro[5]}   {registro[6]}           {registro[8]}           {registro[10]}      {registro[11]}")
                else:
                    print(f"{todos_alumnos_inscritos[3]}    {todos_alumnos_inscritos[4]}    {todos_alumnos_inscritos[5]}    {todos_alumnos_inscritos[6]}        {todos_alumnos_inscritos[8]}        {todos_alumnos_inscritos[10]}   {todos_alumnos_inscritos[11]}")
        except BaseDatosError as error:
                print(error)