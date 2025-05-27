import pygame
from config import *
from sprites.abstract import AbstractNoteSprite


class TapNoteSprite(AbstractNoteSprite):
    tapimg = pygame.image.load("./src/img/tap.png")

    def __init__(self, decision_time, fn_calc_midbottom, parent: pygame.sprite.Sprite = None):
        super().__init__(decision_time, fn_calc_midbottom, parent)
        self.image = TapNoteSprite.tapimg
        self.rect = self.image.get_rect()

    @staticmethod
    def gen_default_fn(flow_speed: float, decision_pos: int, init_pos: int):
        def f(gametime: float, decision_time: float):
            return 0, decision_pos + (init_pos - decision_pos) * (decision_time - gametime) / 5000 * flow_speed

        return f


class HoldStartNoteSprite(TapNoteSprite):
    def __init__(self, decision_time, bottom_pos, fn_calc_midbottom, parent: pygame.sprite.Sprite = None):
        super().__init__(decision_time, fn_calc_midbottom, parent)
        self.bottom_pos = bottom_pos

    def update(self, gametime):
        if gametime < self.decision_time:
            super().update(gametime)
        else:
            self.rect.midbottom = (self.parent.rect.midbottom[0], self.bottom_pos)