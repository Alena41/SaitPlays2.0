from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, \
    QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPalette, QColor


class ONE(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('игры')

        # Открывает окно на весь экран
        screen_geometry = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, screen_geometry.width(),
                         screen_geometry.height())

        # Установка цвета фона
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(144, 238, 144))
        self.setPalette(palette)

        # Создаем layout для кнопок сверху "Котики", "Кликер"
        horizontal_layout_top = QHBoxLayout()

        Kotiki_but = QPushButton('Таракашка', self)
        Kotiki_but.setFixedSize(300, 200)
        Kotiki_but.setStyleSheet(self.button_style())
        Kotiki_but.setFont(QFont("Arial", 24))
        Kotiki_but.clicked.connect(self.clicked5)
        horizontal_layout_top.addWidget(Kotiki_but)

        cl_but = QPushButton('Кликер', self)
        cl_but.setFixedSize(300, 200)
        cl_but.setStyleSheet(self.button_style())
        cl_but.setFont(QFont("Arial", 24))
        cl_but.clicked.connect(self.clicked)
        horizontal_layout_top.addWidget(cl_but)

        # Создаем layout для кнопок снизу "Соты", "Последовательность"
        horizontal_layout_middle = QHBoxLayout()

        Hone_but = QPushButton('Соты', self)
        Hone_but.setFixedSize(300, 200)
        Hone_but.setStyleSheet(self.button_style())
        Hone_but.setFont(QFont("Arial", 24))
        Hone_but.clicked.connect(self.clicked4)
        horizontal_layout_middle.addWidget(Hone_but)

        Sub_but = QPushButton('Цвета', self)
        Sub_but.setFixedSize(300, 200)
        Sub_but.setStyleSheet(self.button_style())
        Sub_but.setFont(QFont("Arial", 24))
        Sub_but.clicked.connect(self.cliked3)
        horizontal_layout_middle.addWidget(Sub_but)

        # Создаем layout для кнопок снизу "Дельфины", "Попочка"
        horizontal_layout_bottom = QHBoxLayout()

        delf_but = QPushButton('Дельфины', self)
        delf_but.setFixedSize(300, 200)
        delf_but.setStyleSheet(self.button_style())
        delf_but.setFont(QFont("Arial", 24))
        delf_but.clicked.connect(self.cliked52)
        horizontal_layout_bottom.addWidget(delf_but)

        pop_but = QPushButton('Пин-Понг', self)
        pop_but.setFixedSize(300, 200)
        pop_but.setStyleSheet(self.button_style())
        pop_but.setFont(QFont("Arial", 24))
        pop_but.clicked.connect(self.cliked53)
        # Добавьте функционал для "Попочка"
        horizontal_layout_bottom.addWidget(pop_but)

        # Создаем главный вертикальный layout
        vertical_layout = QVBoxLayout()
        vertical_layout.addLayout(horizontal_layout_top)   # Добавляем верхний ряд
        vertical_layout.addLayout(horizontal_layout_middle)  # Добавляем средний ряд
        vertical_layout.addLayout(horizontal_layout_bottom)  # Добавляем нижний ряд

        # Устанавливаем layout для QWidget
        self.setLayout(vertical_layout)

        self.exites = QPushButton("Выйти", self)
        self.exites.setGeometry(10, 20, 150, 50)
        self.exites.setStyleSheet(
            "background-color: rgb(255, 108, 47); color: rgb(0, 0, 0);")
        self.exites.setFont(QFont("Arial", 20))
        self.exites.clicked.connect(self.exet)

    def button_style(self):
        return """
            QPushButton {
                background-color: #6B8E23; /* Цвет фона */
                color: white; /* Цвет текста */
                border-radius: 10px; /* Радиус закругления углов */
                border: none; /* Убираем рамку */
            }

            QPushButton:hover {
                background-color: #556B2F; /* Цвет фона при наведении */
            }

            QPushButton:pressed {
                background-color: #6B8E23; /* Цвет фона при нажатии */
            }
        """

    def cliked52(self):
        self.close()
        from delphin import DolphinGame
        delp = DolphinGame()
        delp.run()

    # переход в файл с сотами
    def clicked4(self):
        self.close()
        from Honeycombs import Honeycomb
        sota = Honeycomb()
        sota.run()

    # выход из программы
    def exet(self):
        from main import MainWindow
        self.cals = MainWindow()
        self.cals.showFullScreen()
        self.close()

    # переход в файл с последовательностью
    def cliked3(self):
        self.close()
        from Colorposled import MemoryGame
        self.my_game = MemoryGame()
        self.my_game.showFullScreen()
        self.close()

    # Переход в файл Klicker
    def clicked(self):
        self.close()
        from Klicker import ReactionTimeTest
        reaction_time_test = ReactionTimeTest()
        reaction_time_test.run()

    # обработчик для кнопки "Таракашка"
    def clicked5(self):
        self.close()
        from Kykaracha_headsGame import WhackACat
        my_game = WhackACat()
        my_game.run()

    def cliked53(self):
        self.close()
        from pinPONG import PongGame
        my_game = PongGame()
        my_game.run()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = ONE()
    window.showFullScreen()
    sys.exit(app.exec())
