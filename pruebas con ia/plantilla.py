from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QListWidget, 
    QListWidgetItem, QHBoxLayout, QLabel, QPushButton
)
from PyQt5.QtCore import Qt

class ListWidgetWithButtons(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lista con Botones por Elemento")
        self.resize(400, 300)

        # Layout principal
        layout = QVBoxLayout()
        self.setLayout(layout)

        # ListWidget que contendrá los elementos personalizados
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        # Botón para agregar nuevos elementos (opcional)
        self.add_button = QPushButton("Agregar Elemento")
        self.add_button.clicked.connect(self.add_item)
        layout.addWidget(self.add_button)

        # Agregar algunos elementos iniciales
        self.add_item("Manzana")
        self.add_item("Banana")
        self.add_item("Naranja")

    def add_item(self, text=None):
        # Crear un QListWidgetItem
        item = QListWidgetItem()
        self.list_widget.addItem(item)

        # Crear un widget personalizado para la fila
        widget = QWidget()
        row_layout = QHBoxLayout()
        widget.setLayout(row_layout)

        # Label para el texto
        label = QLabel(text if text else f"Elemento {self.list_widget.count() + 1}")
        row_layout.addWidget(label)

        # Botón para eliminar
        delete_button = QPushButton("Eliminar")
        delete_button.clicked.connect(lambda: self.delete_item(item))
        row_layout.addWidget(delete_button)

        # Asignar el widget al QListWidgetItem
        item.setSizeHint(widget.sizeHint())
        self.list_widget.setItemWidget(item, widget)

    def delete_item(self, item):
        # Obtener la fila del item y eliminarlo
        row = self.list_widget.row(item)
        self.list_widget.takeItem(row)

if __name__ == "__main__":
    app = QApplication([])
    window = ListWidgetWithButtons()
    window.show()
    app.exec_()