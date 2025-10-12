import os
import sys
from io import StringIO
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox,
    QProgressBar, QListWidget, QListWidgetItem
)
from PySide2.QtCore import QThread, Signal
from PyQt5.uic import compileUi  # Se usa solo para compilar en memoria


class UiConverterThread(QThread):
    progress = Signal(int)
    finished = Signal(bool, str)

    def __init__(self, input_files, output_folder):
        super().__init__()
        self.input_files = input_files
        self.output_folder = output_folder

    def run(self):
        try:
            total_files = len(self.input_files)
            for index, input_file in enumerate(self.input_files):
                base_name = os.path.splitext(os.path.basename(input_file))[0]
                output_file = os.path.join(self.output_folder, f"{base_name}_gui.py")

                buffer = StringIO()
                compileUi(input_file, buffer)
                content = buffer.getvalue()

                # Limpiar línea con ruta absoluta
                lines = [line for line in content.splitlines() if "reading ui file" not in line]
                content = "\n".join(lines)

                # Reemplazar PyQt5 → PySide2
                content = content.replace("from PyQt5 import", "from PySide2 import")

                # Guardar archivo convertido
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(content)

                self.progress.emit(int((index + 1) / total_files * 100))

            self.finished.emit(True, "Conversión completada con éxito!")
        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conversor UI → PySide2")
        self.setGeometry(100, 100, 600, 400)
        self.init_ui()
        self.converter_thread = None
        self.output_folder = ""
        self.selected_files = []

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # Sección selección de archivos
        input_layout = QHBoxLayout()
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Selecciona archivos .ui")
        self.input_line.setReadOnly(True)
        self.input_btn = QPushButton("Examinar...")
        self.input_btn.clicked.connect(self.browse_ui_files)
        input_layout.addWidget(self.input_line)
        input_layout.addWidget(self.input_btn)

        # Lista de archivos seleccionados
        self.file_list_widget = QListWidget()
        self.file_list_widget.setStyleSheet("""
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 5px;
                background-color: #f9f9f9;
            }
        """)

        # Carpeta de salida
        output_layout = QHBoxLayout()
        self.output_line = QLineEdit()
        self.output_line.setPlaceholderText("Selecciona carpeta para guardar .py")
        self.output_line.setReadOnly(True)
        self.output_btn = QPushButton("Examinar...")
        self.output_btn.clicked.connect(self.browse_output_folder)
        output_layout.addWidget(self.output_line)
        output_layout.addWidget(self.output_btn)

        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #bbb;
                border-radius: 8px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #5cb85c;
                border-radius: 8px;
            }
        """)

        # Botón de conversión
        self.convert_btn = QPushButton("Convertir")
        self.convert_btn.clicked.connect(self.convert_ui)
        self.convert_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                border-radius: 10px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # Agregar todos los widgets al layout principal
        main_layout.addLayout(input_layout)
        main_layout.addWidget(QLabel("Archivos seleccionados:"))
        main_layout.addWidget(self.file_list_widget)
        main_layout.addLayout(output_layout)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.convert_btn)

    def browse_ui_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Seleccionar archivo(s) UI", "", "Qt Designer Files (*.ui)"
        )
        if files:
            self.selected_files = files
            self.input_line.setText(f"{len(files)} archivo(s) seleccionado(s)")
            self.file_list_widget.clear()
            for f in files:
                item = QListWidgetItem(os.path.basename(f))
                self.file_list_widget.addItem(item)

    def browse_output_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de destino")
        if folder_path:
            self.output_folder = folder_path
            self.output_line.setText(folder_path)

    def convert_ui(self):
        if not self.selected_files:
            QMessageBox.warning(self, "Advertencia", "Debes seleccionar al menos un archivo .ui!")
            return
        if not self.output_folder:
            QMessageBox.warning(self, "Advertencia", "Debes seleccionar una carpeta de destino!")
            return

        self.input_btn.setEnabled(False)
        self.output_btn.setEnabled(False)
        self.convert_btn.setEnabled(False)
        self.progress_bar.setValue(0)

        self.converter_thread = UiConverterThread(self.selected_files, self.output_folder)
        self.converter_thread.progress.connect(self.update_progress)
        self.converter_thread.finished.connect(self.conversion_finished)
        self.converter_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def conversion_finished(self, success, message):
        self.input_btn.setEnabled(True)
        self.output_btn.setEnabled(True)
        self.convert_btn.setEnabled(True)

        if success:
            QMessageBox.information(self, "Éxito", message)
        else:
            QMessageBox.critical(self, "Error", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
