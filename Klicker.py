import subprocess
import pygame
import random
import time


class ReactionTimeTest:
    """
    Класс, реализующий тест времени реакции.
    """

    def __init__(self):
        """
        Инициализирует игру, создает окно, загружает музыку и настраивает элементы интерфейса.
        """
        pygame.init()
        self.result_file = open("res_txt/Klicker_res.txt", "a")
        screen_info = pygame.display.Info()
        self.width, self.height = screen_info.current_w, screen_info.current_h
        self.screen = pygame.display.set_mode((self.width, self.height))

        pygame.mixer.music.load("songs/klik.mp3")
        pygame.mixer.music.play(-1)

        # Перемещаем кнопку выхода в левый верхний угол
        self.close_button_rect = pygame.Rect(10, 10, 140, 50)
        self.rules_button_radius = 20
        self.show_rules = False

        self.blue_screen()

    def too_soon_screen(self):
        """
        Отображает экран с сообщением "Click too soon" (кликнули слишком рано).
        """
        self.screen.fill((50, 50, 155))
        font = pygame.font.Font(None, 100)
        text = font.render("Click too soon", True, (255, 255, 255))
        self.screen.blit(text,
                         (self.width // 2 - text.get_width() // 2,
                          self.height // 2 - text.get_height() // 2))
        pygame.display.flip()

    def blue_screen(self):
        """
        Отображает начальный экран с названием теста.
        """
        self.screen.fill((50, 50, 155))
        font = pygame.font.Font(None, 100)
        text = font.render("Reaction time test", True, (255, 255, 255))
        self.screen.blit(text,
                         (self.width // 2 - text.get_width() // 2,
                          self.height // 2 - text.get_height() // 2))
        pygame.display.flip()

    def red_screen(self):
        """
        Отображает красный экран с сообщением "Wait for green".
        """
        self.screen.fill((155, 0, 0))
        font = pygame.font.Font(None, 100)
        text = font.render("Wait for green", True, (255, 255, 255))
        self.screen.blit(text,
                         (self.width // 2 - text.get_width() // 2,
                          self.height // 2 - text.get_height() // 2))
        pygame.display.flip()

    def green_screen(self):
        """
        Отображает зеленый экран с сообщением "Click!".
        """
        self.screen.fill((0, 155, 20))
        font = pygame.font.Font(None, 100)
        text = font.render("Click!", True, (255, 255, 255))
        self.screen.blit(text,
                         (self.width // 2 - text.get_width() // 2,
                          self.height // 2 - text.get_height() // 2))
        pygame.display.flip()

    def result_screen(self, result):
        """
        Отображает экран с результатом теста в миллисекундах.
        """
        self.screen.fill((0, 155, 20))
        font = pygame.font.Font(None, 100)
        text = font.render(f"{result} ms", True, (255, 255, 255))
        self.screen.blit(text,
                         (self.width // 2 - text.get_width() // 2,
                          self.height // 2 - text.get_height() // 2))
        pygame.display.flip()
        self.result_file.write(str(result) + "\n")

    def draw_exit_button(self):
        """
        Рисует кнопку "Выход" в левом верхнем углу экрана.
        """
        pygame.draw.rect(self.screen, (0, 0, 0), self.close_button_rect)
        font = pygame.font.Font(None, 36)
        text = font.render("Выход", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.close_button_rect.center)
        self.screen.blit(text, text_rect)

    def draw_rules_button(self):
        """
        Рисует кнопку "?" в правом верхнем углу экрана.
        """
        pygame.draw.circle(self.screen, (255, 0, 0), (self.width - 30, 30),
                           self.rules_button_radius)
        font = pygame.font.Font(None, 36)
        text = font.render("!", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.width - 30, 30))  # Центрируем текст в круге
        self.screen.blit(text, text_rect)

    def display_rules(self):
        """
        Отображает правила теста на 3 секунды.
        """
        font = pygame.font.Font(None, 36)
        rules_text = "Правила: Нажмите на экран, когда он станет зеленым."
        text = font.render(rules_text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.width // 2, 50))
        pygame.draw.rect(self.screen, (0, 0, 0), text_rect.inflate(20, 10))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(3000)  # Показать на 3 секунды

    def open_main_screen(self):
        """
        Открывает главный экран (plays.py).
        """
        import os
        os.system("python plays.py")

    def run(self):
        """
        Запускает главный цикл теста.
        """
        start = True
        self.is_running = True

        while start and self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.close_button_rect.collidepoint(event.pos):
                        self.is_running = False
                        pygame.quit()
                        self.open_main_screen()

                    if (event.pos[
                        0] >= self.width - 30 - self.rules_button_radius and
                            event.pos[1] <= 30 + self.rules_button_radius):
                        self.show_rules = True
                        self.display_rules()

                    self.red_screen()

                    running = True
                    is_red = True

                    while running:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False

                            elif (
                                    event.type == pygame.MOUSEBUTTONDOWN and is_red):
                                running = False
                                self.too_soon_screen()

                            elif (
                                    event.type == pygame.MOUSEBUTTONDOWN and not is_red):
                                running = False
                                result = int((time.time() - result) * 1000)
                                self.result_screen(result)

                            if not self.is_running:
                                running = False

                        if random.randint(0, 100) == 1:
                            self.green_screen()
                            result = time.time()
                            is_red = False

                        pygame.time.wait(30)
            self.draw_exit_button()
            self.draw_rules_button()
            pygame.display.flip()

        self.result_file.close()
        pygame.quit()


if __name__ == "__main__":
    reaction_time_test = ReactionTimeTest()
    reaction_time_test.run()

