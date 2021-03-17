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
        self.air_time_color = (255, 255, 255)
        self.score = 0
        self.last_collision = -1

        self.platforms = []

        random.seed(self.random_seed)
        platforms = [random.randint(100, int(width/2)) for _ in range(0, 500)]
        y = 100
        for j, w in enumerate(platforms):
            x = random.randint(20, width-w-20)
            platforms[j] = (platforms[j], [x, y])

            y += random.randint(75, 100)

        self.platforms = [pygame.Rect(plt[1][0], height-(plt[1][1]), plt[0], 8) for plt in platforms]
        self.platforms.append(pygame.Rect(0, height-50, width, 50))

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        self.surface.fill((0, 0, 0))
        global height
        for plt in self.platforms:
            pygame.draw.rect(self.surface, (255, 255, 255), plt)

        pygame.draw.rect(self.surface, (255, 0, 0), self.rect)

        font = pygame.font.SysFont("Tahoma", 20, False, False)
        text_object1 = font.render("Air-Time: "+str(round(self.air_time, 4)), True, self.air_time_color)
        text_object2 = font.render("Score: "+str(self.score), True, (255, 255, 255))
        self.surface.blit(text_object1, (20, 10))
        self.surface.blit(text_object2, (20, 35))

        pygame.display.update()

    def collide(self, rect):
        collision = rect.collidelist(self.platforms)

        if collision == -1:
            for i in numpy.arange(0.1, 1, 0.001):
                x, y, rect_width, rect_height = self.rect
                rect = pygame.Rect(x, y+i+(rect_height-1), rect_width, 1)
                collision = rect.collidelist(self.platforms)
                if collision != -1:
                    self.y -= i
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

        x, y, rect_width, rect_height = self.rect
        rect = pygame.Rect(x, y+(rect_height - 1), rect_width, 1)
        collision = self.collide(rect)

        if collision != -1 and self.vel >= 0:
            if keys[pygame.K_UP]:
                self.acceleration -= 10 + self.air_time
                if self.y < 0:
                    self.y = 0
            else:
                self.acceleration = 0
                self.vel = 0
                self.air_time -= 0.2
                self.air_time_color = (255, 0, 0)
                if self.air_time < 0:
                    self.air_time = 0
                    self.air_time_color = (255, 255, 255)
                elif self.air_time > 5:
                    self.air_time = 5
                    self.air_time_color = (0, 0, 255)
        else:
            self.acceleration = 0.2
            if self.vel < 0:
                self.air_time += 0.01
                self.air_time_color = (0, 255, 0)

        rect = pygame.Rect(0, self.y, width, 10)
        score_collision = self.collide(rect)
        if score_collision == 500:
            score_collision = 0
        if score_collision != -1 and score_collision != self.last_collision:
            if self.last_collision > score_collision:
                self.score -= abs(self.last_collision-score_collision)
            elif self.last_collision < score_collision:

                self.score += abs(self.last_collision-score_collision)

            self.last_collision = score_collision

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


