import pygame
from config import *


class Marker(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((5, 50))
        self.image.fill((45, 222, 235))
        self.image.set_alpha(255)
        self.rect = self.image.get_rect()

    def dec_alpha(self):
        self.image.set_alpha(self.image.get_alpha() * 3 / 4)


class DeltaBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((800, 30))
        self.image.fill((108, 108, 108))
        self.image.fill((22, 255, 123), (400 - 2 * GOOD_INTERVAL, 0, 4 * GOOD_INTERVAL, 30))
        self.image.fill((255, 63, 134), (400 - 2 * GREAT_INTERVAL, 0, 4 * GREAT_INTERVAL, 30))
        self.image.fill((255, 122, 0), (400 - 2 * PERFECT_INTERVAL, 0, 4 * PERFECT_INTERVAL, 30))
        self.rect = self.image.get_rect()
        self.markers: list[Marker] = []

    def add_marker(self, marker: Marker, delta: float):
        self.markers.append(marker)
        for g in self.groups():
            g.add(marker)
        marker.rect.center = self.rect.center[0] + 2 * delta, self.rect.center[1]
        for m in self.markers:
            m.dec_alpha()
        if len(self.markers) > 8:
            for m in self.markers[0: -8]:
                m.kill()
            self.markers = self.markers[-8:]


