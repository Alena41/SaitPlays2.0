import sys
import subprocess
import pygame
import random


class WhackACat:
    def __init__(self):
        # Константы
        self.HOLE_COUNT = 6
        self.LIFE_COUNT = 5
        self.SCORE_INCREMENT = 1

        # Цвета
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BROWN = (139, 69, 19)  # Коричневый цвет
        self.BACKGROUND_COLOR = (154, 205, 50)  # Цвет фона

        # Инициализация Pygame
        pygame.init()

        # Получаем информацию о дисплее после инициализации
        self.info_object = pygame.display.Info()
        self.SCREEN_WIDTH = self.info_object.current_w
        self.SCREEN_HEIGHT = self.info_object.current_h

        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT),
            pygame.FULLSCREEN)  # Открытие на весь экран

        # Шрифты
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)

        # Кнопка "Выход"
        self.exit_button_rect = pygame.Rect(10, self.SCREEN_HEIGHT - 60, 100,
                                            50)

        # Кнопка "Начать сначала"
        self.restart_button_rect = pygame.Rect(
            self.SCREEN_WIDTH // 2 - 100,
            self.SCREEN_HEIGHT // 2 - 25,
            200,
            50
        )

        # Кнопка "Правила"
        self.rules_button_rect = pygame.Rect(
            self.SCREEN_WIDTH - 50, 10, 50, 50
        )

        # Рамка правил
        self.rules_frame_rect = pygame.Rect(
            self.SCREEN_WIDTH - 300, 100, 0, 200
        )

        # Музыка
        pygame.mixer.music.load(
            "songs/Create fun background music suitable for a childre... (bd1c7931d7b54b66b3b5b72fbaab1de2).mp3"
        )  # Загрузите свою музыку в файл "music.mp3"
        pygame.mixer.music.play(-1)  # Циклическое воспроизведение музыки

        self.miss_sound = pygame.mixer.Sound(
            "songs/strela-proletaet-mimo.wav")

        # Загружаем изображение кота
        self.cat_image = pygame.image.load(
            "foto/tarakan.png").convert_alpha()
        self.cat_image = pygame.transform.scale(self.cat_image,
                                                (90,
                                                 90))  # Изменяем размер изображения

        # Загружаем изображение сердца
        self.heart_image = pygame.image.load("foto/h2.png").convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (40, 40))

        # Загружаем изображение молотка
        self.hammer_image = pygame.image.load(
            "foto/tapok.png").convert_alpha()
        self.hammer_image = pygame.transform.scale(self.hammer_image,
                                                   (180, 180))

        # Создаем список лунок
        self.holes = [
            {'x': self.SCREEN_WIDTH // 2 - 200,
             'y': self.SCREEN_HEIGHT // 2 - 150, 'letter': 'q',
             'has_cat': False},
            {'x': self.SCREEN_WIDTH // 2, 'y': self.SCREEN_HEIGHT // 2 - 150,
             'letter': 'w', 'has_cat': False},
            {'x': self.SCREEN_WIDTH // 2 + 200,
             'y': self.SCREEN_HEIGHT // 2 - 150, 'letter': 'e',
             'has_cat': False},
            {'x': self.SCREEN_WIDTH // 2 - 200,
             'y': self.SCREEN_HEIGHT // 2 + 150, 'letter': 'a',
             'has_cat': False},
            {'x': self.SCREEN_WIDTH // 2, 'y': self.SCREEN_HEIGHT // 2 + 150,
             'letter': 's', 'has_cat': False},
            {'x': self.SCREEN_WIDTH // 2 + 200,
             'y': self.SCREEN_HEIGHT // 2 + 150, 'letter': 'd',
             'has_cat': False},
        ]

        self.lives = self.LIFE_COUNT
        self.score = 0
        self.clock = pygame.time.Clock()
        self.next_cat_timer = 0

        # Начальное положение молотка
        self.hammer_x = self.SCREEN_WIDTH - self.hammer_image.get_width() - 20
        self.hammer_y = self.SCREEN_HEIGHT - self.hammer_image.get_height() - 20
        self.hammer_is_moving = False  # Флаг для отслеживания движения молотка
        self.game_over = False  # Флаг для отслеживания конца игры
        self.show_rules = False  # Флаг для отображения правил
        self.game_started = False  # Флаг для начала игры

        # Основная игра

    def run(self):
        """Запускает основную игру."""
        while True:
            # Начальный экран (Press Start)
            if not self.game_started:
                self.screen.fill(self.BACKGROUND_COLOR)
                start_text = self.font.render("Нажмите пробел", True,
                                              self.WHITE)
                self.screen.blit(start_text, (
                    self.SCREEN_WIDTH // 2 - start_text.get_width() // 2,
                    self.SCREEN_HEIGHT // 2 - start_text.get_height() // 2
                ))
                pygame.display.flip()

                # Обработка события нажатия на пробел
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.game_started = True  # Начинаем игру

            # Основная игра
            else:
                self.screen.fill(
                    self.BACKGROUND_COLOR)  # Заполняем экран цветом фона

                # Проверка нажатия кнопок
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN and not self.game_over:
                        if event.key == pygame.K_q and not self.hammer_is_moving:
                            self.hammer_x, self.hammer_y = self.move_hammer(0)
                            self.hammer_is_moving = True
                            self.score, self.lives = self.hit_hole(0)
                        elif event.key == pygame.K_w and not self.hammer_is_moving:
                            self.hammer_x, self.hammer_y = self.move_hammer(1)
                            self.hammer_is_moving = True
                            self.score, self.lives = self.hit_hole(1)
                        elif event.key == pygame.K_e and not self.hammer_is_moving:
                            self.hammer_x, self.hammer_y = self.move_hammer(2)
                            self.hammer_is_moving = True
                            self.score, self.lives = self.hit_hole(2)
                        elif event.key == pygame.K_a and not self.hammer_is_moving:
                            self.hammer_x, self.hammer_y = self.move_hammer(3)
                            self.hammer_is_moving = True
                            self.score, self.lives = self.hit_hole(3)
                        elif event.key == pygame.K_s and not self.hammer_is_moving:
                            self.hammer_x, self.hammer_y = self.move_hammer(4)
                            self.hammer_is_moving = True
                            self.score, self.lives = self.hit_hole(4)
                        elif event.key == pygame.K_d and not self.hammer_is_moving:
                            self.hammer_x, self.hammer_y = self.move_hammer(5)
                            self.hammer_is_moving = True
                            self.score, self.lives = self.hit_hole(5)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.exit_button_rect.collidepoint(event.pos):
                            # Открываем другой файл .py и закрываем текущий
                            import os
                            os.system("python plays.py")
                            pygame.quit()
                            sys.exit()
                        if self.game_over:
                            if self.restart_button_rect.collidepoint(
                                    event.pos):
                                self.restart_game()
                            if self.exit_button_rect.collidepoint(
                                    event.pos):  # Кнопка "Выход" в окне проигрыша
                                # Открываем другой файл .py и закрываем текущий
                                import os
                                os.system("python plays.py")
                                pygame.quit()
                                sys.exit()
                        if self.rules_button_rect.collidepoint(event.pos):
                            self.show_rules = not self.show_rules  # Переключение отображения правил
                        if self.show_rules:
                            if self.rules_frame_rect.collidepoint(event.pos):
                                # Проверка нажатия внутри рамки правил
                                if event.pos[
                                    0] > self.rules_frame_rect.x + self.rules_frame_rect.width - 30 and \
                                        event.pos[
                                            1] < self.rules_frame_rect.y + 30:
                                    self.show_rules = False  # Закрытие рамки

                # Эмитация появления котиков
                if not self.game_over:
                    self.next_cat_timer += self.clock.get_time()
                    if self.next_cat_timer > 1000:
                        self.spawn_cat()
                        self.next_cat_timer = 0

                    # Выводим счёт и жизни
                    score_text = self.small_font.render(
                        f'Попаданий: {self.score}', True, self.WHITE)
                    self.screen.blit(score_text, (10, 10))

                    # Отрисовка жизней
                    for i in range(self.lives):
                        self.screen.blit(self.heart_image, (
                            10 + i * self.heart_image.get_width(), 50))

                    # Рисование лунок
                    for hole in self.holes:
                        self.draw_hole(hole)

                    # Отрисовка молотка
                    self.screen.blit(self.hammer_image,
                                     (self.hammer_x, self.hammer_y))

                    # Возврат молотка в исходное положение, если он двигался
                    if self.hammer_is_moving:
                        self.hammer_x = self.SCREEN_WIDTH - self.hammer_image.get_width() - 20
                        self.hammer_y = self.SCREEN_HEIGHT - self.hammer_image.get_height() - 20
                        self.hammer_is_moving = False

                    # Рисуем кнопку "Выход"
                    pygame.draw.rect(self.screen, self.BROWN,
                                     self.exit_button_rect)
                    exit_text = self.small_font.render(
                        "Выход", True, self.WHITE)
                    self.screen.blit(exit_text, (
                        self.exit_button_rect.x + self.exit_button_rect.width // 2 - exit_text.get_width() // 2,
                        self.exit_button_rect.y + self.exit_button_rect.height // 2 - exit_text.get_height() // 2))

                    # Рисуем кнопку "Правила"
                    pygame.draw.circle(self.screen, self.BROWN, (
                        self.rules_button_rect.centerx,
                        self.rules_button_rect.centery), 25)
                    pygame.draw.circle(self.screen, self.WHITE, (
                        self.rules_button_rect.centerx,
                        self.rules_button_rect.centery), 20)
                    rules_text = self.small_font.render(
                        "!", True, self.BROWN)
                    self.screen.blit(rules_text, (
                        self.rules_button_rect.centerx - rules_text.get_width() // 2,
                        self.rules_button_rect.centery - rules_text.get_height() // 2))

                    # Проверка на количество жизней и сброс
                    if self.lives <= 0:
                        self.game_over = True  # Устанавливаем флаг окончания игры

                        # Сохраняем итоговый счет в файл
                        with open("res_txt/final_score_cats.txt", "a") as file:
                            file.write(f"{self.score}\n")

                # Если игра окончена, покажите кнопку "Начать сначала"
                if self.game_over:
                    game_over_text = self.font.render(
                        "Вы проиграли", True, self.WHITE)
                    self.screen.blit(game_over_text, (
                        self.SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                        self.SCREEN_HEIGHT // 2 - game_over_text.get_height() - 50
                    ))
                    restart_text = self.small_font.render(
                        "Начать сначала", True, self.WHITE)
                    pygame.draw.rect(self.screen, self.BROWN,
                                     self.restart_button_rect)
                    self.screen.blit(restart_text, (
                        self.restart_button_rect.x + self.restart_button_rect.width // 2 - restart_text.get_width() // 2,
                        self.restart_button_rect.y + self.restart_button_rect.height // 2 - restart_text.get_height() // 2))

                    # Рисуем кнопку "Выход" в левом нижнем углу
                    pygame.draw.rect(self.screen, self.BROWN,
                                     self.exit_button_rect)
                    exit_text = self.small_font.render(
                        "Выход", True, self.WHITE)
                    self.screen.blit(exit_text, (
                        self.exit_button_rect.x + self.exit_button_rect.width // 2 - exit_text.get_width() // 2,
                        self.exit_button_rect.y + self.exit_button_rect.height // 2 - exit_text.get_height() // 2))

                # Отрисовка правил
                if self.show_rules:
                    # Рамка над лунками
                    rules_text = self.small_font.render(
                        "Правила игры:", True, self.WHITE)

                    # Обновляем ширину рамки на весь текст о правилах
                    text_width = max(rules_text.get_width(),
                                     # Ширина строки заголовка
                                     self.small_font.render(
                                         "Нажмите клавиши Q, W, E, A, S, D, "
                                         "чтобы ударить по лункам.",
                                         True, self.WHITE).get_width(),
                                     self.small_font.render(
                                         "Цель - ударить по коту как "
                                         "можно больше раз.",
                                         True,
                                         self.WHITE).get_width(),
                                     self.small_font.render(
                                         "У вас 5 жизней. Промах - минус "
                                         "жизнь.",
                                         True,
                                         self.WHITE).get_width()) + 20

                    text_height = (len(["Правила игры:",
                                        "Нажмите клавиши Q, W, E, A, S, D, чтобы "
                                        "ударить по лункам.",
                                        "Цель - ударить по коту как можно "
                                        "больше раз.",
                                        "У вас 5 жизней. Промах - минус жизнь."]) *
                                   self.small_font.get_height()) + 20

                    # Обновляем размер рамки
                    self.rules_frame_rect.width = text_width
                    self.rules_frame_rect.height = text_height

                    # Расположение рамки
                    self.rules_frame_rect.x = self.SCREEN_WIDTH // 2 - self.rules_frame_rect.width // 2
                    self.rules_frame_rect.y = 10  # Верхний край
                    pygame.draw.rect(self.screen, self.BROWN,
                                     self.rules_frame_rect, 4)
                    self.screen.blit(rules_text, (
                        self.rules_frame_rect.x + 10,
                        self.rules_frame_rect.y + 10))

                    rules_texts = [
                        "Нажмите клавиши Q, W, E, A, S, D, чтобы ударить по лункам.",
                        "Цель - ударить по коту как можно больше раз.",
                        "У вас 5 жизней. Промах - минус жизнь."
                    ]

                    for i, text in enumerate(rules_texts):
                        rules_text = self.small_font.render(
                            text, True, self.WHITE)
                        self.screen.blit(rules_text, (
                            self.rules_frame_rect.x + 10,
                            self.rules_frame_rect.y + 40 + i * self.small_font.get_height()))

                pygame.display.flip()
                self.clock.tick(60)

    # Функция удара по лунке
    def hit_hole(self, index):
        """Обрабатывает удар по лунке, уве��ичивает счет или отнимает жизнь."""
        if self.holes[index]['has_cat']:
            self.score += self.SCORE_INCREMENT
            self.holes[index]['has_cat'] = False
        else:
            self.lives -= 1
            self.miss_sound.play()  # Воспроизводим звук промаха
        return self.score, self.lives

    # Функция перемещения молотка
    def move_hammer(self, index):
        """Перемещает молоток на выбранную лунку."""
        # Перемещаем молоток на лунку
        self.hammer_x = self.holes[index][
                            'x'] - self.hammer_image.get_width() // 2
        self.hammer_y = self.holes[index][
                            'y'] - self.hammer_image.get_height() // 2
        return self.hammer_x, self.hammer_y

    # Функция появления кота
    def spawn_cat(self):
        """Случайно помещает кота в одну из лунок."""
        # Сначала убираем всех котов из лунок
        for hole in self.holes:
            hole['has_cat'] = False

        # Выбираем случайную лунку и помещаем туда кота
        random_hole = random.choice(self.holes)
        random_hole['has_cat'] = True

    def draw_hole(self, hole):
        """Рисует лунку на экране с опциональным изображением кота."""
        # Рисуем коричневый контур
        pygame.draw.circle(self.screen, self.BROWN, (hole['x'], hole['y']), 70,
                           8)  # Изменяем толщину контура на 6 пикселей
        # Рисуем белую сердцевину
        pygame.draw.circle(self.screen, self.WHITE, (hole['x'], hole['y']),
                           62)  # Изменяем радиус сердцевины
        # Выводим букву под лункой
        letter_text = self.small_font.render(hole['letter'], True, self.WHITE)
        self.screen.blit(letter_text,
                         (hole['x'] - letter_text.get_width() // 2,
                          hole['y'] + 70 + 10))

        if hole['has_cat']:
            # Выводим изображение кота
            self.screen.blit(self.cat_image,
                             (hole['x'] - self.cat_image.get_width() // 2,
                              hole['y'] - self.cat_image.get_height() // 2))

    # Функция перезапуска игры
    def restart_game(self):
        """Сбрасывает игру до начального состояния."""
        self.lives = self.LIFE_COUNT
        self.score = 0
        self.game_over = False
        for hole in self.holes:
            hole['has_cat'] = False


if __name__ == '__main__':
    game = WhackACat()
    game.run()
