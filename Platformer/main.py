from platform import *
import pygame
from level import *
from platformer import Player

pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption('YAA!')

running = True

clock = pygame.time.Clock()
time_speed = 60

#should do the loading level thingy too (after the rooms ofc)
L=Level(path='level.png')
P=Player(L, time_speed)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()


    screen.fill((0,255,255))
    L.update(screen)
    P.update()

    clock.tick(time_speed)
    pygame.display.update()