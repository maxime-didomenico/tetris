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
pg.display.set_caption("Welcome to Tetris")
screen = pg.display.set_mode(screen_res)
clock = pg.time.Clock()
score = 0

# open or create a file to save the highest score
if not os.path.exists('score.txt'):
    with open('score.txt', 'w') as f:
        f.write("0")

font_path = "font/pixel_font.ttf"
pixel_font_title = pg.font.Font(font_path, 90)


def credit():
    pg.display.set_caption("Tetris - Credits")
    pixel_font_medium = pg.font.Font("font/pixel_font.ttf", 60)
    pixel_font_small = pg.font.Font("font/pixel_font.ttf", 40)
    credits_label_1 = pixel_font_small.render("Made by : ", True, (255, 255, 255))
    credits_label_2 = pixel_font_small.render("Maxime D.", True, (255, 255, 255))
    credits_label_3 = pixel_font_small.render("Melvin P.", True, (255, 255, 255))
    credits_label_4 = pixel_font_small.render("Chat GPT.", True, (255, 255, 255))

    back = pg.image.load("img/back_button.png")
    back = pg.transform.scale(back, (100, 100))
    back_rect = back.get_rect(topleft=(10, 10))

    running = True
    while running:
        credit_mouse = pg.mouse.get_pos()
        screen.fill((120, 120, 120))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(credit_mouse):
                    menu()
        screen.blit(credits_label_1, (200, 200))
        screen.blit(credits_label_2, (200, 300))
        screen.blit(credits_label_3, (200, 350))
        screen.blit(credits_label_4, (200, 400))
        screen.blit(back, (10, 10))
        pg.display.flip()


def menu():

    title_label = pixel_font_title.render("Tetris", True, (255, 255, 255))
    start = pg.image.load("img/start_button.png")
    credits = pg.image.load("img/credits_button.png")
    exit = pg.image.load("img/exit_button.png")

    start_rect = start.get_rect(topleft=(50, 160))
    credits_rect = credits.get_rect(topleft=(90, 350))
    exit_rect = exit.get_rect(topleft=(140, 530))

    running = True
    while running:
        pg.display.set_caption("Welcome to Tetris")
        screen.fill((120, 120, 120))
        menu_mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                running = False

            if event.type == pg.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(menu_mouse_pos):
                    os.system("python game.py")
                    pg.quit()
                    running = False
                if credits_rect.collidepoint(menu_mouse_pos):
                    credit()
                if exit_rect.collidepoint(menu_mouse_pos):
                    pg.quit()
                    running = False

        screen.blit(title_label, (150, 35))
        screen.blit(start, start_rect)
        screen.blit(credits, credits_rect)
        screen.blit(exit, exit_rect)
        pg.display.flip()
        clock.tick(fps)

menu()