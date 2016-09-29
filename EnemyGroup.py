from Enemy import *
import random


class EnemyGroup(object):
    def __init__(self, region):
        self.members = []
        self.populate_enemies(region)

    def populate_enemies(self, region):
        seed = random.randrange(0, 100)
        if region == 'SnowWorld':
            if seed < 65:
                self.members.append(Pengy())
                self.members.append(Pengy())
                self.members.append(Pengy())
            else:
                self.members.append(IceDragon())
                self.members.append(Pengy())
