import sys
import random
import os
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QPainter, QColor, QFont

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
TIMER_INTERVAL = 150  # milisegundos
RECORD_FILE = "record.txt"

class SnakeGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Culebrita - PyQt5 Mejorada')
        self.setFixedSize(GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE + 50)  # espacio para puntaje

        self.timer = QTimer()
        self.timer.timeout.connect(self.move)

        # Elementos de UI
        self.retry_button = QPushButton('Reintentar', self)
        self.retry_button.setGeometry(self.width() // 2 - 50, self.height() // 2 - 25, 100, 50)
        self.retry_button.clicked.connect(self.start_game)
        self.retry_button.hide()

        self.score_label = QLabel(self)
        self.score_label.setGeometry(10, GRID_HEIGHT * CELL_SIZE + 10, 250, 30)
        self.score_label.setFont(QFont('Arial', 12))

        self.load_record()
        self.start_game()

    def load_record(self):
        if os.path.exists(RECORD_FILE):
            with open(RECORD_FILE, "r") as f:
                self.best_score = int(f.read())
        else:
            self.best_score = 0

    def save_record(self):
        with open(RECORD_FILE, "w") as f:
            f.write(str(self.best_score))

    def start_game(self):
        self.snake = [(5, 5), (4, 5), (3, 5)]  # posiciones iniciales
        self.direction = (1, 0)  # movemos a la derecha
        self.generate_food()
        self.timer.start(TIMER_INTERVAL)
        self.score = 0
        self.retry_button.hide()
        self.update_score_label()
        self.setFocus()  # <-- ¡esto es lo que faltaba!

    def generate_food(self):
        while True:
            self.food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if self.food not in self.snake:
                break

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Up and self.direction != (0, 1):
            self.direction = (0, -1)
        elif key == Qt.Key_Down and self.direction != (0, -1):
            self.direction = (0, 1)
        elif key == Qt.Key_Left and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif key == Qt.Key_Right and self.direction != (-1, 0):
            self.direction = (1, 0)

    def move(self):
        head_x, head_y = self.snake[0]
        delta_x, delta_y = self.direction
        new_head = (head_x + delta_x, head_y + delta_y)

        # Revisar colisiones
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
            new_head in self.snake):
            self.timer.stop()
            self.retry_button.show()
            if self.score > self.best_score:
                self.best_score = self.score
                self.save_record()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.generate_food()
            self.score += 1
            self.update_score_label()
        else:
            self.snake.pop()

        self.update()

    def update_score_label(self):
        self.score_label.setText(f"Puntaje: {self.score} | Mejor: {self.best_score}")

    def paintEvent(self, event):
        painter = QPainter(self)

        # Pintar culebra
        painter.setBrush(QColor(0, 255, 0))
        for x, y in self.snake:
            painter.drawRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

        # Pintar comida
        painter.setBrush(QColor(255, 0, 0))
        fx, fy = self.food
        painter.drawRect(fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = SnakeGame()
    game.show()
    sys.exit(app.exec_())
