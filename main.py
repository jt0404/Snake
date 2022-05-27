import pygame as pg
import random

# initialize pygame
pg.init() # constants
SCRS = 600
GS = 500
FPS = 15
DELAY = 50
GN = 21
CS = GS // (GN - 1)
SGP = (SCRS-GS) // 2
EGP = SGP + GS
BGC = (0, 0, 0)
GC = (255, 255, 255)
SC = (120,190,33)
FC = (255, 0, 0)
FS = 25

# variables
screen = pg.display.set_mode((SCRS, SCRS))
clock = pg.time.Clock()
font = pg.font.SysFont('Comic Sans', FS)

# functions
def adj_snake(pos):
    if pos <= SGP - CS:
        return EGP - CS
    if pos >= EGP:
        return SGP
    return pos


def rfp():
    return random.randrange(GN - 1)*CS + SGP


def draw_grid():
    gp = SGP
    for _ in range(GN):
        # vertical
        pg.draw.line(screen, GC, (gp, SGP), (gp, EGP))
        # horizontal
        pg.draw.line(screen, GC, (SGP, gp), (EGP, gp))
        gp += CS


def draw(snake, fx, fy, score):
    screen.fill(BGC)
    # score
    text = font.render(f'Score {score}', True, GC)
    screen.blit(text, (25, 25))
    # fruit
    pg.draw.rect(screen, FC, (fx, fy, CS, CS))
    # snake
    for sx, sy in snake:
        pg.draw.rect(screen, SC, (sx, sy, CS, CS))
    draw_grid()
    pg.display.update()

# main function
if __name__ == '__main__':
    run = True
    ssp = (GN-1)//2 * CS + SGP
    snake = [(ssp, ssp)]
    sxv, syv = CS, 0
    fx = rfp()
    fy = rfp()
    score = 0

    while run:
        draw(snake, fx, fy, score)
        hx, hy = snake[0]
        tx, ty = snake[-1]

        # fruit capture
        if hx == fx and hy == fy:
            snake.append([tx - sxv, ty - syv])
            fx = rfp()
            fy = rfp()
            score += 1

        # snake movement
        sx = adj_snake(snake[0][0] + sxv)
        sy = adj_snake(snake[0][1] + syv)
        snake[0] = sx, sy
        for i in range(1, len(snake)):
            phx, phy = snake[i]
            snake[i] = hx, hy
            hx, hy = phx, phy

        # snake collision
        if len(snake) != len(set(snake)):
            snake = [[ssp, ssp]]
            sxv, syv = CS, 0
            fx = rfp()
            fy = rfp()
            score = 0

        # event handling
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    sxv = -CS
                    syv = 0
                elif event.key == pg.K_RIGHT:
                    sxv = CS
                    syv = 0
                elif event.key == pg.K_UP:
                    sxv = 0
                    syv = -CS
                elif event.key == pg.K_DOWN:
                    sxv = 0
                    syv = CS

        clock.tick(FPS)
        pg.time.delay(DELAY)

    quit()
