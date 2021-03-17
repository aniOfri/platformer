import pygame
import random
import numpy

pygame.font.init()

width = 500
height = 700


class Platformer:
    def __init__(self, x, y, win):
        self.random_seed = random.randint(0, 100)
        self.surface = win

        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.vel = 3
        self.acceleration = 0
        self.air_time = 0

        self.platforms = []

        random.seed(self.random_seed)
        platforms = [random.randint(100, int(width/2)) for _ in range(0, 500)]
        y = 100
        for j, w in enumerate(platforms):
            x = random.randint(20, width-w-20)
            platforms[j] = (platforms[j], [x, y])

            y += random.randint(75, 100)

        self.platforms = [pygame.Rect(plt[1][0], height-(plt[1][1]), plt[0], 8) for plt in platforms]
        self.platforms.append(pygame.Rect(0, height-52, width, 50))

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        self.surface.fill((0, 0, 0))
        global height
        for plt in self.platforms:
            pygame.draw.rect(self.surface, (255, 255, 255), plt)

        pygame.draw.rect(self.surface, (255, 0, 0), self.rect)

        font = pygame.font.SysFont("Tahoma", 30, False, False)
        text_object = font.render("Air-Time: "+str(self.air_time), True, (255, 255, 255))
        self.surface.blit(text_object, (20, 10))

        pygame.display.update()

    def collide(self):
        x, y, rect_width, rect_height = self.rect
        rect = pygame.Rect(x, y+(rect_height - 1), rect_width, 1)
        collision = rect.collidelist(self.platforms)

        if collision == -1:
            for i in numpy.arange(0.1, 1, 0.001):
                x, y, rect_width, rect_height = self.rect
                rect = pygame.Rect(x, y+i+(rect_height-1), rect_width, 1)
                collision = rect.collidelist(self.platforms)
                if collision != -1:
                    break

        return collision

    def move(self):
        while self.y < height / 2 - 50:
            for plt in range(0, len(self.platforms)):
                self.platforms[plt].y += 1
            self.y += 1
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

            self.draw()

        while self.y > height / 2:
            for plt in range(0, len(self.platforms)):
                self.platforms[plt].y -= 5
            self.y -= 5
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

            self.draw()

        keys = pygame.key.get_pressed()
        collision = self.collide()

        if collision != -1 and self.vel >= 0:
            if keys[pygame.K_UP]:
                self.acceleration -= 8 + self.air_time
                if self.y < 0:
                    self.y = 0
            else:
                self.acceleration = 0
                self.vel = 0
                self.air_time -= 0.05
                if self.air_time < 0:
                    self.air_time = 0
                elif self.air_time < 8:
                    self.air_time = 8

        else:
            self.air_time += 0.01
            self.acceleration = 0.2

        if keys[pygame.K_LEFT]:
            self.x -= 3

            if self.x < 0:
                self.x += width

        if keys[pygame.K_RIGHT]:
            self.x += 3

            if self.x > width:
                self.x -= width

        self.vel += self.acceleration

        self.y += self.vel
        self.vel *= 0.98


