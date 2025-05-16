import pygame
from config import *


class TapSprite(pygame.sprite.Sprite):
    tapimg = pygame.image.load("./src/img/tap.png")

    def __init__(self, gametime, decision_time, calc_midbottom, parent: pygame.sprite.Sprite = None):
        super().__init__()
        self.image = TapSprite.tapimg
        self.parent = parent
        self.rect = self.image.get_rect()
        self.calc_midbottom = calc_midbottom
        self.decision_time = decision_time
        self.update(gametime)

    def update(self, gametime):
        if self.parent is not None:
            t1 = self.calc_midbottom(gametime, self.decision_time)
            t2 = self.parent.rect.midbottom
            self.rect.midbottom = (t1[0] + t2[0], t1[1])
        else:
            self.rect.midbottom = self.calc_midbottom(gametime, self.decision_time)


def linear_calc_midbottom(flow_speed: float, decision_pos: int, init_pos: int):
    def f(gametime: float, decision_time):
        return 0, decision_pos + (init_pos - decision_pos) * (decision_time - gametime) / 5000 * flow_speed
    return f
