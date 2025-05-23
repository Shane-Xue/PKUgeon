import scenes
import pygame
import pygame_gui as gui
from config import *
from gamedata.score import Score


class GameOverScene(scenes.Scene):
    def __init__(self, main_window: pygame.Surface, clock: pygame.Clock):
        super().__init__(main_window, clock)
        self.uimgr = gui.UIManager((WD_WID, WD_HEI), theme_path="./src/theme/gameover.json")
        layout_rect = pygame.Rect(0, 0, WD_WID * 0.8, 50)
        layout_rect.center = (WD_WID * 0.5, WD_HEI * 0.2)
        self.badge_label = gui.elements.UILabel(layout_rect, "", self.uimgr)
        layout_rect.size = (WD_WID * 0.4, 50)
        layout_rect.center = (WD_WID * 0.25, WD_HEI * 0.3)
        self.perfects_label = gui.elements.UILabel(layout_rect, "", self.uimgr)
        layout_rect.center = (WD_WID * 0.75, WD_HEI * 0.3)
        self.greats_label = gui.elements.UILabel(layout_rect, "", self.uimgr)
        layout_rect.center = (WD_WID * 0.25, WD_HEI * 0.4)
        self.goods_label = gui.elements.UILabel(layout_rect, "", self.uimgr)
        layout_rect.center = (WD_WID * 0.75, WD_HEI * 0.4)
        self.misses_label = gui.elements.UILabel(layout_rect, "", self.uimgr)
        layout_rect.center = (WD_WID * 0.5, WD_HEI * 0.5)
        self.maxcombo_label = gui.elements.UILabel(layout_rect, "", self.uimgr)
        layout_rect.size = (WD_WID * 0.3, 50)
        layout_rect.center = (WD_WID * 0.5, WD_HEI * 0.6)
        self.score_label = gui.elements.UILabel(layout_rect, "", self.uimgr)
        layout_rect.center = (WD_WID * 0.5, WD_HEI * 0.7)
        self.retry_button = gui.elements.UIButton(layout_rect, "Retry", self.uimgr)
        layout_rect.center = (WD_WID * 0.5, WD_HEI * 0.8)
        self.exit_button = gui.elements.UIButton(layout_rect, "Exit", self.uimgr)

    def main_loop(self, *args, **kwargs) -> tuple[scenes.Scene | None, list, dict]:
        score: Score = kwargs['score']
        retry_which: str = kwargs['retry_which']

        self.badge_label.set_text(f"{'AP' if score.is_ap else '  '} {'FC+' if score.is_fcplus else '   '}"
                                  f"{'FC' if score.is_fc else '  '}")
        self.perfects_label.set_text(f"Perfect: {score.perfects}")
        self.greats_label.set_text(f"Greats: {score.greats}")
        self.goods_label.set_text(f"Goods: {score.goods}")
        self.misses_label.set_text(f"Misses: {score.misses}")
        self.maxcombo_label.set_text(f"Max Combo: {score.max_combo}")
        self.score_label.set_text(f"Score: {score.score}")

        going = True

        while going:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None, [], {}
                elif event.type == gui.UI_BUTTON_PRESSED:
                    match event.ui_element:
                        case self.retry_button:
                            return (scenes.GameScene(self.main_window, self.clock), [],
                                    {"trackfile_name": retry_which})
                        case self.exit_button:
                            return scenes.MainScene(self.main_window, self.clock), [], {}
                self.uimgr.process_events(event)
            delta = self.clock.tick(FPS)
            self.main_window.fill((255, 255, 255))
            self.uimgr.update(delta / 1000)
            self.uimgr.draw_ui(self.main_window)

            pygame.display.flip()

