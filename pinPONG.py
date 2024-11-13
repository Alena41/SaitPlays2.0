import pygame
import random
import sys


class PongGame:
    """Класс, представляющий игру пинг-понг."""

    def __init__(self):
        """Инициализация игры."""
        pygame.init()

        # Устанавливаем разрешение для полноэкранного режима
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_x, self.screen_y = self.screen.get_size()

        # Размеры игры
        self.game_width = 800
        self.game_height = 400
        self.padding = 20  # Отступ для рамки

        self.points_left = 0
        self.points_right = 0

        self.p_width = 15
        self.p_height = 100
        self.p_speed = 15

        self.ball_r = 10
        self.ball_speed = 6
        self.ball_d = self.ball_r * 2

        self.ball_start_x = self.game_width / 2 - self.ball_r
        self.ball_start_y = self.game_height / 2 - self.ball_r

        self.fps = 60

        # Вычисляем координаты для центрирования игрового экрана
        self.game_screen_x = (self.screen_x - self.game_width) // 2
        self.game_screen_y = (self.screen_y - self.game_height) // 2

        # Внутренний экран для игры
        self.game_screen = pygame.Surface((self.game_width, self.game_height))

        self.platform_right = pygame.Rect(
            self.game_width - self.p_width - 5,
            self.game_height / 2 - self.p_height / 2, self.p_width,
            self.p_height
        )
        self.platform_left = pygame.Rect(5,
                                         self.game_height / 2 - self.p_height / 2,
                                         self.p_width, self.p_height)
        self.ball = pygame.Rect(self.ball_start_x, self.ball_start_y,
                                self.ball_d, self.ball_d)

        self.font = pygame.font.Font(None, 30)  # Уменьшенный размер шрифта

        self.dx = 1
        self.dy = -1

        # Цвета
        self.black = (0, 0, 0)
        self.green = (34, 139, 34)
        self.gray = (0, 48, 59)

        self.clock = pygame.time.Clock()
        self.pause = False
        self.game = True

        # Параметры кнопки выхода
        self.exit_button_rect = pygame.Rect(10, 10, 150, 45)
        self.exit_button_color = (107, 142, 35)

        # Параметры кнопки правил
        self.rules_button_radius = 16
        self.rules_button_center = (self.screen_x - 40, 40)  # Центр кнопки
        self.rules_button_color = (107, 142, 35)
        self.show_rules = False

        # Текст правил
        self.rules_text = [
            "Правила игры:",
            "1. Игроки управляют платформами.",
            "2. Мяч отскакивает от платформ.",
            "3. Попадание мяча в ворота приносит очки.",
            "4. Игра заканчивается по договоренности."
        ]

    def run(self):
        """Запускает цикл игры."""
        while self.game:
            # Отрисовка серого фона
            self.screen.fill(self.gray)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # ЛКМ
                        if self.exit_button_rect.collidepoint(event.pos):
                            pygame.quit()
                            import os
                            os.system("python plays.py")
                        if (self.rules_button_center[
                            0] - self.rules_button_radius < event.pos[0] <
                                self.rules_button_center[
                                    0] + self.rules_button_radius and
                                self.rules_button_center[
                                    1] - self.rules_button_radius < event.pos[
                                    1] < self.rules_button_center[
                                    1] + self.rules_button_radius):
                            self.show_rules = not self.show_rules  # Переключаем отображение правил

            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and self.platform_right.top > 0:
                self.platform_right.top -= self.p_speed
            elif key[
                pygame.K_DOWN] and self.platform_right.bottom < self.game_height:
                self.platform_right.bottom += self.p_speed
            elif key[pygame.K_w] and self.platform_left.top > 0:
                self.platform_left.top -= self.p_speed
            elif key[
                pygame.K_s] and self.platform_left.bottom < self.game_height:
                self.platform_left.bottom += self.p_speed

            # Отрисовка игровых объектов на вспомогательном экране
            self.game_screen.fill(self.green)
            pygame.draw.rect(self.game_screen, pygame.Color("White"),
                             self.platform_right)
            pygame.draw.rect(self.game_screen, pygame.Color("White"),
                             self.platform_left)
            pygame.draw.circle(self.game_screen, pygame.Color("White"),
                               self.ball.center, self.ball_r)

            # Логика движения мяча
            self.ball.x += self.ball_speed * self.dx
            self.ball.y += self.ball_speed * self.dy

            if self.ball.centery < self.ball_r or self.ball.centery > self.game_height - self.ball_r:
                self.dy = -self.dy
            elif self.ball.colliderect(
                    self.platform_left) or self.ball.colliderect(
                    self.platform_right):
                self.dx = -self.dx
                self.ball_speed += 0.2

            if self.ball.centerx > self.game_width:
                self.points_right += 1
                self.ball.x = self.ball_start_x
                self.ball.y = self.ball_start_y
                self.dx, self.dy = 0, 0
                self.goal_time = pygame.time.get_ticks()
                self.pause = True
                self.ball_speed = 6
            elif self.ball.centerx < 0:
                self.points_left += 1
                self.ball.x = self.ball_start_x
                self.ball.y = self.ball_start_y
                self.dx, self.dy = 0, 0
                self.goal_time = pygame.time.get_ticks()
                self.pause = True
                self.ball_speed = 6

            if self.pause:
                current_time = pygame.time.get_ticks()
                if current_time - self.goal_time > 3000:
                    self.dx = random.choice((1, -1))
                    self.dy = random.choice((1, -1))
                    self.pause = False

            right_text = self.font.render(f"{self.points_left}", False,
                                          pygame.Color("White"))
            self.game_screen.blit(right_text, (self.game_width - 40, 20))

            left_text = self.font.render(f"{self.points_right}", False,
                                         pygame.Color("White"))
            self.game_screen.blit(left_text, (20, 20))

            # Отрисовываем рамку вокруг игрового экрана
            pygame.draw.rect(self.screen, self.black, (
            self.game_screen_x + self.padding,
            self.game_screen_y + self.padding, self.game_width,
            self.game_height), 2)

            # Отрисовка кнопки выхода
            pygame.draw.rect(self.screen, self.exit_button_color,
                             self.exit_button_rect)
            exit_text = self.font.render("Выход", True, (255, 255, 255))
            self.screen.blit(exit_text, (
            self.exit_button_rect.x + 10, self.exit_button_rect.y + 10))

            # Отрисовка кнопки правил
            pygame.draw.circle(self.screen, self.rules_button_color,
                               self.rules_button_center,
                               self.rules_button_radius)
            rules_text_surface = self.font.render("!", True, (255, 255, 255))
            text_rect = rules_text_surface.get_rect(
                center=self.rules_button_center)
            self.screen.blit(rules_text_surface, text_rect)

            # Отображение игрового экрана в окне
            self.screen.blit(self.game_screen,
                             (self.game_screen_x, self.game_screen_y))

            # Если показываем правила, рисуем рамку с текстом
            if self.show_rules:
                rules_rect = pygame.Rect(self.screen_x // 4,
                                         self.screen_y // 4,
                                         self.screen_x // 2,
                                         self.screen_y // 2)
                pygame.draw.rect(self.screen, (0, 0, 0),
                                 rules_rect)  # Черный фон
                pygame.draw.rect(self.screen, (255, 255, 255), rules_rect,
                                 5)  # Белая рамка

                # Выводим текст правил
                y_offset = 20
                for i, line in enumerate(self.rules_text):
                    rule_surface = self.font.render(line, True,
                                                    (255, 255, 255))
                    self.screen.blit(rule_surface, (
                    rules_rect.x + 20, rules_rect.y + y_offset))
                    y_offset += rule_surface.get_height() + 10  # Добавляем отступ между строками

            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()


# Запускаем игру
if __name__ == "__main__":
    game = PongGame()
    game.run()

