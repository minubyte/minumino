import pygame
import sys
pygame.init()
from utils import *

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

        self.gm = Gm("level")

        from scenes.menu import Menu
        from scenes.level import Level
        self.states = {
            "menu": Menu(self.screen, self.gm),
            "level": Level(self.screen, self.gm),
        }
        
        self.dt = 1

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.states[self.gm.get()].run(self.dt, events)

            pygame.display.update()
            self.dt = self.clock.tick(120)*60/1000

class Gm:
    def __init__(self, current_state):
        self.current_state = current_state
    
    def get(self):
        return self.current_state
    
    def set(self, state):
        self.current_state = state

if __name__ == "__main__":
    game = Game()
    game.run()