from Action import *


class Potion(Action):
    def __init__(self):
        super(Potion, self).__init__('Potion', False, None)
        pass

    def enact(self, caster, target):
        target.hp += 30
        print(caster.name + ' uses Potion to heal ' + target.name)
        super(Potion, self).enact(caster, target)


class PhoenixDown(Action):
    def __init__(self):
        super(PhoenixDown, self).__init__('Phoenix Down', False, None)
        pass

    def enact(self, caster, target):
        target.hp += 30
        print(caster.name + ' uses Phoenix Down to revive ' + target.name)
        super(PhoenixDown, self).enact(caster, target)