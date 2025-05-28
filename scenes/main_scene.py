import pygame
import pygame_gui as gui
import scenes
from config import *


class MainScene(scenes.Scene):
    def __init__(self, main_window: pygame.Surface, clock: pygame.Clock):
        super().__init__(main_window, clock)
        self.uimgr = gui.UIManager((WD_WID, WD_HEI))

        self.start_button = gui.elements.UIButton(pygame.Rect((100, 100), (200, 100)),
                                                  "start", manager=self.uimgr)
        self.exit_button = gui.elements.UIButton(pygame.Rect((100, 500), (200, 100)),
                                                 "quit", manager=self.uimgr)
        self.chart_maker_button = gui.elements.UIButton(pygame.Rect((100, 300), (200, 100)),
                                                        "chart maker", manager=self.uimgr)
        self.chart_maker_button.disable()
        self.title_label = gui.elements.UILabel(pygame.Rect(WD_WID * 0.3, WD_HEI * 0.2, WD_WID * 0.4, 50),
                                                "PKUgeon",  manager=self.uimgr)

    def main_loop(self, *args, **kwargs) -> tuple[scenes.Scene | None, list, dict]:
        going = True

        while going:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None, [], {}
                elif event.type == gui.UI_BUTTON_PRESSED:
                    match event.ui_element:
                        case self.start_button:
                            return (scenes.ChartInfoScene(self.main_window, self.clock), [],
                                    {'trackfile_name': 'demo'})
                        case self.exit_button:
                            return None, [], {}
                        case self.chart_maker_button:
                            print("chart maker not implemented")
                self.uimgr.process_events(event)
            delta = self.clock.tick(FPS)
            self.uimgr.update(delta / 1000)

            self.main_window.fill((255, 255, 255))
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
