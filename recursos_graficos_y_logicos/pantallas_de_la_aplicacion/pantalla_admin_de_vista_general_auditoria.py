from PyQt5.QtCore import Qt,QPoint, QSortFilterProxyModel
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (QWidget, QHeaderView,  QVBoxLayout, 
                             QPushButton , QHBoxLayout,QMessageBox, QListWidget, QListWidgetItem, QLabel, QApplication)
from PyQt5 import QtGui, QtCore
from configuraciones.configuracion import app_configuracion
from ..elementos_graficos_a_py import Ui_VistaGeneralAuditorias
from ..utilidades.base_de_datos import auditoria_servicio, usuario_servicio
from ..utilidades.funciones_sistema import FuncionSistema

class PantallaDeVistaGeneralAuditorias(QWidget, Ui_VistaGeneralAuditorias):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.setupUi(self)
        
        self.usuario_auditados = auditoria_servicio.obtener_todos_auditorias() 
        
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
        
        
        self.cargar_usuarios_auditados_en_tabla(self.tbl_auditorias, self.usuario_auditados )
        
        
    def actualizar_auditorias(self):
        self.modelo.clear()
        self.usuario_auditados = auditoria_servicio.obtener_todos_auditorias() 
        self.cargar_usuarios_auditados_en_tabla(self.tbl_auditorias, self.usuario_auditados )
    
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
        
    
    def filtrar_por_usuario_id(self, index):
        """
            Metodo para filtrar las auditoria de x usuario tomando su id
        """
        
        try:
            
            cedula = self.modelo.item(index, 1).text()
            usuario = usuario_servicio.obtener_usuario_por_rol_o_cedula_empleado(cedula_empleado= cedula)
            usuario_id = usuario[0]
            
            auditoria_servicio.obtener_auditoria_por_id()
            
        except:
            self.modelo.removeRows(0, self.modelo.rowCount())
            
        else:
            self.cargar_usuarios_auditados_en_tabla(self.tbl_auditorias)

           
        