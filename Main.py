import math as m
import pygame
from pygame import *

EXPLORING = 0
BATTLE = 1
MENU = 2
LOOP_STATE = ["Exploring", "Battle", "Menu"]

WIN_WIDTH = 800
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30

class Controls(object):
    def __init__(self):
        self.up = self.down = self.left = self.right = self.running = False

def main():
    global cameraX, cameraY
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    pygame.display.set_caption("Pygame RPG Prototype")
    timer = pygame.time.Clock()
    control = Controls()

    bg = Surface((32,32))
    bg.convert()
    bg.fill(Color("#000000"))
    entities = pygame.sprite.Group()
    player = Player(32, 32)
    platforms = []
    enemies = []

    x = y = 0
    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPP",
        "P             P         P",
        "PPPP     PPPPPP         P",
        "P                       P",
        "PPP   PPPPPPPPPPPPPPPPPPP",
        "P                       P",
        "P                X      P",
        "P                       P",
        "P    PPPPPPPP     PPPPPPP",
        "P                       P",
        "P          PPPPPPP      P",
        "P                 PPPPPPP",
        "P                       P",
        "P         PPPPPPP       P",
        "P                       P",
        "P          PPPPPP       P",
        "P                       P",
        "P    PPPPPPPPPP         P",
        "P                       P",
        "P       PPP    PPP      P",
        "P         P    P        P",
        "P         P    P        P",
        "P         P    P        P",
        "P         P    P        P",
        "PPPPPPPPPPPPPPEPPPPPPPPPP",]
    # build the level
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
            if col == "E":
                e = ExitBlock(x, y)
                platforms.append(e)
                entities.add(e)
            if col == "X":
                n = Enemy(x, y, 0)
                # platforms.append(e)
                enemies.append(n)
                entities.add(n)
            x += 32
        y += 32
        x = 0

    total_level_width  = len(level[0])*32
    total_level_height = len(level)*32
    camera = Camera(complex_camera, total_level_width, total_level_height)
    entities.add(player)

    while 1:
        timer.tick(60)

        handleControls(control)
        # draw background
        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))

        camera.update(player)

        # update player, draw everything else
        player.update(control, platforms, enemies)
        for e in enemies:
            e.update(player)
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()

def handleControls(control):
    for e in pygame.event.get():
        if e.type == QUIT: raise SystemExit
        if e.type == KEYDOWN and e.key == K_ESCAPE:
            raise SystemExit
        if e.type == KEYDOWN and e.key == K_UP:
            control.up = True
        if e.type == KEYDOWN and e.key == K_DOWN:
            control.down = True
        if e.type == KEYDOWN and e.key == K_LEFT:
            control.left = True
        if e.type == KEYDOWN and e.key == K_RIGHT:
            control.right = True
        if e.type == KEYDOWN and e.key == K_SPACE:
            control.running = True

        if e.type == KEYUP and e.key == K_UP:
            control.up = False
        if e.type == KEYUP and e.key == K_DOWN:
            control.down = False
        if e.type == KEYUP and e.key == K_RIGHT:
            control.right = False
        if e.type == KEYUP and e.key == K_LEFT:
            control.left = False

def exploreLoop():
    pass
def battleLoop():
    pass
def menuLoop():
    pass
class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return Rect(l, t, w, h)

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Enemy(Entity):
    def __init__(self, x, y, sprite):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.x = x + 16
        self.y = y + 16
        self.speed = 2
        #self.onGround = False
        self.image = Surface((32,32))
        self.image.fill(Color("#FF00FF"))
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)

    def update(self, player):
        dist = distance(self, player)

        #Watch out for zeroes
        dx = (player.x - self.x) / dist
        dy = (player.y - self.y) / dist

        if dist < 200:
            print("enemy tracking!")
            self.xvel = dx * self.speed
            self.yvel = dy * self.speed

        else:
            self.xvel = 0
            self.yvel = 0
        self.rect.left += self.xvel
        self.x = self.rect.left +16
        self.rect.top += self.yvel
        self.y = self.rect.top +16
        print(self.xvel)
        print(self.yvel)


class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.x = x + 16
        self.y = y + 16
        #self.onGround = False
        self.image = Surface((32,32))
        self.image.fill(Color("#FF0000"))
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)

    def update(self, control, platforms, enemies):
        if control.up:
            self.yvel = -2
        if control.down:
            self.yvel = 2
        if control.running:
            self.xvel = 12
        if control.left:
            self.xvel = -2
        if control.right:
            self.xvel = 2
        if not(control.left or control.right):
            self.xvel = 0
        if not(control.up or control.down):
            self.yvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        self.x = self.rect.left +16
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms, enemies)
        # increment in y direction
        self.rect.top += self.yvel
        self.y = self.rect.top + 16
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.yvel, platforms, enemies)

    def collide(self, xvel, yvel, platforms, enemies):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    pygame.event.post(pygame.event.Event(QUIT))
                if xvel > 0:
                    self.rect.right = p.rect.left
                    print ("collide right")
                if xvel < 0:
                    self.rect.left = p.rect.right
                    print ("collide left")
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    print ("collide top")
                    self.yvel = 0
        for n in enemies:
            if pygame.sprite.collide_rect(self, n):
                print("Collide with enemy, start battle!")

class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#0000DD"))
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass

class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image.fill(Color("#00FF00"))

def distance(first, second):

    dist = (second.x-first.x) ** 2 + (second.y-first.y) ** 2
    return m.sqrt(dist)

if __name__ == "__main__":
    main()