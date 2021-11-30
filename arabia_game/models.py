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
    def __init__(
        self,
        type: str,
        surface: Surface,
        random:bool=False,
        **kwargs
    ) -> None:
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
                topleft=(kwargs["x"], kwargs["y"])
            )
    
    def __repr__(self) -> str:
        return f"{self.type} at {self.rect[0:2]}"


class Resource(GameElement):
    def __init__(
        self,
        type: str,
        surface: Surface,
        inside_cost: int,
        outside_cost: int,
        random:bool=True,
        **kwargs
        ) -> None:
            super().__init__(type, surface, random, **kwargs)
            self.inside_cost = inside_cost
            self.outside_cost = outside_cost


class Market():
    def __init__(self) -> None:
        self.prices: dict = {
            "oil": 5,
            "uranium": 10,
            "stones": 7
        }

        self.modifiers: dict = {
            "oil": 0.7,
            "stones": 0.8,  
            "uranium": 1.0,
        }

    def modify_price(self, resource_type: str) -> None:
        self.prices[resource_type] -= self.modifiers[resource_type]
        print(f"Modified {resource_type} price by -{self.modifiers[resource_type]}")