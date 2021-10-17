import pygame
from pygame import draw

from models import Token, Player
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
        self.map = load_surface("map.png", False)
        self.transparent_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.transparent_surface.set_alpha(55)
        # Sprites
        self.border = Token("Square", load_surface("arabia_mask.png"), random=False)
        # self.sprite_group = []
        self.resources = pygame.sprite.Group()

        #Fonts
        self.font_left_margin:int = 10
        self.font = pygame.font.SysFont("monospace", 35)
        self.font_small = pygame.font.SysFont("monospace", 20)
        # FPS control
        self.clock = pygame.time.Clock()

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()
            # Limit the FPS
            self.clock.tick(60)

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Dawn of Arabia")

    def _handle_input(self):
        for event in pygame.event.get():
            # Quitting game
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quit()
            # Sprite clicking
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print(pos)

                # Check if a resource has been clicked, then remove it
                for s in self.resources:
                    if s.rect.collidepoint(pos):

                        if s in self.arabia_col:
                            print(f"Clicked on token {s.__repr__()} inside of Arabia")
                            if s.type == "Oil":
                                self.player.oil += 1
                            elif s.type == "Uranium":
                                self.player.uranium += 1
                            elif s.type == "Stones":
                                self.player.stones += 1
                        else:
                            print(f"Clicked on token {s.__repr__()} outside of Arabia")
                            if s.type == "Oil":
                                self.player.oil += 1
                            elif s.type == "Uranium":
                                self.player.uranium += 1
                            elif s.type == "Stones":
                                self.player.stones += 1
                            self.player.money -= 5

                        self.resources.remove(s)


    def _process_game_logic(self):
        # TODO don't load_surface() on every instance. load it once, then reuse it
        if randint(1, 500) == 1:
            self.resources.add(
                Token("Oil", load_surface("oil_token.png"))
            )
        if randint(1, 1000) == 1:
            self.resources.add(
                Token("Uranium", load_surface("uranium_token.png"))
            )

        if randint(1, 1000) == 1:
            self.resources.add(
                Token("Stones", load_surface("ruby_token.png"))
            )

        # Resources inside of Arabia
        self.arabia_col = pygame.sprite.spritecollide(
            self.border, self.resources,
            False, pygame.sprite.collide_mask
        )


    def _render_text(self):
        money = self.font.render(f"Money:{str(self.player.money)}", True, (0,0,0))
        oil = self.font.render(f"Oil:{str(self.player.oil)}", True, (0,0,0))
        uranium = self.font.render(f"Uranium:{str(self.player.uranium)}", True, (0,0,0))
        stones = self.font.render(f"Stones:{str(self.player.stones)}", True, (0,0,0))
        fps = self.font_small.render(f"FPS:{str(int(self.clock.get_fps()))}", True, (0,0,0))
        self.screen.blit(money, (self.font_left_margin, 10))
        self.screen.blit(oil, (self.font_left_margin, 55))
        self.screen.blit(uranium, (self.font_left_margin, 100))
        self.screen.blit(stones, (self.font_left_margin, 145))
        self.screen.blit(fps, (self.font_left_margin, 870))


    def _draw(self):
        self.screen.blit(self.map, (MENU_WIDTH, 0))
        self.screen.blit(self.menu_bg, (0, 0))
        # Uncomment for border-debugging
        # self.screen.blit(self.border.image, self.border.rect)

        for sprite in self.resources:
            self.screen.blit(
                sprite.image, sprite.rect
            )

        self._render_text()

        pygame.display.flip()