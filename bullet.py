import pygame
import globals
width, height = globals.width, globals.height
class Bullet:
    def __init__(self):
        self.x = -1
        self.y = -1
        self.s = 5
        self.speed = 500
        self.vx = -1
        self.vy = -1
        self.alive = False
    def update(self, dt, targetlist):
        if self.alive:
            self.x = self.x + self.vx * self.speed * dt
            self.y = self.y - self.vy * self.speed * dt
            if self.x < 0 or self.x > width or self.y < 0 or self.y > height:
                self.kill()
            rect = (self.x - self.s / 2.0, self.y - self.s / 2.0, self.s, self.s)
            for target in targetlist:
                if target.alive == True:
                    targetrect = pygame.Rect(target.get_rect())
                    if targetrect.colliderect(rect):
                        target.takedamage(1)
                        self.kill()
                        return
    def draw(self, surface):
        rect = (self.x - self.s / 2.0, self.y - self.s / 2.0, self.s, self.s)
        pygame.draw.rect(surface, (255, 0, 0), rect)
    def fire(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.alive = True
    def kill(self):
        self.alive = False
