import pygame, math, pygame.freetype
import globals
from bullet import Bullet
from player import Player
from enemy import Enemy
#import menu
size = globals.width, globals.height
pygame.init()
screen = pygame.display.set_mode(size)
pygame.mixer.init()

music = pygame.mixer.Sound("monaco.ogg")
music.play()
#if pygame.mixer.get_init() is None:
#    print("could not initialize sound")
#    sys.exit()

options = globals.options

player = Player()
enemies = [Enemy() for _ in range(3)]
#enemy1 = Enemy()

clock = pygame.time.Clock()
dt = 0
clock.tick()

up = False
down = False
left = False
right = False
quit = False

mouse_buttons = (False, False, False)

pygame.mouse.set_cursor(*pygame.cursors.broken_x)

wall_frame = [1, 1, globals.width, globals.height]

roboto_font = pygame.freetype.Font("fonts/Roboto-Regular.ttf", 20)
while not quit:
    dt = clock.tick() / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_buttons = pygame.mouse.get_pressed()
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_buttons = pygame.mouse.get_pressed()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        quit = True

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        left = True
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        right = True
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        up = True
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        down = True
    if keys[pygame.K_m]:
        pygame.key.set_repeat()
        if options["mute"] == False:
            options["mute"] = True
        elif options["mute"] == True:
            options["mute"] = False
    if options["mute"] == True:
        pygame.mixer.pause()
    elif options["mute"] == False:
        pygame.mixer.unpause()

    if player.alive:
        player.update(up, down, left, right, dt, pygame.mouse.get_pos(), mouse_buttons, enemies)

        for enemy in enemies:
            if enemy.alive == True:
                enemy.update(player.x, player.y, dt, [player])
        left = right = up = down = False

        screen.fill((0, 0, 0))
        player.draw(screen)
        pygame.draw.rect(screen, (255, 255, 255), wall_frame, 50)
        for enemy in enemies:
            if enemy.alive == True:
                enemy.draw(screen)
    else:
        screen.fill((0, 0, 0))
        roboto_font.render_to(screen, (globals.width / 2.0 - 30, globals.height / 2.0 - 10), "Game Over!", (255, 255, 255))
        roboto_font.render_to(screen, (globals.width / 2.0 - 30, globals.height / 2.0 + 20), "Press R to restart !", (255, 255, 255))
        if keys[pygame.K_r]:
            player.hp = player.starthp
            for enemy in enemies:
                enemy.hp = enemy.starthp
                enemy.alive = True
            player.alive = True

    pygame.display.update()
