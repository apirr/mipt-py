import pygame
from pygame.draw import *
from random import randint, choice
import pickle
import operator
import pygame.freetype

pygame.font.init()
font = pygame.font.Font(pygame.font.get_default_font(), 36)

name = input()
print(1)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
BACKGROUND_COLOR = (0, 0, 0)
BORIS = pygame.image.load("boris.png")  # картинка для альернативного врага
BALL_CHOICE = [0] * 10 + [1]
BORIS_CHOICE = [0] * 100 + [1]


pygame.init()
FPS = 3000000
screen = pygame.display.set_mode((1000, 800))
DT = 0.1  # приращение времени

# Объявляется класс для шарика

class Ball:

    def __init__(self):
        '''x, y - координаты
           vx, vy - скорости
           color - цвет
           vx, vy - скорости
           r - характерный размер
           surface - личная поверхность объекта
        '''
        self.x = randint(200, 500)
        self.y = randint(200, 500)
        self.vx = randint(-2, 2)
        self.vy = randint(-2, 2)
        self.vx *= 0.50
        self.vy *= 0.50
        self.color = choice(COLORS)
        self.r = randint(20, 40)
        self.surface = pygame.Surface(
            (self.r * 2, self.r * 2), pygame.SRCALPHA, 32)
        self.surface = self.surface.convert_alpha()
        circle(self.surface, self.color, (self.r, self.r), self.r)
        self.starting_time = pygame.time.get_ticks()

    def draw(self, surface=screen):
        '''Рисует объект на поверхности'''
        surface.blit(self.surface, (self.x - self.r / 2, self.y - self.r / 2))

    def remove(self, surface=screen):
        self.color = BACKGROUND_COLOR
        circle(self.surface, self.color, (self.r, self.r), self.r)

    def move(self, surface=screen):
        self.x += self.vx
        self.y += self.vy

    def collision(self):

        '''Определяются коллизии со стенками'''

        if self.x >= 1000 - self.r:
            self.vx *= -1
        if self.y >= 800 - self.r:
            self.vy *= -1
        if self.x <= self.r:
            self.vx *= -1
        if self.y <= self.r:
            self.vy *= -1

    def should_it_commit_suicide(self, surface=screen):
        '''Проверяет, достаточно ли объект прожил перед уничтожением'''
        if pygame.time.get_ticks() - self.starting_time > 6000:
            return True
        else:
            return False

# Объявляется класс для Бориса (почти такой же как для шарика)

class Boris:

    '''Этот класс задает Бориса
           x, y - координаты
           vx, vy - скорости
           color - цвет
           vx, vy - скорости
           r - характерный размер
           surface - личная поверхность объекта
        '''

    def __init__(self):
        self.image = BORIS
        self.x = randint(200, 500)
        self.y = randint(200, 500)
        self.vx = randint(-2, 2)
        self.vy = randint(-2, 2)
        self.vx *= 0.50
        self.vy *= 0.50
        self.color = choice(COLORS)
        self.r = randint(20, 40)
        self.surface = pygame.Surface(
            (self.r * 2, self.r * 2), pygame.SRCALPHA, 32)
        self.surface = self.surface.convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (self.r * 2, self.r * 2))
        self.surface.blit(self.image, pygame.rect.Rect(
            0, 0, self.r * 2, self.r * 2))
        self.starting_time = pygame.time.get_ticks()

    def draw(self, surface=screen):
        '''Draw the object
           par: surface is the pygame surface to draw on'''
        surface.blit(self.surface, (self.x, self.y))

    def remove(self, surface=screen):
        '''Remove the object
           par: surface=screen is the surface to remove from'''
        self.color = BACKGROUND_COLOR
        circle(self.surface, self.color, (self.r, self.r), self.r)

    def move(self, surface=screen):
        '''Move the object
        par: surface=screen '''
        # self.remove(surface)
        self.x += randint(-2, 2)
        self.y += randint(-2, 2)
        # self.draw(surface)

    def collision(self):

        # Определяются коллизии со стенками

        if self.x >= 1000 - self.r:
            self.vx *= -1
        if self.y >= 800 - self.r:
            self.vy *= -1
        if self.x <= self.r:
            self.vx *= -1
        if self.y <= self.r:
            self.vy *= -1

    def should_it_commit_suicide(self, surface=screen):
        if pygame.time.get_ticks() - self.starting_time > 6000:
            return True
        else:
            return False


balls_pool = []  # массив шариков
boris_pool = []  # массив борисов


def draw_pool(balls_pool):
    '''Рисует весь пул объектов который подали аргументом'''
    for i in balls_pool:
        i.draw()


def move_pool(balls_pool):
    '''Двигает весь пул, который подали аргументом'''
    for i in balls_pool:
        i.move()
        i.collision()


finished = False

clock = pygame.time.Clock()

ball_genocide_counter = 0
have_i_shown_the_menu_enough = 900
list_of_players = []


def print_the_player_list(list_of_players):
    for num, player in enumerate(list_of_players):
        if num < 10:
            screen.blit(font.render(str(num + 1) + '. ' +
                                    player[0] + ' ' + str(player[1]), True, (255, 255, 255)), (150, 60 * num))


# with open("data.pickle", 'wb') as f:
#     pickle.dump(list_of_players, f)

with open("data.pickle", 'rb') as f:
    list_of_players = pickle.load(f)


while not finished:
    if(have_i_shown_the_menu_enough > 0):
        have_i_shown_the_menu_enough -= 1
        print_the_player_list(list_of_players)
    screen.blit(font.render(str(ball_genocide_counter),
                            True, (255, 255, 255)), (60, 60))
    for _ in range(choice(BALL_CHOICE)):
        balls_pool.append(Ball())

    for _ in range(choice(BORIS_CHOICE)):
        boris_pool.append(Boris())
    draw_pool(balls_pool)
    move_pool(balls_pool)
    for number, ball in enumerate(balls_pool):
        if ball.should_it_commit_suicide():
            balls_pool.pop(number)
    for number, boris in enumerate(boris_pool):
        if boris.should_it_commit_suicide():
            boris_pool.pop(number)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('Click!')
            click_x = pygame.mouse.get_pos()[0]
            click_y = pygame.mouse.get_pos()[1]
            for num, ball in enumerate(balls_pool):
                if ((click_x - ball.x)**2 + (click_y - ball.y)**2)**0.5 < 1.2 * ball.r:
                    balls_pool.pop(num)
                    ball_genocide_counter += 10
                    print(ball_genocide_counter)
            for num, boris in enumerate(boris_pool):
                if ((click_x - boris.x)**2 + (click_y - boris.y)**2)**0.5 < 0.3 * boris.r:
                    boris_pool.pop(num)
                    ball_genocide_counter += 100
                    print(ball_genocide_counter)
    pygame.display.update()
    screen.fill(BLACK)
    clock.tick(FPS)
list_of_players.append([name, ball_genocide_counter])
list_of_players = sorted(list_of_players, key=operator.itemgetter(1))
list_of_players.reverse()

with open("data.pickle", 'wb') as f:
    pickle.dump(list_of_players, f)
pygame.quit()
