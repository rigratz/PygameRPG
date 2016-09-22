class Levels(object):
    def __init__(self):
        self.maps = {}
        self.createMaps(self.maps)

    def getLevel(self, index):
        return self.maps[index]

    def createMaps(self, maps):
        maps[0] = [
            "PPPPPPPPPPPPPPPPPPPPPPPPP",
            "P             P         P",
            "PPPP     PPPPPP         P",
            "P                       P",
            "PPP   PPPPPPPPPPPPPPPPPPP",
            "P                       P",
            "P                X      P",
            "P                       P",
            "P    PPPPPPPP     PPPPPPP",
            "P                       P",
            "P          PPPPPPP      P",
            "P                 PPPPPPP",
            "P                       P",
            "P         PPPPPPP       P",
            "P                       P",
            "P          PPPPPP       P",
            "P                       P",
            "P    PPPPPPPPPP         P",
            "P                       P",
            "P       PPP    PPP      P",
            "P         P    P        P",
            "P         P    P        P",
            "P         P    P        P",
            "P         P    P        P",
            "PPPPPPPPPPPPPPEPPPPPPPPPP",]