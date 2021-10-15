import pygame
from pygame import draw

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
        self.transparent_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.transparent_surface.set_alpha(55)
        # Sprites
        # self.border = self._draw_borders()
        self.border = Token("Square", load_surface("square.png"), random=False)
        # pygame.mask.from_surface(pygame.Surface((self.sa.w, self.sa.h)
        # self.border_group = pygame.sprite.Group([])
        # self.sprite_group = pygame.sprite.Group([])
        self.sprite_group = []

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

    def _draw_borders(self):
        # Draw Arabia borders onto an invisible surface
        # TODO problem with wrong collision-detection can be solved
        # by creating smaller borders around arabia.
        sa = pygame.draw.polygon(
            self.screen,
            pygame.Color(125,0,0),
            saudi_arabia
        )
        sa_surface = pygame.Surface((sa.w, sa.h), pygame.SRCALPHA)
        return Token(
            "Map",
            sa_surface,
            random=False
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

                for s in self.sprite_group:
                    if s.rect.collidepoint(pos):
                        print(s)
                        self.sprite_group.remove(s)

                        # arabia_col = pygame.sprite.spritecollide(
                        #     self.border, self.sprite_group,
                        #     False, pygame.sprite.collide_mask
                        # )

                        """
                        if self.sa.collidepoint(pos):
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
                        """

    def _process_game_logic(self):
        # TODO don't load_surface() on every instance. load it once, then reuse it
        if randint(1, 50) == 1:
            # self.sprite_group.add(
            self.sprite_group.append(
                Token("Oil", load_surface("oil_symbol_small.png"))
            )
        if randint(1, 50) == 1:
            # self.sprite_group.add(
            self.sprite_group.append(
                Token("Uranium", load_surface("uranium_small.png"))
            )

        if randint(1, 50) == 1:
            # self.sprite_group.add(
            self.sprite_group.append(
                Token("Stones", load_surface("ruby.png"))
            )
        if self.sprite_group:
            arabia_col = pygame.sprite.collide_mask(self.border, self.sprite_group[-1])
            print(arabia_col)


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
        # self.screen.blit(self.transparent_surface, (0, 0))
        self.screen.blit(self.border.image, self.border.rect)

        for sprite in self.sprite_group:
            self.screen.blit(
                sprite.image, sprite.rect
            )

        self._render_text()

        pygame.display.flip()