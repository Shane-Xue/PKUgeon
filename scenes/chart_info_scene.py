import gamedata.track_file
import scenes
import pygame
from pygame import Rect
import pygame_gui as gui
import event_number as en
from game_manager import GameManager
from gamedata.mediaplayer import MediaPlayer, SEID
from scenes import GameScene
from config import *
from gamedata.user_profile import UserProfile


class ChartInfoScene(scenes.Scene):

    def __init__(self, main_window: pygame.Surface, clock: pygame.time.Clock):
        super().__init__(main_window, clock)

        self.uimgr = gui.UIManager(main_window.size, theme_path='res/theme/chartinfo.json')
        cover_size = int(WD_HEI * 0.5)  # 540 is 0.5 of 1080
        self.cover = pygame.Surface((cover_size, cover_size))
        self.cover_rect = self.cover.get_rect()
        self.cover_rect.topleft = (int(WD_WID * 0.1875), int(WD_HEI * 0.1667))  # 360/1920, 180/1080

        label_width = int(WD_WID * 0.1875)  # 360/1920
        label_height = int(WD_HEI * 0.0463)  # 50/1080
        tr = Rect(0, 0, label_width, label_height)
        
        label_x = int(WD_WID * 0.625)  # 1200/1920
        tr.midleft = (label_x, int(WD_HEI * 0.2222))  # 240/1080
        self.title_label = gui.elements.UILabel(tr, "Title:", manager=self.uimgr)
        tr.midleft = (label_x, int(WD_HEI * 0.3333))  # 360/1080
        self.bpm_label = gui.elements.UILabel(tr, "BPM:", manager=self.uimgr)
        tr.midleft = (label_x, int(WD_HEI * 0.4444))  # 480/1080
        self.artist_label = gui.elements.UILabel(tr, "Artist:", manager=self.uimgr)
        tr.midleft = (label_x, int(WD_HEI * 0.5556))  # 600/1080
        self.chart_label = gui.elements.UILabel(tr, "Chart:", manager=self.uimgr)
        tr.midleft = (label_x, int(WD_HEI * 0.6667))  # 720/1080
        self.level_label = gui.elements.UILabel(tr, "Level:", manager=self.uimgr)
        tr.midleft = (label_x, int(WD_HEI * 0.7778))  # 840/1080
        self.best_label = gui.elements.UILabel(tr, "HI-score:", manager=self.uimgr)
        
        
        # Add keybinding bar at the bottom
        bar_width = int(WD_WID * 0.6)  # 60% of window width
        bar_height = int(WD_HEI * 0.05)  # 5% of window height
        margin_bottom = int(WD_HEI * 0.03)  # 3% margin from bottom
        
        tr = Rect(0, 0, bar_width, bar_height)
        tr.centerx = WD_WID // 2
        tr.bottom = WD_HEI - margin_bottom
        
        profile = UserProfile()
        key_letters = ' '.join(binding[1].split('_')[1].upper() for binding in profile.key_bindings.values())
        key_text = f"Track keys: {key_letters}"
        self.key_label = gui.elements.UILabel(
            tr, 
            key_text,
            manager=self.uimgr,
            object_id="#hint"
        )
        self.key_label.rebuild()

    def main_loop(self, *args, **kwargs):
        tf = kwargs["trackfile"]
        gamescn = GameScene(self.main_window, self.clock)

        # 加载并缩放封面图片到固定大小
        cover_img = pygame.image.load(tf.cover_img_path()).convert_alpha()
        cover_img = pygame.transform.smoothscale(cover_img, (540, 540))
        self.cover.blit(cover_img, (0, 0))
        self.title_label.set_text(f"Title: {tf.title}")
        self.bpm_label.set_text(f"BPM: {tf.bpm}")
        self.artist_label.set_text(f"Artist: {tf.artist}")
        self.chart_label.set_text(f"Chart: {tf.chart_maker}")
        self.level_label.set_text(f"Level: {tf.level}")
        self.best_label.set_text(f"Best: {None}")

        MediaPlayer.global_player.play_sound_effect(SEID.SHOW_INFO)

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

