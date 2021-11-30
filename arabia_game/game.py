import pygame

from models import Player, GameElement, Market, Resource
from utils import load_surface
from random import randint

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 900
MENU_WIDTH = 339

class Arabia:
    def __init__(self) -> None:
        # Init stuff
        self._init_pygame()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Player
        self.player = Player()
        self.market = Market()
        # Surfaces
        self.map = load_surface("map.png", False)
        self.menu_bg = load_surface("controls.png", False)
        self.border = GameElement(  # Technically a sprite, not a surface
            "ArabiaMask", load_surface("arabia_mask.png"), x=MENU_WIDTH, y=0
        )
        self.oil_token = load_surface("oil_token.png")
        self.uranium_token = load_surface("uranium_token.png")
        self.stones_token = load_surface("stone_token.png")
        self.resources = pygame.sprite.Group()
        #Fonts
        self.font = pygame.font.SysFont("monospace", 35)
        self.font_medium = pygame.font.SysFont("monospace", 27)
        self.font_small = pygame.font.SysFont("monospace", 20)
        self.font_left_margin:int = 10
        # Market
        self.market_items = pygame.sprite.Group()
        self._init_market()
        # FPS control
        self.clock = pygame.time.Clock()

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()
            self.clock.tick(60)


    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Twilight: Arabia")


    def _handle_input(self):
        for event in pygame.event.get():
            # Quitting game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                quit()
            # Sprite clicking
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_position:tuple[int, int] = pygame.mouse.get_pos()
                # Check if a resource has been clicked
                for resource in self.resources:
                    if resource.rect.collidepoint(mouse_position):
                        # Add resource to Player's resources
                        self.player.add_resource(resource.type)
                        if resource in self.arabia_col:
                            print(f"Clicked on token {resource.__repr__()} inside of Arabia")
                            self.player.money -= resource.inside_cost
                        else:
                            print(f"Clicked on token {resource.__repr__()} outside of Arabia")
                            self.player.money -= resource.outside_cost
                        self.resources.remove(resource)
                for market_item in self.market_items:
                    if market_item.rect.collidepoint(mouse_position):
                        self.player.money += self.market.prices[market_item.type]
                        self.player.resources[market_item.type] -= 1
                        print(f"Sold {market_item.type} for {self.market.prices[market_item.type]}")
                        self.market.modify_price(market_item.type)


    def _process_game_logic(self):
        if randint(1, 100) == 1:
            self.resources.add(
                Resource("oil", self.oil_token, 3, 5, random=True)
            )
        if randint(1, 100) == 1:
            self.resources.add(
                Resource("uranium", self.uranium_token, 8, 10, random=True)
            )

        if randint(1, 100) == 1:
            self.resources.add(
                Resource("stones", self.stones_token, 5, 8, random=True)
            )

        # Calculate resources touching the Arabia
        # TODO This should rather be "inside of Arabia"
        # That could be achieved by using a smaller mask
        self.arabia_col: list = pygame.sprite.spritecollide(
            self.border, self.resources,
            False, pygame.sprite.collide_mask
        )

    def _init_market(self):
        # Font
        self.sell = self.font_medium.render("Sell:", True, (0,0,0))
        # Icons
        self.sell_oil = GameElement("oil", self.oil_token, x=self.font_left_margin + 80, y=760)
        self.sell_uranium = GameElement("uranium", self.uranium_token, x=self.font_left_margin + 130, y=766)
        self.sell_stones = GameElement("stones", self.stones_token, x=self.font_left_margin + 190, y=769)

        self.market_items.add(self.sell_oil)
        self.market_items.add(self.sell_uranium)
        self.market_items.add(self.sell_stones)


    def _render_market(self):
        # Font
        self.screen.blit(self.sell, (self.font_left_margin, 770))
        # Icons
        self.screen.blit(self.sell_oil.image, (self.font_left_margin + 90, 760))
        self.screen.blit(self.sell_uranium.image, (self.font_left_margin + 140, 766))
        self.screen.blit(self.sell_stones.image, (self.font_left_margin + 200, 769))


    # TODO I think I'm going to split the render_text method into two methods,
    # one for rendering all info about resources (including texts and sell icons),
    # and another strictly for textual info, like FPS.
    def _render_text(self):
        # Resources
        money = self.font.render(f"Money:{str(self.player.money)}", True, (0,0,0))
        oil = self.font.render(
            f"Oil:{str(self.player.resources.get('oil', 0))}", True, (0,0,0)
        )
        uranium = self.font.render(
            f"Uranium:{str(self.player.resources.get('uranium', 0))}", True, (0,0,0)
        )
        stones = self.font.render(
            f"Stones:{str(self.player.resources.get('stones', 0))}", True, (0,0,0)
        )
        self.screen.blit(money, (self.font_left_margin, 10))
        self.screen.blit(oil, (self.font_left_margin, 55))
        self.screen.blit(uranium, (self.font_left_margin, 100))
        self.screen.blit(stones, (self.font_left_margin, 145))
        # FPS
        fps = self.font_small.render(f"FPS:{str(int(self.clock.get_fps()))}", True, (0,0,0))
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
        self._render_market()

        pygame.display.flip()