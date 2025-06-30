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
    def __init__(self):
        self.name = None
        self.bpm = None
        self.duration_ms = None
        self.difficulty = None
        self.cover_path = None
        self.music_path = None
        self.chart_path = None

    def is_complete(self):
        return all([self.name, self.bpm, self.duration_ms, self.difficulty,
                    self.cover_path, self.music_path, self.chart_path])


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
        self.chart_diffi_label = gui.elements.UILabel(
            pygame.Rect(ts[0] * 0.05, ts[1] * 0.5, ts[0] * 0.3, 50),
            "difficulty:", manager=self.import_mgr, container=self.import_menu)
        self.chart_diffi_entry = gui.elements.UITextEntryLine(
            pygame.Rect(ts[0] * 0.38, ts[1] * 0.5, ts[0] * 0.3, 50),
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
        self.import_save_button = gui.elements.UIButton(
            pygame.Rect(ts[0] * 0.7, ts[1] * 0.5, ts[0] * 0.25, 50),
            "Save", manager=self.import_mgr, container=self.import_menu)
        self.import_save_button.disable()  # Initially disable save button until all fields are filled
        self.import_quit_button = gui.elements.UIButton(
            pygame.Rect(ts[0] * 0.4, ts[1] * 0.6, ts[0] * 0.25, 50),
            "Quit", manager=self.import_mgr, container=self.import_menu)
        

        self.flag = 0
        self.img_file_dialog = None
        self.music_file_dialog = None
        self.chart_file_dialog = None
        self.info = None

    def get_path(self, file_path: str):
        match self.flag:
            case 1:  # cover
                self.info.cover_path = file_path
                self.import_cover_button.set_text(os.path.basename(file_path))
            case 2:  # music
                self.info.music_path = file_path
                self.import_music_button.set_text(os.path.basename(file_path))
            case 3:  # chart
                self.info.chart_path = file_path
                self.import_chart_button.set_text(os.path.basename(file_path))

    def save_chart(self):
        div_path = chart_generater.generate_chart_div(self.info.name)   
        chart_generater.generate_cover(self.info.cover_path, div_path)
        chart_generater.generate_music(self.info.music_path, div_path)
        chart_generater.generate_chart(self.info.chart_path, div_path, self.info.name,
                                                               self.info.duration_ms, self.info.bpm)    

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
                            self.info = basicinfo()
                        case self.exit_button:
                            return scenes.MainScene(self.main_window, self.clock), [], {}
                        case self.import_quit_button:
                            self.import_menu.hide()
                            self.detailed = False
                            self.import_button.enable()
                            self.info = None
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
                        case self.import_save_button:
                            if self.info and self.info.is_complete():
                                self.save_chart()
                        case self.import_chart_button:
                            self.flag = 3
                            self.chart_file_dialog = gui.windows.UIFileDialog(
                                rect = pygame.Rect(0.25 * WD_WID, 0.2 * WD_HEI, 0.7 * WD_WID, 0.75 * WD_HEI),
                                manager = self.import_mgr,
                                window_title = 'Choose Chart File',
                                allow_picking_directories = False,
                                allowed_suffixes =  ['.osu'], # 根据需求筛选
                                always_on_top = True
                            )
                            # self.chart_file_dialog.show()
                elif event.type == gui.UI_TEXT_ENTRY_FINISHED:
                    if event.ui_element == self.chart_name_entry:
                        self.info.name = event.text
                    elif event.ui_element == self.chart_bpm_entry:
                        try:
                            self.info.bpm = int(event.text)
                        except ValueError:
                            self.info.bpm = 0
                    elif event.ui_element == self.chart_dura_entry:
                        try:
                            self.info.duration_ms = int(event.text)
                        except ValueError:
                            self.info.duration_ms = 0
                    elif event.ui_element == self.chart_diffi_entry:
                        try:
                            self.info.difficulty = int(event.text)
                        except ValueError:
                            self.info.difficulty = 0
                elif event.type == gui.UI_FILE_DIALOG_PATH_PICKED:
                    self.get_path(event.text)
                    # print(f"Selected path: {event.text}")
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
            if self.info and self.info.is_complete():
                self.import_save_button.enable()
            else:
                self.import_save_button.disable()
            self.uimgr.draw_ui(self.main_window)
            self.import_mgr.draw_ui(self.main_window)
            pygame.display.flip()

        # pygame.display.set_caption("Import Chart")
        # pygame.display.set_icon(pygame.image.load(resource_path('res/img/PKUGeon.png')))