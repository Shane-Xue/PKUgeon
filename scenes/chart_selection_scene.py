import pygame
import pygame_gui as gui
import pygame.mixer

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
        self.charts_lst = TrackInfoGetter().get_tracks(False)
        self.charts = [
            gui.elements.UIButton(
                pygame.Rect(0, i * 0.12 * WD_HEI, 0.45 * WD_WID, 0.1 * WD_HEI),
                f"{track['title']} BPM:{track['bpm']} LV{track['level']}",
                self.uimgr,
                self.selection_container,
                object_id = f"#track_{i}",
                text_kwargs={'file_name': track['file_name']},
            ) for i, track in enumerate(self.charts_lst)
        ]
        self.initialize_chart_info()
        self.drumbeat = pygame.mixer.Sound('res/sound/cali.ogg')
        
    
    def initialize_chart_info(self):
        self.info_mgr = gui.UIManager((WD_WID, WD_HEI), theme_path='res/theme/chart_selection.json')
        self.info_container = gui.core.UIContainer(
            pygame.Rect(0.05 * WD_WID, 0.1 * WD_HEI, 0.4 * WD_WID, 0.7 * WD_HEI),
            manager=self.info_mgr,
            object_id='#info_panel'
        )

        self.track_image = gui.elements.UIImage(
            pygame.Rect(0.1 * WD_WID, 0.20 * WD_HEI, 0.2 * WD_WID, 0.3 * WD_HEI),
            pygame.Surface((1, 1)),
            self.info_mgr,
            container=self.info_container
        )

        self.title_text = gui.elements.UILabel(
            pygame.Rect(0.1 * WD_WID, 0.5 * WD_HEI, 0.08 * WD_WID, 0.05 * WD_HEI),
            "Title:", self.info_mgr,
            container=self.info_container
        )

        self.title_value = gui.elements.UILabel(
            pygame.Rect(0.19 * WD_WID, 0.5 * WD_HEI, 0.21 * WD_WID, 0.05 * WD_HEI),
            "", self.info_mgr,
            container=self.info_container
        )

        self.artist_text = gui.elements.UILabel(
            pygame.Rect(0.1 * WD_WID, 0.55 * WD_HEI, 0.08 * WD_WID, 0.05 * WD_HEI),
            "Artist:", self.info_mgr,
            container=self.info_container
        )

        self.artist_value = gui.elements.UILabel(
            pygame.Rect(0.19 * WD_WID, 0.55 * WD_HEI, 0.21 * WD_WID, 0.05 * WD_HEI),
            "", self.info_mgr,
            container=self.info_container
        )

        # self.difficulty_text = gui.elements.UILabel(
        #     pygame.Rect(0.1 * WD_WID, 0.6 * WD_HEI, 0.08 * WD_WID, 0.05 * WD_HEI),
        #     "Difficulty:", self.info_mgr,
        #     container=self.info_container
        # )

        # self.difficulty_value = gui.elements.UILabel(
        #     pygame.Rect(0.19 * WD_WID, 0.6 * WD_HEI, 0.21 * WD_WID, 0.05 * WD_HEI),
        #     "", self.info_mgr,
        #     container=self.info_container
        # )

        self.auto_checkbox = gui.elements.UIButton(
            pygame.Rect(0.1 * WD_WID, 0.6 * WD_HEI, -1, -1),  # Moved up to 0.6
            "Autoplay Off", self.info_mgr,  # Added default unchecked symbol
            object_id='#checkbox',
            container=self.info_container
        )
        
        self.play_button = gui.elements.UIButton(
            pygame.Rect(0.1 * WD_WID, 0.65 * WD_HEI, 0.3 * WD_WID, 0.05 * WD_HEI),
            "Let's Roll!", self.info_mgr,
            container=self.info_container,
            object_id="#play_button"
        )
    
    def set_chart_info(self, track: dict):
        try:
            cover_path = os.path.join("save", "trackfile", track['file_name'], "cover.png")
            if os.path.exists(cover_path):
                cover_image = pygame.image.load(cover_path)
                # Calculate new height based on image ratio
                img_ratio = cover_image.get_height() / cover_image.get_width()
                new_height = 0.2 * WD_WID * img_ratio
                
                new_rect = pygame.Rect(
                    0.30 * WD_WID - (0.3 * WD_WID / 2),  # Center horizontally
                    0.45 * WD_HEI - new_height,  # Position from bottom
                    0.2 * WD_WID,   # Keep width
                    new_height      # Adjusted height
                )
                self.track_image.set_relative_position(new_rect.topleft)
                self.track_image.set_dimensions(new_rect.size)
                self.track_image.set_image(cover_image)
            else:
                self.track_image.set_image(pygame.Surface((1, 1)))
        except Exception:
            self.track_image.set_image(pygame.Surface((1, 1)))
            
        self.title_value.set_text(track['title'] or "Unknown")
        self.artist_value.set_text(track['artist'] or "Unknown")
    
    def begin_play(self, selected):
        self.on_exit()
        return scenes.GameScene(self.main_window, self.clock, self.auto_checkbox.is_selected), [], \
                            {'trackfile': read_track_file(selected.text_kwargs['file_name'])}
    
    
    def main_menu(self):
        self.on_exit()
        return scenes.MainScene(self.main_window, self.clock), [], {}
        
    def on_exit(self):
        self.drumbeat.stop()
        
    def main_loop(self, *args, **kwargs) -> tuple[Scene | None, list, dict]:
        going = True
        selected = None
        
        self.drumbeat.play(-1)

        while going:
            for event in pygame.event.get():
                self.uimgr.process_events(event)
                self.info_mgr.process_events(event)
                if event.type == pygame.QUIT:
                    self.on_exit()
                    return None, [], {}
                elif event.type == gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.back_button:
                        return self.main_menu()
                    elif event.ui_element == self.auto_checkbox:
                        if self.auto_checkbox.is_selected:
                            self.auto_checkbox.unselect()
                            self.auto_checkbox.set_text("Autoplay Off")
                            print("Autoplay Off")
                        else:
                            self.auto_checkbox.select()
                            self.auto_checkbox.set_text("Autoplay On")
                            print("Autoplay On")
                    elif event.ui_element == selected or event.ui_element == self.play_button: # Second Click
                        return self.begin_play(selected)
                    else: # First Click
                        if selected is not None:
                            selected.unselect()
                        selected = event.ui_element
                        event.ui_element.select()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return self.main_menu()
                    elif event.key == pygame.K_UP:
                        if selected is None:
                            selected = self.charts[-1]  # Start from bottom if nothing selected
                        else:
                            track_id = int(selected.object_ids[1].split('_')[1])
                            selected.unselect()
                            track_id = (track_id - 1) if track_id > 0 else len(self.charts) - 1
                            selected = self.charts[track_id]
                        selected.select()
                    elif event.key == pygame.K_DOWN:
                        if selected is None:
                            selected = self.charts[0]  # Start from top if nothing selected
                        else:
                            track_id = int(selected.object_ids[1].split('_')[1])
                            selected.unselect()
                            track_id = (track_id + 1) if track_id < len(self.charts) - 1 else 0
                            selected = self.charts[track_id]
                        selected.select()
                    elif event.key == pygame.K_RETURN and selected is not None:
                        return self.begin_play(selected)
            delta = self.clock.tick(FPS)
            self.uimgr.update(delta / 1000)
            self.main_window.fill(THEME_COLOR)
            self.uimgr.draw_ui(self.main_window)
            if selected is not None:
                track_id = int(selected.object_ids[1].split('_')[1])
                self.set_chart_info(self.charts_lst[track_id])
                self.info_mgr.update(delta / 1000)
                self.info_mgr.draw_ui(self.main_window)
            pygame.display.flip()
