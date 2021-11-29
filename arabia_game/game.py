import pygame

from models import Player, GameElement, Market
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
        self.menu_bg = load_surface("controls.png", False)
        self.map = load_surface("map.png", False)
        self.border = GameElement(  # Technically a sprite, not a surface
            "ArabiaMask", load_surface("arabia_mask.png"), random=False, x=MENU_WIDTH, y=0
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
                        else:
                            print(f"Clicked on token {resource.__repr__()} outside of Arabia")
                            self.player.money -= 5
                        self.resources.remove(resource)
                for market_item in self.market_items:
                    if market_item.rect.collidepoint(mouse_position):
                        print("collision")
                        if market_item == self.sell_oil:
                            self.player.money += self.market.oil_price
                            self.player.resources["Oil"] -= 1


    def _process_game_logic(self):
        if randint(1, 300) == 1:
            self.resources.add(
                GameElement("Oil", self.oil_token)
            )
        if randint(1, 500) == 1:
            self.resources.add(
                GameElement("Uranium", self.uranium_token)
            )

        if randint(1, 500) == 1:
            self.resources.add(
                GameElement("Stones", self.stones_token)
            )

        # Calculate resources touching the Arabia
        # TODO This should rather be "inside of Arabia"
        # That could be achieved by using a smaller mask
        self.arabia_col: list = pygame.sprite.spritecollide(
            self.border, self.resources,
            False, pygame.sprite.collide_mask
        )

    def _init_market(self):
        # Place and render
        self.buy = self.font_medium.render("Buy:", True, (0,0,0))
        self.sell = self.font_medium.render("Sell:", True, (0,0,0))

        self.sell_oil = GameElement("Oil", self.oil_token, random=False, x=self.font_left_margin + 80, y=760)
        # self.sell_uranium = GameElement("Uranium", self.uranium_token, random=False)
        # self.sell_stones = GameElement("Stones", self.stones_token, random=False)

        # self.buy_oil = GameElement("Oil", self.oil_token, random=False)
        # self.buy_uranium = GameElement("Uranium", self.uranium_token, random=False)
        # self.buy_stones = GameElement("Stones", self.stones_token, random=False)

        self.market_items.add(self.sell_oil)
        # self.market_items.add(self.sell_uranium)
        # self.market_items.add(self.sell_stones)

        # self.market_items.add(self.buy_oil)
        # self.market_items.add(self.buy_uranium)
        # self.market_items.add(self.buy_stones)


    def _render_market(self):
        # Blit
        # self.screen.blit(self.sell_oil.image, (self.font_left_margin + 80, 690))
        # self.screen.blit(self.sell_uranium.image, (self.font_left_margin + 130, 696))
        # self.screen.blit(self.sell_stones.image, (self.font_left_margin + 190, 699))

        # TODO WARNING: buy and sell are vice versa
        self.screen.blit(self.sell_oil.image, (self.font_left_margin + 80, 760))

        # self.screen.blit(self.buy_uranium.image, (self.font_left_margin + 130, 766))
        # self.screen.blit(self.buy_stones.image, (self.font_left_margin + 190, 769))

        # self.screen.blit(self.buy, (self.font_left_margin, 700))
        self.screen.blit(self.sell, (self.font_left_margin, 770))

    # TODO I think I'm going to split the render_text method into two methods,
    # one for rendering all info about resources (including texts and sell icons),
    # and another strictly for textual info, like FPS.
    def _render_text(self):
        # Resources
        money = self.font.render(f"Money:{str(self.player.money)}", True, (0,0,0))
        oil = self.font.render(
            f"Oil:{str(self.player.resources.get('Oil', 0))}", True, (0,0,0)
        )
        uranium = self.font.render(
            f"Uranium:{str(self.player.resources.get('Uranium', 0))}", True, (0,0,0)
        )
        stones = self.font.render(
            f"Stones:{str(self.player.resources.get('Stones', 0))}", True, (0,0,0)
        )
        self.screen.blit(money, (self.font_left_margin, 10))
        self.screen.blit(oil, (self.font_left_margin, 55))
        self.screen.blit(uranium, (self.font_left_margin, 100))
        self.screen.blit(stones, (self.font_left_margin, 145))
        # FPS
        fps = self.font_small.render(f"FPS:{str(int(self.clock.get_fps()))}", True, (0,0,0))
        self.screen.blit(fps, (self.font_left_margin, 870))
        # Resource price
        prices = self.market.resource_price(self.resources)
        print(prices)


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