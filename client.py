import pygame
import random
from platformer import Platformer
pygame.font.init()

width = 500
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Platformer")


def main():
    run = True
    clock = pygame.time.Clock()
    pfmr = Platformer(width/2, height-100, win)
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        pfmr.update()
        pfmr.move()
        pfmr.draw()


main()