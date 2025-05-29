import pygame


class Marker(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 50))
        self.image.fill((45, 222, 235))
        self.image.set_alpha(255)
        self.rect = self.image.get_rect()

    def dec_alpha(self):
        self.image.set_alpha(self.image.get_alpha() * 3 / 4)


class DeltaBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((400, 30))
        self.image.fill((126, 199, 133))
        self.rect = self.image.get_rect()
        self.markers: list[Marker] = []

    def add_marker(self, marker: Marker, delta: float):
        print(delta)
        self.markers.append(marker)
        for g in self.groups():
            g.add(marker)
        marker.rect.center = self.rect.center[0] + delta, self.rect.center[1]
        for m in self.markers:
            m.dec_alpha()
        if len(self.markers) > 8:
            for m in self.markers[0: -8]:
                m.kill()
            self.markers = self.markers[-8:]


