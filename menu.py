import pygame
import globals

menu = True
size = globals.width, globals.height

while menu == True:
    roboto_font.render_to(screen, (globals.width / 2.0 - 30, globals.height / 2.0 - 10), "Game title goes here!", (255, 255, 255))
    roboto_font.render_to(screen, (globals.width / 2.0 - 30, globals.height / 2.0 + 20), "Press M to start !", (255, 255, 255))
    pygame.display.update()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_t]:
        menu = False
        pygame.display.update()
        break
