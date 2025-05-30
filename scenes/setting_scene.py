import gamedata.track_file
import time
import event_number as en
import scenes
import pygame
from pygame import Rect
import pygame_gui as gui

from game_renderer import GameRenderer
from gamedata.user_profile import UserProfile
from gamedata.mediaplayer import MediaPlayer, SEID
from config import *

class SettingScene(scenes.Scene):
    def __init__(self, main_window: pygame.Surface, clock: pygame.time.Clock):
        super().__init__(main_window, clock)
        self.uimgr = gui.UIManager((WD_WID, WD_HEI), theme_path='res/theme/setting.json')
        self.profile = UserProfile()
        # 延迟说明与滑块
        self.latency_label = gui.elements.UILabel(
            Rect(WD_WID * 0.05, WD_HEI * 0.065, WD_WID * 0.06, WD_HEI * 0.028), "latency(ms):", self.uimgr)
        self.latency_slider = gui.elements.UIHorizontalSlider(
            Rect(WD_WID * 0.125, WD_HEI * 0.093, WD_WID * 0.11, WD_HEI * 0.037), self.profile.latency, (-200, 200), self.uimgr)
        self.latency_entry = gui.elements.UITextEntryLine(
            Rect(WD_WID * 0.26, WD_HEI * 0.093, WD_WID * 0.031, WD_HEI * 0.037), self.uimgr)
        self.latency_entry.set_text(str(self.profile.latency))
        # 流速说明与滑块
        self.flow_label = gui.elements.UILabel(
            Rect(WD_WID * 0.05, WD_HEI * 0.12, WD_WID * 0.06, WD_HEI * 0.028), "flow speed:", self.uimgr)
        self.flow_speed_slider = gui.elements.UIHorizontalSlider(
            Rect(WD_WID * 0.125, WD_HEI * 0.148, WD_WID * 0.11, WD_HEI * 0.037), self.profile.flow_speed, (1, 10), self.uimgr)
        self.flow_entry = gui.elements.UITextEntryLine(
            Rect(WD_WID * 0.26, WD_HEI * 0.148, WD_WID * 0.031, WD_HEI * 0.037), self.uimgr)
        self.flow_entry.set_text(str(self.profile.flow_speed))
        # 键位绑定按钮
        self.key_buttons = []
        for i, path in enumerate(['path_0', 'path_1', 'path_2', 'path_3']):
            btn = gui.elements.UIButton(Rect(WD_WID * 0.05, WD_HEI * 0.204 + i * WD_HEI * 0.056, WD_WID * 0.104, WD_HEI * 0.037),
                                        f"{path}: {pygame.key.name(self.profile.get_key(path))}", manager=self.uimgr)
            self.key_buttons.append(btn)
        # 辅助延迟校准
        self.calibrate_button = gui.elements.UIButton(Rect(WD_WID * 0.05, WD_HEI * 0.463, WD_WID * 0.104, WD_HEI * 0.037), "latency test", manager=self.uimgr)
        self.save_button = gui.elements.UIButton(Rect(WD_WID * 0.182, WD_HEI * 0.463, WD_WID * 0.104, WD_HEI * 0.037), "save", manager=self.uimgr)
        self.back_button = gui.elements.UIButton(Rect(WD_WID * 0.313, WD_HEI * 0.463, WD_WID * 0.104, WD_HEI * 0.037), "back", manager=self.uimgr)
        self.waiting_for_key = None
        self.calibrating = False
        self.calibration_start_time = 0
        self.calibration_round = 0
        self.expected_time = 0
        self.real_time = 0
        self.delta_sum = 0
        self.calibrate_banned_group = [self.latency_slider, self.latency_entry, self.flow_speed_slider, self.flow_entry,
                                       self.calibrate_button, self.save_button, self.back_button] + self.key_buttons
        self.calibrate_popup: gui.windows.UIMessageWindow = None



    def main_loop(self, *args, **kwargs):
        running = True
        while running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None, [], {}
                # 滑块同步到输入框
                if event.type == gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == self.latency_slider:
                        value = int(self.latency_slider.get_current_value())
                        self.profile.latency = value
                        self.latency_entry.set_text(str(value))
                    elif event.ui_element == self.flow_speed_slider:
                        value = float(self.flow_speed_slider.get_current_value())
                        self.profile.flow_speed = value
                        self.flow_entry.set_text(str(value))
                # 输入框同步到滑块
                if event.type == gui.UI_TEXT_ENTRY_FINISHED:
                    if event.ui_element == self.latency_entry:
                        try:
                            value = int(self.latency_entry.get_text())
                            value = max(-200, min(200, value))
                            self.profile.latency = value
                            self.latency_slider.set_current_value(value)
                        except ValueError:
                            pass
                    elif event.ui_element == self.flow_entry:
                        try:
                            value = float(self.flow_entry.get_text())
                            value = max(1, min(10, value))
                            self.profile.flow_speed = value
                            self.flow_speed_slider.set_current_value(value)
                        except ValueError:
                            pass
                # 处理键位绑定
                if event.type == gui.UI_BUTTON_PRESSED:
                    if event.ui_element in self.key_buttons:
                        idx = self.key_buttons.index(event.ui_element)
                        self.waiting_for_key = idx
                        # Store the original key binding
                        self.original_binding = self.profile.key_bindings[f'path_{idx}']
                        self.key_buttons[idx].set_text("Press the new key...")
                    elif event.ui_element == self.calibrate_button:
                        self.start_calibration()
                    elif event.ui_element == self.save_button:
                        self.profile.update()
                    elif event.ui_element == self.back_button:
                        return scenes.MainScene(self.main_window, self.clock), [], {}
                # 捕获键盘事件用于键位绑定
                if self.waiting_for_key is not None and event.type == pygame.KEYDOWN:
                    path = f'path_{self.waiting_for_key}'
                    keyname = pygame.key.name(event.key)
                    # Check if keyname is a single letter
                    if len(keyname) == 1:
                        self.profile.key_bindings[path] = [getattr(pygame, "K_" + keyname), "K_" + keyname]
                        self.key_buttons[self.waiting_for_key].set_text(f"{path}: {keyname}")
                    else:
                        # Restore original binding
                        self.profile.key_bindings[path] = self.original_binding
                        self.key_buttons[self.waiting_for_key].set_text(f"{path}: {pygame.key.name(self.original_binding[0])}")
                    self.waiting_for_key = None
                self.uimgr.process_events(event)
                if self.calibrate_popup is not None:
                    self.calibrate_popup.process_event(event)
                    if (event.type == gui.UI_BUTTON_PRESSED
                            and (event.ui_element == self.calibrate_popup.dismiss_button
                                 or event.ui_element == self.calibrate_popup.close_window_button)):
                        self.calibrate_popup = None
                        self.calibrating = True
                        pygame.time.set_timer(pygame.Event(en.CALIBRATION, {'idx': 0}), 1000)
                if self.calibrating:
                    self.calibrate_process(event)

            self.uimgr.update(time_delta)
            self.main_window.fill((255, 255, 255))
            self.uimgr.draw_ui(self.main_window)
            pygame.display.flip()

    def start_calibration(self):
        for c in self.calibrate_banned_group:
            c.disable()
        self.calibration_round = 0
        self.delta_sum = 0
        self.real_time = None
        self.expected_time = None
        self.calibrate_popup = gui.windows.UIMessageWindow(Rect(WD_WID * 0.3, WD_HEI * 0.3, WD_WID * 0.4, WD_HEI * 0.4),
                                                           r"Next, you will hear four sets of sounds. Each set consists of three evenly spaced 'beep' sounds. Your task is to press the key as accurately as possible when the third 'beep' occurs. For the first set, press the key corresponding to path_0; for the second set, press the key corresponding to path_1, and so on. Press the 'dismiss' button when you're ready to begin.",
                                                           self.uimgr)

    def calibrate_process(self, event: pygame.event.Event):
        if event.type == en.CALIBRATION:
            idx = event.dict['idx']
            if idx == 0 or idx == 1:
                MediaPlayer.global_player.play_sound_effect(SEID.CALIBRATION)
                pygame.time.set_timer(pygame.Event(en.CALIBRATION, {'idx': idx + 1}), 700, 1)
            elif idx == 2:
                MediaPlayer.global_player.play_sound_effect(SEID.GAME_PERFECT)
                self.expected_time = time.time() * 1000
        elif event.type == pygame.KEYDOWN:
            if event.key == self.profile.get_key(f"path_{self.calibration_round}"):
                self.real_time = time.time() * 1000
        if self.real_time is not None and self.expected_time is not None:
            self.delta_sum += self.real_time - self.expected_time
            self.real_time = None
            self.expected_time = None
            if self.calibration_round < PATHS - 1:
                self.calibration_round += 1
                pygame.time.set_timer(pygame.Event(en.CALIBRATION, {'idx': 0}), 1400, 1)
            else:
                self.end_calibration()

    def end_calibration(self):
        for c in self.calibrate_banned_group:
            c.enable()
        value = self.delta_sum / PATHS
        self.profile.latency = value
        self.latency_entry.set_text(str(value))
        self.latency_slider.set_current_value(value)
        self.calibrating = False

