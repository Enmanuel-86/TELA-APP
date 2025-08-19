from PyQt5.QtWidgets import (QApplication, QTableView, QHeaderView,
                            QStyledItemDelegate)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem

# Datos de ejemplo (deberías reemplazarlos con tus datos reales)
datos = [
    ["17356256", "DOUGLAS", "JOSE", "MARQUEZ", "BETANCOURT", "Activo"],
    ["18128119", "ROSMARY", "DEL VALLE", "SALAS", "JIMENEZ", "Activo"],
    # ... resto de tus datos
]

model = QStandardItemModel()
model.setHorizontalHeaderLabels(["Cédula", "Primer Nombre", "Segundo Nombre",
                               "Apellido Paterno", "Apellido Materno", "Estado"])

for row in datos:
    items = [QStandardItem(str(item)) for item in row]
    model.appendRow(items)

tableView = QTableView()
tableView.setModel(model)

# Configurar el ajuste de columnas
tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
tableView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

# Opcional: ajustar algunas columnas manualmente si es necesario
tableView.setColumnWidth(0, 100)  # Cédula

# Mostrar la tabla
tableView.show()