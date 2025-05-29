import threading
import time

import pygame
from config import *


class PathSprite(pygame.sprite.Sprite):
    pathimg = pygame.image.load("./res/img/path.png")

    def __init__(self, pathid: int):
        super().__init__()
        self.unpressed_img = pygame.Surface((240, 840))
        self.unpressed_img.fill((255, 255, 255))
        pygame.draw.line(self.unpressed_img, (0, 0, 0), (120, 0), (120, 840), 5)
        pygame.draw.line(self.unpressed_img, (0, 0, 0), (0, 838), (240, 838), 5)
        self.pressed_img = pygame.Surface((240, 840))
        self.pressed_img.fill((255, 255, 255))
        pygame.draw.line(self.pressed_img, (200, 200, 200), (120, 0), (120, 840), 5)
        pygame.draw.line(self.pressed_img, (0, 0, 0), (0, 838), (240, 838), 5)
        self.image = self.unpressed_img

        self.rect = self.image.get_rect()
        self.rect.center = (pathid * 2 + 1) / (2 * PATHS) * 960, 540

    def tap(self):
        self.pressed()

        def targ():
            time.sleep(0.1)
            self.released()
        threading.Thread(target=targ).start()

    def pressed(self):
        self.image = self.pressed_img

    def released(self):
        self.image = self.unpressed_img
