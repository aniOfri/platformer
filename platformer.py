import pygame
import random
import numpy

pygame.font.init()

width = 500
height = 700


class Platformer:
    def __init__(self, game_id):
        self.random_seed = random.randint(0, 100)
        self.ready = False
        self.started = False
        self.id = game_id
        self.timer = 0
        self.winner = -1
        self.goal = 35

        self.dir = [[False, False, False, False],
                    [False, False, False, False]]
        self.x = [width/2, width/2]
        self.y = [height-100, height-100]
        self.width = 20
        self.height = 20
        self.rect = [pygame.Rect(self.x[0], self.y[0], self.width, self.height),
                     pygame.Rect(self.x[1], self.y[1], self.width, self.height)]
        self.offset = [0, 0]

        self.vel = [3, 3]
        self.acceleration = [0, 0]
        self.air_time = [0, 0]
        self.air_time_color = [(255, 255, 255), (255, 255, 255)]
        self.score = [0, 0]
        self.last_collision = [0, 0]

        self.platforms = [[], []]

        random.seed(self.random_seed)
        platforms = [random.randint(100, int(width/2)) for _ in range(0, self.goal)]
        y = 100
        for j, w in enumerate(platforms):
            x = random.randint(20, width-w-20)
            platforms[j] = (platforms[j], [x, y])

            y += random.randint(50, 75)

        self.platforms[0].append(pygame.Rect(0, height - 50, width, 50))
        self.platforms[0] += [pygame.Rect(plt[1][0], height-(plt[1][1]), plt[0], 8) for plt in platforms]
        self.platforms[1] += self.platforms[0]

    def update(self):
        for p in [0, 1]:
            while self.y[p]+self.offset[p] < height / 2 - 50:
                self.offset[p] += 1

            while self.y[p]+self.offset[p] > height / 2 + 50:
                self.offset[p] -= 1

            self.rect[p] = pygame.Rect(self.x[p], self.y[p], self.width, self.height)

    def collide(self, prov_rect, p):
        collision = prov_rect.collidelist(self.platforms[p])

        if collision == -1:
            for i in numpy.arange(0.1, 1, 0.001):
                x, y, rect_width, rect_height = prov_rect
                rect = pygame.Rect(x, y + i, rect_width, rect_height)
                collision = rect.collidelist(self.platforms[p])
                if collision != -1:
                    break

        return collision

    def move(self, p):
        self.timer += 1

        x, y, rect_width, rect_height = self.rect[p]
        rect = pygame.Rect(x, y+(rect_height - 2), rect_width, 2)
        collision = self.collide(rect, p)

        if collision != -1 and self.vel[p] >= 0:
            if self.dir[p][2]:
                self.acceleration[p] = -(10+self.air_time[p])

                if self.y[p]+self.offset[p] < 0:
                    self.y[p] = 0
            else:
                self.acceleration[p] = 0
                self.vel[p] = 0
                if not self.dir[p][3]:
                    self.air_time[p] -= 0.2
                    self.air_time_color[p] = (255, 0, 0)

                if self.air_time[p] < 0:
                    self.air_time[p] = 0
                    self.air_time_color[p] = (255, 255, 255)

        else:
            if self.vel[p] <= 10:
                self.acceleration[p] = 0.5
            else:
                self.vel[p] = 10
            if self.vel[p] < 0:
                self.air_time[p] += 0.01
                self.air_time_color[p] = (0, 255, 0)

        if self.air_time[p] > 5:
            self.air_time[p] = 5
            self.air_time_color[p] = (0, 0, 255)

        rect = pygame.Rect(0, self.y[p]+10, width, 10)
        score_collision = self.collide(rect, p)

        if score_collision != self.last_collision[p]:
            self.last_collision[p] = score_collision

            if score_collision != -1 and collision != -1 and self.vel[p] <= 0:
                self.score[p] = score_collision
            elif score_collision != -1 and self.vel[p] > 0:
                self.score[p] = score_collision-1

        if self.dir[p][1]:
            if not self.dir[p][3]:
                self.x[p] -= 3

            if self.x[p] < 0:
                self.x[p] += width

        if self.dir[p][0]:
            if not self.dir[p][3]:
                self.x[p] += 3

            if self.x[p] > width:
                self.x[p] -= width

        print(self.vel[1], self.acceleration[1])
        self.vel[p] += self.acceleration[p]

        self.y[p] += self.vel[p]
        self.vel[p] *= 0.98

    def reset_game(self):
        self.random_seed = random.randint(0, 100)
        self.started = False
        self.timer = 0
        self.winner = -1

        self.x = [width/2, width/2]
        self.y = [height-100, height-100]
        self.offset = [0, 0]

        self.vel = [3, 3]
        self.air_time = [0, 0]
        self.score = [0, 0]
        self.last_collision = [0, 0]

        self.platforms = [[], []]

        random.seed(self.random_seed)
        platforms = [random.randint(100, int(width/2)) for _ in range(0, self.goal)]
        y = 100
        for j, w in enumerate(platforms):
            x = random.randint(20, width-w-20)
            platforms[j] = (platforms[j], [x, y])

            y += random.randint(50, 75)

        self.platforms[0].append(pygame.Rect(0, height - 50, width, 50))
        self.platforms[0] += [pygame.Rect(plt[1][0], height-(plt[1][1]), plt[0], 8) for plt in platforms]
        self.platforms[1] += self.platforms[0]
