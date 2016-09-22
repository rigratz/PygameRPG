from Battle import *
from Camera import *
from Controls import *
from Entity import *
from Levels import *
from Party import *
import pygame
from pygame import *

EXPLORING = 0
BATTLE = 1
MENU = 2
DEFAULT = 3


class GameEngine(object):
    def __init__(self):
        self.screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
        self.timer = pygame.time.Clock()
        self.control = Controls()
        self.platforms = []
        self.enemies = []
        self.entities = pygame.sprite.Group()
        self.player = Player(32, 32)
        self.levels = Levels()
        self.state = EXPLORING
        self.party = Party()
        level = self.levels.get_level(0)
        total_level_width = len(level[0])*32
        total_level_height = len(level)*32
        self.camera = Camera(complex_camera, total_level_width, total_level_height)

    def start(self):
        self.state = EXPLORING
        self.party.newMember(Character("Riley"))
        self.party.newMember(Character("Darren"))
        self.party.newMember(Character("John"))
        self.party.newMember(Character("!tits"))
        self.state = BATTLE
        bat = Battle(self.party.getParty(), 3, 4)
        while 1:
            self.timer.tick(60)
            self.control.handle_controls(self.state)
            if self.state == EXPLORING:
                self.explore_loop()
            elif self.state == BATTLE:
                self.battle_loop(bat)
            elif self.state == MENU:
                self.menu_loop()

    def explore_loop(self):
        bg = Surface((32,32))
        bg.convert()
        bg.fill(Color("#000000"))
        # draw background
        for y in range(32):
            for x in range(32):
                self.screen.blit(bg, (x * 32, y * 32))

        self.camera.update(self.player)

        # update player, draw everything else
        self.player.update(self.control, self.platforms, self.enemies)
        for e in self.enemies:
            e.update(self.player)
        for e in self.entities:
            self.screen.blit(e.image, self.camera.apply(e))

        pygame.display.update()

    def battle_loop(self, battle):
        #print(self.party.getMember(0).getName())
        bg = Surface((32,32))
        bg.convert()
        bg.fill(Color("#000000"))
        self.screen.fill((0, 0, 0))
        battle.progress(self.control, self.screen)

        pygame.display.update()

    def menu_loop(self):
        pass
