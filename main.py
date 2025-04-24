import pygame
from os.path import join
import random

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(join('assets', 'images', 'icon.png'))
running = True
clock = pygame.time.Clock()

player_surf = pygame.image.load(join('assets', 'images', 'player.png')).convert_alpha()
player_rect = player_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
player_direction = pygame.math.Vector2()
player_speed = 300

meteor_surf = pygame.image.load(join('assets', 'images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

laser_surf = pygame.image.load(join('assets', 'images', 'laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft = (20, WINDOW_HEIGHT - 20))

star_surf = pygame.image.load(join('assets', 'images', 'star.png')).convert_alpha()
star_positions = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)) for i in range(20)]

go_left = False
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    player_direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
    player_direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
    player_direction = player_direction.normalize() if player_direction else player_direction 
    # handles diagonal movement speed boost bug. The line above is basically:

    # if player_direction: (isn't (0, 0))
    #     player_direction = player_direction.normalize()
    # else:
    #     player_direction = player_direction

    if pygame.key.get_just_pressed()[pygame.K_SPACE]:
        print("fire laser")

    player_rect.center += player_direction * player_speed * dt
    display_surface.fill('darkgrey')
    for pos in star_positions:
        display_surface.blit(star_surf, pos)

    display_surface.blit(meteor_surf, meteor_rect)
    display_surface.blit(laser_surf, laser_rect)
    display_surface.blit(player_surf, player_rect)

    pygame.display.update()

pygame.quit()