import pygame
import socket
from network import Network
from platformer import Platformer
pygame.font.init()

width = 500
height = 700
win = pygame.display.set_mode((width, height))


def update_window(pfmr, p):
    win.fill((0, 0, 0))
    global height

    for plt in pfmr.platforms[p]:
        pygame.draw.rect(win, (255, 255, 255), plt)

    pygame.draw.rect(win, (255, 0, 0), pfmr.rect[p])

    font = pygame.font.SysFont("Tahoma", 20, False, False)
    text_object1 = font.render("Air-Time: "+str(round(pfmr.air_time[p], 4)), True, pfmr.air_time_color[p])
    text_object2 = font.render("Score: "+str(pfmr.score[p]), True, (255, 255, 255))
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
        clock.tick(60)

        try:
            pfmr = n.send("update")
        except socket.error as e:
            print(e)
            print("Couldn't get game..")
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    n.send("down0")
                if event.key == pygame.K_LEFT:
                    n.send("down1")
                if event.key == pygame.K_UP:
                    n.send("down2")

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    n.send("up0")
                if event.key == pygame.K_LEFT:
                    n.send("up1")
                if event.key == pygame.K_UP:
                    n.send("up2")

        if pfmr.ready:
            pfmr = n.send("move")

        update_window(pfmr, player)


main()
