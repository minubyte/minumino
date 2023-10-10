import pygame
from utils import *

class Menu:
    def __init__(self, screen, gm):
        self.screen = screen
        self.gm = gm

    def run(self, dt, events):
        self.screen.fill("#ffffff")
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.gm.set("level")

        draw_text(self.screen, "press [space] to start")
