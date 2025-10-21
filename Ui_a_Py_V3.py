import os
import sys
from io import StringIO
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox,
    QProgressBar, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.uic import compileUi  # Compila el archivo .ui


class UiConverterThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)

    def __init__(self, input_files, output_folder):
        super().__init__()
        self.input_files = input_files
        self.output_folder = output_folder

    def run(self):
        try:
            import re

            total_files = len(self.input_files)
            for index, input_file in enumerate(self.input_files):
                base_name = os.path.splitext(os.path.basename(input_file))[0]
                output_file = os.path.join(self.output_folder, f"{base_name}_gui.py")

                # Compilar .ui a texto en memoria
                buffer = StringIO()
                compileUi(input_file, buffer)
                content = buffer.getvalue()

                # 1️⃣ Eliminar línea "reading ui file"
                lines = [line for line in content.splitlines() if "reading ui file" not in line]
                content = "\n".join(lines)

                # 2️⃣ Insertar definición BASE_DIR al principio
                content_lines = content.splitlines()
                insert_index = 0
                for i, line in enumerate(content_lines):
                    if line.startswith("from") or line.startswith("import"):
                        insert_index = i + 1
                content_lines.insert(insert_index, "import os\nBASE_DIR = os.path.dirname(__file__)")
                content = "\n".join(content_lines)

                # 3️⃣ Convertir rutas absolutas → os.path.join(BASE_DIR, "ruta_relativa")
                ui_dir = os.path.dirname(input_file)
                py_dir = os.path.dirname(output_file)

                def make_relative(abs_path):
                    # Ruta relativa desde el archivo .py
                    rel_path = os.path.relpath(abs_path, start=py_dir)
                    rel_path = rel_path.replace("\\", "/")
                    return f'os.path.join(BASE_DIR, "{rel_path}")'

                # QPixmap(...)
                matches = re.findall(r'QtGui\.QPixmap\("([^"]+)"\)', content)
                for abs_path in matches:
                    if os.path.isabs(abs_path) and os.path.exists(abs_path):
                        content = content.replace(
                            f'QtGui.QPixmap("{abs_path}")',
                            f'QtGui.QPixmap({make_relative(abs_path)})'
                        )

                # addPixmap(QtGui.QPixmap(...))
                matches = re.findall(r'addPixmap\(QtGui\.QPixmap\("([^"]+)"\)', content)
                for abs_path in matches:
                    if os.path.isabs(abs_path) and os.path.exists(abs_path):
                        content = content.replace(
                            f'addPixmap(QtGui.QPixmap("{abs_path}")',
                            f'addPixmap(QtGui.QPixmap({make_relative(abs_path)})'
                        )

                # 4️⃣ Guardar archivo convertido
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(content)

                # Progreso
                self.progress.emit(int((index + 1) / total_files * 100))

            self.finished.emit(True, "Conversión completada con rutas portables 🟢")
        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conversor UI → PyQt5 (rutas portables)")
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

        # Agregar widgets al layout principal
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
