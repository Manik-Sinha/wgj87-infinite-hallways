import pygame
import globals

menu = True
size = globals.width, globals.height

def menu():
    roboto_font.render_to(screen, (globals.width / 2.0 - 30, globals.height / 2.0 - 10), "Game title goes here!", (255, 255, 255))
    roboto_font.render_to(screen, (globals.width / 2.0 - 30, globals.height / 2.0 + 20), "Press M to start !", (255, 255, 255))
    while menu == True:
        mkeys = pygame.key.get_pressed()
        if mkeys[pygame.K_m]:
            menu == False
        pass
        