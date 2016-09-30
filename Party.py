from BattleEntity import BattleEntity
from Item import *

class Party(object):
    """Representation of a party of Characters"""
    
    def __init__(self):
        self.members = []
        self.items = [Potion(), PhoenixDown()]

    def __iter__(self):
        self._i = 0
        return self

    def add_member(self, member):
        """Add character to party."""
        self.members.append(member)

    def get_member(self, index):
        """Get party member by position."""
        return self.members[index]

    def get_party(self):
        """Return reference to party property."""
        return self.members

    def next(self):
        if self._i < len(self.members):
            self._i += 1
            return self.members[self._i - 1]
        else:
            raise StopIteration()


class Knight(BattleEntity):
    """Class representing one of the game's main characters. Specifically, this is for the character who follows
        the typical Knight trope"""
    def __init__(self):
        knightTechs = [Cover()]
        super(Knight, self).__init__(name='Darren', job='Knight', hp=100, mp=20, str=15, mag=5, dfn=15, mgd=8,
                                     spd=8, techs=knightTechs, friendly=True)


class Rogue(BattleEntity):
    """Class representing one of the game's main characters. Specifically, this is for the character who follows
        the typical Rogue trope"""
    def __init__(self):
        rogueTechs = [Steal()]
        super(Rogue, self).__init__(name='Riley', job='Rogue', hp=75, mp=25, str=9, mag=8, dfn=10, mgd=8,
                                    spd=12, techs=rogueTechs, friendly=True)


class Mage(BattleEntity):
    """Class representing one of the game's main characters. Specifically, this is for the character who follows
        the typical Mage trope"""
    def __init__(self):
        mageTechs = [Fire(), Ice(), Lightning()]
        super(Mage, self).__init__(name='John', job='Mage', hp=50, mp=40, str=4, mag=14, dfn=6, mgd=12,
                                   spd=9, techs=mageTechs, friendly=True)


class Cleric(BattleEntity):
    """Class representing one of the game's main characters. Specifically, this is for the character who follows
        the typical Cleric trope"""
    def __init__(self):
        clericTechs = [Heal(), Revive()]
        super(Cleric, self).__init__(name='Rick', job='Cleric', hp=50, mp=40, str=4, mag=13, dfn=6, mgd=13,
                                     spd=9, techs=clericTechs, friendly=True)


def default_party():
    """Create default Party."""
    party = Party()
    party.add_member(Knight())
    party.add_member(Rogue())
    party.add_member(Mage())
    party.add_member(Cleric())
    return party
