import pygame, math

pygame.init()

size = width, height = 960, 540

screen = pygame.display.set_mode(size)

pygame.mixer.init()

music = pygame.mixer.Sound("monaco.ogg")
music.play()
#if pygame.mixer.get_init() is None:
#    print("could not initialize sound")
#    sys.exit()

options = {
    'mute': False
}

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
            rect = pygame.Rect(self.x - self.s / 2.0, self.y - self.s / 2.0, self.s, self.s)
            for target in targetlist:
                targetrect = pygame.Rect(target.get_rect())
                if rect.colliderect(targetrect):
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
