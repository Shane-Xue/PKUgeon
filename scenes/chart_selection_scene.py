import pygame
import pygame_gui as gui

import scenes
from gamedata.track_file import read_track_file
from scenes.scene import Scene
from config import *
from utils.infogetter import TrackInfoGetter


class ChartSelectionScene(Scene):
    def __init__(self, main_window: pygame.Surface, clock: pygame.time.Clock):
        super().__init__(main_window, clock)

        self.uimgr = gui.UIManager((WD_WID, WD_HEI), theme_path='res/theme/chart_selection.json')
        self.back_button = gui.elements.UIButton(pygame.Rect(0.05 * WD_WID, 0.90 * WD_HEI, 0.05 * WD_WID, 0.05 * WD_HEI),
                 'Back', self.uimgr, object_id='#centered_button')
        self.selection_container = gui.elements.UIScrollingContainer(
            pygame.Rect(0.5 * WD_WID, 0.1 * WD_HEI, 0.45 * WD_WID, 0.8 * WD_HEI),
            self.uimgr,
            should_grow_automatically=True,
            allow_scroll_x=False,
            allow_scroll_y=True,
        )
        self.charts = [
            gui.elements.UIButton(
                pygame.Rect(0, i * 0.12 * WD_HEI, 0.45 * WD_WID, 0.1 * WD_HEI),
                f"{track['title']} BPM:{track['bpm']} LV{0}",
                self.uimgr,
                self.selection_container,
                text_kwargs={'file_name': track['file_name']},
            ) for i, track in enumerate(TrackInfoGetter().get_tracks(True))
        ]

    def main_loop(self, *args, **kwargs) -> tuple[Scene | None, list, dict]:
        going = True
        selected = None

        while going:
            for event in pygame.event.get():
                self.uimgr.process_events(event)
                if event.type == pygame.QUIT:
                    return None, [], {}
                elif event.type == gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.back_button:
                        return scenes.MainScene(self.main_window, self.clock), [], {}
                    if event.ui_element == selected: # Second Click
                        return scenes.GameScene(self.main_window, self.clock), [], \
                            {'trackfile': read_track_file(event.ui_element.text_kwargs['file_name'])}
                    else: # First Click
                        print(event.ui_element.colours.keys())
                        if selected is not None:
                            selected.unselect()
                        selected = event.ui_element
                        event.ui_element.select()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return scenes.MainScene(self.main_window, self.clock), [], {}
            delta = self.clock.tick(FPS)
            self.uimgr.update(delta / 1000)
            self.main_window.fill(THEME_COLOR)
            self.uimgr.draw_ui(self.main_window)

            pygame.display.flip()
