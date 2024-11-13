import subprocess
import pygame
import random
import math

SQRT3 = math.sqrt(3)
ORANGE = (247, 187, 57)
YELLOW = (250, 230, 115)
ALMOSTWHITE = (255, 240, 150)
BACKGROUND = (235, 185, 105)
EDGE = (180, 115, 63)
DISTANCE = 10
DELAY = 300


class Honeycomb:
    def __init__(self):
        pygame.init()
        # создание окна
        screen_info = pygame.display.Info()
        self.WIDTH, self.HEIGHT = screen_info.current_w, screen_info.current_h
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        # Кнопка выхода на главный экран
        self.button_rect = pygame.Rect(self.WIDTH - 50, 10, 50, 50)

    # счётчик игры
    def ShowScore(self, score):
        """Отображает текущий счет игрока на экране."""
        rect = pygame.Rect(0, 0, self.WIDTH / 2 - 100, self.HEIGHT / 6)
        self.screen.fill(BACKGROUND, rect)
        font = pygame.font.Font(None, 70)
        text = font.render(f"Ваш счёт: {score}", True,
                           ALMOSTWHITE)
        self.screen.blit(text,
                         (self.WIDTH // 4 - text.get_width() // 2,
                          self.HEIGHT // 8 - text.get_height() // 2))
        pygame.draw.rect(self.screen, EDGE, self.button_rect)
        font = pygame.font.Font(None, 20)
        text = font.render("Выход", True, ALMOSTWHITE)
        self.screen.blit(text,
                         (self.button_rect.x + 10, self.button_rect.y + 10))
        pygame.display.flip()

    # создаёт соты
    def CreateHoneycombs(self):
        """Создает 7 сот в центре экрана, возвращает список сот."""
        self.screen.fill(BACKGROUND)
        x_0 = self.WIDTH // 2
        y_0 = self.HEIGHT // 2
        honeycombs = []
        honeycombs.append(Polygon(x_0, y_0, EDGE))
        dist = DISTANCE + 2 * honeycombs[0].side_size * SQRT3 / 2
        honeycombs.append(
            Polygon(x_0 - SQRT3 / 2 * dist, y_0 - 1 / 2 * dist, EDGE))
        honeycombs.append(Polygon(x_0, y_0 - dist, EDGE))
        honeycombs.append(
            Polygon(x_0 + SQRT3 / 2 * dist, y_0 - 1 / 2 * dist, EDGE))
        honeycombs.append(
            Polygon(x_0 + SQRT3 / 2 * dist, y_0 + 1 / 2 * dist, EDGE))
        honeycombs.append(Polygon(x_0, y_0 + dist, EDGE))
        honeycombs.append(
            Polygon(x_0 - SQRT3 / 2 * dist, y_0 + 1 / 2 * dist, EDGE))
        self.DrawHoneycombs(honeycombs)
        return honeycombs

    # отрисовывает соты
    def DrawHoneycombs(self, honeycombs):
        """Отрисовывает список сот на экране."""
        for i in range(len(honeycombs)):
            honeycombs[i].Draw(self.screen)
            new_polygon = Polygon(honeycombs[i].x, honeycombs[i].y, ORANGE,
                                  100)
            new_polygon.Draw(self.screen)
        pygame.display.update()

    # показывает последовательность подсветки сот для игрока
    def ShowSequence(self, sequence, honeycombs):
        """Отображает последовательность подсветки сот для игрока."""
        pygame.event.pump()
        for i in sequence:
            new_polygon = Polygon(honeycombs[i].x, honeycombs[i].y, YELLOW,
                                  100)
            new_polygon.Draw(self.screen)
            pygame.display.flip()
            pygame.event.pump()
            pygame.time.delay(DELAY)
            self.DrawHoneycombs(honeycombs)
            pygame.event.pump()
            pygame.time.delay(DELAY)

    # запускает игровой цикл, проверяет правильность
    # нажатия игрока и определяет окончание игры
    def Run(self):
        """Запускает главный цикл игры."""
        score = 0
        game_over = False
        snd1 = pygame.mixer.Sound("songs/snd1.wav")
        snd3 = pygame.mixer.Sound("songs/snd3.wav")
        honeycombs = self.CreateHoneycombs()
        sequence = [random.randint(0, 6)]
        queue = [sequence[0]]
        self.ShowScore(score)
        self.ShowSequence(sequence, honeycombs)
        print(sequence)

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(event.pos):
                        pygame.quit()
                        import os
                        os.system("python plays.py")
                    x, y = pygame.mouse.get_pos()
                    if not honeycombs[queue[-1]].Popal(x, y):
                        pygame.mixer.Sound.play(snd3)
                        pygame.event.pump()
                        pygame.time.delay(4 * DELAY)
                        game_over = True
                        Restart.RestartScreen(self, score)
                        restart_button = Button(self.WIDTH // 2 - 50,
                                                self.HEIGHT // 2 + 30,
                                                100, 50,
                                                ALMOSTWHITE)
                        restart_button.Draw(self.screen)
                        restart_button.DrawButtonText(self.screen)
                        pygame.display.update()
                        if game_over:
                            break
                    else:
                        pygame.mixer.Sound.play(snd1)
                        queue.pop()
                        if len(queue) == 0:
                            sequence.append(random.randint(0, 6))
                            self.ShowScore(score + 1)
                            self.ShowSequence(sequence, honeycombs)
                            queue = sequence.copy()
                            queue.reverse()
                            print(sequence)
                            score += 1

            if game_over:
                with open("res_txt/sota_res.txt", "a") as file:
                    file.write(str(score) + "\n")

        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    restart_button.CheckIfClicked(pos)
                    if restart_button.clicked:
                        self.Run()
                    if self.button_rect1.collidepoint(event.pos):
                        pygame.quit()
                        import os
                        os.system("python plays.py")


# проверяет, была ли нажата кнопка "Restart"
# и перезапускает игру при необходимости
class Restart:
    def init(self):
        pygame.init()
        screen_info = pygame.display.Info()
        self.WIDTH, self.HEIGHT = screen_info.current_w, screen_info.current_h
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    # выводит окно с сообщением о конце игры и показывает счет игрока
    def RestartScreen(self, score):
        """Отображает экран "Игра окончена" и предлагает перезапустить игру."""
        self.screen.fill(BACKGROUND)

        # Кнопка выхода
        self.button_rect1 = pygame.Rect(self.WIDTH // 2 - 75, 550, 150, 50)

        font = pygame.font.Font(None, 80)
        text = font.render(f"Вы проиграли! Ваш счёт: {score}", True,
                           ALMOSTWHITE)
        self.screen.blit(text,
                         (self.WIDTH // 2 - text.get_width() // 2,
                          self.HEIGHT // 2 - text.get_height() // 2))

        # Рисуем кнопки
        pygame.draw.rect(self.screen, EDGE, self.button_rect1)

        # Рисуем текст на кнопках
        font = pygame.font.Font(None, 20)
        text = font.render("Выход", True, ALMOSTWHITE)
        self.screen.blit(text,
                         (self.button_rect1.x + 10, self.button_rect1.y + 10))

        pygame.display.update()


# представляет точку на плокости
class Point:
    def __init__(self, x, y):
        """Создает точку с заданными координатами."""
        self.x = x
        self.y = y


# представляет вектор
class Vector:
    def __init__(self, point_a: Point, point_b: Point):
        """Создает вектор между двумя точками."""
        self.x = point_b.x - point_a.x
        self.y = point_b.y - point_a.y


# вычисляет векторное произведение двух векторов
def VectorProduct(a: Vector, b: Vector):
    """Вычисляет векторное произведение двух векторов."""
    return a.x * b.y - a.y * b.x


# создание сот
class Polygon:
    def __init__(self, x, y, color, side_size=125):
        """Создает шестиугольник (соту) с заданными параметрами."""
        self.x = x
        self.y = y
        self.color = color
        self.clicked = False
        self.side_size = side_size

    # возвращает координаты вершин шестиугольника
    def PolygonPoint(self, number):
        """Возвращает координаты вершины шестиугольника по номеру."""
        if (number == 0):
            return Point(-self.side_size / 2 + self.x,
                         SQRT3 * self.side_size / 2 + self.y)
        if (number == 1):
            return Point(self.side_size / 2 + self.x,
                         SQRT3 * self.side_size / 2 + self.y)
        if (number == 2):
            return Point(self.side_size + self.x, self.y)
        if (number == 3):
            return Point(self.side_size / 2 + self.x,
                         -SQRT3 * self.side_size / 2 + self.y)
        if (number == 4):
            return Point(-self.side_size / 2 + self.x,
                         -SQRT3 * self.side_size / 2 + self.y)
        if (number == 5):
            return Point(-self.side_size + self.x, self.y)

    # рисует шестиугольник на экране
    def Draw(self, screen):
        """Отрисовывает шестиугольник на экране."""
        coordinades = []
        for i in range(6):
            point = self.PolygonPoint(i)
            coordinades.append((point.x, point.y))
        pygame.draw.polygon(screen, self.color, coordinades)

    # проверяет, попал ли клик игрока внутрь шестиугольника
    def Popal(self, x, y):
        """Проверяет, попал ли клик мыши в шестиугольник."""
        for i in range(6):
            a = self.PolygonPoint(i)
            b = self.PolygonPoint((i + 1) % 6)
            c = Point(x, y)
            if VectorProduct(Vector(a, b), Vector(a, c)) > 0:
                return False
        return True


# создание кнопки в окне смерти
class Button:
    def __init__(self, x, y, width, height, color):
        """Создает кнопку с заданными параметрами."""
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.clicked = False
        self.width = x + 15
        self.height = y + 15

    def Draw(self, screen):
        """Отрисовывает кнопку на экране."""
        pygame.draw.rect(screen, self.color, self.rect)

    # текст на кнопке
    def DrawButtonText(self, screen):
        """Отрисовывает текст на кнопке."""
        self.screen = screen
        font = pygame.font.Font(None, 30)
        text = font.render("Начать сначала", True, EDGE)
        text_width = text.get_width()
        self.rect.width = text_width + 20  # Увеличиваем ширину кнопки
        self.rect.x = self.rect.x - (
                    text_width + 20 - self.rect.width) / 2  # Центрируем кнопку
        pygame.draw.rect(screen, self.color, self.rect)
        self.screen.blit(text,
                         (self.rect.x + (self.rect.width - text_width) // 2,
                          self.rect.y + (
                                      self.rect.height - text.get_height()) // 2))

    def CheckIfClicked(self, pos):
        """Проверяет, была ли нажата кнопка."""
        if self.rect.collidepoint(pos):
            self.clicked = True
        else:
            self.clicked = False


visual_memory_honeycombs_test = Honeycomb()
visual_memory_honeycombs_test.Run()
