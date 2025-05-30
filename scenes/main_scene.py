import pygame
import pygame_gui as gui

import gamedata.track_file
import scenes
from config import *
from game_renderer import GameRenderer
from gamedata.user_profile import UserProfile


class MainScene(scenes.Scene):
    def __init__(self, main_window: pygame.Surface, clock: pygame.Clock):
        super().__init__(main_window, clock)
        # TODO
        self.songname = "supernova"

        self.uimgr = gui.UIManager((WD_WID, WD_HEI))

        self.start_button = gui.elements.UIButton(pygame.Rect((100, 100), (200, 100)),
                                                  "Start", manager=self.uimgr)
        self.exit_button = gui.elements.UIButton(pygame.Rect((100, 500), (200, 100)),
                                                 "Quit", manager=self.uimgr)
        self.chart_maker_button = gui.elements.UIButton(pygame.Rect((100, 300), (200, 100)),
                                                        "Chart Maker", manager=self.uimgr)
        self.settings_button = gui.elements.UIButton(pygame.Rect((500, 100), (200, 100)),
                                                     "Settings", manager=self.uimgr)
        self.chart_maker_button.disable()
        self.title_label = gui.elements.UILabel(pygame.Rect(WD_WID * 0.3, WD_HEI * 0.2, WD_WID * 0.4, 50),
                                                "PKUgeon",  manager=self.uimgr)

        self.demo = GameRenderer(UserProfile(), gamedata.track_file.read_track_file(self.songname))
        self.demo_over = False

    def main_loop(self, *args, **kwargs) -> tuple[scenes.Scene | None, list, dict]:
        going = True

        while going:
            for event in pygame.event.get():
                self.demo.process_events(event)
                if event.type == pygame.QUIT:
                    return None, [], {}
                elif event.type == gui.UI_BUTTON_PRESSED:
                    match event.ui_element:
                        case self.start_button:
                            return (scenes.ChartInfoScene(self.main_window, self.clock), [],
                                    {'trackfile': gamedata.track_file.read_track_file(self.songname)})
                        case self.exit_button:
                            return None, [], {}
                        case self.chart_maker_button:
                            print("chart maker not implemented")
                        case self.settings_button:
                            return (scenes.SettingScene(self.main_window, self.clock), [], {})
                self.uimgr.process_events(event)
            delta = self.clock.tick(FPS)
            for i in range(PATHS):
                self.demo.key_down(i, True)
                self.demo.key_up(i, True)
            self.uimgr.update(delta / 1000)
            self.demo.update(delta)
            self.main_window.fill((255, 255, 255))
            self.main_window.blit(self.demo.render(), (WD_WID / 2, 0))
            self.uimgr.draw_ui(self.main_window)

            pygame.display.flip()


def test():
    pygame.init()
    window = pygame.display.set_mode((WD_WID, WD_HEI))
    clock = pygame.time.Clock()
    mainscn = MainScene(window, clock)
    mainscn.main_loop()


if __name__ == "__main__":
    test()
