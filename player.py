import pygame, math
from bullet import Bullet
import globals
class Player:
    sqrt2 = math.sqrt(2)
    def __init__(self):
        self.hp = 10
        self.x = self.y = self.w = self.h = 50
        self.mx = self.x
        self.my = self.y
        self.speed = 200
        self.turret_vector = pygame.math.Vector2(0, 0)
        self.turret_length = self.w * 1.5
        self.turret_end = (-1, -1)
        self.bullets = [Bullet() for _ in range(10)]
        self.next_bullet = 0
        self.fire_rate = 0.5
        self.fired_bullet = False
        self.fire_timer = 0
        self.sound_pew = pygame.mixer.Sound("pew.wav")
    def draw(self, surface):
        #Draw body.
        rect = (self.x - self.w / 2.0, self.y - self.h / 2.0, self.w, self.h)
        pygame.draw.rect(surface, (255, 255, 255), rect)
        #Draw turret.
        center = (self.x, self.y)
        end = self.turret_end
        pygame.draw.line(surface, (255, 0, 0), center, end)
        #Draw bullets.
        for bullet in self.bullets:
            if bullet.alive:
                bullet.draw(surface)
    def update(self, up, down, left, right, dt, mouse_position, mouse_buttons, enemylist):
        self.move(up, down, left, right, dt)
        self.update_turret(mouse_position)
        left_mouse_button = mouse_buttons[0]
        if self.fire_timer <= 0 and left_mouse_button:
            bullet = self.bullets[self.next_bullet]
            if not bullet.alive:
                x = self.turret_end[0]
                y = self.turret_end[1]
                vx = self.turret_vector.x
                vy = self.turret_vector.y
                self.sound_pew.play()
                bullet.fire(x, y, vx, vy)
                self.next_bullet = (self.next_bullet + 1) % len(self.bullets)
                self.fire_timer = self.fire_rate
                self.fired_bullet = True
        for bullet in self.bullets:
            if bullet.alive:
                bullet.update(dt, enemylist)
        if self.fired_bullet:
            self.fire_timer -= dt
    def move(self, up, down, left, right, dt):
        speed = self.speed
        if (left and up) or (left and down) or (right and up) or (right and down):
            speed = self.speed / self.sqrt2
        if left:
            self.x = self.x - speed * dt
        if right:
            self.x = self.x + speed * dt
        if up:
            self.y = self.y - speed * dt
        if down:
            self.y = self.y + speed * dt
    def update_turret(self, mouse_position):
        self.mx = mouse_position[0]
        self.my = mouse_position[1]
        self.turret_vector.x = self.mx - self.x
        self.turret_vector.y = self.y - self.my
        self.turret_vector.normalize_ip()
        vector = self.turret_vector
        length = self.turret_length
        self.turret_end = (self.x + vector.x * length, self.y - vector.y * length)
    def takedamage(self, amount):
        self.hp -= amount
        print("player hp: " + str(self.hp))
    def get_rect(self):
        return (self.x - self.w / 2.0, self.y - self.h / 2.0, self.w, self.h)
