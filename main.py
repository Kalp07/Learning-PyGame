import pygame
from os.path import join
import random

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('assets/ufo.png')
running = True

surf = pygame.Surface((100, 200))
surf.fill('orange')
x = 100

player_surf = pygame.image.load(join('assets', 'images', 'player.png')).convert_alpha()
star_surf = pygame.image.load(join('assets', 'images', 'star.png')).convert_alpha()
star_positions = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)) for i in range(20)]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_surface.fill('darkgrey')
    x += 0.1
    for pos in star_positions:
        display_surface.blit(star_surf, pos)
    display_surface.blit(player_surf, (x, 150))
    pygame.display.update()

pygame.quit()