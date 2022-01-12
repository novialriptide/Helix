"""
Helix: Flight Test (c) 2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

x = 0
y = 0
dt = 0
fps = 30

while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                fps += 5

    screen.fill((0,0,0))
    pygame.draw.rect(screen, (255,255,255), pygame.Rect(x, y, 10, 10))

    x += 0.05 * dt
    
    pygame.display.update()
    dt = clock.tick(fps)
    print(clock.get_fps())
