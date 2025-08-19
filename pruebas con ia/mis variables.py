import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableView, QStyledItemDelegate,
    QPushButton, QStyle, QStyleOptionButton, QMessageBox
)
from PyQt5.QtCore import Qt, QModelIndex, QRect
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class ButtonDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        """Dibuja dos botones (Editar y Borrar) en la celda"""
        self.edit_button = QStyleOptionButton()
        self.delete_button = QStyleOptionButton()

        # Botón Editar
        self.edit_button.rect = QRect(option.rect.x(), option.rect.y(), 60, option.rect.height())
        self.edit_button.text = "Editar"
        self.edit_button.state = QStyle.State_Enabled

        # Botón Borrar
        self.delete_button.rect = QRect(option.rect.x() + 65, option.rect.y(), 60, option.rect.height())
        self.delete_button.text = "Borrar"
        self.delete_button.state = QStyle.State_Enabled

        # Pintar botones
        QApplication.style().drawControl(QStyle.CE_PushButton, self.edit_button, painter)
        QApplication.style().drawControl(QStyle.CE_PushButton, self.delete_button, painter)

    def editorEvent(self, event, model, option, index):
        """Detecta clics en los botones"""
        if event.type() == event.MouseButtonRelease:
            x = event.pos().x()
            if option.rect.x() <= x <= option.rect.x() + 60:
                QMessageBox.information(None, "Acción", f"Editar fila {index.row()}")
            elif option.rect.x() + 65 <= x <= option.rect.x() + 125:
                QMessageBox.warning(None, "Acción", f"Borrar fila {index.row()}")
        return True


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tabla con botones en PyQt5")

        # Modelo
        self.model = QStandardItemModel(0, 3)
        self.model.setHorizontalHeaderLabels(["Nombre", "Edad", "Acciones"])

        # Agregar datos de ejemplo
        data = [("Juan", 25), ("María", 30), ("Pedro", 28)]
        for nombre, edad in data:
            self.model.appendRow([
                QStandardItem(nombre),
                QStandardItem(str(edad)),
                QStandardItem("")  # Columna de botones
            ])

        # Vista
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.setItemDelegateForColumn(2, ButtonDelegate())
        self.setCentralWidget(self.view)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(500, 300)
    window.show()
    sys.exit(app.exec_())
