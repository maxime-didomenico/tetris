import numpy as np
import pygame as pg
import random
import os
from copy import deepcopy
import time

pg.init()
pg.font.init()

w, h = 10, 20
square = 36
fps = 60
screen_res = (w * square * 1.7, h * square)
pg.display.set_caption("Tetris - Game")
screen = pg.display.set_mode(screen_res)
clock = pg.time.Clock()
score = 0
bg_color = (0, 0, 0)
field = np.zeros((h, w))

# open or create a file to save the highest score
if not os.path.exists('score.txt'):
    with open('score.txt', 'w') as f:
        f.write("0")

font_path = "font/pixel_font.ttf"
pixel_font_title = pg.font.Font(font_path, 90)

score = 0

with open('score.txt') as f:
    highest_score = f.read()

# time
drop_time = 0.5
last_drop = time.time()
landed = False

# configures the figures
# figures_pos is the position of the figures and figures is the figure itself

figures_pos = [[(0, 0), (-2, 0), (-1, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = []
for fig_pos in figures_pos:
    fg = []
    for i in range(len(fig_pos)):
        x, y = fig_pos[i]
        fg.append(pg.Rect(x + w // 2, y + 1, 1, 1))
    figures.append(fg)

# color of the figures
color = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

# function

def run():

    with open('score.txt') as f:
        highest_score = f.read()

    # labels
    title_font_pixel = pg.font.Font(font_path, 60)
    label_font_pixel1 = pg.font.Font(font_path, 35)
    label_font_pixel2 = pg.font.Font(font_path, 30)
    title_label = title_font_pixel.render("Tetris", True, (255, 255, 255))
    score_label = label_font_pixel1.render("Score :", True, (255, 255, 255))
    point_label = label_font_pixel2.render(str(score), True, (255, 255, 255))
    score_font_pixel = pg.font.Font(font_path, 26)
    highest_score_label = score_font_pixel.render("Highest Score :", True, (255, 255, 255))
    highest_score_data = label_font_pixel2.render(str(highest_score), True, (255, 255, 255))
    screen.blit(title_label, (w * square + 20, 20))
    screen.blit(score_label, (w * square + 20, 430))
    screen.blit(point_label, (w * square + 50, 490))
    screen.blit(highest_score_label, (w * square + 20, 560))
    screen.blit(highest_score_data, (w * square + 40, 600))

    draw()
    check()
    line()
    endgame()

def check():
    global figure, fig_color, landed, next_figure, next_figure_int

    for i in range(4):
        if figure[i].y == h - 1:
            landed = True
            break
        if field[figure[i].y + 1][figure[i].x] == 1:
            landed = True
            break
    if landed:
        for i in range(4):
            field[figure[i].y][figure[i].x] = 1
        figure = next_figure
        fig_color = color[figures.index(figure)]
        next_figure_int = next_int(next_figure_int)
        next_figure = figures[next_figure_int]
        landed = False


def draw():
    grid()
    draw_field()
    draw_form()
    draw_field()
    print_next_fig()

def print_next_fig():
    global next_figure
    for i in range(4):
        figure_rect.x = next_figure[i].x * square + 300
        figure_rect.y = next_figure[i].y * square + 200
        pg.draw.rect(screen, fig_color, figure_rect)

def grid():
    for x in range(w):
        for y in range(h):
            pg.draw.rect(screen, (128, 128, 128), (x * square, y * square, square, square), 1)


def draw_field():
    for x in range(w):
        for y in range(h):
            if field[y][x] == 1:
                figure_rect.x = x * square
                figure_rect.y = y * square
                pg.draw.rect(screen, (255, 255, 255), figure_rect)



def draw_form():
    for i in range(4):
        figure_rect.x = figure[i].x * square
        figure_rect.y = figure[i].y * square
        pg.draw.rect(screen, fig_color, figure_rect)


def endgame():
    global field, running
    for x in range(w):
        if field[0][x] == 1 or field[1][x] == 1:
            running = False
            break
    


def line():
    global score, field
    for y in range(h):
        if 0 not in field[y]:
            field = np.delete(field, y, 0)
            field = np.insert(field, 0, 0, 0)
            score += 1
            if score > int(highest_score):
                with open('score.txt', 'w') as f:
                    f.write(str(score))


def move(dx):
    a = 0
    b = 0
    for i in range(4):
        if figure[i].x + dx > -1:
            a += 1
    if a == 4:
        for i in range(4):
            if figure[i].x + dx < w:
                b += 1
    if b == 4:
        for i in range(4):
            figure[i].x += dx


def draw_next_figure():
    for i in range(4):
        figure_rect.x = figure[i].x * square + 100
        figure_rect.y = figure[i].y * square + 100
        pg.draw.rect(screen, fig_color, figure_rect)


def is_valid():
    for i in range(4):
        if figure[i].x < 0 or figure[i].x > w - 1 or figure[i].y > h - 1:
            return False
        if field[figure[i].y][figure[i].x] == 1:
            return False
    return True


def rotate():
    global figure
    figure_old = deepcopy(figure)
    center = figure[0]
    if figure == figures[1]:
        return
    for i in range(4):
        x = figure[i].y - center.y
        y = figure[i].x - center.x
        figure[i].x = center.x - x
        figure[i].y = center.y + y
    if not is_valid():
        figure = figure_old

def next_int(figure_int):
    check = 0
    next_figure_int = random.randint(0, 6)
    while check == 0:
        if next_figure_int != figure_int:
            check = 1
            return next_figure_int
        else:
            next_figure_int = random.randint(0, 6)



# figure_rect is the rectangle that will be drawn on the screen
figure_rect = pg.Rect(0, 0, square - 1, square - 1)

figure_int = random.randint(0, 6)
figure = figures[figure_int]

fig_color = color[figures.index(figure)]

next_figure_int = next_int(figure_int)
next_figure = figures[next_figure_int]

# main loop

running = True

while running:
    screen.fill(bg_color)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                move(-1)
            if event.key == pg.K_RIGHT:
                move(1)
            if event.key == pg.K_UP:
                rotate()
            if event.key == pg.K_DOWN:
                drop_time = 0.05
        if event.type == pg.KEYUP:
            if event.key == pg.K_DOWN:
                drop_time = 0.5
    run()
    if time.time() - last_drop > drop_time:
        last_drop = time.time()
        for i in range(4):
            figure[i].y += 1
    pg.display.flip()
    clock.tick(fps)

if __name__ == '__main__':
    run()