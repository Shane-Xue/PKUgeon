import threading
import time

import pygame
from config import *


class PathSprite(pygame.sprite.Sprite):
    unpressed_img = pygame.image.load(resource_path("./res/img/path.png"))
    pressed_img = pygame.image.load(resource_path("./res/img/path_hl.png"))

    def __init__(self, pathid: int):
        super().__init__()
        self.image = PathSprite.unpressed_img

        self.rect = self.image.get_rect()
        self.rect.center = (pathid * 2 + 1) / (2 * PATHS) * 960, 540

    def tap(self):
        self.pressed()

        def targ():
            time.sleep(0.1)
            self.released()
        threading.Thread(target=targ).start()

    def pressed(self):
        self.image = PathSprite.pressed_img

    def released(self):
        self.image = PathSprite.unpressed_img
