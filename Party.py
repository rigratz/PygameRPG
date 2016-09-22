class Party(object):
    """Representation of a party of Characters"""
    
    def __init__(self):
        self.members = []

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

class Character(object):
    """Representation of a playable character"""
    
    def __init__(self, name, **kwargs):
        self.name = name
        self.atb = 0
        self.ready = False
        self.hp = 999
        self.mp = 99
        self.str = 10
        self.mag = 10
        self.dfn = 10
        self.mgd = 10
        self.spd = 10
        self.techs = self.default_techs()
        
        for prop, value in kwargs.items():
            if hasattr(self, prop):
                setattr(self, prop, value)
            else:
                pass # throw some type of exception

    def get_name(self):
        return self.name

    def atb_charge(self, increment):
        if self.atb >= 100:
            self.atb = 100
        else:
            self.atb += self.spd * (increment / 1000)

    def get_atb_charge(self):
        return self.atb

    def reset_atb(self):
        self.atb = 0
        self.ready = False

    @staticmethod
    def default_techs():
        """Return list of default techs for a new Character."""
        return ['Fire', 'Ice', 'Lightning']

def default_party():
    """Create default Party."""
    party = Party()
    party.add_member(Character('Riley', spd=15))
    party.add_member(Character('Darren'))
    party.add_member(Character('John', spd=20))
    party.add_member(Character('!tits', spd=5))
    return party
