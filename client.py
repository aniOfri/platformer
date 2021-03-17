import pygame
from platformer import Platformer
from network import Network
pygame.font.init()

width = 500
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Platformer")


def main():
    run = True
    n = Network("localhost")
    player = int(n.get())
    clock = pygame.time.Clock()
    pygame.display.set_caption("Hippel! | Player " + str(player + 1))
    print("You are player number ", player)

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
