import pygame
import random
import os


class AnimalGame:
    def __init__(self):
        # Инициализация Pygame
        pygame.init()

        # Размеры окна (будем использовать весь экран)
        self.WIDTH, self.HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT),
                                              pygame.FULLSCREEN)

        # Заголовок окна
        pygame.display.set_caption("Угадай животное!")

        # Шрифт для текста
        self.font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 24)

        # Список животных
        self.animals = [
            "Змея", "Крокодил", "Лягушка", "Улитка",
            "Краб", "Акула", "Дельфин", "Орёл", "Голубь", "Лебедь", "Утка",
            "Павлин", "Фламинго", "Лев", "Тигр", "Слон",
            "Жираф", "Зебра", "Медведь", "Лиса", "Носорог", "Горилла",
            "Кенгуру",
            "Лось",
            "Корова", "Лошадь", "Свинья", "Овца", "Курица",
            "Петух", "Коза", "Кролик",
            "Кот", "Собака", "Хомяк", "Мышь", "Рыба", "Осёл", "Коала", "Панда"
        ]

        # Загрузка изображений
        self.images = {}
        for animal in self.animals:
            image_path = os.path.join("animalss", animal + ".png")
            if os.path.exists(image_path):
                self.images[animal] = pygame.image.load(image_path)

        # Загрузка фонового изображения
        self.background_image = pygame.image.load("animalss/fon.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (
        self.WIDTH, self.HEIGHT))

        # Цвета
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.pistachio = (107, 142, 35)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.wrong_color = (255, 0, 0)
        self.rules_color = (50, 205, 50)

        # Кнопки
        self.button_width = self.WIDTH // 7
        self.button_height = 40
        self.button_margin = 5

        # Параметры для области кнопок
        self.button_area_height = (self.button_height + self.button_margin) * (
                    (
                            len(self.animals) + 7 - 1) // 7) + self.button_margin

        # Кнопка выхода
        self.exit_button_rect = self.draw_button(10, 50, "Выход",
                                                 self.red)  # Отрисовка красной кнопки выхода

        # Кнопка с правилами
        self.rules_button_radius = 30
        self.rules_button_rect = self.draw_circle_button(
            self.WIDTH - self.rules_button_radius - 10,
            self.rules_button_radius + 10,
            self.rules_button_radius, self.white)
        # Отрисовка знака "!"
        self.rules_button_text = self.button_font.render("!", True, self.black)
        self.rules_button_text_rect = self.rules_button_text.get_rect(
            center=self.rules_button_rect.center)
        self.screen.blit(self.rules_button_text, self.rules_button_text_rect)

        # Добавлены переменные для индикатора "Верно/Неверно"
        self.answer_indicator_rect = None
        self.answer_indicator_text = ""
        self.answer_indicator_color = self.black  # Изначально черный

        # Добавлен флаг для показа правил
        self.show_rules = False

        # Файл для сохранения результатов
        self.results_file = "res_txt/animals_res.txt"

        # Загрузка результатов из файла (если он существует)
        try:
            with open(self.results_file, "r") as f:
                self.previous_results = f.readlines()
        except FileNotFoundError:
            self.previous_results = []

        # Переменная для отслеживания нажатия на кнопку выхода
        self.exit_button_pressed = False

        # Начальные параметры игры
        self.current_animal = random.choice(self.animals)
        self.score = 0

    # Функция для отрисовки кнопки
    def draw_button(self, x, y, text, color):
        # Отрисовывает кнопку с заданным текстом, цветом и позицией.
        button_rect = pygame.Rect(x, y, self.button_width - self.button_margin,
                                  self.button_height)
        pygame.draw.rect(self.screen, color, button_rect)
        text_surface = self.button_font.render(text, True, self.black)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)
        return button_rect

    # Функция для проверки нажатия на кнопку
    def check_button_click(self, x, y, button_rect):
        # Проверяет, была ли нажата кнопка в заданной позиции.
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_x, mouse_y):
            return True
        return False

    # Функция для отрисовки круглой кнопки
    def draw_circle_button(self, x, y, radius, color):
        # Отрисовывает круглую кнопку с заданными параметрами.
        pygame.draw.circle(self.screen, color, (x, y), radius)
        return pygame.Rect(x - radius, y - radius, 2 * radius, 2 * radius)

    # Функция для отрисовки правил игры
    def draw_rules(self):
        # Отрисовывает правила игры на экране.
        # Определение текста правил игры
        rules_text = [
            "Правила игры:",
            "1. Вам нужно угадать животное, изображенное на картинке.",
            "2. Если вы угадали правильно, счет увеличится на 1.",
            "3. Если вы угадали неправильно, счет не изменится.",
        ]

        # Определение шрифта и цвета текста
        rules_font = pygame.font.Font(None, 24)
        text_color = self.white

        # Определение максимальной ширины и высоты текста
        max_width = 0
        max_height = 0
        for line in rules_text:
            text_surface = rules_font.render(line, True, text_color)
            text_rect = text_surface.get_rect()
            max_width = max(max_width, text_rect.width)
            max_height += text_rect.height

        # Добавляем отступ к ширине и высоте
        max_width += 40
        max_height += 50

        # Определение позиции для отрисовки текста
        text_x = (self.WIDTH - max_width) // 2
        text_y = (self.HEIGHT - self.button_area_height - max_height) // 2

        # Определение размера прямоугольника для правил
        rules_rect = pygame.Rect(text_x, text_y, max_width, max_height)

        # Отрисовка зеленого прямоугольника
        pygame.draw.rect(self.screen, self.rules_color, rules_rect)

        # Отрисовка текста правил внутри прямоугольника
        y_offset = 5
        for i, line in enumerate(rules_text):
            text_surface = rules_font.render(line, True, text_color)
            text_rect = text_surface.get_rect(
                topleft=(rules_rect.left + 10, rules_rect.top + y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += text_rect.height + 5  # Добавляем отступ между строками

    def run(self):
        # Запускает главный цикл игры.
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Проверка нажатия на кнопки
                    for i, animal in enumerate(self.animals):
                        x = (i % 7) * self.button_width
                        y = (
                                        self.HEIGHT - self.button_area_height) + self.button_margin + (
                                    self.button_height + self.button_margin) * (
                                        i // 7)

                        button_rect = pygame.Rect(x, y,
                                                  self.button_width - self.button_margin,
                                                  self.button_height)
                        if self.check_button_click(x, y, button_rect):
                            if animal == self.current_animal:
                                # Правильный ответ
                                self.score += 1
                                self.current_animal = random.choice(
                                    self.animals)
                                self.answer_indicator_text = "Верно"
                                self.answer_indicator_color = self.green
                            else:
                                # Неправильный ответ
                                self.answer_indicator_text = "Неверно"
                                self.answer_indicator_color = self.wrong_color

                    # Проверка нажатия на кнопку выхода
                    if self.check_button_click(10, 50, self.exit_button_rect):
                        running = False
                        import os

                        os.system("python studies.py")

                    # Проверка нажатия на кнопку с правилами
                    if self.check_button_click(
                            self.WIDTH - self.rules_button_radius - 10,
                            self.rules_button_radius + 10,
                            self.rules_button_rect):
                        self.show_rules = not self.show_rules

            # Отрисовка экрана
            self.screen.blit(self.background_image,
                             (0, 0))  # Отрисовка фонового изображения

            # Отрисовка фисташкового прямоугольника
            frame_rect = pygame.Rect((self.WIDTH - 300) // 2,
                                     (
                                                 self.HEIGHT - self.button_area_height - 200) // 2,
                                     300, 200)
            pygame.draw.rect(self.screen, self.pistachio, frame_rect)

            # Отрисовка изображения животного
            image = pygame.transform.scale(self.images[self.current_animal],
                                           (280, 180))
            image_rect = image.get_rect(center=frame_rect.center)
            self.screen.blit(image, image_rect)

            # Отрисовка индикатора "Верно/Неверно" в нижнем правом углу
            answer_text = self.font.render(self.answer_indicator_text, True,
                                           self.white)
            answer_text_rect = answer_text.get_rect(
                bottomright=(frame_rect.right - 10, frame_rect.bottom - 10))
            self.answer_indicator_rect = answer_text_rect.copy()
            self.answer_indicator_rect.inflate_ip(5, 5)  # Добавляем отступ
            pygame.draw.rect(self.screen, self.answer_indicator_color,
                             self.answer_indicator_rect)
            self.screen.blit(answer_text, answer_text_rect)

            # Отрисовка кнопок
            for i, animal in enumerate(self.animals):
                x = (i % 7) * self.button_width
                y = (
                                self.HEIGHT - self.button_area_height) + self.button_margin + (
                            self.button_height + self.button_margin) * (i // 7)

                self.draw_button(x, y, animal, (100, 100, 255))

            # Отрисовка кнопки выхода
            self.exit_button_rect = self.draw_button(10, 50, "Выход",
                                                     self.red)  # Отрисовка красной кнопки выхода

            # Отрисовка счетчика
            score_text = self.font.render(f"Счет: {self.score}", True,
                                          self.white)
            self.screen.blit(score_text, (10, 10))

            # Отрисовка кнопки с правилами
            self.rules_button_rect = self.draw_circle_button(
                self.WIDTH - self.rules_button_radius - 10,
                self.rules_button_radius + 10,
                self.rules_button_radius, self.white)
            self.screen.blit(self.rules_button_text,
                             self.rules_button_text_rect)

            # Отрисовка правил
            if self.show_rules:
                self.draw_rules()

            # Обновление экрана
            pygame.display.flip()

        # Сохранение результата в файл
        with open(self.results_file, "a") as f:
            f.write(f"{self.score}\n")

        # Выход из Pygame
        pygame.quit()


# Запуск игры
if __name__ == "__main__":
    game = AnimalGame()
    game.run()

