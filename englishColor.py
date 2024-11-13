import pygame
import random
import os


class ColorGuessingGame:
    """Класс, представляющий игру на узнавание цветов."""

    def __init__(self):
        """Инициализирует игру, устанавливает цвета, размеры экрана, шрифт, цвета, текущий цвет, счёт, видимость правил."""
        pygame.init()
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.ORANGE = (255, 165, 0)
        self.YELLOW = (255, 255, 0)
        self.BROWN = (139, 69, 19)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 128, 0)
        self.PURPLE = (128, 0, 128)
        self.PINK = (255, 20, 147)
        self.GRAY = (128, 128, 128)
        self.PISTACHIO = (144, 184, 108)
        self.WIDTH, self.HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT),
                                              pygame.FULLSCREEN)
        self.BUTTON_SIZE = 60
        self.font = pygame.font.Font(None, 60)
        self.colors = {
            "Black": self.BLACK,
            "White": self.WHITE,
            "Red": self.RED,
            "Orange": self.ORANGE,
            "Yellow": self.YELLOW,
            "Brown": self.BROWN,
            "Blue": self.BLUE,
            "Green": self.GREEN,
            "Purple": self.PURPLE,
            "Pink": self.PINK,
            "Gray": self.GRAY
        }
        self.current_color = random.choice(list(self.colors.keys()))
        self.score = 0
        self.rule_visible = False
        self.rule_width = 500
        self.rule_height = 200
        self.rule_x = self.WIDTH // 2 - self.rule_width // 2
        self.rule_y = 50

    def draw_button(self, color, x, y, text=None, text_color=(0, 0, 0),
                    button_width=None):
        """Рисует кнопку с заданным цветом, текстом и размером."""
        if button_width is None:
            button_width = self.BUTTON_SIZE
        pygame.draw.rect(self.screen, color,
                         (x, y, button_width, self.BUTTON_SIZE))
        pygame.draw.rect(self.screen, self.BLACK,
                         (x, y, button_width, self.BUTTON_SIZE), 2)
        if text:
            text_surface = self.font.render(text, True, text_color)
            text_rect = text_surface.get_rect(
                center=(x + button_width // 2, y + self.BUTTON_SIZE // 2))
            self.screen.blit(text_surface, text_rect)

    def display_text(self, text):
        """Отображает текст на экране в центре."""
        text_surface = self.font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect(
            center=(self.WIDTH // 2, self.HEIGHT // 2 - 50))
        self.screen.blit(text_surface, text_rect)

    def display_score(self):
        """Отображает текущий счёт в левом верхнем углу экрана."""
        score_text = self.font.render(f"Счёт: {self.score}", True, self.BLACK)
        self.screen.blit(score_text, (10, 10))

    def draw_rule_box(self):
        """Рисует прямоугольник с правилами игры."""
        pygame.draw.rect(self.screen, self.WHITE, (
            self.rule_x, self.rule_y, self.rule_width, self.rule_height))
        pygame.draw.rect(self.screen, self.BLACK, (
            self.rule_x, self.rule_y, self.rule_width, self.rule_height), 2)
        rule_text = [
            "Правила игры:",
            "1. Назовите цвет слова",
            "2. Используйте кнопки цветов",
            "3. Правильный ответ - 1 очко",
            "4. Неправильный ответ - конец игры"
        ]
        rule_font = pygame.font.Font(None, 30)
        y_offset = 0
        for text_line in rule_text:
            rule_text_surface = rule_font.render(text_line, True, self.BLACK)
            rule_text_rect = rule_text_surface.get_rect(
                topleft=(self.rule_x + 10, self.rule_y + 10 + y_offset))
            self.screen.blit(rule_text_surface, rule_text_rect)
            y_offset += rule_text_surface.get_height()

    def run(self):
        """Запускает основной цикл игры."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, (color_name, color_value) in enumerate(
                            self.colors.items()):
                        x = (self.WIDTH // 2 - (
                                len(self.colors) // 2 * self.BUTTON_SIZE)) + (
                                    i * self.BUTTON_SIZE)
                        y = self.HEIGHT // 2 + 50
                        if event.pos[0] >= x and event.pos[
                            0] <= x + self.BUTTON_SIZE and \
                                event.pos[1] >= y and event.pos[
                            1] <= y + self.BUTTON_SIZE:
                            if color_name == self.current_color:
                                self.score += 1
                                self.current_color = random.choice(
                                    list(self.colors.keys()))
                            else:
                                self.save_score()
                                self.show_game_over()
                                running = False
                    exit_text = self.font.render("Выход", True, self.WHITE)
                    exit_text_width = exit_text.get_width()
                    exit_button_x = 10
                    exit_button_y = self.HEIGHT - self.BUTTON_SIZE - 10
                    if event.pos[0] >= exit_button_x and event.pos[
                        0] <= exit_button_x + exit_text_width and \
                            event.pos[1] >= exit_button_y and event.pos[
                        1] <= exit_button_y + self.BUTTON_SIZE:
                        running = False
                        os.system('python studies.py')
                    button_x = self.WIDTH - self.BUTTON_SIZE - 10
                    button_y = 10
                    if event.pos[0] >= button_x and event.pos[
                        0] <= button_x + self.BUTTON_SIZE and \
                            event.pos[1] >= button_y and event.pos[
                        1] <= button_y + self.BUTTON_SIZE:
                        self.rule_visible = not self.rule_visible

            self.screen.fill(self.PISTACHIO)
            for i, (color_name, color_value) in enumerate(self.colors.items()):
                x = (self.WIDTH // 2 - (
                        len(self.colors) // 2 * self.BUTTON_SIZE)) + (
                            i * self.BUTTON_SIZE)
                y = self.HEIGHT // 2 + 50
                self.draw_button(color_value, x, y)
            self.display_text(self.current_color)
            self.display_score()
            exit_text = self.font.render("Выход", True, self.WHITE)
            exit_text_width = exit_text.get_width()
            exit_button_x = 10
            exit_button_y = self.HEIGHT - self.BUTTON_SIZE - 10
            self.draw_button(self.RED, exit_button_x, exit_button_y,
                             text="Выход", text_color=self.WHITE,
                             button_width=exit_text_width)
            button_x = self.WIDTH - self.BUTTON_SIZE - 10
            button_y = 10
            pygame.draw.circle(self.screen, self.RED, (
                button_x + self.BUTTON_SIZE // 2,
                button_y + self.BUTTON_SIZE // 2), self.BUTTON_SIZE // 2)
            pygame.draw.rect(self.screen, self.BLACK, (
                button_x, button_y, self.BUTTON_SIZE, self.BUTTON_SIZE), 2)
            self.screen.blit(self.font.render("!", True, self.WHITE), (
                button_x + self.BUTTON_SIZE // 2 - 10,
                button_y + self.BUTTON_SIZE // 2 - 10))
            if self.rule_visible:
                self.draw_rule_box()
            pygame.display.flip()

        pygame.quit()

    def show_game_over(self):
        """Отображает экран "Игра окончена" с результатом и кнопками "Начать сначала" и "Выход"."""
        game_over_screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT),
                                                   pygame.FULLSCREEN)
        game_over_screen.fill(self.PISTACHIO)
        score_text = self.font.render(f"Счёт: {self.score}", True, self.BLACK)
        score_rect = score_text.get_rect(
            center=(self.WIDTH // 2, self.HEIGHT // 2 - 100))
        game_over_screen.blit(score_text, score_rect)
        restart_text = self.font.render("Начать сначала", True, self.WHITE)
        restart_text_width = restart_text.get_width()
        restart_button_x = self.WIDTH // 2 - restart_text_width // 2
        restart_button_y = self.HEIGHT // 2
        self.draw_button(self.GREEN, restart_button_x, restart_button_y,
                         text="Начать сначала", text_color=self.WHITE,
                         button_width=restart_text_width + 20)
        exit_text = self.font.render("Выход", True, self.WHITE)
        exit_text_width = exit_text.get_width()
        exit_button_x = self.WIDTH // 2 - exit_text_width // 2
        exit_button_y = self.HEIGHT // 2 + self.BUTTON_SIZE + 20
        self.draw_button(self.RED, exit_button_x, exit_button_y, "Выход",
                         text_color=self.WHITE,
                         button_width=exit_text_width + 20)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[0] >= restart_button_x and event.pos[
                        0] <= restart_button_x + self.BUTTON_SIZE and \
                            event.pos[1] >= restart_button_y and event.pos[
                        1] <= restart_button_y + self.BUTTON_SIZE:
                        self.score = 0
                        self.current_color = random.choice(
                            list(self.colors.keys()))
                        running = False
                        self.screen.fill(self.PISTACHIO)
                        self.run()
                    elif event.pos[0] >= exit_button_x and event.pos[
                        0] <= exit_button_x + self.BUTTON_SIZE and \
                            event.pos[1] >= exit_button_y and event.pos[
                        1] <= exit_button_y + self.BUTTON_SIZE:
                        running = False
                        os.system('python studies.py')

            pygame.display.flip()

        pygame.quit()

    def save_score(self):
        """Сохраняет текущий счёт в файл."""
        with open("res_txt/english.txt", "a") as file:
            file.write(f"{self.score}\n")


if __name__ == "__main__":
    game = ColorGuessingGame()
    game.run()
