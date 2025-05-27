import pygame
from config import *
from sprites.abstract import AbstractNoteSprite


class HoldLineSprite(AbstractNoteSprite):
    def __init__(self, decision_time, length, fn_calc_midbottom, parent: pygame.sprite.Sprite = None):
        super().__init__(decision_time, fn_calc_midbottom, parent)
        self.image = pygame.surface.Surface((HOLD_LINE_WIDTH, length))
        self.image.fill((0, 162, 232))
        self.rect = self.image.get_rect()

    @staticmethod
    def gen_default_fn(flow_speed: float, decision_pos: int, init_pos: int):
        def f(gametime: float, decision_time: float):
            return 0, decision_pos + (init_pos - decision_pos) * (decision_time - gametime) / 5000 * flow_speed - 30

        return f

    @staticmethod
    def gen_calc_length_fn(flow_speed: float, decision_pos: int, init_pos: int):
        return lambda interval: (decision_pos - init_pos) * interval / 5000 * flow_speed
