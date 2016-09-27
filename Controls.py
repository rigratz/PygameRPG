import pygame
from pygame import *

EXPLORING = 0
BATTLE = 1
MENU = 2
DEFAULT = 3


class Controls(object):
    def __init__(self):
        self.up = self.down = self.left = self.right = self.running = self.select = self.skip = False

    def handle_controls(self, theState):
        if theState == EXPLORING:
            for e in pygame.event.get():
                if e.type == QUIT: raise SystemExit
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    raise SystemExit
                if e.type == KEYDOWN and e.key == K_UP:
                    self.up = True
                if e.type == KEYDOWN and e.key == K_DOWN:
                    self.down = True
                if e.type == KEYDOWN and e.key == K_LEFT:
                    self.left = True
                if e.type == KEYDOWN and e.key == K_RIGHT:
                    self.right = True

                if e.type == KEYUP and e.key == K_UP:
                    self.up = False
                if e.type == KEYUP and e.key == K_DOWN:
                    self.down = False
                if e.type == KEYUP and e.key == K_RIGHT:
                    self.right = False
                if e.type == KEYUP and e.key == K_LEFT:
                    self.left = False
        elif theState == BATTLE:
            for e in pygame.event.get():
                if e.type == QUIT: raise SystemExit
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    raise SystemExit
                if e.type == KEYDOWN and e.key == K_UP:
                    self.up = True
                if e.type == KEYDOWN and e.key == K_DOWN:
                    self.down = True
                if e.type == KEYDOWN and e.key == K_SPACE:
                    self.select = True
                if e.type == KEYDOWN and e.key == K_s:
                    self.skip = True

                if e.type == KEYUP and e.key == K_UP:
                    self.up = False
                if e.type == KEYUP and e.key == K_DOWN:
                    self.down = False
                if e.type == KEYUP and e.key == K_s:
                    self.skip = False
                if e.type == KEYUP and e.key == K_SPACE:
                    self.select = False
        elif theState == MENU:
            pass

    def initialize(self):
        self.up = self.down = self.left = self.right = self.select = self.skip = False
