import pygame


class ColoredTextSprite(pygame.sprite.Sprite):
    def __init__(self, text, color, center):
        super().__init__()
        self.image = pygame.font.Font(size=30).render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = center

    @staticmethod
    def perfect(center):
        return ColoredTextSprite("Perfect", (255, 122, 0), center)

    @staticmethod
    def great(center):
        return ColoredTextSprite("Great", (255, 63, 134), center)

    @staticmethod
    def good(center):
        return ColoredTextSprite("Good", (22, 255, 123), center)

    @staticmethod
    def miss(center):
        return ColoredTextSprite("Miss", (108, 108, 108), center)

