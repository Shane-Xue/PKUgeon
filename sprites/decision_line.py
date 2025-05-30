import pygame
from config import *


class DecisionLine(pygame.sprite.Sprite):
    decision_line_img = pygame.image.load('res/img/decision_line.png')

    def __init__(self):
        super().__init__()
        self.image = DecisionLine.decision_line_img
        self.rect = self.image.get_rect()
        self.rect.midtop = WD_WID / 4, DECISION_POS
