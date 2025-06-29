import pygame

class ProgressBar(pygame.sprite.Sprite):
    def __init__(self, 
                 surface: pygame.Surface, 
                 height, 
                 foreground_color: tuple[int, int, int] = (255,255,255),
                 background_color: tuple[int, int, int] = (128,128,128)):
        super().__init__()

        self.surface = surface

        self.bar_width = self.surface.width
        self.bar_height = height
        
        self.foreground_color = foreground_color
        self.background_color = background_color


    def update_bar(self, times: tuple[int, int]):
        self.current_value, self.max_value = times
        
        # 绘制背景
        pygame.draw.rect(self.surface, self.background_color, (0, 0, self.bar_width, self.bar_height))

        # 计算前景宽度
        fill_width = int((self.current_value / self.max_value) * self.bar_width)
        if fill_width > 0:
            pygame.draw.rect(self.surface, self.foreground_color, (0, 0, fill_width, self.bar_height))
    
    def set_foreground_color(self, color: tuple[int, int, int]):
        self.foreground_color = color
        self.update_bar()

    def set_background_color(self, color: tuple[int, int, int]):
        self.background_color = color
        self.update_bar()
