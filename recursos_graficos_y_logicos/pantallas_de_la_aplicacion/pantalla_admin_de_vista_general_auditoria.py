from PyQt5.QtCore import (Qt, QDate)
from PyQt5.QtGui import (QStandardItemModel, QStandardItem)
from PyQt5.QtWidgets import (QWidget, QHeaderView,
                            )
from ..elementos_graficos_a_py import Ui_VistaGeneralAuditorias
from ..utilidades.base_de_datos import auditoria_servicio, usuario_servicio
from ..utilidades.funciones_sistema import FuncionSistema
from datetime import date

class PantallaDeVistaGeneralAuditorias(QWidget, Ui_VistaGeneralAuditorias):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.setupUi(self)
        
        self.usuario_auditados = auditoria_servicio.obtener_todos_auditorias() 
        self.lista_usuarios = usuario_servicio.obtener_todos_usuarios()
        self.dateedit_filtro_fecha_auditoria.setDate(QDate.currentDate())
        
        # definimos el modelo para el qtableview
        self.modelo = QStandardItemModel()
        
        # Estableciendo estilo de la tabla
        #self.tabla_ver_alumnos.setColumnWidth(6, 300) 

        self.tbl_auditorias.horizontalHeader().setVisible(True)
        self.tbl_auditorias.horizontalHeader().setMinimumHeight(50)
        self.tbl_auditorias.horizontalHeader().setMinimumWidth(10)
        self.tbl_auditorias.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tbl_auditorias.horizontalHeader().setSectionsClickable(False)
        
        self.tbl_auditorias.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tbl_auditorias.verticalHeader().setVisible(True)
        self.tbl_auditorias.verticalHeader().setMinimumWidth(40)
        self.tbl_auditorias.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.tbl_auditorias.verticalHeader().setFixedWidth(20)

        #esto me da el valor de la cedula al darle click a la persona que quiero
        self.tbl_auditorias.clicked.connect(lambda index: print(index.sibling(index.row(), 0).data()))

        # Opcional: desactivar clic en el encabezado vertical
        self.tbl_auditorias.verticalHeader().setSectionsClickable(True)

        self.boton_de_regreso.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(12))
        self.dateedit_filtro_fecha_auditoria.dateChanged.connect(lambda: self.filtrar_auditoria_por_fecha())
        self.barra_de_busqueda.returnPressed.connect(lambda texto: self.filtrar_auditoria_por_fecha(texto))
        self.barra_de_busqueda.textChanged.connect(lambda texto: None if not texto == "" else self.filtrar_auditoria_por_fecha())
        self.boton_buscar.clicked.connect(lambda: self.filtrar_auditoria_por_fecha(self.barra_de_busqueda.text()))
        
        FuncionSistema.configurar_barra_de_busqueda(self, self.barra_de_busqueda, self.lista_usuarios, 4, 5, 1 )
        
        
        
        
    def actualizar_auditorias(self):
        self.modelo.clear()
        self.filtrar_auditoria_por_fecha()
    
    def cargar_usuarios_auditados_en_tabla(self, tabla, usuarios_auditados):
        columnas = [
            "Cédula", "Usuario", "Rol", "Entidad Afectada", 
            "Acción", "Fecha", "Hora"
            
        ]

        usuarios_auditados = reversed(usuarios_auditados)
        
        self.modelo = QStandardItemModel()
        self.modelo.setHorizontalHeaderLabels(columnas)

        # Primero cargamos los datos
        for indice, usuario in enumerate(usuarios_auditados):
            datos_visibles = [
            usuario[2],  # cedula
            usuario[1],  # Nombre del usuario
            usuario[4],  # Rol
            usuario[5],  # Ente afectado
            usuario[6],  # accion
            usuario[7],  # Fecha
            usuario[8]   # Hora
            ]

            items = []
            for dato in datos_visibles:
                item = QStandardItem(str(dato) if dato is not None else "")
                # Evita edición del usuario
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                items.append(item)

            # Agregar la fila completa
            self.modelo.appendRow(items)

            # Numerar filas en el encabezado vertical
            header_item = QStandardItem(str(indice + 1))
            header_item.setFlags(Qt.ItemIsEnabled)
            self.modelo.setVerticalHeaderItem(indice, header_item)
            
            tooltip_text = usuario[6]
            
            if tooltip_text:
                # Aplicamos el tooltip a TODAS las celdas de esta fila
                for col in range(self.modelo.columnCount() - 1):  # -1 para excluir columna Opciones
                    item = self.modelo.item(indice, col)
                    if item:
                        item.setToolTip(tooltip_text)
            
        # Muy importante: asignar self.modelo primero
        tabla.setModel(self.modelo)
        
            # AJUSTES DE ALTURA DE FILAS
        for fila in range(self.modelo.rowCount()):
            tabla.setRowHeight(fila, 40)
        
    
    def filtrar_auditoria_por_fecha(self, nombre_usuario = None):
        """
            Metodo para filtrar las auditoria de x usuario tomando su id
        """
        
        try:
            
            
            rol_usuario = None
            fecha = date(self.dateedit_filtro_fecha_auditoria.date().year(),
                         self.dateedit_filtro_fecha_auditoria.date().month(), 
                         self.dateedit_filtro_fecha_auditoria.date().day())
            
            lista_auditorias = auditoria_servicio.obtener_auditorias_por_fecha_rol_y_usuario(fecha_accion= fecha, tipo_rol= rol_usuario, nombre_usuario= nombre_usuario)
            
        except:
            self.modelo.removeRows(0, self.modelo.rowCount())
            
        else:
            self.cargar_usuarios_auditados_en_tabla(self.tbl_auditorias, lista_auditorias)

            
           
        