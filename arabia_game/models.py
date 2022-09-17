import game

from pygame import Rect, Surface, mask
from pygame.sprite import Sprite
from random import randint


class Player():
    def __init__( self) -> None:
        # Resources
        self.resources: dict[str, int] = {}
        self.resources["money"] = 50
        self.resources_to_display = 10

    def add_resource(self, resource_type: str) -> None:
        if resource_type in self.resources:
            self.resources[resource_type] += 1
        else:
            self.resources[resource_type] = 1

    def has_resource(self, resource_type: str, amount=1) -> bool:
        return (
            resource_type in self.resources
            and self.resources[resource_type] >= amount
        )


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
            # Resources
            "oil": 5,
            "uranium": 10,
            "stones": 7,
            "refined_oil": 10,
            # Tech
            "radar": 10
        }

        self.modifiers: dict = {
            # Resources
            "oil": 0.2,
            "stones": 0.3,  
            "uranium": 0.5,
            "refined_oil": 0.5,
        }

    def modify_price(self, resource_type: str) -> None:
        modifier = round(self.modifiers[resource_type], 1)
        self.prices[resource_type] -= modifier
        print(f"Modified {resource_type} price by -{modifier}")
        if randint(0, 5) == 0:
            self.prices[resource_type] += self.modifiers[resource_type] * randint(1, 3)
            print("Unpredictable price hike!")
