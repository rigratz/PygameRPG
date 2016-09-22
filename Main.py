from GameEngine import *
import pygame
from pygame import *


def main():
    global cameraX, cameraY
    global state
    pygame.init()
    game = GameEngine()
    pygame.display.set_caption("Pygame RPG Prototype")

    # Set-up level. Will change when other Tile-map method is employed.
    level = game.levels.getLevel(0)
    x = y = 0
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                game.platforms.append(p)
                game.entities.add(p)
            if col == "E":
                e = ExitBlock(x, y)
                game.platforms.append(e)
                game.entities.add(e)
            if col == "X":
                n = Enemy(x, y, 0)
                game.enemies.append(n)
                game.entities.add(n)
            if col == "W":
                w = Walkable(x, y, "Grass")
                game.entities.add(w)
            x += 32
        y += 32
        x = 0
        game.entities.add(game.player)
    #----------------------------------------------------------------------

    game.start()


if __name__ == "__main__":
    main()
