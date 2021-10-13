from pygame.image import load


def load_surface(name, with_alpha=True):
    path = f"assets/sprites/{name}"
    loaded_surface = load(path)

    if with_alpha:
        return loaded_surface.convert_alpha()
    else:
        return loaded_surface.convert()