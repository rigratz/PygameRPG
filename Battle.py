import pygame
from pygame import *


class Battle(object):
    def __init__(self, players, enemies, background):
        self.players = players
        self.enemies = enemies
        self.bg = background
        self.battleTimer = pygame.time.Clock()
        self.battleQueue = BattleQueue()

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
        for p in self.players:
            p.atb_charge(self.battleTimer.get_time())
            if p.ready is False and p.get_atb_charge() == 100:
                print("Enqueueing")
                self.battleQueue.enqueue(p)
                p.ready = True

            # Display info on screen
            txt = pygame.font.Font(None, 36)
            string = p.get_name() + " - " + str(p.get_atb_charge())
            render = txt.render(string[0:12], 0, (255, 255, 255))
            screen.blit(render, (textX, textY))
            textY += 40

        textY = 200
        txt = pygame.font.Font(None, 36)
        string = "Battle Queue:"
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
            print(self.battleQueue.peek().get_name())
            if self.battleQueue.peek().ready:
                if controls.select:
                    player = self.battleQueue.dequeue()
                    player.reset_atb()
                if controls.skip:
                    self.battleQueue.front_to_back()

            # if p.ready and controls.select:
            #     p.reset_atb()
            #     p.ready = False



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
