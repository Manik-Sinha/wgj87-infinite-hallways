import pygame, math

pygame.init()

size = width, height = 960, 540

screen = pygame.display.set_mode(size)

class Player:
    sqrt2 = math.sqrt(2)
    def __init__(self):
        self.x = self.y = self.w = self.h = 50
        self.mx = self.x
        self.my = self.y
        self.speed = 200
        self.turret_vector = pygame.math.Vector2(0, 0)
        self.turret_length = self.w * 1.5
    def draw(self, surface):
        #Draw body.
        rect = (self.x, self.y, self.w, self.h)
        pygame.draw.rect(surface, (255, 255, 255), rect)
        #Draw turret.
        cx = self.x + self.w / 2.0
        cy = self.y + self.h / 2.0
        center = (cx, cy)
        vector = self.turret_vector
        length = self.turret_length
        end = (cx + vector.x * length, cy - vector.y * length)
        pygame.draw.line(surface, (255, 0, 0), center, end)
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
    def update_turret(self, mouse):
        self.mx = mouse[0]
        self.my = mouse[1]
        cx = self.x + self.w / 2.0
        cy = self.y + self.h / 2.0
        self.turret_vector.x = self.mx - cx
        self.turret_vector.y = cy - self.my
        self.turret_vector.normalize_ip()

player = Player()

clock = pygame.time.Clock()
dt = 0
clock.tick()

up = False
down = False
left = False
right = False
quit = False

pygame.mouse.set_cursor(*pygame.cursors.broken_x)

while not quit:
    dt = clock.tick() / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True

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

    player.move(up, down, left, right, dt)
    player.update_turret(pygame.mouse.get_pos())

    left = right = up = down = False

    screen.fill((0, 0, 0))
    player.draw(screen)
    pygame.display.update()
