import pygame
import random


class HangmanGame:
    def __init__(self):
        pygame.init()

        # Цвета
        self.BLACK = (0, 0, 0)
        self.WHITE = (230, 230, 250)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (100, 149, 237)  # Голубой цвет

        # Размеры экрана
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.fullscreen_width, self.fullscreen_height = self.screen.get_size()

        # Настройки игры
        self.FONT_SIZE = 52
        self.HANGMAN_PICS = [
            #  Этап 0 - начальная
            """
                  +---+
                      |
                      |
                      |
                      |
                      |
            =========""",

            """
                  +---+
                  |   |
                      |
                      |
                      |
                      |
            =========""",
            """
                  +---+
                  |   |
                  O   |
                      |
                      |
                      |
            =========""",
            """
                  +---+
                  |   |
                  O   |
                  |   |
                      |
                      |
            =========""",
            """
                  +---+
                  |   |
                  O   |
                 /|   |
                      |
                      |
            =========""",
            """
                  +---+
                  |   |
                  O   |
                 /|\  |
                      |
                      |
            =========""",
            """
                  +---+
                  |   |
                  O   |
                 /|\  |
                 /    |
                      |
            =========""",
            """
                  +---+
                  |   |
                  O   |
                 /|\  |
                 / \  |
                      |
            =========""",
        ]

        # Инициализация игры
        self.font = pygame.font.Font(None, self.FONT_SIZE)
        self.exit_font = pygame.font.Font(None,
                                          self.FONT_SIZE - 10)  # Шрифт для кнопки выхода

        # Выбор слова
        self.words = [
            "указатель",
            "радуга",
            "мармелад",
            "поиск",
            "прятки",
            "сторож",
            "копейка",
            "леопард",
            "аттракцион",
            "дрессировка",
            "ошейник",
            "карамель",
            "водолаз",
            "защита",
            "батарея",
            "решётка",
            "квартира",
            "дельфинарий",
            "непогода",
            "вход",
            "полиция",
            "перекрёсток",
            "башня",
            "стрелка",
            "градусник",
            "бутылка",
            "щипцы",
            "наволочка",
            "павлин",
            "карточка",
            "записка",
            "лестница",
            "переулок",
            "сенокос",
            "рассол",
            "закат",
            "сигнализация",
            "журнал",
            "заставка",
            "тиранозавр",
            "микрофон",
            "прохожий",
            "квитанция",
            "пауза",
            "новости",
            "скарабей",
            "серебро",
            "творог",
            "осадок",
            "песня",
            "корзина",
            "сдача",
            "овчарка",
            "хлопья",
            "телескоп",
            "микроб",
            "угощение",
            "экскаватор",
            "письмо",
            "пришелец",
            "айсберг",
            "пластик",
            "доставка",
            "полка",
            "билет",
            "вторник",
            "льдина",
            "интерес",
            "троллейбус",
            "футболист",
            "лисёнок",
            "пример",
            "баклажан",
            "лягушка",
            "джокер",
            "котлета",
            "накидка",
            "дикобраз",
            "барбарис",
            "работник",
            "кристалл",
            "доспехи",
            "халва",
            "велосипед",
            "крючок",
            "кочка",
            "черепаха",
            "петля",
            "осень",
            "яйцо"
        ]

        self.reset_game()

        # Кнопка выхода
        self.exit_button_rect = pygame.Rect(10, self.fullscreen_height - 50,
                                            # В левый нижний угол
                                            100, 30)

        # Кнопка с !
        self.rules_button_radius = 20
        self.rules_button_center_x = self.fullscreen_width - self.rules_button_radius - 10
        self.rules_button_center_y = self.rules_button_radius + 10
        self.rules_button_rect = pygame.Rect(
            self.rules_button_center_x - self.rules_button_radius,
            self.rules_button_center_y - self.rules_button_radius,
            self.rules_button_radius * 2,
            self.rules_button_radius * 2)
        self.rules_button_visible = True  # Флаг видимости кнопки

        # Правила игры
        self.rules_text = [
            "Правила игры:",
            "- Угадайте слово, используя буквы.",
            "- За каждую неправильную букву добавляется часть виселицы.",
            "- Выигрывает тот, кто угадает слово до того, как виселица будет полностью построена.",
        ]
        self.rules_font = pygame.font.Font(None, 36)

        # Флаг видимости рамок с правилами
        self.show_rules = False

    def reset_game(self):
        self.word = random.choice(self.words)
        self.hidden_word = ["_"] * len(self.word)
        self.mistakes = 0
        self.letters_guessed = []

    def run(self):
        running = True
        while running:
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    # Проверяет, была ли нажата буква
                    if event.unicode.lower() in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя":
                        letter = event.unicode.lower()
                        # Проверяет, не была ли эта буква уже угадана
                        if letter not in self.letters_guessed:
                            self.letters_guessed.append(letter)
                            if letter in self.word:
                                for i in range(len(self.word)):
                                    if self.word[i].lower() == letter:
                                        self.hidden_word[i] = self.word[i]
                            else:
                                self.mistakes += 1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Проверяет, была ли нажата кнопка выхода
                    if self.exit_button_rect.collidepoint(event.pos):
                        running = False
                        # Открыть другой файл питона
                        import os

                        os.system("python studies.py")
                    # Проверяет, была ли нажата кнопка с !
                    if self.rules_button_rect.collidepoint(event.pos):
                        self.show_rules = not self.show_rules

            # Отрисовка экрана
            self.screen.fill(self.WHITE)

            # Отрисовка виселицы
            hangman_pic = self.HANGMAN_PICS[self.mistakes]
            hangman_lines = hangman_pic.splitlines()
            # Отрисовка виселицы справа по центру
            for i, line in enumerate(hangman_lines):
                text = self.font.render(line, True, self.BLACK)
                self.screen.blit(text,
                                 (
                                 self.fullscreen_width - text.get_width() - 50,
                                 # Сдвиг вправо
                                 self.fullscreen_height // 4 + i * self.FONT_SIZE))

            # Отрисовка скрытого слова по центру слева
            hidden_word_text = self.font.render(" ".join(self.hidden_word),
                                                True, self.BLACK)
            self.screen.blit(hidden_word_text, (
                self.fullscreen_width // 2 - hidden_word_text.get_width() // 2,
                self.fullscreen_height // 2))

            # Отрисовка использованных букв
            letters_text = self.font.render(
                "Использованные буквы: " + ", ".join(self.letters_guessed),
                True, self.BLACK)

            # Вычисление размеров прямоугольника для использованных букв
            letters_rect_width = letters_text.get_width() + 20  # Добавляем отступы
            letters_rect_height = letters_text.get_height() + 10  # Добавляем отступы
            letters_rect = pygame.Rect(
                self.fullscreen_width // 2 - letters_rect_width // 2,
                self.fullscreen_height // 2 + self.FONT_SIZE * 2,
                letters_rect_width,
                letters_rect_height)

            # Отрисовка голубого прямоугольника
            pygame.draw.rect(self.screen, self.BLUE, letters_rect)

            # Отрисовка текста использованных букв внутри прямоугольника
            self.screen.blit(letters_text, (
                letters_rect.x + letters_rect.width // 2 - letters_text.get_width() // 2,
                letters_rect.y + letters_rect.height // 2 - letters_text.get_height() // 2))

            # Проверка на победу или поражение
            if "_" not in self.hidden_word:
                win_text = self.font.render("Вы победили! Слово: " + self.word,
                                            True, self.GREEN)
                self.screen.blit(win_text, (
                    self.fullscreen_width // 2 - win_text.get_width() // 2,
                    self.fullscreen_height // 2 + self.FONT_SIZE * 3))
                pygame.display.flip()
                pygame.time.delay(3000)

                # Сброс игры
                self.reset_game()

            elif self.mistakes == len(self.HANGMAN_PICS) - 1:
                lose_text = self.font.render(
                    "Вы проиграли! Слово: " + self.word, True, self.RED)
                self.screen.blit(lose_text, (
                    self.fullscreen_width // 2 - lose_text.get_width() // 2,
                    self.fullscreen_height // 2 + self.FONT_SIZE * 3))
                pygame.display.flip()
                pygame.time.delay(3000)

                # Сброс игры
                self.reset_game()

            # Кнопка выхода
            pygame.draw.rect(self.screen, self.BLACK, self.exit_button_rect, 2)
            exit_text = self.exit_font.render("Выход", True,
                                              self.BLACK)  # Используем exit_font
            self.screen.blit(exit_text, (
                self.exit_button_rect.x + self.exit_button_rect.width // 2 - exit_text.get_width() // 2,
                self.exit_button_rect.y + self.exit_button_rect.height // 2 - exit_text.get_height() // 2))

            # Кнопка с !
            if self.rules_button_visible:
                pygame.draw.circle(self.screen, self.BLACK,
                                   (self.rules_button_center_x,
                                    self.rules_button_center_y),
                                   self.rules_button_radius, 2)
                exclamation_mark_text = self.font.render("!", True, self.BLACK)
                exclamation_mark_rect = exclamation_mark_text.get_rect(
                    center=(
                    self.rules_button_center_x, self.rules_button_center_y))
                self.screen.blit(exclamation_mark_text, exclamation_mark_rect)

            # Отрисовка рамок с правилами
            if self.show_rules:
                rules_frame_width = max(
                    [self.rules_font.render(rule, True, self.BLACK).get_width()
                     for rule in
                     self.rules_text]) + 20
                rules_frame_height = len(
                    self.rules_text) * self.rules_font.get_height() + 20
                rules_frame_x = self.fullscreen_width // 2 - rules_frame_width // 2
                rules_frame_y = self.fullscreen_height // 8
                pygame.draw.rect(self.screen, self.BLACK, (
                    rules_frame_x, rules_frame_y, rules_frame_width,
                    rules_frame_height),
                                 2)

                for i, rule in enumerate(self.rules_text):
                    rule_text = self.rules_font.render(rule, True, self.BLACK)
                    self.screen.blit(rule_text, (rules_frame_x + 10,
                                                 rules_frame_y + 10 + i * self.rules_font.get_height()))

            # Обновление экрана
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = HangmanGame()
    game.run()
