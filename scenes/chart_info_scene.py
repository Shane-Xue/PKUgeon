import gamedata.track_file
import scenes
import pygame
from pygame import Rect
import pygame_gui as gui
import event_number as en
from game_manager import GameManager
from scenes import GameScene
from config import *


class ChartInfoScene(scenes.Scene):

    def __init__(self, main_window: pygame.Surface, clock: pygame.time.Clock):
        super().__init__(main_window, clock)

        self.uimgr = gui.UIManager(main_window.size, theme_path='res/theme/chartinfo.json')
        self.cover = pygame.Surface((540, 540))
        self.cover_rect = self.cover.get_rect()
        self.cover_rect.topleft = 360, 180
        tr = Rect(0, 0, 360, 50)
        tr.midleft = (1200, 240)
        self.title_label = gui.elements.UILabel(tr, "Title:", manager=self.uimgr)
        tr.midleft = (1200, 360)
        self.bpm_label = gui.elements.UILabel(tr, "BPM:", manager=self.uimgr)
        tr.midleft = (1200, 480)
        self.artist_label = gui.elements.UILabel(tr, "Artist:", manager=self.uimgr)
        tr.midleft = (1200, 600)
        self.chart_label = gui.elements.UILabel(tr, "Chart:", manager=self.uimgr)
        tr.midleft = (1200, 720)
        self.level_label = gui.elements.UILabel(tr, "Level:", manager=self.uimgr)
        tr.midleft = (1200, 840)
        self.best_label = gui.elements.UILabel(tr, "HI-score:", manager=self.uimgr)

    def main_loop(self, *args, **kwargs):
        tf = kwargs["trackfile"]
        gamescn = GameScene(self.main_window, self.clock)

        self.cover.blit(pygame.image.load(tf.cover_img_path()))
        self.title_label.set_text(f"Title: {tf.title}")
        self.bpm_label.set_text(f"BPM: {tf.bpm}")
        self.artist_label.set_text(f"Artist: {tf.artist}")
        self.chart_label.set_text(f"Chart: {tf.chart_maker}")
        self.level_label.set_text(f"Level: {tf.level}")
        self.best_label.set_text(f"Best: {None}")

        pygame.time.set_timer(en.EXIT_CHART_INFO, 3000, loops=1)

        while True:
            self.main_window.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None, [], {}
                elif event.type == en.EXIT_CHART_INFO:
                    return gamescn, args, kwargs
                self.uimgr.process_events(event)
            delta = self.clock.tick(FPS)
            self.uimgr.update(delta / 1000)
            self.main_window.blit(self.cover, self.cover_rect)
            self.uimgr.draw_ui(self.main_window)
            pygame.display.flip()

