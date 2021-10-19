from pygame.sprite import Sprite
from pygame import Surface, Rect, mask

import game
from random import randint

class Player():
    def __init__( self) -> None:
        self.money:int = 50
        self.oil:int = 0
        self.uranium:int = 0
        self.stones:int = 0


class Token(Sprite):
    def __init__(self, type: str, surface: Surface, random:bool=True) -> None:
        super().__init__()
        self.image = surface 
        self.type = type
        self.mask = mask.from_surface(surface)
        if random:
            self.rect: Rect = self.image.get_rect(
                topleft=(
                    randint(game.MENU_WIDTH, game.SCREEN_WIDTH-30),
                    randint(0, game.SCREEN_HEIGHT-45)
                )
            )
        else:
            self.rect = self.image.get_rect(
                topleft=(
                    game.MENU_WIDTH,
                    0
                    )
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


    def resource_price(self, resources: list[Token]) -> dict:
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