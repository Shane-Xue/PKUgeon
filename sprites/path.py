import pygame
from config import *


class PathSprite(pygame.sprite.Sprite):
    pathimg = pygame.image.load("./src/img/path.png")

    def __init__(self, pathid: int):
        super().__init__()
        self.id = pathid
        self.image = PathSprite.pathimg
        self.rect = self.image.get_rect()
        self.rect.midtop = ((pathid * 2 + 1) / (2 * PATHS) * 640, 0)

