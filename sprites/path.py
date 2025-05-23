import pygame
from config import *


class PathSprite(pygame.sprite.Sprite):
    pathimg = pygame.image.load("./src/img/path.png")

    def __init__(self, pathid: int):
        super().__init__()
        self.id = pathid
        # tr = PathSprite.pathimg.get_rect()
        # self.image = pygame.transform.scale(PathSprite.pathimg, (WD_WID / 640 * tr[0], WD_WID / 640 * tr[1]))
        self.image = PathSprite.pathimg
        self.rect = self.image.get_rect()
        self.rect.midtop = ((pathid * 2 + 1) / (2 * PATHS) * 640, 0)

