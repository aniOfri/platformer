import pygame
import socket
from network import Network
from platformer import Platformer
pygame.font.init()
pygame.init()

width = 500
height = 700
win = pygame.display.set_mode((width, height))


def add_offset(rect, offset):
    x, y, rect_w, rect_h = rect
    modified_rect = pygame.Rect(x, y + offset, rect_w, rect_h)
    return modified_rect


def update_window(pfmr, p):
    win.fill((0, 0, 0))
    global height
    global width

    if not pfmr.ready:
        num = 10
        for i in range(0, num):
            pygame.draw.line(win, (230, 130, 120), (width / num * i, -1), (-1, height / num * i), width=4)
            pygame.draw.line(win, (230, 130, 120), (width - (width / num * i), height),
                             (width, height - (height / num * i)), width=4)
        pygame.draw.line(win, (230, 130, 120), (width, 0), (0, height),
                         width=4)

        font = pygame.font.SysFont("comicssans", 75)
        text = font.render("Waiting for player..", True, (30, 100, 250))
        win.blit(text, (width / 2 - text.get_width() / 2-1, height / 2 - text.get_height() / 2-1))

        font = pygame.font.SysFont("comicssans", 75)
        text = font.render("Waiting for player..", True, (255, 255, 255))
        win.blit(text, (width/2 - text.get_width()/2+1, height/2 - text.get_height()/2+1))
    else:
        for plt in pfmr.platforms[p]:
            rect = add_offset(plt, pfmr.offset[p])
            pygame.draw.rect(win, (255, 255, 255), rect)

        if p == 0:
            rect1 = add_offset(pfmr.rect[0], pfmr.offset[0])
            pygame.draw.rect(win, (255, 0, 0), rect1)

            if pfmr.ready:
                rect2 = add_offset(pfmr.rect[1], pfmr.offset[0])
                pygame.draw.rect(win, (0, 255, 0), rect2)
        else:
            rect1 = add_offset(pfmr.rect[0], pfmr.offset[1])
            pygame.draw.rect(win, (255, 0, 0), rect1)

            if pfmr.ready:
                rect2 = add_offset(pfmr.rect[1], pfmr.offset[1])
                pygame.draw.rect(win, (0, 255, 0), rect2)

        font = pygame.font.SysFont("Tahoma", 20, False, False)
        text_object1 = font.render("Air-Time: "+str(round(pfmr.air_time[p], 4)), True, pfmr.air_time_color[p])
        text_object2 = font.render("Score: "+str(pfmr.score[p]), True, (255, 255, 255))
        win.blit(text_object1, (20, 10))
        win.blit(text_object2, (20, 35))

    pygame.display.update()


def countdown(time):
    win.fill((0, 0, 0))
    font = pygame.font.SysFont("comicssans", 75)
    text = font.render(str(time), True, (30, 100, 250))
    win.blit(text, (width / 2 - text.get_width() / 2 - 1, height / 2 - text.get_height() / 2 - 1))

    font = pygame.font.SysFont("comicssans", 75)
    text = font.render(str(time), True, (255, 255, 255))
    win.blit(text, (width / 2 - text.get_width() / 2 + 1, height / 2 - text.get_height() / 2 + 1))
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

        if pfmr.ready and not pfmr.started:
            countdown(1)
            pygame.time.delay(1000)
            countdown(2)
            pygame.time.delay(1000)
            countdown(3)
            pygame.time.delay(1000)
            countdown("RUSH")
            pygame.time.delay(200)

            pfmr = n.send("started")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    pfmr = n.send("down0")
                if event.key == pygame.K_LEFT:
                    pfmr = n.send("down1")
                if event.key == pygame.K_UP:
                    pfmr = n.send("down2")
                if event.key == pygame.K_SHIFT:
                    pfmr = n.send("down3")

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    pfmr = n.send("up0")
                if event.key == pygame.K_LEFT:
                    pfmr = n.send("up1")
                if event.key == pygame.K_UP:
                    pfmr = n.send("up2")
                if event.key == pygame.K_SHIFT:
                    pfmr = n.send("up3")

        if pfmr.started:
            pfmr = n.send("move")
        else:
            print(pygame.time.get_ticks())

        update_window(pfmr, player)


main()
