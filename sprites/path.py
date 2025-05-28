import pygame
from config import *


class PathSprite(pygame.sprite.Sprite):
    pathimg = pygame.image.load("./res/img/path.png")

    def __init__(self, pathid: int):
        super().__init__()
        # self.id = pathid
        # self.image = PathSprite.pathimg
        # self.rect = self.image.get_rect()
        # self.rect.midtop = ((pathid * 2 + 1) / (2 * PATHS) * 640, 0)
        self.image = pygame.Surface((240, 840))
        self.image.fill((255, 255, 255))
        pygame.draw.line(self.image, (0, 0, 0), (120, 0), (120, 840), 5)
        pygame.draw.line(self.image, (0, 0, 0), (0, 838), (240, 838), 5)
        self.rect = self.image.get_rect()
        self.rect.center = (pathid * 2 + 1) / (2 * PATHS) * 960, 540
