import pygame
import random
import sys
import subprocess


class MemoryGame:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    def __init__(self):
        """Инициализирует игру, настраивает Pygame и запускает главный цикл."""
        # Инициализация Pygame
        pygame.init()
        pygame.mixer.init()

        # Получение разрешения экрана
        self.WIDTH, self.HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT),
                                              pygame.FULLSCREEN)

        # Настройка и проигрывание фоновой музыки
        pygame.mixer.music.load("songs/posled.mp3")
        pygame.mixer.music.play(-1)

        # Размеры квадратиков и кнопок
        self.SQUARE_SIZE = 100
        self.OFFSET = 20
        self.HELP_BUTTON_SIZE = 25

        self.correct_answers_count = 0
        self.show_help = False

        # Запуск игры
        self.main()

    def generate_color_sequence(self):
        """Генерирует случайную последовательность из 5 цветов."""
        return [random.choice([self.RED, self.GREEN, self.BLUE]) for _ in
                range(5)]

    def draw_squares(self, squares, highlighted_index):
        """Отрисовывает квадраты на экране."""
        total_width = (self.SQUARE_SIZE * len(squares)) + (
                self.OFFSET * (len(squares) - 1))
        start_x = (self.WIDTH - total_width) // 2

        for i, color in enumerate(squares):
            x = start_x + i * (self.SQUARE_SIZE + self.OFFSET)
            pygame.draw.rect(self.screen, color, (
                x, self.HEIGHT // 3, self.SQUARE_SIZE, self.SQUARE_SIZE))
            pygame.draw.rect(self.screen, self.BLACK, (
                x, self.HEIGHT // 3, self.SQUARE_SIZE, self.SQUARE_SIZE), 2)

            if i == highlighted_index:
                pygame.draw.rect(self.screen, self.YELLOW, (
                    x, self.HEIGHT // 3, self.SQUARE_SIZE, self.SQUARE_SIZE),
                                 4)

    def draw_end_screen(self):
        """Отрисовывает экран окончания игры."""
        font = pygame.font.Font(None, 72)
        text = font.render("Игра окончена!", True, self.BLACK)
        text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 4))
        self.screen.blit(text, text_rect)

        score_text = font.render(
            f"Правильные ответы: {self.correct_answers_count}", True,
            self.BLACK)
        score_rect = score_text.get_rect(
            center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.blit(score_text, score_rect)

        restart_text = "Начать заново"
        quit_text = "Выйти"

        restart_button_size = font.size(restart_text)
        quit_button_size = font.size(quit_text)

        restart_button_rect = pygame.Rect(
            self.WIDTH // 2 - restart_button_size[0] // 2,
            (self.HEIGHT // 2) + 50,
            restart_button_size[0], 50)
        quit_button_rect = pygame.Rect(
            self.WIDTH // 2 - quit_button_size[0] // 2,
            (self.HEIGHT // 2) + 120,
            quit_button_size[0], 50)

        pygame.draw.rect(self.screen, self.GREEN, restart_button_rect)
        pygame.draw.rect(self.screen, self.RED, quit_button_rect)

        restart_text_surface = font.render(restart_text, True, self.BLACK)
        quit_text_surface = font.render(quit_text, True, self.BLACK)

        self.screen.blit(restart_text_surface, (restart_button_rect.x + (
                restart_button_rect.width - restart_text_surface.get_width()) // 2,
                                                restart_button_rect.y + (
                                                        restart_button_rect.height - restart_text_surface.get_height()) // 2))
        self.screen.blit(quit_text_surface, (quit_button_rect.x + (
                quit_button_rect.width - quit_text_surface.get_width()) // 2,
                                             quit_button_rect.y + (
                                                     quit_button_rect.height - quit_text_surface.get_height()) // 2))

        pygame.display.flip()

        return restart_button_rect, quit_button_rect

    def draw_help_text(self):
        """Отрисовывает текст с правилами игры."""
        font = pygame.font.Font(None, 36)
        rules = [
            "Правила игры:",
            "1. Запомните последовательность квадратов.",
            "2. Используйте стрелки для выбора квадрата.",
            "3. Нажмите Enter для проверки.",
            "4. Получайте очки за правильные ответы.",
            "5. Нажмите на кнопку с ! для повторного просмотра правил."
        ]

        max_width = max(font.size(line)[0] for line in rules)
        total_height = len(rules) * 30 + 20
        x = (self.WIDTH - max_width - 20) // 2

        pygame.draw.rect(self.screen, self.BLACK,
                         (x, 5, max_width + 20, total_height), 2)

        for i, line in enumerate(rules):
            rule_text_surface = font.render(line, True, self.BLACK)
            self.screen.blit(rule_text_surface, (x + 10, 5 + 10 + i * 30))

    def main(self):
        """Главный цикл игры."""
        global event
        color_sequence = self.generate_color_sequence()
        user_sequence = [self.WHITE] * 5
        highlighted_index = 0

        start_time = pygame.time.get_ticks()
        time_to_memory = 3000
        memory_mode = True

        while True:
            self.screen.fill((127, 255, 212))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if not memory_mode:
                        if event.key == pygame.K_LEFT:
                            highlighted_index = max(0, highlighted_index - 1)
                        elif event.key == pygame.K_RIGHT:
                            highlighted_index = min(4, highlighted_index + 1)
                        elif event.key == pygame.K_RETURN:
                            if user_sequence == color_sequence:
                                self.correct_answers_count += 1
                            else:
                                with open("res_txt/score.txt", "a") as file:
                                    file.write(
                                        f"{self.correct_answers_count}\n")
                                while True:
                                    restart_button, quit_button = self.draw_end_screen()
                                    for event_end in pygame.event.get():
                                        if event_end.type == pygame.QUIT:
                                            pygame.quit()
                                            sys.exit()

                                        if event_end.type == pygame.MOUSEBUTTONDOWN:
                                            mouse_pos = event_end.pos
                                            if restart_button.collidepoint(
                                                    mouse_pos):
                                                self.main()
                                            elif quit_button.collidepoint(
                                                    mouse_pos):
                                                import os
                                                os.system("python plays.py")
                                                pygame.quit()
                                                sys.exit()

                            user_sequence = [self.WHITE] * 5
                            color_sequence = self.generate_color_sequence()
                            highlighted_index = 0
                            start_time = pygame.time.get_ticks()
                            memory_mode = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if not memory_mode:
                        if self.RED_BUTTON.collidepoint(mouse_pos):
                            user_sequence[highlighted_index] = self.RED
                        elif self.GREEN_BUTTON.collidepoint(mouse_pos):
                            user_sequence[highlighted_index] = self.GREEN
                        elif self.BLUE_BUTTON.collidepoint(mouse_pos):
                            user_sequence[highlighted_index] = self.BLUE

                    if self.help_button_rect.collidepoint(mouse_pos):
                        self.show_help = not self.show_help

            if memory_mode and (
                    pygame.time.get_ticks() - start_time > time_to_memory):
                memory_mode = False

            if memory_mode:
                self.draw_squares(color_sequence, highlighted_index)
            else:
                self.draw_squares(user_sequence, highlighted_index)

            button_y = (self.HEIGHT // 2) + 50
            buttons_x_pos = (self.WIDTH - 3 * (
                    self.SQUARE_SIZE + self.OFFSET) + self.OFFSET) // 2
            self.RED_BUTTON = pygame.draw.rect(self.screen, self.RED, (
                buttons_x_pos, button_y, self.SQUARE_SIZE, 50))
            self.GREEN_BUTTON = pygame.draw.rect(self.screen, self.GREEN, (
                buttons_x_pos + self.SQUARE_SIZE + self.OFFSET, button_y,
                self.SQUARE_SIZE, 50))
            self.BLUE_BUTTON = pygame.draw.rect(self.screen, self.BLUE, (
                buttons_x_pos + 2 * (self.SQUARE_SIZE + self.OFFSET), button_y,
                self.SQUARE_SIZE, 50))

            quit_button_rect = pygame.draw.rect(self.screen, self.RED, (
                10, self.HEIGHT - 60, 150, 50))
            quit_text = pygame.font.Font(None, 36).render("Выход", True,
                                                          self.WHITE)
            self.screen.blit(quit_text, (40, self.HEIGHT - 50))

            self.help_button_rect = pygame.draw.circle(self.screen,
                                                       self.YELLOW,
                                                       (self.WIDTH - 40, 40),
                                                       self.HELP_BUTTON_SIZE)
            help_text_surface = pygame.font.Font(None, 36).render("!", True,
                                                                  self.BLACK)
            help_text_rect = help_text_surface.get_rect(
                center=self.help_button_rect.center)
            self.screen.blit(help_text_surface, help_text_rect)

            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and quit_button_rect.collidepoint(
                    mouse_pos):
                import os
                os.system("python plays.py")
                pygame.quit()
                sys.exit()

            font = pygame.font.Font(None, 36)
            text = font.render(f"Ваш счёт: {self.correct_answers_count}", True,
                               self.BLACK)
            self.screen.blit(text, (10, 10))

            if self.show_help:
                self.draw_help_text()

            pygame.display.flip()


if __name__ == "__main__":
    MemoryGame()
