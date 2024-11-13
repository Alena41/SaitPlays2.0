import pygame
import subprocess
import random


class DolphinGame:
    """Класс, представляющий игру с дельфином."""

    def __init__(self):
        """Инициализирует игру."""
        # Инициализация Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width, self.screen_height = self.screen.get_size()
        self.clock = pygame.time.Clock()

        # Загружаем изображения
        self.bird_image = pygame.image.load('foto/delphin.png')
        self.bird_image = pygame.transform.scale(self.bird_image, (100, 100))
        self.background_image = pygame.image.load('foto/fon_ocean.jpg')
        self.background_image = pygame.transform.scale(self.background_image, (
            self.screen_width, self.screen_height))

        # Загружаем музыку
        pygame.mixer.music.load(
            'songs/Ksenon-—-Дельфины-_Symphony-пародия-БЕЗ-МАТА_-_.mp3')
        pygame.mixer.music.play(-1)

        # Параметры игры
        self.gravity = 0.25
        self.flap_strength = -5
        self.pipe_gap = 250
        self.pipe_width = 80
        self.pipe_speed = 3
        self.pipe_horizontal_distance = 150

        self.running = True
        self.score = 0
        self.bird = None
        self.pipes = []

    class Bird:
        """Класс, представляющий дельфина."""

        def __init__(self, game):
            """Инициализирует дельфина."""
            self.x = 50
            self.y = game.screen_height // 2
            self.velocity = 0
            self.radius = 20
            self.game = game

        def flap(self):
            """Заставляет дельфина взлететь."""
            self.velocity += self.game.flap_strength

        def update(self):
            """Обновляет позицию и скорость дельфина."""
            self.velocity += self.game.gravity
            self.y += self.velocity

        def draw(self):
            """Рисует дельфина на экране."""
            self.game.screen.blit(self.game.bird_image, (self.x, int(self.y)))

    class Pipe:
        """Класс, представляющий трубы."""

        def __init__(self, game, x_offset):
            """Инициализирует трубы."""
            self.x = game.screen_width + x_offset
            self.height = random.randint(50,
                                         game.screen_height - game.pipe_gap - 50)
            self.passed = False
            self.game = game

        def update(self):
            """Обновляет позицию трубы."""
            self.x -= self.game.pipe_speed

        def draw(self):
            """Рисует трубы на экране."""
            pygame.draw.rect(self.game.screen, (50, 50, 50),
                             (self.x, 0, self.game.pipe_width, self.height))
            pygame.draw.rect(self.game.screen, (50, 50, 50), (
                self.x, self.height + self.game.pipe_gap, self.game.pipe_width,
                self.game.screen_height))

    class GameOverScreen:
        """Класс, представляющий экран окончания игры."""

        def __init__(self, game, score):
            """Инициализирует экран окончания игры."""
            self.game = game
            self.score = score

        def display(self):
            """Отображает экран окончания игры."""
            self.game.screen.fill((173, 216, 230))
            font = pygame.font.SysFont(None, 74)
            text = font.render(f'Ваш результат: {self.score}', True, (0, 0, 0))
            self.game.screen.blit(text, (
                self.game.screen_width // 2 - text.get_width() // 2,
                self.game.screen_height // 2 - 50))

            with open("res_txt/delphin.txt", "a") as file:
                file.write(str(self.score) + "\n")

            # Кнопка "Начать заново"
            self.restart_button = pygame.Rect(
                self.game.screen_width // 2 - 100,
                self.game.screen_height // 2 + 20, 200, 50)
            pygame.draw.rect(self.game.screen, (0, 0, 0), self.restart_button)
            restart_text = pygame.font.SysFont(None, 36).render(
                'Начать заново', True, (255, 255, 255))
            self.game.screen.blit(restart_text, (
                self.game.screen_width // 2 - restart_text.get_width() // 2,
                self.game.screen_height // 2 + 30))

            # Кнопка "Выход"
            self.exit_button = pygame.Rect(self.game.screen_width // 2 - 100,
                                           self.game.screen_height // 2 + 80,
                                           200, 50)
            pygame.draw.rect(self.game.screen, (0, 0, 0), self.exit_button)
            exit_text = pygame.font.SysFont(None, 36).render('Выход', True,
                                                             (255, 255, 255))
            self.game.screen.blit(exit_text, (
                self.game.screen_width // 2 - exit_text.get_width() // 2,
                self.game.screen_height // 2 + 90))

            pygame.display.flip()
            self.waiting = True

            while self.waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if self.restart_button.collidepoint(mouse_pos):
                            return True
                        elif self.exit_button.collidepoint(mouse_pos):
                            pygame.quit()
                            import os
                            os.system("python plays.py")

            return False

    def start_screen(self):
        """Отображает стартовый экран."""
        self.screen.fill((173, 216, 230))
        font = pygame.font.SysFont(None, 74)
        title_text = font.render('Нажмите пробел чтобы начать', True,
                                 (0, 0, 0))
        self.screen.blit(title_text, (
            self.screen_width // 2 - title_text.get_width() // 2,
            self.screen_height // 2 - 50))

        # Кнопка "Правила"
        rules_button = pygame.Rect(self.screen_width // 2 - 100,
                                   self.screen_height // 2 + 20, 200, 50)
        pygame.draw.rect(self.screen, (0, 0, 0), rules_button)
        rules_text = pygame.font.SysFont(None, 36).render('Правила', True,
                                                          (255, 255, 255))
        self.screen.blit(rules_text, (
            self.screen_width // 2 - rules_text.get_width() // 2,
            self.screen_height // 2 + 30))

        # Кнопка "Выход" в левом нижнем углу
        exit_button = pygame.Rect(10, self.screen_height - 60, 180, 50)
        pygame.draw.rect(self.screen, (0, 0, 0), exit_button)
        exit_text = pygame.font.SysFont(None, 36).render('Выход', True,
                                                         (255, 255, 255))
        self.screen.blit(exit_text, (
            10 + 90 - exit_text.get_width() // 2, self.screen_height - 50))

        pygame.display.flip()
        waiting = True

        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if rules_button.collidepoint(mouse_pos):
                        self.display_rules()
                    elif exit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        import os
                        os.system("python plays.py")

    def display_rules(self):
        """Отображает правила игры."""
        rules = [
            "Правила игры:",
            "1. Управляйте дельфином, нажимая пробел.",
            "2. Избегайте столкновений с трубами.",
            "3. Накапливайте очки, пройдя трубы.",
            "4. Наберите максимальное количество очков!"
        ]
        self.screen.fill((173, 216, 230))
        font = pygame.font.SysFont(None, 36)
        for i, line in enumerate(rules):
            text = font.render(line, True, (0, 0, 0))
            self.screen.blit(text, (
                self.screen_width // 2 - text.get_width() // 2, 100 + i * 30))

        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False

    def game_loop(self):
        """Запускает основной игровой цикл."""
        while self.running:
            if not self.start_screen():
                break  # Если игрок вышел, заканчиваем игру

            self.bird = self.Bird(self)
            self.pipes = [self.Pipe(self, 0)]
            self.score = 0
            running = True

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.bird.flap()

                self.bird.update()

                if self.bird.y > self.screen_height or self.bird.y < 0:
                    running = False

                if self.pipes[
                    -1].x < self.screen_width - self.pipe_horizontal_distance:
                    self.pipes.append(
                        self.Pipe(self, self.pipe_horizontal_distance))

                for pipe in self.pipes:
                    pipe.update()
                    if pipe.x + self.pipe_width < self.bird.x and not pipe.passed:
                        self.score += 1
                        pipe.passed = True

                    if pipe.x < self.bird.x + self.bird.radius < pipe.x + self.pipe_width:
                        if self.bird.y - self.bird.radius < pipe.height or self.bird.y + self.bird.radius > pipe.height + self.pipe_gap:
                            running = False

                # Отображаем фон
                self.screen.blit(self.background_image, (0, 0))

                # Рисуем птицу и трубы
                self.bird.draw()
                for pipe in self.pipes:
                    pipe.draw()

                # Отображаем счёт
                score_text = pygame.font.SysFont(None, 36).render(
                    f'Счёт: {self.score}', True, (0, 0, 0))
                self.screen.blit(score_text, (10, 10))

                pygame.display.flip()
                self.clock.tick(30)

            restart = self.GameOverScreen(self, self.score).display()
            if not restart:
                break


if __name__ == '__main__':
    DolphinGame().game_loop()

