import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QFrame
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
from docx import Document
import random


class TextChecker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Проверка текста")

        # Установка пастельно-желтого фона
        palette = self.palette()
        palette.setColor(QPalette.Window,
                         QColor(255, 255, 204))
        self.setPalette(palette)

        # Загрузка текстов из файлов
        self.right_text0 = self.load_text("Dictation_txt/right_texts (2).docx")
        self.wrong_text0 = self.load_text("Dictation_txt/wrong_texts (2).docx")

        # Инициализация текста для проверки
        self.check_text = self.get_random_wrong_paragraph()

        # Сохраняем номер проверяемого текста
        self.wrong_text_2 = self.wrong_text0.split("\n")
        self.wrong_text_index = self.wrong_text_2.index(self.check_text)

        # Инициализация текста без ошибок
        self.right_text = self.get_random_right_paragraph()

        # QLabel для отображения текста для проверки
        self.check_label = QLabel(self.check_text)
        self.check_label.setAlignment(Qt.AlignCenter)
        self.check_label.setFont(QFont("Arial", 14))
        self.check_label.setWordWrap(True)
        self.check_label.setFixedHeight(200)

        # Поле для ввода текста
        self.input_field = QTextEdit()
        self.input_field.setFont(QFont("Arial", 12))
        self.input_field.setPlaceholderText("Введите текст")
        self.input_field.setFixedHeight(200)
        self.input_field.setFixedWidth(800)
        self.input_field.setFrameShape(QFrame.StyledPanel)

        # Кнопка "Проверить"
        self.check_button = QPushButton("Проверить")
        self.check_button.setFixedWidth(100)
        self.check_button.clicked.connect(self.check_text_similarity)

        # Кнопка "Далее"
        self.next_button = QPushButton("Далее")
        self.next_button.setFixedWidth(100)
        self.next_button.clicked.connect(self.load_new_paragraph)

        # Кнопка "Выйти"
        self.save_button = QPushButton('Выйти', self)
        self.save_button.setStyleSheet(
            "background-color: rgb(255, 204, 153); color: rgb(0, 0, 0);")
        self.save_button.setFont(QFont("Arial", 16))
        self.save_button.clicked.connect(self.saveResult)

        # Размещение элементов в компоновке
        layout = QVBoxLayout()
        layout.setContentsMargins(200, 100, 200, 100)

        # Добавление пустого пространства над check_label
        layout.addItem(
            QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Полоса с текстом для проверки
        layout.addWidget(self.check_label)

        # Добавление пустого пространства под check_label
        layout.addItem(
            QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Оборачиваем поле ввода в QHBoxLayout для центрирования
        input_layout = QHBoxLayout()
        input_layout.addStretch()
        input_layout.addWidget(self.input_field)
        input_layout.addStretch()

        # Добавим вертикальный отступ для поднимания элементов
        layout.addItem(
            QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        layout.addLayout(input_layout)

        # Делаем кнопку "Далее" и "Проверить" в одну строку
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.check_button)
        button_layout.addWidget(self.next_button)
        layout.addLayout(button_layout)

        # Добавляем пустое пространство под кнопками
        layout.addItem(
            QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Добавляем кнопку "Выйти" в нижнюю часть
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.save_button)
        bottom_layout.addStretch()
        layout.addLayout(bottom_layout)

        self.setLayout(layout)

        self.showMaximized()

    def load_text(self, file_path):
        """Загружает текст из файла .docx."""
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()

    def get_random_wrong_paragraph(self):
        """Возвращает случайный абзац из wrong_texts.docx."""
        paragraphs = [p for p in self.wrong_text0.split("\n") if p.strip()]
        return random.choice(paragraphs) if paragraphs else ""

    def get_random_right_paragraph(self):
        """Возвращает случайный абзац из right_texts.docx."""
        paragraphs = [p for p in self.right_text0.split("\n") if p.strip()]
        return paragraphs[self.wrong_text_index] if paragraphs else ""

    def load_new_paragraph(self):
        """Загружает новый текст для проверки."""
        self.check_text = self.get_random_wrong_paragraph()

        self.wrong_text_2 = self.wrong_text0.split("\n")
        self.wrong_text_index = self.wrong_text_2.index(self.check_text)

        self.right_text = self.get_random_right_paragraph()

        self.check_label.setText(self.check_text)
        self.input_field.clear()

    def saveResult(self):
        """Закрывает текущее окно и запускает studies.py"""
        self.close()
        import os
        os.system("python studies.py")

    def check_text_similarity(self):
        """Проверяет сходство введенного текста с правильным текстом."""
        user_text = self.input_field.toPlainText()

        if user_text.strip() == "":
            QMessageBox.warning(self, "Ошибка", "Введите текст для проверки!")
            return

        right_words = self.right_text.split()
        check_words = self.check_text.split()
        user_words = user_text.split()

        correct_html = ""
        errors = []

        # Проверка на соответствие слов
        for i, word in enumerate(user_words):
            if i < len(user_words) and word == right_words[i]:
                correct_html += f"<font color='green'>{word}</font> "
            else:
                correct_html += f"<font color='red'>{word}</font> "
                if i < len(user_words):
                    errors.append((word, right_words[i]))
                else:
                    errors.append(("", word))

        # Обработка сообщения об ошибках
        if not errors:
            QMessageBox.information(self, "Результат проверки", "Все верно!",
                                    QMessageBox.Ok)
        else:
            error_message = "Ошибки:<br>"
            for user_word, correct_word in errors:
                error_message += f"- Правильно: <b>{correct_word}</b>, Введено: <b>{user_word}</b><br>"

            result_message = f"<b>Результат проверки:</b><br>{correct_html}<br><br>{error_message}"
            QMessageBox.information(self, "Результат проверки", result_message,
                                    QMessageBox.Ok)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    checker = TextChecker()
    checker.show()
    sys.exit(app.exec_())
