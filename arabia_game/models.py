from pygame.sprite import Sprite
from pygame import Surface, Rect, mask

import game
from random import randint

class Player():
    def __init__( self) -> None:
        self.money = 50
        self.oil = 0
        self.uranium = 0
        self.stones = 0

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

