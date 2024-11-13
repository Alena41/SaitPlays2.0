from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel


class static1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 100, 300, 400)
        self.setWindowTitle('Рейтинг по математике')
        self.setFixedSize(self.size())

        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        pixmap = QPixmap('foto/statik.jpg')
        self.background_label.setPixmap(pixmap.scaled(self.width(),
                                                      self.height()))

        # Считываем данные из файла
        data = []
        with open("res_txt/results.txt", "r") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 2:  # Проверяем, что строка содержит 2 числа
                    data.append((int(parts[0]), int(parts[1])))

        # Сортировка по первому числу (максимальное в начале)
        # Затем по второму числу (минимальное в начале)
        data.sort(key=lambda x: (x[0], x[1]), reverse=True)

        vbox = QVBoxLayout()
        for i, (first, second) in enumerate(data[:10]):
            label = QLabel(f"{i+1} место: {first} {second}")
            label.setAlignment(Qt.AlignCenter)
            vbox.addWidget(label)
            font = label.font()
            font.setPointSize(20)
            font.setFamily("Times New Roman")
            label.setFont(font)
            label.setStyleSheet("color: black;")

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)


class static2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 100, 300, 400)
        self.setWindowTitle('Рейтинг в кликере')
        self.setFixedSize(self.size())

        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        pixmap = QPixmap('foto/statik.jpg')
        self.background_label.setPixmap(pixmap.scaled(self.width(),
                                                      self.height()))

        numbers = []
        with open("res_txt/Klicker_res.txt", "r") as file:
            for line in file:
                numbers.append(int(line.strip()))

        numbers = sorted(set(numbers))

        vbox = QVBoxLayout()
        for i in range(min(len(numbers), 10)):
            label = QLabel(f"{i + 1} место: {numbers[i]}")
            label.setAlignment(Qt.AlignCenter)
            vbox.addWidget(label)
            font = label.font()
            font.setPointSize(20)
            font.setFamily("Times New Roman")
            label.setFont(font)
            label.setStyleSheet("color: black;")

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)


class static3(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 100, 300, 400)
        self.setWindowTitle('Рейтинг в Сотах')
        self.setFixedSize(self.size())

        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        pixmap = QPixmap('foto/statik.jpg')
        self.background_label.setPixmap(
            pixmap.scaled(self.width(), self.height()))

        numbers = set()
        with open("res_txt/sota_res.txt", "r") as file:
            for line in file:
                numbers.add(int(line.strip()))

        numbers = sorted(numbers, reverse=True)[:10]

        vbox = QVBoxLayout()
        for i in range(len(numbers)):
            label = QLabel(f"{i + 1} место: {numbers[i]}")
            label.setAlignment(Qt.AlignCenter)
            vbox.addWidget(label)
            font = label.font()
            font.setPointSize(20)
            font.setFamily("Times New Roman")
            label.setFont(font)
            label.setStyleSheet("color: black;")

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)


class static4(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 100, 300, 400)
        self.setWindowTitle('Рейтинг в последовательности')
        self.setFixedSize(self.size())

        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        pixmap = QPixmap('foto/statik.jpg')
        self.background_label.setPixmap(
            pixmap.scaled(self.width(), self.height()))

        numbers = set()
        with open("res_txt/score.txt", "r") as file:
            for line in file:
                numbers.add(int(line.strip()))

        numbers = sorted(numbers, reverse=True)[:10]

        vbox = QVBoxLayout()
        for i in range(len(numbers)):
            label = QLabel(f"{i + 1} место: {numbers[i]}")
            label.setAlignment(Qt.AlignCenter)
            vbox.addWidget(label)
            font = label.font()
            font.setPointSize(20)
            font.setFamily("Times New Roman")
            label.setFont(font)
            label.setStyleSheet("color: black;")

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)


