from pygame.sprite import Sprite
from pygame import Surface, Rect

import game
from random import randint

class Player():
    def __init__(self, money: int, oil: int) -> None:
        self.money = money
        self.oil = oil

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


saudi_arabia = [
    (482, 254),
    (476, 260),
    (470, 285),
    (465, 300),
    (487, 388),
    (536, 479),
    (570, 571),
    (606, 643),
    (668, 732),
    (692, 749),
    (705, 746),
    (730, 748),
    (732, 745),
    (733, 744),
    (739, 741),
    (744, 734),
    (744, 731),
    (739, 729),
    (741, 721),
    (743, 713),
    (751, 706),
    (756, 706),
    (764, 711),
    (776, 712),
    (794, 710),
    (816, 709),
    (822, 714),
    (839, 715),
    (853, 716),
    (869, 715),
    (876, 723),
    (882, 728),
    (893, 722),
    (893, 722),
    (903, 703),
    (921, 681),
    (954, 663),
    (1054, 646),
    (1157, 601),
    (1175, 526),
    (1157, 500),
    (1157, 503),
    (1068, 498),
    (1032, 457),
    (1033, 445),
    (1021, 436),
    (1014, 440),
    (1011, 439),
    (1004, 433),
    (991, 397),
    (987, 379),
    (988, 354),
    (957, 309),
    (942, 293),
    (922, 294),
    (897, 295),
    (891, 290),
    (888, 278),
    (858, 274),
    (854, 276),
    (798, 271),
    (716, 202),
    (667, 168),
    (623, 156),
    (615, 161),
    (552, 176),
    (582, 216),
    (570, 221),
    (564, 232),
    (539, 237),
    (531, 250),
    (517, 261),
    (483, 254),
]