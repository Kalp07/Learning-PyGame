import pygame
from os.path import join
from random import randint, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('assets', 'images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 300

        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True


    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            laser_sound.play()
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 500)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

def collisions():
    global running, score
    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, False)
    if collision_sprites:
        damage_sound.play()
        running = False
    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            explosion_sound.play()
            laser.kill()
            # score += len(collided_sprites)  # Removed score increment for destroying meteors

# general setup
pygame.init()
pygame.mixer.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(join('assets', 'images', 'icon.png'))
running = True
clock = pygame.time.Clock()

# score setup
score = 0
font = pygame.font.Font(join('assets', 'images', 'Oxanium-Bold.ttf'), 48)

# Timer setup
survival_start_time = 0

def draw_score(surface, score):
    score_surf = font.render(f"Time Survived: {score:.2f}s", True, (255,255,255))
    surface.blit(score_surf, (30, 20))

# import
star_surf = pygame.image.load(join('assets', 'images', 'star.png')).convert_alpha()
meteor_surf = pygame.image.load(join('assets', 'images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('assets', 'images', 'laser.png')).convert_alpha()

# audio
laser_sound = pygame.mixer.Sound(join('assets', 'audio', 'laser.wav'))
explosion_sound = pygame.mixer.Sound(join('assets', 'audio', 'explosion.wav'))
damage_sound = pygame.mixer.Sound(join('assets', 'audio', 'damage.ogg'))
pygame.mixer.music.load(join('assets', 'audio', 'game_music.wav'))
pygame.mixer.music.play(-1)

# sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
for i in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)

# custom events - meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

# Game loop
while True:
    running = True
    # reset game state
    all_sprites.empty()
    meteor_sprites.empty()
    laser_sprites.empty()
    for i in range(20):
        Star(all_sprites, star_surf)
    player = Player(all_sprites)
    score = 0
    survival_start_time = pygame.time.get_ticks()

    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == meteor_event:
                x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
                Meteor(meteor_surf, (x, y), (all_sprites, meteor_sprites))

        # update
        all_sprites.update(dt)
        collisions()

        # update score as time survived
        score = (pygame.time.get_ticks() - survival_start_time) / 1000

        # draw the game
        display_surface.fill('darkgrey')
        all_sprites.draw(display_surface)
        draw_score(display_surface, score)
        pygame.display.update()

    # Game Over screen
    display_surface.fill('black')
    game_over_surf = font.render("Game Over! Press R to Restart or Q to Quit", True, (255,0,0))
    display_surface.blit(game_over_surf, (WINDOW_WIDTH//2 - game_over_surf.get_width()//2, WINDOW_HEIGHT//2 - game_over_surf.get_height()//2))
    # Display final survival time below the game over message
    final_score_surf = font.render(f"Time Survived: {score:.2f}s", True, (255,255,255))
    display_surface.blit(final_score_surf, (WINDOW_WIDTH//2 - final_score_surf.get_width()//2, WINDOW_HEIGHT//2 + game_over_surf.get_height()))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False  # restart
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()