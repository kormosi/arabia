import pygame

from utils import load_sprite

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 900

class Arabia:
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.map = load_sprite("map_relief.png", False)
        self.controls_bg = load_sprite("paper.png", False)


    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()


    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Dawn of Arabia")


    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


    def _process_game_logic(self):
        pass


    def _draw(self):
        self.screen.blit(self.map, (339, 0))
        self.screen.blit(self.controls_bg, (0, 0))
        pygame.display.flip()