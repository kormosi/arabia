from pygame.sprite import Sprite
from pygame import Surface, Rect

import game
from random import randint

class Player():
    def __init__(self) -> None:
        pass

class Token(Sprite):
    def __init__(self, type: str, surface: Surface) -> None:
        super().__init__()
        self.image = surface 
        self.type = type
        self.rect: Rect = self.image.get_rect(
            topleft=(
                randint(game.MENU_WIDTH, game.SCREEN_WIDTH-30),
                randint(0, game.SCREEN_HEIGHT-45)
            )
        )
    
    def __repr__(self) -> str:
        return f"{self.type} at {self.rect[0:2]}"