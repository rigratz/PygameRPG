from BattleEntity import BattleEntity
import random


class Enemy(BattleEntity):
    """Class used to represent enemy creatures who will be battled over the course of the game. Enemies will
        extend this class to enforce their specific rules, abilities, and AI logic"""
    def __init__(self, **kwargs):
        super(Enemy, self).__init__(**kwargs)

    def battle_script(self):
        """Method to be overridden by extending class. Contains logic determining how enemies act during battle"""
        self.reset_atb()


class Pengy(Enemy):
    """A penguin-like enemy found in the Snow World"""
    def __init__(self):
        self.charged = False
        abilities = ['Peck', 'Snowball', 'Charge']
        super(Pengy, self).__init__(name='Pengy', hp=10, str=5, spd=7, techs=abilities, resistance=['Ice'],
                                    weakness=['Fire'])

    def battle_script(self):
        seed = random.randrange(0,100)
        damage = self.str
        if self.charged:
            damage *= 2
            self.charged = False

        if 0 <= seed < 25:
            print('Pengy uses ' + self.techs[0])
        elif 25 <= seed < 65:
            print('Pengy uses ' + self.techs[1])
        else:
            print('Pengy uses ' + self.techs[2])
            self.charged = True

        super(Pengy, self).battle_script()


class IceDragon(Enemy):
    """A dragon with ice abilities found in the Snow World"""
    def __init__(self):
        super(IceDragon, self).__init__(name='Ice Dragon', hp=30, str=20, spd=3)

    def battle_script(self):
        if self.hp <= 10:
            print("Desperation attack from Ice Dragon!")
        else:
            print("Ice Dragon whips tail at you!")
        super(IceDragon, self).battle_script()