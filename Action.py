class Action(object):
    """Actions entities can take. Not implemented yet"""
    def __init__(self):
        pass

    def activate(self, caster, target):
        """Method to be overridden by extending classes. Enacts Action"""
        pass


class Attack(Action):
    """Default attack action"""
    def __init__(self):
        super(Attack, self).__init__()

    def activate(self, caster, target):
        target.hp -= caster.str
        super(Attack, self).activate(caster, target)
