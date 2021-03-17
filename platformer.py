import pygame
import random

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

        self.platforms = []

    def update(self):
        random.seed(self.random_seed)
        platforms = [random.randint(100, int(width/2)) for _ in range(0, 500)]
        y = 100
        for j, w in enumerate(platforms):
            x = random.randint(20, width-w-20)
            platforms[j] = (platforms[j], [x, y])

            y += random.randint(50, 100)

        self.platforms = [pygame.Rect(plt[1][0], height-(plt[1][1]), plt[0], 5) for plt in platforms]
        self.platforms.append(pygame.Rect(0, height-5, width, 5))

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        self.surface.fill((0, 0, 0))
        global height
        for plt in self.platforms:
            pygame.draw.rect(self.surface, (255, 255, 255), plt)

        pygame.draw.rect(self.surface, (255, 0, 0), self.rect)
        pygame.display.update()

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.y -= 3
            if self.y < 0:
                self.y = 0

        if keys[pygame.K_LEFT]:
            self.x -= 3

            if self.x < 0:
                self.x = 0

        if keys[pygame.K_RIGHT]:
            self.x += 3

            if self.x + self.width > width:
                self.x = width - self.width

        self.vel += self.acceleration
        self.y += self.vel
        self.vel *= 0.998