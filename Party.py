class Party(object):
    def __init__(self):
        self.party = []

    def newMember(self, member):
        self.party.append(member)

    def getMember(self, index):
        return self.party[index]

    def getParty(self):
        return self.party


class Character(object):
    def __init__(self, name):
        if name == "Riley":
            self.name = "Riley"
            self.atb = 0
            self.ready = False
            self.hp = 999
            self.mp = 99
            self.str = 10
            self.mag = 10
            self.dfn = 10
            self.mgd = 10
            self.spd = 15
            self.techs = ["Fire", "Ice", "Lightning"]
        elif name == "Darren":
            self.name = "Darren"
            self.atb = 0
            self.ready = False
            self.hp = 999
            self.mp = 99
            self.str = 10
            self.mag = 10
            self.dfn = 10
            self.mgd = 10
            self.spd = 10
            self.techs = ["Fire", "Ice", "Lightning"]
        elif name == "John":
            self.name = "John"
            self.atb = 0
            self.ready = False
            self.hp = 999
            self.mp = 99
            self.str = 10
            self.mag = 10
            self.dfn = 10
            self.mgd = 10
            self.spd = 20
            self.techs = ["Fire", "Ice", "Lightning"]
        elif name == "!tits":
            self.name = "!tits"
            self.atb = 0
            self.ready = False
            self.hp = 999
            self.mp = 99
            self.str = 10
            self.mag = 10
            self.dfn = 10
            self.mgd = 10
            self.spd = 5
            self.techs = ["Fire", "Ice", "Lightning"]

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