class static5(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 100, 300, 400)
        self.setWindowTitle('Рейтинг в Дельфинах')
        self.setFixedSize(self.size())

        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        pixmap = QPixmap('foto/statik.jpg')
        self.background_label.setPixmap(
            pixmap.scaled(self.width(), self.height()))

        numbers = set()
        with open("res_txt/delphin.txt", "r") as file:
            for line in file:
                numbers.add(int(line.strip()))

        numbers = sorted(numbers, reverse=True)[:10]

        vbox = QVBoxLayout()
        for i in range(len(numbers)):
            label = QLabel(f"{i + 1} место: {numbers[i]}")
            label.setAlignment(Qt.AlignCenter)
            vbox.addWidget(label)
            font = label.font()
            font.setPointSize(20)
            font.setFamily("Times New Roman")
            label.setFont(font)
            label.setStyleSheet("color: black;")

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)


class static6(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 100, 300, 400)
        self.setWindowTitle('Рейтинг в Таракашке')
        self.setFixedSize(self.size())

        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        pixmap = QPixmap('foto/statik.jpg')
        self.background_label.setPixmap(
            pixmap.scaled(self.width(), self.height()))

        numbers = set()
        with open("res_txt/final_score_cats.txt", "r") as file:
            for line in file:
                numbers.add(int(line.strip()))

        numbers = sorted(numbers, reverse=True)[:10]

        vbox = QVBoxLayout()
        for i in range(len(numbers)):
            label = QLabel(f"{i + 1} место: {numbers[i]}")
            label.setAlignment(Qt.AlignCenter)
            vbox.addWidget(label)
            font = label.font()
            font.setPointSize(20)
            font.setFamily("Times New Roman")
            label.setFont(font)
            label.setStyleSheet("color: black;")

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

class static7(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 100, 300, 400)
        self.setWindowTitle('Рейтинг в Лабиринте')
        self.setFixedSize(self.size())

        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        pixmap = QPixmap('foto/statik.jpg')
        self.background_label.setPixmap(
            pixmap.scaled(self.width(), self.height()))

        numbers = set()
        with open("res_txt/LABIR.txt", "r") as file:
            for line in file:
                numbers.add(int(line.strip()))

        numbers = sorted(numbers, reverse=True)[:10]

        vbox = QVBoxLayout()
        for i in range(len(numbers)):
            label = QLabel(f"{i + 1} место: {numbers[i]}")
            label.setAlignment(Qt.AlignCenter)
            vbox.addWidget(label)
            font = label.font()
            font.setPointSize(20)
            font.setFamily("Times New Roman")
            label.setFont(font)
            label.setStyleSheet("color: black;")

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)


class static8(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 100, 300, 400)
        self.setWindowTitle('Рейтинг в Английском цвете')
        self.setFixedSize(self.size())

        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        pixmap = QPixmap('foto/statik.jpg')
        self.background_label.setPixmap(
            pixmap.scaled(self.width(), self.height()))

        numbers = set()
        with open("res_txt/english.txt", "r") as file:
            for line in file:
                numbers.add(int(line.strip()))

        numbers = sorted(numbers, reverse=True)[:10]

        vbox = QVBoxLayout()
        for i in range(len(numbers)):
            label = QLabel(f"{i + 1} место: {numbers[i]}")
            label.setAlignment(Qt.AlignCenter)
            vbox.addWidget(label)
            font = label.font()
            font.setPointSize(20)
            font.setFamily("Times New Roman")
            label.setFont(font)
            label.setStyleSheet("color: black;")

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)


class static9(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 100, 300, 400)
        self.setWindowTitle('Рейтинг в животных')
        self.setFixedSize(self.size())

        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        pixmap = QPixmap('foto/statik.jpg')
        self.background_label.setPixmap(
            pixmap.scaled(self.width(), self.height()))

        numbers = set()
        with open("res_txt/animals_res.txt", "r") as file:
            for line in file:
                numbers.add(int(line.strip()))

        numbers = sorted(numbers, reverse=True)[:10]

        vbox = QVBoxLayout()
        for i in range(len(numbers)):
            label = QLabel(f"{i + 1} место: {numbers[i]}")
            label.setAlignment(Qt.AlignCenter)
            vbox.addWidget(label)
            font = label.font()
            font.setPointSize(20)
            font.setFamily("Times New Roman")
            label.setFont(font)
            label.setStyleSheet("color: black;")

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)
