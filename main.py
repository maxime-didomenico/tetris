import pygame
import os
import time
import random
from copy import deepcopy

pygame.init()
pygame.font.init()

# setting
w, h = 10, 20
square = 36
fps = 60
screen_res = (w * square * 1.7, h * square)
pygame.display.set_caption("Welcome to Tetris")
icon = pygame.image.load('img/ico.png')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode(screen_res)
clock = pygame.time.Clock()
last_drop = time.time()


# configures the figures
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
        fg.append(pygame.Rect(x + w // 2, y + 1, 1, 1))
    figures.append(fg)

# color of the figures
color = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

# start figure
figure = random.choice(figures)
figure_color = color[figures.index(figure)]
figure_rect = pygame.Rect(0, 0, square - 1, square - 1)

next_figure = deepcopy(random.choice(figures))
next_figure_color = color[figures.index(next_figure)]

# open or create a file to save the highest score
if not os.path.exists('score.txt'):
    with open('score.txt', 'w') as f:
        f.write("0")

font_path = "font/pixel_font.ttf"
pixel_font_title = pygame.font.Font(font_path, 90)


def game():
    global score, highest_score
    pygame.display.set_caption("Tetris - Game")

    # variables
    drop_time = 0.5
    last_drop = time.time()

    # field
    field = [[0 for x in range(w)] for y in range(h)]

    # score
    with open('score.txt') as f:
        highest_score = f.read()
    score = 0

    # functions

    def draw():
        draw_grid()
        draw_label()
        draw_field()
        draw_form()
        draw_next_form()
        pygame.display.flip()

    def draw_label():
        global score, highest_score

        title_font_pixel = pygame.font.Font(font_path, 60)
        label_font_pixel1 = pygame.font.Font(font_path, 35)
        label_font_pixel2 = pygame.font.Font(font_path, 30)
        title_label = title_font_pixel.render("Tetris", True, (255, 255, 255))
        score_label = label_font_pixel1.render("Score :", True, (255, 255, 255))
        point_label = label_font_pixel2.render(str(score), True, (255, 255, 255))
        score_font_pixel = pygame.font.Font(font_path, 26)
        highest_score_label = score_font_pixel.render("Highest Score :", True, (255, 255, 255))
        highest_score_data = label_font_pixel2.render(str(highest_score), True, (255, 255, 255))

        screen.blit(title_label, (w * square + 20, 20))
        screen.blit(score_label, (w * square + 20, 430))
        point_label = label_font_pixel2.render(str(score), True, (255, 255, 255))
        screen.blit(point_label, (w * square + 40, 490))
        screen.blit(highest_score_label, (w * square + 20, 560))
        screen.blit(highest_score_data, (w * square + 40, 600))

    def draw_grid():
        for x in range(w):
            for y in range(h):
                pygame.draw.rect(screen, (120, 120, 120), (x * square, y * square, square, square), 1)

    def draw_form():
        for i in range(len(figure)):
            figure_rect.x = figure[i].x * square
            figure_rect.y = figure[i].y * square
            pygame.draw.rect(screen, figure_color, figure_rect)

    def draw_next_form():
        for i in range(len(next_figure)):
            figure_rect.x = next_figure[i].x * square + 300
            figure_rect.y = next_figure[i].y * square + 200
            pygame.draw.rect(screen, next_figure_color, figure_rect)

    def draw_field():
        for x in range(w):
            for y in range(h):
                if field[y][x] != 0:
                    figure_rect.x = x * square
                    figure_rect.y = y * square
                    pygame.draw.rect(screen, color[int(field[y][x]-1)], figure_rect)
    
    def update_field():
        for i in range(4):
            field[figure[i].y][figure[i].x] = color.index(figure_color) + 1

    def move(dx):
        a = 0
        b = 0
        for i in range(4):
            if figure[i].x + dx > -1:
                a += 1
        if a == 4:
            for i in range(4):
                if figure[i].x + dx < w:
                    if can_move(dx):
                        b += 1
        if b == 4:
            for i in range(4):
                if can_move(dx):
                    figure[i].x += dx

    def can_move(dx):
        if dx > 0:
            for i in range(4):
                try:
                    if field[figure[i].y][figure[i].x + 1] != 0:
                        return False
                except IndexError:
                    break
        if dx < 0:
            for i in range(4):
                if field[figure[i].y][figure[i].x - 1] != 0:
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

    def is_valid():
        for i in range(4):
            if figure[i].x < 0 or figure[i].x > w - 1 or figure[i].y > h - 1:
                return False
            if field[figure[i].y][figure[i].x] != 0:
                return False
        return True

    def check():
        global figure, next_figure, figure_color, next_figure_color
        for i in range(4):
            if figure[i].y == h - 1 or field[figure[i].y + 1][figure[i].x] != 0:
                update_field()
                figure = deepcopy(next_figure)
                figure_color = color[figures.index(figure)]

                next_figure = deepcopy(random.choice(figures))
                next_figure_color = color[figures.index(next_figure)]

                return

    def line():
        global score, highest_score
        for i in range(h):
            if 0 not in field[i]:
                del field[i]
                field.insert(0, [0 for i in range(w)])
                score += 100
                if score > int(highest_score):
                    with open("score.txt", "w") as file:
                        file.write(str(score))
                    highest_score = score

    def endgame():
        for x in range(w):
            if field[0][x] != 0 or field[1][x] != 0:
                for i in range(w):
                    for j in range(h):
                        field[j][i] = 0
                game_over()
        if score > int(highest_score):
            with open("score.txt", "w") as file:
                file.write(str(score))

    # game loop
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.fill((120,120,120), (w * square, 0, w * square * 1.7, h * square))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move(-1)
                if event.key == pygame.K_RIGHT:
                    move(1)
                if event.key == pygame.K_UP:
                    rotate()
                if event.key == pygame.K_DOWN:
                    drop_time = 0.05
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    drop_time = 0.5
        if time.time() - last_drop > drop_time:
            last_drop = time.time()
            for i in range(4):
                global figure
                figure[i].y += 1
        draw()
        check()
        line()
        endgame()
        pygame.display.flip()

def credit():
    pygame.display.set_caption("Tetris - Credits")
    pixel_font_medium = pygame.font.Font("font/pixel_font.ttf", 60)
    pixel_font_small = pygame.font.Font("font/pixel_font.ttf", 40)
    credits_label_1 = pixel_font_small.render("Made by : ", True, (255, 255, 255))
    credits_label_2 = pixel_font_small.render("Maxime D.", True, (255, 255, 255))
    credits_label_3 = pixel_font_small.render("Melvin P.", True, (255, 255, 255))
    credits_label_4 = pixel_font_small.render("With the help of : ", True, (255, 255, 255))
    credits_label_5 = pixel_font_small.render("Chat GPT.", True, (255, 255, 255))
    credits_label_6 = pixel_font_small.render("Coder Space. ", True, (255, 255, 255))

    back = pygame.image.load("img/back_button.png")
    back = pygame.transform.scale(back, (90, 100))
    back_rect = back.get_rect(topleft=(10, 10))

    running = True
    while running:
        credit_mouse = pygame.mouse.get_pos()
        screen.fill((120, 120, 120))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(credit_mouse):
                    menu()
        screen.blit(credits_label_1, (150, 150))
        screen.blit(credits_label_2, (200, 250))
        screen.blit(credits_label_3, (200, 300))
        screen.blit(credits_label_4, (150, 400))
        screen.blit(credits_label_5, (200, 500))
        screen.blit(credits_label_6, (200, 550))
        screen.blit(back, (10, 10))
        pygame.display.flip()


def menu():

    title_label = pixel_font_title.render("Tetris", True, ((255, 255, 255)))
    start = pygame.image.load("img/start_button.png")
    credits = pygame.image.load("img/credits_button.png")
    exit = pygame.image.load("img/exit_button.png")
    start_rect = start.get_rect(topleft=(140, 250))
    credits_rect = credits.get_rect(topleft=(125, 400))
    exit_rect = exit.get_rect(topleft=(140, 550))

    running = True
    while running:
        pygame.display.set_caption("Welcome to Tetris")
        screen.fill((120, 120, 120))
        menu_mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(menu_mouse_pos):
                    game()
                if credits_rect.collidepoint(menu_mouse_pos):
                    credit()
                if exit_rect.collidepoint(menu_mouse_pos):
                    pygame.quit()
                    running = False

        screen.blit(title_label, (150, 50))
        screen.blit(start, start_rect)
        screen.blit(credits, credits_rect)
        screen.blit(exit, exit_rect)
        pygame.display.flip()
        clock.tick(fps)

def game_over():
    with open('score.txt') as f:
        highest_score = f.read()
    pygame.display.set_caption("Game Over")
    pixel_font_medium = pygame.font.Font("font/pixel_font.ttf", 60)
    pixel_font_small = pygame.font.Font("font/pixel_font.ttf", 30)
    game_over_label = pixel_font_medium.render("Game Over", True, (255, 0, 0))
    restart_label = pixel_font_small.render("Click anywhere to restart", True, (255, 255, 255))
    high_score_label = pixel_font_small.render("Highest Score : " + str(highest_score), True, (255, 255, 255))

    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                    menu()
        screen.blit(game_over_label, (150, 150))
        screen.blit(restart_label, (110, 450))
        screen.blit(high_score_label, (180, 290))
        pygame.display.flip()

menu()