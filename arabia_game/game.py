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
                "chance_to_appear": 100,
                "y_coordinate": 50,
                "inside_cost": 3,
                "outside_cost": 5
            },
            "uranium": {
                "token": load_surface("uranium_token.png"),
                "chance_to_appear": 100,
                "y_coordinate": 103,
                "inside_cost": 7,
                "outside_cost": 10
            },
            "stones": {
                "token": load_surface("stone_token.png"),
                "chance_to_appear": 100,
                "y_coordinate": 145,
                "inside_cost": 3,
                "outside_cost": 5
            }
        }
        self.resources_on_map = pygame.sprite.Group()
        #Fonts
        self.font = pygame.font.SysFont("monospace", 35)
        self.font_medium = pygame.font.SysFont("monospace", 27)
        self.font_small = pygame.font.SysFont("monospace", 20)
        self.font_left_margin:int = 10
        # Market
        self.market_symbols = pygame.sprite.Group()
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
                for resource in self.market_symbols:
                    if (
                        resource.rect.collidepoint(mouse_position)
                        and resource.type != "money"
                    ):
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


    def _process_game_logic(self):
        for _type, info in self.resource_info.items():
            if _type == "money":
                continue
            if randint(0, info["chance_to_appear"]) == 0:
                self.resources_on_map.add(
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
            self.market_symbols.add(
                GameElement(
                    _type, info["token"],
                    x=self.font_left_margin, y=info["y_coordinate"]
                )
            )

    def _render_text(self):
        # T0D0 put this into for-loop
        # Resources
        for key in self.resource_info.keys():
            self.screen.blit(
                self.font.render(
                    f"{str(self.player.resources.get(key, 0))}", True, (0,0,0)
                ),
                (
                    self.font_left_margin+40,
                    self.resource_info[key]["y_coordinate"]
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
        for resource in self.market_symbols:
            self.screen.blit(
                resource.image, resource.rect
            )

        self._render_text()

        pygame.display.flip()