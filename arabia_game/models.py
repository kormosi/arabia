import game

from pygame import Rect, Surface, mask
from pygame.sprite import Sprite
from random import randint


class Player():
    def __init__( self) -> None:
        self.money:int = 50
        self.resources:dict[str, int] = {}

    def add_resource(self, resource_type: str) -> None:
        if resource_type in self.resources:
            self.resources[resource_type] += 1
        else:
            self.resources[resource_type] = 1


class GameElement(Sprite):
    def __init__(self, type: str, surface: Surface, random:bool=True) -> None:
        super().__init__()
        self.image = surface 
        self.type = type
        self.mask = mask.from_surface(surface)
        if random:
            # Place the element randomly on the map
            self.rect: Rect = self.image.get_rect(
                topleft=(
                    # Subtracted values are hard-coded for now;
                    # they fit the current token size.
                    randint(game.MENU_WIDTH, game.SCREEN_WIDTH-30),
                    randint(0, game.SCREEN_HEIGHT-45)
                )
            )
        else:
            self.rect = self.image.get_rect(
                topleft=(0, 0)
            )
    
    def __repr__(self) -> str:
        return f"{self.type} at {self.rect[0:2]}"


class Market():
    def __init__( self) -> None:
        self.oil_base_price: int = 5
        self.oil_min_price: int = 2
        self.oil_modifier = 0.5

        self.stone_base_price: int = 7
        self.stone_min_price: int = 3
        self.stone_modifier = 0.5

        self.uranium_base_price: int = 10
        self.uranium_min_price: int = 4
        self.uranium_modifier = 0.5


    def resource_price(self, resources: list[GameElement]) -> dict:
        oil = len([r for r in resources if r.type == "Oil"])
        stones = len([r for r in resources if r.type == "Stones"])
        uranium = len([r for r in resources if r.type == "Uranium"])

        oil_price = self.oil_base_price - self.oil_modifier * oil
        stone_price = self.stone_base_price - self.stone_modifier * stones
        uranium_price = self.uranium_base_price - self.uranium_modifier * uranium

        return {
            "oil": self.oil_min_price if oil_price < self.oil_min_price else oil_price,
            "uranium": self.uranium_min_price if uranium_price < self.uranium_min_price else uranium_price,
            "stones": self.stone_min_price if stone_price < self.stone_min_price else stone_price
        }