import pygame

from models import Token
from random import randint, random
from utils import load_surface

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 900
MENU_WIDTH = 339

class Arabia:
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Surfaces
        self.map = load_surface("map_relief.png", False)
        self.controls_bg = load_surface("paper.png", False)
        # Sprites
        self.oil_tokens = [
            Token("Oil", load_surface("oil_symbol_small.png")) for i in range(3)
        ]

    def main_loop(self):
        for i in self.oil_tokens:
            print(i.rect)

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                for s in self.oil_tokens:
                    if s.rect.collidepoint(pos):
                        print(f"Clicked on sprite {s.__repr__()}")
                        self.oil_tokens.remove(s)

    def _process_game_logic(self):
        if randint(1, 10000) == 1:
            self.oil_tokens.append(
                Token("Oil", load_surface("oil_symbol_small.png"))
            )

    def _draw(self):
        self.screen.blit(self.map, (MENU_WIDTH, 0))
        self.screen.blit(self.controls_bg, (0, 0))
        for token in self.oil_tokens:
            self.screen.blit(
                token.image, token.rect
            )
        pygame.display.flip()