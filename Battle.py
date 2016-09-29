import pygame
from pygame import *
import random

# Constants for identifying default battle actions
ATTACK = 0
SPECIAL = 1
ITEM = 2
DEFEND = 3
ACTIONS = ['Attack', 'Special', 'Item', 'Defend']

# Constants for returning state of Battle
BATTLE_OVER = 0
BATTLE_CONTINUE = 1

SELECTION_BUFFER = 150


class Battle(object):
    def __init__(self, party, enemyGroup, background):
        self.party = party
        self.players = party.members
        self.enemyGroup = enemyGroup
        self.bg = background
        self.battleTimer = pygame.time.Clock()
        self.battleQueue = BattleQueue()
        self.highlightedAction = -1
        self.highlightedEnemy = -1
        self.magicMenu = False
        self.itemMenu = False
        self.targeting = False
        self.selectionBuffer = 0

        # Each character's starting ATB value is random
        for p in self.players:
            p.atb = random.randrange(0, 100)

    def progress(self, controls, screen):
        """Main logic controlling the flow of the Battle loop"""

        # Check if all enemies have been defeated
        if len(self.enemyGroup.members) <= 0:
            print('You win! Collect XP and such')
            self.battle_results()
            return BATTLE_OVER

        self.battleTimer.tick(60)
        textX = 10
        textY = 10
        atbIncrement = self.battleTimer.get_time()

        # Timer handling for input buffering
        if self.selectionBuffer > 0:
            self.selectionBuffer -= atbIncrement
            if self.selectionBuffer < 0:
                self.selectionBuffer = 0

        for p in self.players:
            # Adjust player character's ATB gauge
            p.atb_charge(atbIncrement)
            if p.ready is False and p.atb == 100:
                # Place player character in Battle Queue if ready for action
                self.battleQueue.enqueue(p)
                if self.highlightedAction == -1:
                    self.highlightedAction = ATTACK
                p.ready = True

            # Display Character info on screen
            self.display_single_line((p.name + ' - ' + str(p.atb)), textX, textY, screen)
            textY += 40

        textX = 300
        textY = 10

        for e in self.enemyGroup.members:
            # Adjust enemy ATB gauge
            e.atb_charge(atbIncrement)
            if e.atb == 100:
                e.ready = True
                e.battle_script()
                # Wait for 4 seconds (attack animation)
                # time.sleep(4)

            # Display Enemy info on screen
            self.display_single_line((e.name + ' - ' + str(e.atb)), textX, textY, screen)
            textY += 40

        textX = 10
        textY = 200
        self.display_single_line('Battle Queue:', textX, textY, screen)

        textY += 40

        # Display all characters readied in Battle Queue
        for p in self.battleQueue.queue:
            self.display_single_line(p.name, textX, textY, screen)
            textY += 40

        # Display and navigate available Action options
        if self.battleQueue.get_size() > 0:
            availableTechs = self.battleQueue.peek().techs
            availableItems = self.party.items
            if self.magicMenu is False and self.itemMenu is False and self.targeting is False:
                # Display default Battle options
                self.display_options(ACTIONS, self.highlightedAction, 300, 200, screen)

                if self.selectionBuffer == 0:
                    if controls.select:
                        if self.highlightedAction == ATTACK:
                            # player = self.battleQueue.dequeue()
                            # print(player.name + ' attacks!')
                            self.targeting = True
                            self.highlightedAction = 0
                            # player.reset_atb()
                        elif self.highlightedAction == SPECIAL:
                            self.magicMenu = True
                            self.highlightedAction = 0
                        elif self.highlightedAction == ITEM:
                            self.itemMenu = True
                            self.highlightedAction = 0
                        elif self.highlightedAction == DEFEND:
                            player = self.battleQueue.dequeue()
                            print(player.name + ' defends!')
                            self.highlightedAction = 0
                            player.reset_atb()
                        self.selectionBuffer = SELECTION_BUFFER

                    if controls.skip:
                        self.battleQueue.front_to_back()
                        self.highlightedAction = 0
                        self.selectionBuffer = SELECTION_BUFFER
                    if controls.up:
                        self.highlightedAction -= 1
                        if self.highlightedAction < ATTACK:
                            self.highlightedAction = DEFEND
                        self.selectionBuffer = SELECTION_BUFFER
                    if controls.down:
                        self.highlightedAction += 1
                        if self.highlightedAction > DEFEND:
                            self.highlightedAction = ATTACK
                        self.selectionBuffer = SELECTION_BUFFER
            elif self.magicMenu is False and self.itemMenu is False and self.targeting is True:
                self.display_targets(self.enemyGroup.members, self.highlightedAction,300, 200, screen)

                if self.selectionBuffer == 0:
                    if controls.select:
                        target = self.enemyGroup.members[self.highlightedAction]
                        player = self.battleQueue.dequeue()
                        print(target.name + ' HP: ' + str(target.hp))
                        print(player.name + ' attacks ' + target.name)
                        self.calculate_damage(player, target, 'Attack')
                        print(target.name + ' HP: ' + str(target.hp))
                        if target.hp <= 0:
                            print(target.name + ' defeated!')
                            self.enemyGroup.members.remove(target)
                        self.highlightedAction = 0
                        self.targeting = False
                        player.reset_atb()
                        self.selectionBuffer = SELECTION_BUFFER

                    if controls.cancel:
                        self.targeting = False
                        self.selectionBuffer = SELECTION_BUFFER

                    if controls.skip:
                        if self.battleQueue.size > 1:
                            self.battleQueue.front_to_back()
                            self.highlightedAction = 0
                            self.selectionBuffer = SELECTION_BUFFER
                    if controls.up:
                        self.highlightedAction -= 1
                        if self.highlightedAction < 0:
                            self.highlightedAction = len(self.enemyGroup.members) - 1
                        self.selectionBuffer = SELECTION_BUFFER
                    if controls.down:
                        self.highlightedAction += 1
                        if self.highlightedAction > len(self.enemyGroup.members) - 1:
                            self.highlightedAction = 0
                        self.selectionBuffer = SELECTION_BUFFER
            elif self.magicMenu and not self.targeting:
                # Display Magic options
                self.display_options(self.battleQueue.peek().techs, self.highlightedAction, 300, 200, screen)

                if self.selectionBuffer == 0:
                    if controls.select:
                        # player = self.battleQueue.dequeue()
                        # print(player.name + ' uses ' + availableTechs[self.highlightedAction] + " magic!")
                        # self.magicMenu = False
                        self.targeting = True
                        self.highlightedAction = 0
                        self.selectionBuffer = SELECTION_BUFFER
                        # player.reset_atb()
                    if controls.cancel:
                        self.magicMenu = False
                        self.selectionBuffer = SELECTION_BUFFER
                    if controls.up:
                        self.highlightedAction -= 1
                        if self.highlightedAction < 0:
                            self.highlightedAction = len(availableTechs) - 1
                        self.selectionBuffer = SELECTION_BUFFER
                    if controls.down:
                        self.highlightedAction += 1
                        if self.highlightedAction > len(availableTechs) - 1:
                            self.highlightedAction = 0
                        self.selectionBuffer = SELECTION_BUFFER
            elif self.itemMenu and not self.targeting:
                # Display available Item options
                self.display_options(self.party.items, self.highlightedAction, 300, 200, screen)

                if self.selectionBuffer == 0:
                    if controls.select:
                        player = self.battleQueue.dequeue()
                        print(player.name + ' uses ' + availableItems[self.highlightedAction] + " item!")
                        self.itemMenu = False
                        self.selectionBuffer = SELECTION_BUFFER
                        player.reset_atb()
                    if controls.cancel:
                        self.itemMenu = False
                        self.selectionBuffer = SELECTION_BUFFER
                    if controls.up:
                        self.highlightedAction -= 1
                        if self.highlightedAction < 0:
                            self.highlightedAction = len(availableItems) - 1
                        self.selectionBuffer = SELECTION_BUFFER
                    if controls.down:
                        self.highlightedAction += 1
                        if self.highlightedAction > len(availableItems) - 1:
                            self.highlightedAction = 0
                        self.selectionBuffer = SELECTION_BUFFER
            elif self.magicMenu and self.targeting:
                self.display_targets(self.enemyGroup.members, self.highlightedAction, 300, 200, screen)
                pass
            elif self.itemMenu and self.targeting:
                pass
        else:
            self.highlightedAction = -1
        return BATTLE_CONTINUE

    @staticmethod
    def display_single_line(line, x, y, screen):
        """Displays a single line of text on Battle screen"""
        txt = pygame.font.Font(None, 36)
        render = txt.render(line[0:13], 0, (255, 255, 255))
        screen.blit(render, (x, y))

    @staticmethod
    def display_options(options, highlight, startX, startY, screen):
        """Displays list of relevant options"""
        x = startX
        y = startY
        for o in options:
            txt = pygame.font.Font(None, 36)
            if o == options[highlight]:
                render = txt.render(o[0:13], 0, (255, 0, 0))
            else:
                render = txt.render(o[0:13], 0, (255, 255, 255))
            screen.blit(render, (x, y))
            y += 40

    @staticmethod
    def display_targets(targets, highlight, startX, startY, screen):
        """Displays list of targets for currently selected action"""
        x = startX
        y = startY
        for t in targets:
            txt = pygame.font.Font(None, 36)
            if t is targets[highlight]:
                render = txt.render(t.name[0:13], 0, (255, 0, 0))
            else:
                render = txt.render(t.name[0:13], 0, (255, 255, 255))
            screen.blit(render, (x, y))
            y += 40

    def navigate_targets(self, caster, targets, action):
        pass

    def calculate_damage(self, caster, target, action):
        """Determines the result of a caster's action on a target"""
        if action == 'Attack':
            target.hp -= caster.str

    def battle_results(self):
        """Calculate XP gain, level increase, item drops, etc"""
        pass


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
            self.size -= 1
        return data

    def front_to_back(self):
        if self.queue[0] is not None:
            temp = self.dequeue()
            self.enqueue(temp)
