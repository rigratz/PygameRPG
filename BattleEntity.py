import random


class BattleEntity(object):
    """Representation of an Entity that can participate in battles"""

    def __init__(self, **kwargs):
        self.name = ''
        self.level = 1
        self.xp = 0
        self.xpToNext = 100
        self.xpGiven = 0
        self.job = ""
        self.atb = 0
        self.ready = False
        self.hp = 50
        self.mp = 25
        self.str = 10
        self.mag = 10
        self.dfn = 10
        self.mgd = 10
        self.spd = 10
        self.techs = []
        self.friendly = False

        for prop, value in kwargs.items():
            if hasattr(self, prop):
                setattr(self, prop, value)
            else:
                pass # throw some type of exception

        self.set_atb_start()

    def set_atb_start(self):
        """Used to randomly assign ATB value at start of battle"""
        self.atb = random.randrange(0, 100)

    def atb_charge(self, increment):
        """Used to increment entity's ATB gauge"""
        if self.atb >= 100:
            self.atb = 100
        else:
            self.atb += self.spd * (increment / 1000)

    def reset_atb(self):
        """Used to reset entity's ATB gauge to zero after taking action"""
        self.atb = 0
        self.ready = False

    def take_action(self, action):
        """Does something. Not implemented yet"""
        action.activate()
        self.reset_atb()

    def level_up(self):
        """Adjust's entity's stats upon increasing in experience level"""
        self.level += 1
        self.xpToNext += (self.level * 100)

