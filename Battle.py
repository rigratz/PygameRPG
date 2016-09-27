import pygame
from pygame import *
import random
import time

ATTACK = 0
MAGIC = 1
ITEM = 2
DEFEND = 3
ACTIONS = ['Attack', 'Magic', 'Item', 'Defend']


class Battle(object):
    def __init__(self, players, enemyGroup, background):
        self.players = players
        self.enemyGroup = enemyGroup
        self.bg = background
        self.battleTimer = pygame.time.Clock()
        self.battleQueue = BattleQueue()
        self.highlightedAction = -1
        self.highlightedEnemy = -1

        # Each character's starting ATB value is random
        for p in self.players:
            p.atb = random.randrange(0, 100)

    def get_players(self):
        return self.players

    def get_enemies(self):
        return self.enemies

    def get_battle_queue(self):
        return self.battleQueue

    def progress(self, controls, screen):
        self.battleTimer.tick(60)
        textX = 10
        textY = 10
        atbIncrement = self.battleTimer.get_time()
        for p in self.players:
            p.atb_charge(atbIncrement)
            if p.ready is False and p.get_atb_charge() == 100:
                print('Enqueueing ' + p.name)
                self.battleQueue.enqueue(p)
                if self.highlightedAction == -1:
                    self.highlightedAction = ATTACK
                p.ready = True

            # Display Party info on screen
            txt = pygame.font.Font(None, 36)
            string = p.get_name() + ' - ' + str(p.get_atb_charge())
            render = txt.render(string[0:12], 0, (255, 255, 255))
            screen.blit(render, (textX, textY))
            textY += 40

        textX = 300
        textY = 10
        for e in self.enemyGroup.members:
            e.atb_charge(atbIncrement)
            if e.ready:
                e.battle_script()
                # Wait for 4 seconds (attack animation)
                # time.sleep(4)


            # Display Enemy info on screen
            txt = pygame.font.Font(None, 36)
            string = e.name + " - " + str(e.atb)
            render = txt.render(string[0:16], 0, (255, 255, 255))
            screen.blit(render, (textX, textY))
            textY += 40

        textX = 10
        textY = 200
        txt = pygame.font.Font(None, 36)
        string = 'Battle Queue:'
        render = txt.render(string[0:13], 0, (255, 255, 255))
        screen.blit(render, (textX, textY))
        textY += 40
        for p in self.battleQueue.queue:
            txt = pygame.font.Font(None, 36)
            string = p.get_name()
            render = txt.render(string[0:13], 0, (255, 255, 255))

            screen.blit(render, (textX, textY))
            textY += 40

        if self.battleQueue.get_size() > 0:
            textX = 300
            textY = 200
            for a in ACTIONS:
                txt = pygame.font.Font(None, 36)
                if a == ACTIONS[self.highlightedAction]:
                    render = txt.render(a[0:13], 0, (255, 0, 0))
                else:
                    render = txt.render(a[0:13], 0, (255, 255, 255))
                screen.blit(render, (textX, textY))
                textY += 40

            if self.battleQueue.peek().ready:
                if controls.select and self.highlightedAction == ATTACK:
                    player = self.battleQueue.dequeue()
                    print(player.name + ' attacks!')
                    player.reset_atb()
                if controls.skip:
                    self.battleQueue.front_to_back()
                if controls.up:
                    self.highlightedAction -= 1
                    if self.highlightedAction < ATTACK:
                        self.highlightedAction = DEFEND
                if controls.down:
                    self.highlightedAction += 1
                    if self.highlightedAction > DEFEND:
                        self.highlightedAction = ATTACK


class BattleQueue(object):
    def __init__(self):
        self.queue = []
        self.size = 0

    def get_size(self):
        return self.size

    def peek(self):
        if self.queue[0] is not None:
            return self.queue[0]
        else:
            return None

    def enqueue(self, data):
        self.queue.append(data)
        self.size += 1

    def dequeue(self):
        data = None
        if self.queue[0] is not None:
            data = self.queue[0]
            self.queue.remove(data)
            self.size += -1
        return data

    def front_to_back(self):
        if self.queue[0] is not None:
            temp = self.dequeue()
            self.enqueue(temp)
