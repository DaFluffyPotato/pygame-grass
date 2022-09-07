import sys
import time
import math
import random

import pygame
from pygame.locals import *

import grass

# set up pygame
pygame.init()
pygame.display.set_caption('grass demo')

screen = pygame.display.set_mode((600, 600), 0, 32)
display = pygame.Surface((300, 300))

clock = pygame.time.Clock()

# set up the grass manager and enable shadows
gm = grass.GrassManager('grass', tile_size=10, stiffness=600, max_unique=5, place_range=[0, 1])
gm.enable_ground_shadows(shadow_radius=4, shadow_color=(0, 0, 1), shadow_shift=(1, 2))

# fill in the base square
for y in range(20):
    y += 5
    for x in range(20):
        x += 5
        v = random.random()
        if v > 0.1:
            gm.place_tile((x, y), int(v * 12), [0, 1, 2, 3, 4])

# general variables
t = 0
start = time.time()

scroll = [0, 0]
camera_speed = 170
clicking = False
brush_size = 1

# demo loop
while True:
    # calc dt
    dt = time.time() - start
    start = time.time()

    # fill background
    display.fill((27, 66, 52))

    # calculate mouse position in pixels
    mx, my = pygame.mouse.get_pos()
    mx /= 2
    my /= 2

    # move camera based on mouse position
    if mx / display.get_width() < 0.2:
        scroll[0] -= camera_speed * dt
    if mx / display.get_width() > 0.8:
        scroll[0] += camera_speed * dt
    if my / display.get_height() < 0.2:
        scroll[1] -= camera_speed * dt
    if my / display.get_height() > 0.8:
        scroll[1] += camera_speed * dt

    # apply a force from the mouse's position relative to the brush size
    gm.apply_force((mx + scroll[0], my + scroll[1]), 10 * brush_size, 25 * brush_size)

    # create an anonymous function that will apply a wind pattern to the grass when passed to the grass manager's update render function
    # this function uses the X offset of the grass, the master time of the application, and a sine function to create the pattern.
    rot_function = lambda x, y: int(math.sin(t / 60 + x / 100) * 15)

    # run the update/render for the grass
    gm.update_render(display, dt, offset=scroll, rot_function=rot_function)

    # draw the circles for the mouse
    pygame.draw.circle(display, (255, 255, 255), (mx, my), 10 * brush_size - int(clicking) * 2, 2 if not clicking else 0)
    if clicking:
        pygame.draw.circle(display, (255, 255, 255), (mx, my), 10 * brush_size, 1)

    # increment master time
    t += dt * 100

    # place new tiles if clicking
    if clicking:
        gm.place_tile((int((mx + scroll[0]) // gm.tile_size), int((my + scroll[1]) // gm.tile_size)), int(random.random() * 12 * brush_size + 1), [0, 1, 2, 3, 5])
        # place a 3x3 pattern of tiles if the brush is full size
        if brush_size == 1:
            offsets = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
            for offset in offsets:
                gm.place_tile((int((mx + scroll[0]) // gm.tile_size) + offset[0], int((my + scroll[1]) // gm.tile_size) + offset[1]), int(random.random() * 14 + 3), [0, 1, 2, 3, 5])

    # handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_e:
                print(clock.get_fps())

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 4:
                brush_size = min(1, brush_size + 0.1)
            if event.button == 5:
                brush_size = max(0.1, brush_size - 0.1)
            if event.button == 1:
                clicking = True
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                clicking = False

    # render
    screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
    pygame.display.update()
    clock.tick(1000)
