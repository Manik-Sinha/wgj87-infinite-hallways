import pygame, math
from bullet import Bullet
class Enemy:
    sqrt2 = math.sqrt(2)
    def __init__(self):
        self.hp = 5
        self.x = self.y = self.w = self.h = 40
        self.player_x = self.x
        self.player_y = self.y
        self.speed = 200
        self.turret_vector = pygame.math.Vector2(0, 0)
        self.turret_length = self.w * 1.5
        self.turret_end = (-1, -1)
        self.bullets = [Bullet() for _ in range(10)]
        self.fired_bullet = False
        self.next_bullet = 0
        self.fire_rate = 0.5
        self.fire_timer = 0
        self.sound_pew = pygame.mixer.Sound("pew.wav")
    def draw(self, surface):
        #Draw body.
        rect = (self.x - self.w / 2.0, self.y - self.h / 2.0, self.w, self.h)
        pygame.draw.rect(surface, (255, 60, 60), rect)
        #Draw turret.
        center = (self.x, self.y)
        end = self.turret_end
        pygame.draw.line(surface, (255, 50, 0), center, end)
        #Draw bullets.
        for bullet in self.bullets:
            if bullet.alive:
                bullet.draw(surface)
    def update(self, player_x, player_y, dt, playerlist):
        self.update_turret(player_x, player_y)
        self.fire(dt, playerlist)
    def fire(self, dt, playerlist):
        if self.fire_timer <= 0:
            bullet = self.bullets[self.next_bullet]
            if not bullet.alive:
                x = self.turret_end[0]
                y = self.turret_end[1]
                vx = self.turret_vector.x
                vy = self.turret_vector.y
                #self.sound_pew.play()
                bullet.fire(x, y, vx, vy)
                self.next_bullet = (self.next_bullet + 1) % len(self.bullets)
                self.fire_timer = self.fire_rate
                self.fired_bullet = True
        for bullet in self.bullets:
            if bullet.alive:
                bullet.update(dt, playerlist)
        if self.fired_bullet:
            self.fire_timer -= dt
    def update_turret(self, player_x, player_y):
        self.player_x = player_x
        self.player_y = player_y
        self.turret_vector.x = self.player_x - self.x
        self.turret_vector.y = self.y - self.player_y
        self.turret_vector.normalize_ip()
        vector = self.turret_vector
        length = self.turret_length
        self.turret_end = (self.x + vector.x * length, self.y - vector.y * length)
    def takedamage(self, amount):
        self.hp -= amount
        print("enemy hp: " + str(self.hp))
    def get_rect(self):
        return (self.x - self.w / 2.0, self.y - self.h / 2.0, self.w, self.h)
