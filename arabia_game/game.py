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
        self.resource_info = {
            "money": {
                "token": load_surface("money_symbol.png"),
                "y_coordinate": 10
            },
            "oil": {
                "token": load_surface("oil_token.png"),
                "chance_to_appear": 500,
                "y_coordinate": 60,
                "inside_cost": 3,
                "outside_cost": 5
            },
            "uranium": {
                "token": load_surface("uranium_token.png"),
                "chance_to_appear": 900,
                "y_coordinate": 115,
                "inside_cost": 7,
                "outside_cost": 10
            },
            "stones": {
                "token": load_surface("stone_token.png"),
                "chance_to_appear": 900,
                "y_coordinate": 162,
                "inside_cost": 3,
                "outside_cost": 5
            },
            "refined_oil": {
                "token": load_surface("refined_oil_token.png"),
                "y_coordinate": 210
            }
        }
        self.tech_info = {
            "radar": {
                "token": load_surface("radar_icon.png"),
                "y_coordinate": 350,
                "level": 1
            },
        }
        self.sell_button_surface = load_surface("button_sell.png")
        self.refine_button_surface = load_surface("button_refine.png")
        self.resources_on_map = pygame.sprite.Group()
        #Fonts
        self.font = pygame.font.SysFont("monospace", 35)
        self.font_medium = pygame.font.SysFont("monospace", 27)
        self.font_small = pygame.font.SysFont("monospace", 20)
        self.font_left_margin:int = 10
        # Market
        self.market_symbols = pygame.sprite.Group()
        self.sell_buttons = pygame.sprite.Group()
        self._init_market()
        # Technology
        self.technology_symbols = pygame.sprite.Group()
        self._init_tech()
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
                # Check if something clickable has been clicked
                for resource in self.resources_on_map:
                    if resource.rect.collidepoint(mouse_position):
                        self._handle_resource_clicking(resource)
                for button in self.sell_buttons:
                    if button.rect.collidepoint(mouse_position):
                        self._handle_selling(button)
                for tech_symbol in self.technology_symbols:
                    if tech_symbol.rect.collidepoint(mouse_position):
                        self._handle_technology_upgrade()
                if self.refine_button.rect.collidepoint(mouse_position):
                    self._handle_refining()


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
        if self.player.has_resource("money", amount=resource_cost):
            self.player.resources["money"] -= resource_cost
            self.resources_on_map.remove(resource)
            self.player.add_resource(resource.type)
            print(f"Mined {resource.type} for {resource_cost}")
        else:
            print("Not enough money to mine")


    def _handle_selling(self, resource):
        if self.player.has_resource(resource.type):
            self.player.resources[resource.type] -= 1
            self.player.resources["money"] += self.market.prices[resource.type]
            print(f"Sold {resource.type} for {self.market.prices[resource.type]}")
            self.market.modify_price(resource.type)
        else:
            print("You don't own that resource")


    def _handle_refining(self):
        if self.player.has_resource("oil", amount=3):
            self.player.resources["oil"] -= 3
            self.player.add_resource("refined_oil")
            print("Refined oil")
        else:
            print("You don't have enough oil to refine")


    def _handle_technology_upgrade(self):
        if self.player.has_resource("money", amount=self.market.prices["radar"]):
            self.player.resources["money"] -= self.market.prices["radar"]
            self.market.prices["radar"] += 10
            self.tech_info["radar"]["level"] += 1
            self.player.resources_to_display += 5
        else:
            print("Not enough money to buy this technology")

    def _process_game_logic(self):
        # Randomly place resources on map
        for _type, info in self.resource_info.items():
            if _type in ["money", "refined_oil"]:
                continue
            if len(self.resources_on_map) < self.player.resources_to_display and randint(0, info["chance_to_appear"]) == 0:
                self.resources_on_map.add (
                    Resource(
                        _type, info["token"],
                        info["inside_cost"], info["outside_cost"]
                    )
                )

        # Calculate resources touching the Arabia
        # TODO Use smaller mask maybe?
        self.arabia_col: list = pygame.sprite.spritecollide(
            self.border, self.resources_on_map,
            False, pygame.sprite.collide_mask
        )

    def _init_market(self):
        for _type, info in self.resource_info.items():
            # Add resource symbols to market
            self.market_symbols.add(
                GameElement(
                    _type, info["token"],
                    x=self.font_left_margin, y=info["y_coordinate"]
                )
            )
            # Don't add sell button if the resource is money
            if _type == "money":
                continue
            # Add refine button if the resource is oil
            if _type == "oil":
                self.refine_button = GameElement(
                    "refine", self.refine_button_surface,
                    x=self.font_left_margin+210, y=info["y_coordinate"]
                )
            self.sell_buttons.add(
                GameElement(
                    _type, self.sell_button_surface,
                    x=self.font_left_margin+115, y=info["y_coordinate"]
                )
            )

    def _init_tech(self):
        for _type, info in self.tech_info.items():
            # Add resource symbols to technology menu
            self.technology_symbols.add(
                GameElement(
                    _type, info["token"],
                    x=self.font_left_margin, y=info["y_coordinate"]
                )
            )

    def _render_text(self):
        # Resources
        for key in self.resource_info.keys():
            if key == "money":
                self.screen.blit(
                    self.font.render(
                        f"{str(round(self.player.resources.get(key, 0), 1))}", True, (0,0,0)
                    ),
                    (
                        self.font_left_margin+50,
                        self.resource_info[key]["y_coordinate"]
                    )
                )
            else:    
                self.screen.blit(
                    self.font.render(
                        f"{str(self.player.resources.get(key, 0))}", True, (0,0,0)
                    ),
                    (
                        self.font_left_margin+50,
                        self.resource_info[key]["y_coordinate"]
                    )
                )

        # Tech
        for key in self.tech_info.keys():
            self.screen.blit(
                self.font_medium.render(
                    f"LVL: {self.tech_info.get(key).get('level')}",
                    True,
                    (0,0,0)
                ),
                (
                    self.font_left_margin+50,
                    self.tech_info[key]["y_coordinate"]
                )
            )

        # FPS
        fps = self.font_small.render(
            f"FPS:{str(int(self.clock.get_fps()))}", True, (0,0,0)
        )
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
        for symbol in self.market_symbols:
            self.screen.blit(
                symbol.image, symbol.rect
            )
        for button in self.sell_buttons:
            self.screen.blit(
                button.image, button.rect
            )
        for tech in self.technology_symbols:
            self.screen.blit(
                tech.image, tech.rect
            )

        self.screen.blit(self.refine_button.image, self.refine_button.rect)

        self._render_text()

        pygame.display.flip()