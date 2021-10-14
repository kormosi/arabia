import pygame

from models import Token, Player, saudi_arabia
from random import randint
from utils import load_surface

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 900
MENU_WIDTH = 339

class Arabia:
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Player
        self.player = Player()
        # Surfaces
        self.menu_bg = load_surface("controls.png", False)
        self.map = load_surface("map_relief.png", False)
        self.draw_borders()
        # Sprites
        self.tokens = []
        #Fonts
        self.font = pygame.font.SysFont("monospace", 35)

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Dawn of Arabia")

    def draw_borders(self):
        # Draw Arabia borders onto an invisible surface
        # TODO problem with wrong collision-detection can be solved
        # by creating smaller borders around arabia.
        self.transparent_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.transparent_surface.set_alpha(130)
        self.sa = pygame.draw.polygon(
            self.transparent_surface,
            pygame.Color(125,0,0),
            saudi_arabia
        )

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print(pos)

                for t in self.tokens:
                    if t.rect.collidepoint(pos):
                        print(t)
                        # Handle clicking on an oil token
                        self.tokens.remove(t)
                        if self.sa.collidepoint(pos):
                            print(f"Clicked on token {t.__repr__()} inside of Arabia")
                            if t.type == "Oil":
                                self.player.oil += 1
                            elif t.type == "Uranium":
                                self.player.uranium += 1
                            elif t.type == "Stones":
                                self.player.stones += 1
                        else:
                            print(f"Clicked on token {t.__repr__()} outside of Arabia")
                            if t.type == "Oil":
                                self.player.oil += 1
                            elif t.type == "Uranium":
                                self.player.uranium += 1
                            elif t.type == "Stones":
                                self.player.stones += 1
                            self.player.money -= 5


    def _process_game_logic(self):
        # TODO don't load_surface() on every instance. load it once, then reuse it
        if randint(1, 2000) == 1:
            self.tokens.append(
                Token("Oil", load_surface("oil_symbol_small.png"))
            )
        if randint(1, 5000) == 1:
            self.tokens.append(
                Token("Uranium", load_surface("uranium_small.png"))
            )

        if randint(1, 5000) == 1:
            self.tokens.append(
                Token("Stones", load_surface("ruby.png"))
            )

    def _draw(self):
        self.screen.blit(self.map, (MENU_WIDTH, 0))
        self.screen.blit(self.menu_bg, (0, 0))
        # Uncomment for border-debugging
        # self.screen.blit(self.transparent_surface, (0, 0))

        for token in self.tokens:
            self.screen.blit(
                token.image, token.rect
            )

        money = self.font.render(f"Money:{str(self.player.money)}", True, (0,0,0))
        oil = self.font.render(f"Oil:{str(self.player.oil)}", True, (0,0,0))
        uranium = self.font.render(f"Uranium:{str(self.player.uranium)}", True, (0,0,0))
        stones = self.font.render(f"Stones:{str(self.player.stones)}", True, (0,0,0))
        self.screen.blit(money, (10, 10))
        self.screen.blit(oil, (10, 55))
        self.screen.blit(uranium, (10, 100))
        self.screen.blit(stones, (10, 145))

        pygame.display.flip()