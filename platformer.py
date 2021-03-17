import pygame

width = 500
height = 700


class Platformer:
    def __init__(self, x, y, win):
        self.surface = win
        self.x = x
        self.y = y
        self.offset_y = 0
        self.width = 20
        self.height = 20
        self.platforms = []
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.vel = 3
        self.acceleration = 0

    def update(self):
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