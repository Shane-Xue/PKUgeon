import os

import pygame
import pygame_gui as gui

import gamedata.track_file
import scenes
from config import *
from game_renderer import GameRenderer
from gamedata.mediaplayer import MediaPlayer
from gamedata.user_profile import UserProfile
import event_number as en
import chart_generater

class basicinfo:
    def __init__(self, name: str, bpm: int, duration_ms: int):
        self.name = name
        self.bpm = bpm
        self.duration_ms = duration_ms


class ChartImportScene(scenes.Scene):
    def __init__(self, main_window: pygame.Surface, clock: pygame.Clock):
        super().__init__(main_window, clock)

        self.uimgr = gui.UIManager((WD_WID, WD_HEI),
                                   theme_path=resource_path('res/theme/chart_import.json'))

        self.import_button = gui.elements.UIButton(
            pygame.Rect((WD_WID * 0.05, WD_HEI * 0.44), (WD_WID * 0.1, WD_HEI * 0.09)),
            "Import Chart", manager=self.uimgr)
        self.exit_button = gui.elements.UIButton(
            pygame.Rect((WD_WID * 0.05, WD_HEI * 0.8), (WD_WID * 0.1, WD_HEI * 0.09)),
            "Back", manager=self.uimgr)
        self.title_label = gui.elements.UILabel(pygame.Rect(WD_WID * 0.05, WD_HEI * 0.18, WD_WID * 0.4, 100),
                                                "Import Chart", manager=self.uimgr)
        
        self.detailed = False
        self.import_mgr = gui.UIManager((WD_WID, WD_HEI),
                                   theme_path=resource_path('res/theme/chart_import_detail.json'))
        self.import_menu = gui.core.UIContainer(
            pygame.Rect(0.25 * WD_WID, 0.2 * WD_HEI, 0.65 * WD_WID, 0.7 * WD_HEI),
            manager=self.import_mgr,
            object_id='#import_panel'
        )
        self.import_menu.hide()
        ts = self.import_menu.rect.size
        self.chart_name_label = gui.elements.UILabel(
            pygame.Rect(ts[0] * 0.05, ts[1] * 0.2, ts[0] * 0.3, 50),
            "Chart Name:", manager=self.import_mgr, container=self.import_menu)
        self.chart_name_entry = gui.elements.UITextEntryLine(
            pygame.Rect(ts[0] * 0.38, ts[1] * 0.2, ts[0] * 0.3, 50),
            manager=self.import_mgr, container=self.import_menu,)
        self.chart_bpm_label = gui.elements.UILabel(
            pygame.Rect(ts[0] * 0.05, ts[1] * 0.3, ts[0] * 0.3, 50),
            "bpm:", manager=self.import_mgr, container=self.import_menu)
        self.chart_bpm_entry = gui.elements.UITextEntryLine(
            pygame.Rect(ts[0] * 0.38, ts[1] * 0.3, ts[0] * 0.3, 50),
            manager=self.import_mgr, container=self.import_menu,)
        self.chart_dura_label = gui.elements.UILabel(
            pygame.Rect(ts[0] * 0.05, ts[1] * 0.4, ts[0] * 0.3, 50),
            "duration(ms):", manager=self.import_mgr, container=self.import_menu)
        self.chart_dura_entry = gui.elements.UITextEntryLine(
            pygame.Rect(ts[0] * 0.38, ts[1] * 0.4, ts[0] * 0.3, 50),
            manager=self.import_mgr, container=self.import_menu,)
        self.import_cover_button = gui.elements.UIButton(
            pygame.Rect(ts[0] * 0.7, ts[1] * 0.2, ts[0] * 0.25, 50),
            "Upload Cover", manager=self.import_mgr, container=self.import_menu)
        self.import_music_button = gui.elements.UIButton(
            pygame.Rect(ts[0] * 0.7, ts[1] * 0.3, ts[0] * 0.25, 50),
            "Upload Music", manager=self.import_mgr, container=self.import_menu)
        self.import_chart_button = gui.elements.UIButton(
            pygame.Rect(ts[0] * 0.7, ts[1] * 0.4, ts[0] * 0.25, 50),
            "Upload Chart", manager=self.import_mgr, container=self.import_menu)
        self.import_quit_button = gui.elements.UIButton(
            pygame.Rect(ts[0] * 0.38, ts[1] * 0.5, ts[0] * 0.3, 50),
            "Quit", manager=self.import_mgr, container=self.import_menu)
        

        self.flag = 0
        self.img_file_dialog = None
        self.music_file_dialog = None
        self.chart_file_dialog = None


    def main_loop(self, *args, **kwargs) -> tuple[scenes.Scene | None, list, dict]:
        running = True
        while running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                self.uimgr.process_events(event)
                self.import_mgr.process_events(event)
                if event.type == pygame.QUIT:
                    return None, [], {}
                elif event.type == gui.UI_BUTTON_PRESSED:
                    match event.ui_element:
                        case self.import_button:
                            self.import_menu.show() 
                            self.detailed = True
                            self.import_button.disable()
                        case self.exit_button:
                            return scenes.MainScene(self.main_window, self.clock), [], {}
                        case self.import_quit_button:
                            self.import_menu.hide()
                            self.detailed = False
                            self.import_button.enable()
                            self.flag = 0
                        case self.import_cover_button:
                            self.flag = 1
                            self.img_file_dialog = gui.windows.UIFileDialog(
                                rect = pygame.Rect(0.25 * WD_WID, 0.2 * WD_HEI, 0.7 * WD_WID, 0.75 * WD_HEI),
                                manager = self.import_mgr,
                                window_title = 'Choose Cover File',
                                allow_picking_directories = False,
                                allowed_suffixes =  ['.png'], # 根据需求筛选
                                always_on_top = True
                            )
                            # self.img_file_dialog.show()
                        case self.import_music_button:
                            self.flag = 2
                            self.music_file_dialog = gui.windows.UIFileDialog(
                                rect = pygame.Rect(0.25 * WD_WID, 0.2 * WD_HEI, 0.7 * WD_WID, 0.75 * WD_HEI),
                                manager = self.import_mgr,
                                window_title = 'Choose Music File',
                                allow_picking_directories = False,
                                allowed_suffixes =  ['.mp3'], # 根据需求筛选
                                always_on_top = True 
                            )
                            # self.music_file_dialog.show()
                        case self.import_chart_button:
                            self.flag = 3
                            self.chart_file_dialog = gui.windows.UIFileDialog(
                                rect = pygame.Rect(0.25 * WD_WID, 0.2 * WD_HEI, 0.7 * WD_WID, 0.75 * WD_HEI),
                                manager = self.import_mgr,
                                window_title = 'Choose Chart File',
                                allow_picking_directories = False,
                                allowed_suffixes =  ['.json'], # 根据需求筛选
                                always_on_top = True
                            )
                            # self.chart_file_dialog.show()
                elif event.type == gui.UI_TEXT_ENTRY_FINISHED:
                    if event.ui_element == self.chart_name_entry:
                        self.chart_name = event.text
                    elif event.ui_element == self.chart_bpm_entry:
                        try:
                            self.chart_bpm = int(event.text)
                        except ValueError:
                            self.chart_bpm = 120
                    elif event.ui_element == self.chart_dura_entry:
                        try:
                            self.chart_dura = int(event.text)
                        except ValueError:
                            self.chart_dura = 0
                elif event.type == gui.UI_FILE_DIALOG_PATH_PICKED:
                    # TODO
                    continue
                elif event.type == gui.UI_WINDOW_CLOSE:
                    if event.ui_element == self.img_file_dialog:
                        self.img_file_dialog = None
                    elif event.ui_element == self.music_file_dialog:
                        self.music_file_dialog = None
                    elif event.ui_element == self.chart_file_dialog:
                        self.chart_file_dialog = None
                    self.flag = 0

                    
            self.uimgr.update(time_delta)
            self.import_mgr.update(time_delta)
            self.main_window.fill(THEME_COLOR)
            self.uimgr.draw_ui(self.main_window)
            self.import_mgr.draw_ui(self.main_window)
            pygame.display.flip()

        # pygame.display.set_caption("Import Chart")
        # pygame.display.set_icon(pygame.image.load(resource_path('res/img/PKUGeon.png')))