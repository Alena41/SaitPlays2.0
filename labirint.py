import random
import pygame

# Настройки игры
WIDTH = 600
HEIGHT = 600
CELL_SIZE = 20
FPS = 30

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WALL_COLOR = (210, 105, 30)  # Цвет стен

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# --- Добавленные настройки для рамки с правилами ---
RULES_FONT_SIZE = 24
RULES_TEXT_COLOR = BLACK
RULES_PADDING = 10
RULES_WIDTH = 400
RULES_HEIGHT = 200
RULES_BACKGROUND_COLOR = (255, 255, 200)  # Светло-желтый фон

# --- Настройки для кнопки "!" ---
BUTTON_SIZE = 30
BUTTON_COLOR = RED
BUTTON_TEXT_COLOR = WHITE
BUTTON_FONT_SIZE = 20
BUTTON_BORDER_WIDTH = 2


class Game:
    """Класс, управляющий игрой."""
    def __init__(self):
        """Инициализация игры."""
        pygame.init()
        pygame.mixer.init()  # Инициализация микшера для музыки

        # Переход в полноэкранный режим
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.fullscreen_width, self.fullscreen_height = self.screen.get_size()

        # Пересчитываем размеры для отображения
        self.draw_x = (self.fullscreen_width - WIDTH) // 2
        self.draw_y = (self.fullscreen_height - HEIGHT) // 2

        pygame.display.set_caption("Лабиринт")
        self.clock = pygame.time.Clock()

        # Загружаем фоновое изображение
        self.background_image = pygame.image.load("foto/cokie.jpg").convert()
        self.background_image = pygame.transform.scale(
            self.background_image, (self.fullscreen_width, self.fullscreen_height))  # Растягиваем на весь экран

        # Загружаем музыку
        pygame.mixer.music.load(
            "songs/Create fun background music on the piano suitable ... (0d1ee12f81644365bf44c38afb34a82c).mp3"
        )  # Замените "your_music_file.mp3" на ваш файл музыки
        pygame.mixer.music.play(-1)  # Запускаем музыку в цикле (-1)

        # Создаем лабиринт
        self.labyrinth = Labyrinth(WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE)

        # Создаем игрока
        self.player = Player(self.labyrinth.start_pos[0],
                             self.labyrinth.start_pos[1])

        # Уровень счётчик
        self.level_count = 0  # Счетчик уровней

        # --- Добавленные переменные для рамки с правилами ---
        self.show_rules = False
        self.rules_rect = None

        # --- Добавленные переменные для кнопки "!" ---
        self.button_rect = None
        self.button_text = None
        self.button_font = None
        self.button_border_color = BLACK

    def run(self):
        """Запускает главный цикл игры."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.player.move(UP,
                                         self.labyrinth)  # Передаем labyrinth
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.player.move(DOWN,
                                         self.labyrinth)  # Передаем labyrinth
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player.move(LEFT,
                                         self.labyrinth)  # Передаем labyrinth
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player.move(RIGHT,
                                         self.labyrinth)  # Передаем labyrinth
                # Проверка нажатия на кнопку выхода
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.exit_button_rect.collidepoint(event.pos):
                        self.save_score(self.level_count)  # Сохраняем счет
                        running = False
                        # Открыть другой файл питона
                        import os
                        os.system("python studies.py")
                    # --- Проверка нажатия на кнопку "!" ---
                    if self.button_rect.collidepoint(event.pos):
                        self.show_rules = not self.show_rules

            if self.player.x == self.labyrinth.end_pos[0] and self.player.y == \
                    self.labyrinth.end_pos[1]:
                self.level_count += 1  # Увеличиваем счетчик уровня
                self.labyrinth = Labyrinth(WIDTH // CELL_SIZE,
                                           HEIGHT // CELL_SIZE)
                self.player.x = self.labyrinth.start_pos[0]
                self.player.y = self.labyrinth.start_pos[1]

            # Отрисовка
            self.screen.blit(self.background_image, (0, 0))  # Отображаем фон

            # Отрисовка рамки
            pygame.draw.rect(self.screen, BLACK, (
                self.draw_x - 5, self.draw_y - 5, WIDTH + 10,
                HEIGHT + 10))  # рамка

            self.labyrinth.draw(self.screen, self.draw_x, self.draw_y)
            self.player.draw(self.screen, self.draw_x, self.draw_y)

            # Отображение уровня на экране
            font = pygame.font.SysFont(None, 36)
            level_text = font.render(f"Счётчик уровней: {self.level_count}",
                                     True, BLACK)
            self.screen.blit(level_text,
                             (10, 10))  # Отображаем в левом верхнем углу

            # Рисуем кнопку выхода
            self.exit_button_rect = pygame.Rect(
                10, self.fullscreen_height - 40, 100, 30
            )  # Расположение кнопки в левом нижнем углу
            pygame.draw.rect(self.screen, RED, self.exit_button_rect)
            exit_text = font.render("Выход", True, WHITE)
            self.screen.blit(
                exit_text, (15, self.fullscreen_height - 35)
            )  # Центрируем текст

            # --- Рисуем кнопку "!" ---
            self.draw_button()

            # --- Рисуем рамку с правилами ---
            self.draw_rules_frame()

            pygame.display.flip()

            # Ограничение FPS
            self.clock.tick(FPS)

        # Завершение Pygame
        pygame.quit()

    def save_score(self, score):
        """Сохраняет счет игрока в файл."""
        with open("res_txt/LABIR.txt", "a") as f:
            f.write(f"{score}\n")

    # --- Добавлено: Рисуем кнопку "!" ---
    def draw_button(self):
        """Рисует кнопку "!" для показа правил."""
        if self.button_rect is None:
            self.button_rect = pygame.Rect(
                self.fullscreen_width - BUTTON_SIZE - 10,
                10,
                BUTTON_SIZE,
                BUTTON_SIZE,
            )
            self.button_font = pygame.font.SysFont(None, BUTTON_FONT_SIZE)
            self.button_text = self.button_font.render(
                "!", True, BUTTON_TEXT_COLOR
            )
        # Рисуем кнопку с границей
        pygame.draw.circle(
            self.screen,
            BUTTON_COLOR,
            self.button_rect.center,
            BUTTON_SIZE // 2,
        )
        pygame.draw.circle(
            self.screen,
            self.button_border_color,
            self.button_rect.center,
            BUTTON_SIZE // 2,
            BUTTON_BORDER_WIDTH,
        )
        self.screen.blit(
            self.button_text,
            (
                self.button_rect.centerx - self.button_text.get_width() // 2,
                self.button_rect.centery - self.button_text.get_height() // 2,
            ),
        )

    def draw_rules_frame(self):
        """Рисует рамку с правилами игры."""
        if self.show_rules:
            if self.rules_rect is None:
                self.rules_rect = pygame.Rect(
                    self.fullscreen_width // 2 - RULES_WIDTH // 2,
                    self.fullscreen_height // 2 - RULES_HEIGHT // 2,
                    RULES_WIDTH,
                    RULES_HEIGHT,
                )
            # Рисуем фон
            pygame.draw.rect(
                self.screen,
                RULES_BACKGROUND_COLOR,
                self.rules_rect,
            )
            # Рисуем границу
            pygame.draw.rect(
                self.screen,
                BLACK,
                self.rules_rect,
                2,
            )

            # Правила в виде списка строк
            rules = [
                "Правила игры:",
                "1. Перемещайте персонажа стрелками или WASD.",
                "2. Дойдите до зеленого квадрата, чтобы перейти на следующий уровень.",
                "3. В каждом уровне меняется лабиринт."
            ]
            rules_font = pygame.font.SysFont(None, RULES_FONT_SIZE)

            y_offset = self.rules_rect.top + RULES_PADDING

            for rule in rules:
                line_text = rules_font.render(rule, True, RULES_TEXT_COLOR)
                line_rect = line_text.get_rect(
                    topleft=(self.rules_rect.left + RULES_PADDING, y_offset))

                # Проверяем, вмещается ли строка в рамку
                if y_offset + line_rect.height < self.rules_rect.bottom - RULES_PADDING:
                    # Если текст выходит за рамку по ширине, можем сделать перенос строки
                    if line_rect.width > (
                            self.rules_rect.width - 2 * RULES_PADDING):
                        words = rule.split()
                        line = ""
                        for word in words:
                            test_line = line + word + " "
                            test_line_rect = rules_font.render(test_line, True,
                                                               RULES_TEXT_COLOR).get_rect()

                            if test_line_rect.width > (
                                    self.rules_rect.width - 2 * RULES_PADDING):
                                # Отрисовываем текущую строку
                                line_text = rules_font.render(line, True,
                                                              RULES_TEXT_COLOR)
                                line_rect = line_text.get_rect(topleft=(
                                self.rules_rect.left + RULES_PADDING,
                                y_offset))
                                self.screen.blit(line_text, line_rect)
                                y_offset += line_rect.height  # Переходим к следующей строке
                                line = word + " "  # Начинаем новую строку с текущего слова
                            else:
                                line = test_line  # Добавляем слово к текущей строке

                        # Отрисовываем остаток строки
                        if line.strip():  # Проверяем, что строка не пустая
                            line_text = rules_font.render(line, True,
                                                          RULES_TEXT_COLOR)
                            line_rect = line_text.get_rect(topleft=(
                            self.rules_rect.left + RULES_PADDING, y_offset))
                            self.screen.blit(line_text, line_rect)
                            y_offset += line_rect.height  # Переходим к следующей строке

                    else:
                        # Устанавливаем простую отрисовку если текст вмещается по ширине
                        self.screen.blit(line_text, line_rect)
                        y_offset += line_rect.height  # Переходим к следующей строке
                else:
                    break  # Прекращаем, если не вмещается больше строк


class Labyrinth:
    """Класс, представляющий лабиринт."""
    def __init__(self, width, height):
        """Инициализация лабиринта."""
        self.width = width
        self.height = height
        self.grid = [[1 for _ in range(width)] for _ in
                     range(height)]  # 1 - стена, 0 - путь
        self.start_pos = (1, 1)
        self.end_pos = (width - 2, height - 2)
        self.generate()

    def generate(self):
        """Генерирует лабиринт."""
        self.carve_passages_from(1, 1)
        self.start_pos = (1, 1)
        self.end_pos = (self.width - 2, self.height - 2)
        while self.grid[self.end_pos[1]][self.end_pos[0]] == 1:
            self.end_pos = (random.randint(1, self.width - 2),
                            random.randint(1, self.height - 2))

    def carve_passages_from(self, cx, cy):
        """Рекурсивно вырезает проходы в лабиринте."""
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 0 < nx < self.width and 0 < ny < self.height and self.grid[ny][
                nx] == 1:
                self.grid[cy + dy // 2][cx + dx // 2] = 0
                self.grid[ny][nx] = 0
                self.carve_passages_from(nx, ny)

    def draw(self, screen, offset_x, offset_y):
        """Отрисовывает лабиринт на экране."""
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 1:
                    pygame.draw.rect(screen, WALL_COLOR, (
                        offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE,
                        CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(screen, WHITE, (
                        offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE,
                        CELL_SIZE, CELL_SIZE))

        pygame.draw.rect(screen, RED, (
            offset_x + self.start_pos[0] * CELL_SIZE,
            offset_y + self.start_pos[1] * CELL_SIZE,
            CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, GREEN, (
            offset_x + self.end_pos[0] * CELL_SIZE,
            offset_y + self.end_pos[1] * CELL_SIZE,
            CELL_SIZE, CELL_SIZE))


class Player:
    """Класс, представляющий игрока."""
    def __init__(self, x, y):
        """Инициализация игрока."""
        self.x = x
        self.y = y

    def move(self, direction, labyrinth):  # Добавлен аргумент labyrinth
        """Перемещает игрока в заданном направлении."""
        new_x = self.x + direction[0]
        new_y = self.y + direction[1]
        if 0 <= new_x < labyrinth.width and 0 <= new_y < labyrinth.height and labyrinth.grid[new_y][new_x] == 0:
            self.x = new_x
            self.y = new_y

    def draw(self, screen, offset_x, offset_y):
        """Отрисовывает игрока на экране."""
        pygame.draw.circle(screen, BLACK,
                           (offset_x + self.x * CELL_SIZE + CELL_SIZE // 2,
                            offset_y + self.y * CELL_SIZE + CELL_SIZE // 2),
                           CELL_SIZE // 2)


if __name__ == "__main__":
    game = Game()
    game.run()
