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


class Enemy(object):
    def __init__(self, name, **kwargs):
        self.name = name
        self.hp = 10
        self.atk = 10
        self.dfn = 10
        self.spd = 10
        atbSeed = random.randrange(0, 100)
        self.atb = atbSeed
        self.ready = False

        for prop, value in kwargs.items():
            if hasattr(self, prop):
                setattr(self, prop, value)
            else:
                pass # throw some type of exception

    def atb_charge(self, increment):
        """Charges enemy's ATB meter based on speed"""
        if self.atb >= 100:
            self.atb = 100
            self.ready = True
        else:
            self.atb += self.spd * (increment / 1000)

    def battle_script(self):
        """Enemy battle script to be overridden by subclasses"""
        print('No longer ready, reset ATB')
        self.atb = 0
        self.ready = False


class Pengy(Enemy):
    def __init__(self):
        super(Pengy, self).__init__('Pengy', atk=5, spd=7)

    def battle_script(self):
        print('Pengy strikes!')
        super(Pengy, self).battle_script()


class IceDragon(Enemy):
    def __init__(self):
        super(IceDragon, self).__init__('Ice Dragon', hp=30, atk=50, spd=3)

    def battle_script(self):
        print('Ice Dragon strikes!')
        super(IceDragon, self).battle_script()
