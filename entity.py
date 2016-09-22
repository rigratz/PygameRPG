import math as m

from pygame import *
from Spritesheet import *


EXPLORING = 0
BATTLE = 1
MENU = 2
LOOP_STATE = ["Exploring", "Battle", "Menu"]


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
        self.image = Surface((32,32))
        self.image.fill(Color("#FF00FF"))
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)

    def update(self, player):
        dist = distance(self, player)

        # Watch out for zeroes
        if dist == 0:
            dist = 0.00000001
        dx = (player.x - self.x) / dist
        dy = (player.y - self.y) / dist

        if dist < 200:
            self.xvel = dx * self.speed
            self.yvel = dy * self.speed

        else:
            self.xvel = 0
            self.yvel = 0
        self.rect.left += self.xvel
        self.x = self.rect.left +16
        self.rect.top += self.yvel
        self.y = self.rect.top +16


class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.x = x + 16
        self.y = y + 16
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
        global state
        state = LOOP_STATE[EXPLORING]

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
                    state = LOOP_STATE[EXPLORING]
        for n in enemies:
            if pygame.sprite.collide_rect(self, n):
                print("Collide with enemy, start battle!")
                enemies.remove(n)

                state = LOOP_STATE[BATTLE]

        return state


class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        textures = SpriteSheet('rpgtextures.png')

        #textureWater = textures.image_at((0, 0, 32, 32))
        #self.image = textureWater
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#0000DD"))
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass


class Walkable(Entity):
    def __init__(self, x, y, type):
        Entity.__init__(self)
        textures = SpriteSheet('rpgtextures.png')

        # textureGrass = textures.image_at((32, 0, 32, 32))
        # self.image = textureGrass
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