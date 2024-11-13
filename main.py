import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout,
                             QDesktopWidget, QComboBox, QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor

from satisticks import static1, static2, static3, static4, static5, static6, static7, static8,static9


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Главное окно')

        # Открывает окно на весь экран
        screen_geometry = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, screen_geometry.width(),
                         screen_geometry.height())

        # Установка цвета фона
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(144, 238, 144))
        self.setPalette(palette)

        # Создание кнопок
        self.button_games = QPushButton("Моторика")
        self.button_games.clicked.connect(self.open_plays)
        self.button_games.setFixedSize(300, 200)
        self.button_games.setFont(QFont("Arial", 30))
        self.button_games.setStyleSheet("""
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
        """)

        self.button_settings = QPushButton("Образование")
        self.button_settings.clicked.connect(self.open_studies)
        self.button_settings.setFixedSize(300, 200)
        self.button_settings.setFont(QFont("Arial", 30))
        self.button_settings.setStyleSheet("""
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
        """)

        self.exites = QPushButton("Выйти", self)
        self.exites.setGeometry(10, 20, 150, 50)
        self.exites.setStyleSheet(
            "background-color: rgb(220, 20, 60); color: rgb(0, 0, 0);")
        self.exites.setFont(QFont("Arial", 20))
        self.exites.clicked.connect(self.exet)

        # Создание горизонтального макета
        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignCenter)  # Выравниваем по центру
        hbox.addWidget(self.button_games)
        hbox.addWidget(self.button_settings)

        # ComboBox
        combobox = QComboBox(self)
        combobox.setFixedSize(self.width() - 25, 100)
        combobox.setStyleSheet(
            "background-color: rgb(125, 100, 45); color: rgb(0, 0, 0);")
        combobox.setFont(QFont("Arial", 20))
        combobox.addItem("Статистика Кликера")
        combobox.addItem("Статистика Сот")
        combobox.addItem("Статистика Цвета")
        combobox.addItem("Статистика Математики")
        combobox.addItem("Статистика Таракашки")
        combobox.addItem("Статистика Лабиринта")
        combobox.addItem("Статистика Английского цвета")
        combobox.addItem("Статистика Дельфинов")
        combobox.addItem("Статистика Животных")
        combobox.currentIndexChanged.connect(self.combobox_changed)

        # Создание вертикального макета
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)  # Добавляем горизонтальный макет в вертикальный
        vbox.addWidget(combobox)  # Добавляем ComboBox в нижнюю часть
        vbox.setSpacing(20)  # Устанавливаем отступ между элементами

        # Установка макета для окна
        self.setLayout(vbox)

    def open_plays(self):
        # Запускаем файл plays.py
        # Используйте модуль subprocess для запуска скриптов Python
        import subprocess
        self.close()
        subprocess.run(["python", "plays.py"])

    def combobox_changed(self, index):
        if index == 0:
            self.cal2 = static2()
            self.cal2.show()
        elif index == 1:
            self.cal3 = static3()
            self.cal3.show()
        elif index == 2:
            self.cal4 = static4()
            self.cal4.show()
        elif index == 3:
            self.cal1 = static1()
            self.cal1.show()
        elif index == 4:
            self.cal6 = static6()
            self.cal6.show()
        elif index == 5:
            self.cal7 = static7()
            self.cal7.show()
        elif index == 6:
            self.cal8 = static8()
            self.cal8.show()
        elif index == 7:
            self.cal5 = static5()
            self.cal5.show()
        elif index == 8:
            self.cal9 = static9()
            self.cal9.show()



    def open_studies(self):
        # Запускаем файл studies.py
        # Используйте модуль subprocess для запуска скриптов Python
        import subprocess
        self.close()
        subprocess.run(["python", "studies.py"])

    # выход из программы
    def exet(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    sys.exit(app.exec_())
