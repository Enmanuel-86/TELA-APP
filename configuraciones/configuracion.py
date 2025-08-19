import userpaths
from pathlib import Path


class Configuracion:
    USUARIO_ID: None = None
    NOMBRE_BD: str = "tela.db"
    DIRECTORIO_BD: Path = Path(__file__).resolve().parent.parent / "base_datos"
    RUTA_BD: str = str(DIRECTORIO_BD / NOMBRE_BD)
    DIRECTORIO_RESPALDO: Path = Path(userpaths.get_my_documents()) / "respaldos-telapp"
    DIRECTORIO_REPORTES_ALUMNOS: Path = Path(userpaths.get_my_documents()) / "reportes-alumnos"
    DIRECTORIO_REPORTES_EMPLEADOS: Path = Path(userpaths.get_my_documents()) / "reportes-empleados"
    
    _instancia = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instancia:
            cls._instancia = super().__new__(cls, *args, **kwargs)
        return cls._instancia
    
    def actualizar_usuario_id(cls, nuevo_usuario_id: int) -> None:
        cls.USUARIO_ID = nuevo_usuario_id

app_configuracion = Configuracion()