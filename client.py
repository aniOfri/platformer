import pygame
import socket
from network import Network
pygame.font.init()

width = 500
height = 700
win = pygame.display.set_mode((width, height))


def update_window(pfmr):
    win.fill((0, 0, 0))
    global height

    for plt in pfmr.platforms:
        pygame.draw.rect(win, (255, 255, 255), plt)

    pygame.draw.rect(win, (255, 0, 0), pfmr.rect)

    font = pygame.font.SysFont("Tahoma", 20, False, False)
    text_object1 = font.render("Air-Time: "+str(round(pfmr.air_time, 4)), True, pfmr.air_time_color)
    text_object2 = font.render("Score: "+str(pfmr.score), True, (255, 255, 255))
    win.blit(text_object1, (20, 10))
    win.blit(text_object2, (20, 35))

    pygame.display.update()


def main():
    run = True
    n = Network("localhost")
    player = int(n.get())
    clock = pygame.time.Clock()
    pygame.display.set_caption("Platformer | Player " + str(player + 1))
    print("You are player number ", player)

    while run:
        try:
            pfmr = n.send("")
        except socket.error as e:
            print(e)
            print("Couldn't get game..")
            break

        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        n.send("update")
        pfmr = n.send("move")

        update_window(pfmr)


main()
