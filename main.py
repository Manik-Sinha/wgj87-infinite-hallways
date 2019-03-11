import pygame, math
import globals
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

from bullet import Bullet
from player import Player
from enemy import Enemy

player = Player()
enemy1 = Enemy()

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

    player.update(up, down, left, right, dt, pygame.mouse.get_pos(), mouse_buttons, [enemy1])
    #enemy1.update_turret(player.x, player.y)
    enemy1.update(player.x, player.y, dt, [player])
    left = right = up = down = False

    screen.fill((0, 0, 0))
    player.draw(screen)
    enemy1.draw(screen)
    pygame.display.update()
