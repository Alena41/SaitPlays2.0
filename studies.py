from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QFont, QPalette, QColor


class TWO(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Учёба')

        screen_geometry = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, screen_geometry.width(), screen_geometry.height())

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(144, 238, 144))
        self.setPalette(palette)

        horizontal_layout_top = QHBoxLayout()

        matche = QPushButton('Математика', self)
        matche.setFixedSize(300, 200)
        matche.setStyleSheet(self.button_style())
        matche.setFont(QFont("Arial", 24))
        matche.clicked.connect(self.clicked2)
        horizontal_layout_top.addWidget(matche)

        cl_but = QPushButton('Диктант', self)
        cl_but.setFixedSize(300, 200)
        cl_but.setStyleSheet(self.button_style())
        cl_but.setFont(QFont("Arial", 24))
        cl_but.clicked.connect(self.clicked23)
        horizontal_layout_top.addWidget(cl_but)

        horizontal_layout_middle = QHBoxLayout()

        Hone_but = QPushButton('Виселица', self)
        Hone_but.setFixedSize(300, 200)
        Hone_but.setStyleSheet(self.button_style())
        Hone_but.setFont(QFont("Arial", 24))
        Hone_but.clicked.connect(self.clicked71)
        horizontal_layout_middle.addWidget(Hone_but)

        Sub_but = QPushButton('Лабиринт', self)
        Sub_but.setFixedSize(300, 200)
        Sub_but.setStyleSheet(self.button_style())
        Sub_but.setFont(QFont("Arial", 24))
        Sub_but.clicked.connect(self.clicked72)
        horizontal_layout_middle.addWidget(Sub_but)

        horizontal_layout_bottom = QHBoxLayout()

        delf_but = QPushButton('Английский цвет', self)
        delf_but.setFixedSize(300, 200)
        delf_but.setStyleSheet(self.button_style())
        delf_but.setFont(QFont("Arial", 24))
        delf_but.clicked.connect(self.clicked25)
        horizontal_layout_bottom.addWidget(delf_but)

        pop_but = QPushButton('Животные', self)
        pop_but.setFixedSize(300, 200)
        pop_but.setStyleSheet(self.button_style())
        pop_but.setFont(QFont("Arial", 24))
        pop_but.clicked.connect(self.clicked96)
        horizontal_layout_bottom.addWidget(pop_but)

        vertical_layout = QVBoxLayout()
        vertical_layout.addLayout(horizontal_layout_top)
        vertical_layout.addLayout(horizontal_layout_middle)
        vertical_layout.addLayout(horizontal_layout_bottom)

        self.setLayout(vertical_layout)

        self.exites = QPushButton("Выйти", self)
        self.exites.setGeometry(10, 20, 150, 50)
        self.exites.setStyleSheet("background-color: rgb(255, 108, 47); color: rgb(0, 0, 0);")
        self.exites.setFont(QFont("Arial", 20))
        self.exites.clicked.connect(self.exet)

    def button_style(self):
        return """
            QPushButton {
                background-color: #6B8E23; 
                color: white; 
                border-radius: 10px; 
                border: none; 
            }

            QPushButton:hover {
                background-color: #556B2F; 
            }

            QPushButton:pressed {
                background-color: #6B8E23; 
            }
        """

    def exet(self):
        from main import MainWindow
        self.cals = MainWindow()
        self.cals.showFullScreen()
        self.close()

    def clicked2(self):
        from mateha import Evaluator
        self.cal = Evaluator()
        self.cal.showFullScreen()
        self.close()

    def clicked72(self):
        self.close()
        from labirint import Game
        lab = Game()
        lab.run()

    def clicked23(self):
        from texts import TextChecker
        self.cal1 = TextChecker()
        self.cal1.showFullScreen()
        self.close()

    def clicked71(self):
        self.close()
        from gallows import HangmanGame
        lab1 = HangmanGame()
        lab1.run()

    def clicked25(self):
        self.close()
        from englishColor import ColorGuessingGame
        lab2 = ColorGuessingGame()
        lab2.run()

    def clicked96(self):
        self.close()
        from animals import AnimalGame
        lab3 = AnimalGame()
        lab3.run()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = TWO()
    window.showFullScreen()
    sys.exit(app.exec())

