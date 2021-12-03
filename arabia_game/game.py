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
        self.resources_on_map = pygame.sprite.Group()
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
                for resource in self.resources_on_map:
                    if resource.rect.collidepoint(mouse_position):
                        self._handle_resource_clicking(resource)
                for resource in self.market_items:
                    if resource.rect.collidepoint(mouse_position):
                        self._handle_selling(resource)



    def _handle_resource_clicking(self, resource) -> None:
        # Add resource to Player's resources
        if resource in self.arabia_col:
            print(f"Clicked on token {resource.__repr__()} inside of Arabia")
            self._handle_mining(resource, inside_arabia=True)
        else:
            print(f"Clicked on token {resource.__repr__()} outside of Arabia")
            self._handle_mining(resource, inside_arabia=False)


    def _handle_mining(self, resource, inside_arabia=True) -> None:
        resource_cost = (
            resource.inside_cost if inside_arabia else resource.outside_cost
        )
        if self.player.has_enough_money(resource_cost):
            self.player.money -= resource_cost
            self.resources_on_map.remove(resource)
            self.player.add_resource(resource.type)
            print(f"Mined {resource.type} for {resource_cost}")
        else:
            print("Not enough money to mine")


    def _handle_selling(self, resource):
        if self.player.has_resource(resource.type):
            self.player.resources[resource.type] -= 1
            self.player.money += self.market.prices[resource.type]
            print(f"Sold {resource.type} for {self.market.prices[resource.type]}")
            self.market.modify_price(resource.type)
        else:
            print("You don't own that resource")


    def _process_game_logic(self):
        if randint(1, 100) == 1:
            self.resources_on_map.add(
                Resource("oil", self.oil_token, 3, 5, random=True)
            )
        if randint(1, 100) == 1:
            self.resources_on_map.add(
                Resource("uranium", self.uranium_token, 8, 10, random=True)
            )

        if randint(1, 100) == 1:
            self.resources_on_map.add(
                Resource("stones", self.stones_token, 5, 8, random=True)
            )

        # Calculate resources touching the Arabia
        # TODO This should rather be "inside of Arabia"
        # That could be achieved by using a smaller mask
        self.arabia_col: list = pygame.sprite.spritecollide(
            self.border, self.resources_on_map,
            False, pygame.sprite.collide_mask
        )

    def _init_market(self):
        # Font
        self.sell = self.font_medium.render("Sell:", True, (0,0,0))
        # Icons
        # TODO work on alignment of icons and/or text
        self.sell_oil = GameElement("oil", self.oil_token, x=self.font_left_margin, y=50)
        self.sell_uranium = GameElement("uranium", self.uranium_token, x=self.font_left_margin, y=103)
        self.sell_stones = GameElement("stones", self.stones_token, x=self.font_left_margin, y=145)

        self.market_items.add(self.sell_oil)
        self.market_items.add(self.sell_uranium)
        self.market_items.add(self.sell_stones)


    # TODO I think I'm going to split the render_text method into two methods,
    # one for rendering all info about resources (including texts and sell icons),
    # and another strictly for textual info, like FPS.
    def _render_text(self):
        # Resources
        money = self.font.render(f"Money:{str(self.player.money)}", True, (0,0,0))
        oil = self.font.render(
            f"{str(self.player.resources.get('oil', 0))}", True, (0,0,0)
        )
        uranium = self.font.render(
            f"{str(self.player.resources.get('uranium', 0))}", True, (0,0,0)
        )
        stones = self.font.render(
            f"{str(self.player.resources.get('stones', 0))}", True, (0,0,0)
        )
        # TODO I don't like +40 hardcoded below
        # Also, this could be a for loop
        self.screen.blit(money, (self.font_left_margin, 10))
        self.screen.blit(oil, (self.font_left_margin+40, 55))
        self.screen.blit(uranium, (self.font_left_margin+40, 100))
        self.screen.blit(stones, (self.font_left_margin+40, 145))
        # FPS
        fps = self.font_small.render(f"FPS:{str(int(self.clock.get_fps()))}", True, (0,0,0))
        self.screen.blit(fps, (self.font_left_margin, 870))


    def _draw(self):
        self.screen.blit(self.map, (MENU_WIDTH, 0))
        self.screen.blit(self.menu_bg, (0, 0))
        # Uncomment for border-debugging
        # self.screen.blit(self.border.image, self.border.rect)

        for resource in self.resources_on_map:
            self.screen.blit(
                resource.image, resource.rect
            )
        for resource in self.market_items:
            self.screen.blit(
                resource.image, resource.rect
            )

        self._render_text()

        pygame.display.flip()