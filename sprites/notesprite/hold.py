import pygame
from config import *
from sprites.abstract import AbstractNoteSprite


class HoldLineSprite(AbstractNoteSprite):

    def __init__(self, start_note: pygame.sprite.Sprite, end_note: pygame.sprite.Sprite,
                 decision_time, length):
        super().__init__(decision_time, None)
        self.start_note = start_note
        self.end_note = end_note
        self.image = pygame.surface.Surface((HOLD_LINE_WIDTH, length))
        self.image.fill((120, 93, 97))
        self.rect = self.image.get_rect()

    def update(self, gametime):
        self.rect.size = self.rect.width, self.start_note.rect.top - self.end_note.rect.bottom
        if self.rect.height > 0:
            self.rect.midtop = self.end_note.rect.midbottom
            self.image = pygame.surface.Surface((HOLD_LINE_WIDTH, self.rect.height))
            self.image.fill((120, 93, 97))
        else:
            self.image = pygame.surface.Surface((0, 0))

    @staticmethod
    def gen_default_fn(flow_speed: float, decision_pos: int, init_pos: int):
        def f(gametime: float, decision_time: float):
            return 0, decision_pos + (init_pos - decision_pos) * (decision_time - gametime) / 5000 * flow_speed - 30

        return f

    @staticmethod
    def gen_calc_length_fn(flow_speed: float, decision_pos: int, init_pos: int):
        return lambda interval: (decision_pos - init_pos) * interval / 5000 * flow_speed
