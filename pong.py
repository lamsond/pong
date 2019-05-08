import pygame, sys
import math
import random
import time

#constants
DIMS = (700, 700)
FPS = 30
PAD_SPEED = 5
BALL_SPEED_0 = 8
PAD_WIDTH = 20
PAD_HEIGHT = 100
LINE_THK = 3
BALL_DIAMETER = 6
PADDING = 10
DASH_LENGTH = 13
DASH_THK = 1

#colors
BLACK = (0, 0, 0)
ORANGE = (252, 121, 22)
WHITE = (255, 255, 255)


#classes
class Paddle():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = PAD_SPEED
        self.rect = pygame.Rect(self.x, self.y, PAD_WIDTH, PAD_HEIGHT)
        self.color = ORANGE
        self.score = 0

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)
        pygame.draw.rect(surf, BLACK, self.rect, LINE_THK)

class Ball():
    def __init__(self):
        self.x = int((DIMS[0]-BALL_DIAMETER)/2)
        self.y = int(DIMS[1]/2)
        self.speed = BALL_SPEED_0
        self.vector = self.get_unit_vector()
        self.rect = pygame.Rect(self.x, self.y, BALL_DIAMETER, BALL_DIAMETER)
        self.color = ORANGE

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)

    def get_unit_vector(self):
        while True:
            rand_x = random.randint(-8, 8)
            rand_y = random.randint(-8, 8)
            if rand_x == 0 or rand_y == 0:
                continue
            mag = math.sqrt(rand_x**2 + rand_y**2)
            return [rand_x/mag, rand_y/mag]

    def move(self):
        self.x += int(self.speed*self.vector[0])
        self.y += int(self.speed*self.vector[1])
        self.rect = pygame.Rect(self.x, self.y, BALL_DIAMETER, BALL_DIAMETER)

    def check_walls(self, wall):
        for i in range(len(wall.walls)):
            if self.rect.colliderect(wall.walls[i]):
                print("collided with wall " + str(i))
                if i % 2 == 1:
                    self.vector[1] *= -1
                else:
                    return True
        return False

    def reset(self):
        self.x = int((DIMS[0]-BALL_DIAMETER)/2)
        self.y = int(DIMS[1]/2)
        time.sleep(1)
        self.vector = self.get_unit_vector()

class Border():
    def __init__(self):
        self.width = DIMS[0]-2*PADDING
        self.height = DIMS[1] - 2*PADDING
        self.north_wall = pygame.Rect(PADDING, PADDING, self.width, LINE_THK)
        self.east_wall = pygame.Rect(DIMS[0]-PADDING, PADDING, LINE_THK, self.height)
        self.south_wall = pygame.Rect(PADDING, DIMS[1]-PADDING, self.width, LINE_THK)
        self.west_wall = pygame.Rect(PADDING, PADDING, LINE_THK, self.height)
        self.walls = [self.east_wall, self.north_wall, self.west_wall, self.south_wall]
    def draw(self, surf):
        pygame.draw.rect(surf, WHITE, (PADDING, PADDING, self.width,
            self.height), LINE_THK)
        for i in range(PADDING, DIMS[1]-PADDING, DASH_LENGTH*2):
            pygame.draw.line(surf, WHITE, (DIMS[0]/2, i), (DIMS[0]/2,
                i+DASH_LENGTH), DASH_THK)


#defs
def update_score(p1, p2, b):
    if b.x < p1.x:
        p2.score += 1
        print("player 2: " + str(p2.score))
    elif b.x > p2.x:
        p1.score += 1
        print("player 1: " + str(p1.score))
    b.reset()


#init game
pygame.init()

screen = pygame.display.set_mode(DIMS)
pygame.display.set_caption('Pong!')
clock = pygame.time.Clock()

border = Border()
paddle_left = Paddle(50, 300)
paddle_right = Paddle(DIMS[0]-50-PAD_WIDTH, 300)
ball = Ball()

print(ball.vector)
#game loop
while True:
    screen.fill(BLACK)
    border.draw(screen)
    paddle_left.draw(screen)
    paddle_right.draw(screen)
    ball.draw(screen)

    ball.move()
    if ball.check_walls(border):
        update_score(paddle_left, paddle_right, ball)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(30)
