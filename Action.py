NONE = 'None'

FIRE = 'Fire'
ICE = 'Ice'
LIGHTNING = 'Lightning'
PHYSICAL = 'Physical'
COVER = 'Cover'
STEAL = 'Steal'
HEAL = 'Heal'
REVIVE = 'Revive'


class Actions(object):
    def __init__(self, special):
        self.attack = Attack()
        self.defend = Defend()
        self.techs = special


class Action(object):
    """Actions entities can take. Not implemented yet"""
    def __init__(self, name, attack, element):
        self.name = name
        self.attack = attack
        self.element = element

    def enact(self, caster, target):
        """Method to be overridden by extending classes. Enacts Action from one caster on one target"""
        caster.reset_atb()
        pass



class Attack(Action):
    """Default attack action"""
    def __init__(self):
        super(Attack, self).__init__('Attack', True, PHYSICAL)

    def enact(self, caster, target):
        print(target.name + ' just got whacked by ' + caster.name)
        target.hp -= calculate_damage(caster, target, self)
        super(Attack, self).enact(caster, target)


class Defend(Action):
    """Default defend action"""
    def __init__(self):
        super(Defend, self).__init__('Defend', False, None)

    def enact(self, caster, target=None):
        print(caster.name + ' plays it cool. Defending!')
        caster.defending = True
        super(Defend, self).enact(caster, target)


class Fire(Action):
    """Action representing Mage's Fire spell"""
    def __init__(self):
        super(Fire, self).__init__(FIRE, True, FIRE)

    def enact(self, caster, target):
        print(target.name + ' just got burned by ' + caster.name)
        target.hp -= calculate_damage(caster, target, self)
        super(Fire, self).enact(caster, target)


class Ice(Action):
    """Action representing Mage's Ice spell"""
    def __init__(self):
        super(Ice, self).__init__(ICE, True, ICE)

    def enact(self, caster, target):
        print(target.name + ' just got frozen by ' + caster.name)
        target.hp -= calculate_damage(caster, target, self)
        super(Ice, self).enact(caster, target)


class Lightning(Action):
    """Action representing Mage's Ice spell"""
    def __init__(self):
        super(Lightning, self).__init__(LIGHTNING, True, LIGHTNING)

    def enact(self, caster, target):
        print(target.name + ' just got electrocuted by ' + caster.name)
        target.hp -= calculate_damage(caster, target, self)
        super(Lightning, self).enact(caster, target)


class Cover(Action):
    """Action representing Knight's Cover ability"""
    def __init__(self):
        super(Cover, self).__init__(COVER, False, None)

    def enact(self, caster, target):
        print(target.name + ' is being Covered by ' + caster.name)
        target.defending = True
        super(Cover, self).enact(caster, target)


class Steal(Action):
    """Action representing Rogue's Steal ability"""
    def __init__(self):
        super(Steal, self).__init__(STEAL, True, None)

    def enact(self, caster, target):
        print(target.name + ' just got jacked by ' + caster.name)
        super(Steal, self).enact(caster, target)


class Heal(Action):
    """Action representing Cleric's Heal spell"""
    def __init__(self):
        super(Heal, self).__init__(HEAL, False, None)

    def enact(self, caster, target):
        print(caster.name + ' just healed ' + target.name)
        super(Heal, self).enact(caster, target)


class Revive(Action):
    """Action representing Cleric's Revive spell"""
    def __init__(self):
        super(Revive, self).__init__(REVIVE, False, None)

    def enact(self, caster, target):
        print(caster.name + ' just revived ' + target.name)
        super(Revive, self).enact(caster, target)


def calculate_damage(caster, target, action):
    if action.element == PHYSICAL:
        damage = caster.str - (target.dfn / 4)
        if target.defending is True:
            damage /= 2
    else:
        damage = caster.mag - (target.mgd / 4)
        for resistance in target.resistance:
            if action.element == resistance:
                print(target.name + ' is strong against ' + resistance)
                damage /= 2
        for weakness in target.weakness:
            if action.element == weakness:
                print(target.name + ' is weak against ' + weakness)
                damage *= 2

    return damage


def calculate_healing(caster, target, action):
    pass

