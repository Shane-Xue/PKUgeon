import pygame


class AbstractNoteSprite(pygame.sprite.Sprite):
    def __init__(self, decision_time, fn_calc_midbottom, parent: pygame.sprite.Sprite = None):
        super().__init__()
        self.parent = parent
        self.fn_calc_midbottom = fn_calc_midbottom
        self.rect = pygame.Rect()
        self.decision_time = decision_time

    def update(self, gametime):
        if self.parent is not None:
            t1 = self.fn_calc_midbottom(gametime, self.decision_time)
            t2 = self.parent.rect.midbottom
            self.rect.midbottom = (t1[0] + t2[0], t1[1])
        else:
            self.rect.midbottom = self.fn_calc_midbottom(gametime, self.decision_time)
