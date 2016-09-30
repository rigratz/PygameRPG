from Action import Action
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
        self.selectedAction = None
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
            if e.hp <= 0:
                print(e.name + ' has returned from whence they came.')
                self.enemyGroup.members.remove(e)

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
            player = self.battleQueue.peek()
            optionList = self.get_options_list(self.battleQueue.peek())
            options = len(optionList) - 1

            if self.targeting:
                self.display_targets(optionList, self.highlightedAction, 300, 200, screen)
            else:
                self.display_options(optionList, self.highlightedAction, 300, 200, screen)

            if self.selectionBuffer == 0:
                if controls.select:
                    if self.targeting is False:
                        self.make_selection(player, optionList[self.highlightedAction])
                    else:
                        self.selectedAction.enact(player, optionList[self.highlightedAction])
                        self.targeting = self.magicMenu = self.itemMenu = False
                        self.battleQueue.dequeue()
                    self.selectionBuffer = SELECTION_BUFFER
                    self.highlightedAction = 0
                if controls.cancel:
                    if self.targeting:
                        self.targeting = False
                    elif self.magicMenu:
                        self.magicMenu = False
                    elif self.itemMenu:
                        self.itemMenu = False
                    self.highlightedAction = 0
                    self.selectionBuffer = SELECTION_BUFFER
                if controls.skip:
                    self.battleQueue.front_to_back()
                    self.targeting = self.magicMenu = self.itemMenu = False
                    self.highlightedAction = 0
                    self.selectionBuffer = SELECTION_BUFFER
                if controls.up or controls.left:
                    self.highlightedAction -= 1
                    if self.highlightedAction < 0:
                        self.highlightedAction = options
                    self.selectionBuffer = SELECTION_BUFFER
                if controls.down or controls.right:
                    self.highlightedAction += 1
                    if self.highlightedAction > options:
                        self.highlightedAction = 0
                    self.selectionBuffer = SELECTION_BUFFER

        else:
            self.highlightedAction = -1

        return BATTLE_CONTINUE

    def make_selection(self, actor, selection):
        if self.magicMenu is False and self.itemMenu is False:
            if selection == 'Attack':
                self.selectedAction = actor.actions.attack
                self.targeting = True
            elif selection == 'Special':
                self.magicMenu = True
            elif selection == 'Item':
                self.itemMenu = True
            elif selection == 'Defend':
                actor.actions.defend.enact(actor, None)
                self.battleQueue.dequeue()
        elif self.magicMenu:
            for action in actor.actions.techs:
                if selection == action.name:
                    self.selectedAction = action
                    self.targeting = True
                    break

        elif self.itemMenu:
            for item in self.party.items:
                if selection == item.name:
                    self.selectedAction = item
                    self.targeting = True
                    break


    def get_options_list(self, actor):
        """Method to derive list of selectable options in battle. Seems sort of hacky as currently implemented,
            will probably be done differently in later versions"""
        if self.targeting:
            if self.selectedAction.attack:
                return self.enemyGroup.members
            else:
                return self.players

        if self.magicMenu is False and self.itemMenu is False:
            return ACTIONS

        elif self.magicMenu:
            return self.get_named_list(actor.techs)

        elif self.itemMenu:
            return self.get_named_list(self.party.items)

        else:
            return None

    def get_named_list(self, list):
        """MUST BE USED ON LIST OF OBJECTS CONTAINING .name FIELD"""
        result = []
        for i in list:
            result.append(i.name)
        return result

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
