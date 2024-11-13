import sys
import random

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, QLabel,
    QDesktopWidget, QVBoxLayout, QFrame
)


class Evaluator(QWidget):
    """
        Класс, реализующий графический интерфейс приложения для обучения математике.
        """

    def __init__(self):
        """
                Инициализирует объект Evaluator, устанавливает начальное состояние
                и создает элементы пользовательского интерфейса.
                """
        super().__init__()
        self.correct_answers_count = 0
        self.incorrect_answers_count = 0
        self.initUI()
        self.loadNextExample()
        self.playBackgroundMusic()

    def initUI(self):
        """
                Создает элементы пользовательского интерфейса:
                - Поля ввода для примера, ответа, правильных и неправильных ответов.
                - Кнопки "Проверить", "Выйти" и "Информация".
                - Фрейм для отображения информации о правилах.
                """
        screen_geometry = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, screen_geometry.width(),
                         screen_geometry.height())
        self.setStyleSheet("background-color: #007f7f;")

        self.example = QLineEdit(self)
        self.example.setGeometry(self.width() // 2 - 200,
                                 self.height() // 2 - 100, 400, 120)
        self.example.setAlignment(Qt.AlignCenter)
        self.example.setEnabled(False)
        self.example.setStyleSheet("color: black;")
        self.example.setFont(QFont("Arial", 32))

        self.otvet = QLineEdit(self)
        self.otvet.setText("")
        self.otvet.setGeometry(self.width() // 2 - 200,
                               self.height() // 2 + 50, 400, 120)
        self.otvet.setStyleSheet("color: black;")
        self.otvet.setFont(QFont("Arial", 32))

        self.correct_counter = QLineEdit(self)
        self.correct_counter.setText("Правильных ответов: 0")
        self.correct_counter.setGeometry(30, 30, 300, 50)
        self.correct_counter.setStyleSheet(
            "color: black; border: 2px solid white;")
        self.correct_counter.setFont(QFont("Arial", 20))
        self.correct_counter.setEnabled(False)

        self.counter = QLineEdit(self)
        self.counter.setText("Счёт ошибок: 0")
        self.counter.setGeometry(30, 100, 300, 50)
        self.counter.setStyleSheet("color: black; border: 2px solid white;")
        self.counter.setFont(QFont("Arial", 20))
        self.counter.setEnabled(False)

        self.proverka = QPushButton('Проверить', self)
        self.proverka.setGeometry(self.width() - 400, self.height() - 320, 200,
                                  80)
        self.proverka.setStyleSheet(
            "background-color: rgb(255, 204, 153); color: rgb(0, 0, 0);")
        self.proverka.setFont(QFont("Arial", 20))
        self.proverka.clicked.connect(self.checkAnswer)

        self.save_button = QPushButton('Выйти', self)
        self.save_button.setGeometry(10, self.height() - 90, 400, 80)
        self.save_button.setStyleSheet(
            "background-color: rgb(255, 204, 153); color: rgb(0, 0, 0);")
        self.save_button.setFont(QFont("Arial", 20))
        self.save_button.clicked.connect(self.saveResult)

        self.info_button = QPushButton("!", self)
        self.info_button.setStyleSheet(
            "background-color: green; color: white; border-radius: 20px; font-size: 20px;"
        )
        self.info_button.setGeometry(self.width() - 50, 10, 40, 40)
        self.info_button.clicked.connect(self.showInfo)

        self.info_frame = QFrame(self)
        self.info_frame.setGeometry(
            self.width() // 2 - 280,
            self.height() // 2 - 390,
            600,
            200
        )
        self.info_frame.setStyleSheet(
            "background-color: white; border: 2px solid black; padding: 10px;"
        )
        self.info_frame.setVisible(False)

        info_layout = QVBoxLayout()
        info_label = QLabel("<h2>Правила игры</h2>")
        info_label.setAlignment(Qt.AlignCenter)
        info_text = QLabel(
            """
            1. Прочитайте пример.
            2. Введите ответ в поле ввода.
            3. Нажмите "Проверить" для проверки ответа.
            4. После каждой проверки будет выводиться новый пример.
            """
        )
        info_text.setWordWrap(True)
        info_layout.addWidget(info_label)
        info_layout.addWidget(info_text)
        self.info_frame.setLayout(info_layout)

    def playBackgroundMusic(self):
        """
               Запускает фоновую музыку.
               """
        self.player = QMediaPlayer()
        music_path = "songs/1728836356345l44tv41a.mp3"
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(music_path)))
        self.player.setVolume(50)
        self.player.setPlaybackRate(1.0)

        self.player.mediaStatusChanged.connect(self.loopMusic)

        self.player.play()

    def loopMusic(self, status):
        """
               Циклически повторяет фоновую музыку при достижении конца.
               """
        if status == QMediaPlayer.EndOfMedia:
            self.player.setPosition(0)
            self.player.play()

    def keyPressEvent(self, event):
        """
              Обрабатывает нажатие клавиш Enter или Return, вызывая проверку ответа.
              """
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.checkAnswer()

    def loadNextExample(self):
        """
                Генерирует новый пример и отображает его в поле ввода.
                """
        operations_1 = ["*", "/"]
        operations_2 = ["+", "-"]

        operand_1 = random.randint(0, 9)
        operation_1 = random.choice(operations_1)

        if operation_1 == "/":
            operand_2 = random.randint(1, 9)
            while operand_1 % operand_2 != 0:
                operand_2 = random.randint(1, 9)
        else:
            operand_2 = random.randint(1, 9)

        operation_2 = random.choice(operations_2)
        operand_3 = random.randint(0, 9)

        if operation_1 == "*":
            result = operand_1 * operand_2
        else:
            result = operand_1 // operand_2

        if operation_2 == "+":
            result += operand_3
        else:
            result -= operand_3

        self.current_example = (f"{operand_1} {operation_1} {operand_2} "
                                f"{operation_2} {operand_3} =")
        self.current_reward = str(result)

        self.example.setText(self.current_example)

    def checkAnswer(self):
        """
                Проверяет ответ пользователя, обновляет счетчики правильных и неправильных ответов
                и генерирует новый пример.
                """
        user_response = self.otvet.text()

        if user_response == self.current_reward:
            self.updateCorrectAnswersCount()
        else:
            self.updateIncorrectAnswersCount()

        self.loadNextExample()
        self.otvet.clear()

    def updateCorrectAnswersCount(self):
        """
                Обновляет счетчик правильных ответов.
                """
        self.correct_answers_count += 1
        self.correct_counter.setText(
            f"Счёт правильных ответов: {self.correct_answers_count}")

    def updateIncorrectAnswersCount(self):
        """
                Обновляет счетчик неправильных ответов.
                """
        self.incorrect_answers_count += 1
        self.counter.setText(
            "Счёт ошибок: " + str(self.incorrect_answers_count))

    def saveResult(self):
        """
                Сохраняет результаты обучения в файл results.txt.
                """
        with open('res_txt/results.txt', 'a') as file:
            file.write(
                f"{self.correct_answers_count} {self.incorrect_answers_count}\n")

        # Остановить музыку перед запуском другого файла
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.stop()

        import subprocess
        process = subprocess.Popen("python studies.py")
        process.wait()
        self.close()

    def showInfo(self):
        """
               Отображает или скрывает фрейм с информацией о правилах игры.
               """
        self.info_frame.setVisible(not self.info_frame.isVisible())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Evaluator()
    ex.showFullScreen()
    sys.exit(app.exec_())
