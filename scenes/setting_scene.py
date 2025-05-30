import scenes
import pygame
from pygame import Rect
import pygame_gui as gui
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
            Rect(100, 70, 120, 30), "latency(ms):", self.uimgr)
        self.latency_slider = gui.elements.UIHorizontalSlider(
            Rect(240, 100, 210, 40), self.profile.latency, (-200, 200), self.uimgr)
        self.latency_entry = gui.elements.UITextEntryLine(
            Rect(500, 100, 60, 40), self.uimgr)
        self.latency_entry.set_text(str(self.profile.latency))
        # 流速说明与滑块
        self.flow_label = gui.elements.UILabel(
            Rect(100, 130, 120, 30), "flow speed:", self.uimgr)
        self.flow_speed_slider = gui.elements.UIHorizontalSlider(
            Rect(240, 160, 210, 40), self.profile.flow_speed, (1, 10), self.uimgr)
        self.flow_entry = gui.elements.UITextEntryLine(
            Rect(500, 160, 60, 40), self.uimgr)
        self.flow_entry.set_text(str(self.profile.flow_speed))
        # 键位绑定按钮
        self.key_buttons = []
        for i, path in enumerate(['path_0', 'path_1', 'path_2', 'path_3']):
            btn = gui.elements.UIButton(Rect(100, 220 + i*60, 200, 40),
                                        f"{path}: {pygame.key.name(self.profile.get_key(path))}", manager=self.uimgr)
            self.key_buttons.append(btn)
        # 辅助延迟校准
        self.calibrate_button = gui.elements.UIButton(Rect(100, 500, 200, 40), "latency test", manager=self.uimgr)
        self.calibrate_button.disable()
        self.save_button = gui.elements.UIButton(Rect(350, 500, 200, 40), "save", manager=self.uimgr)
        self.back_button = gui.elements.UIButton(Rect(600, 500, 200, 40), "back", manager=self.uimgr)
        self.waiting_for_key = None  # 当前等待按键绑定的按钮索引

        # 校准相关
        self.calibrating = False
        self.calibrate_times = []
        self.calibrate_note_time = 0
        self.calibrate_audio_played = False

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
                    self.profile.key_bindings[path] = [getattr(pygame, "K_" + keyname), "K_" + keyname]
                    self.key_buttons[self.waiting_for_key].set_text(f"{path}: {keyname}")
                    self.waiting_for_key = None
                self.uimgr.process_events(event)

            # 校准逻辑
            if self.calibrating:
                self.update_calibration()

            self.uimgr.update(time_delta)
            self.main_window.fill((255, 255, 255))
            self.uimgr.draw_ui(self.main_window)
            # 校准动画
            if self.calibrating:
                self.draw_calibration()
            pygame.display.flip()

    # 辅助延迟校准相关
    def start_calibration(self):
        self.calibrating = True
        self.calibrate_times = []
        self.calibrate_note_time = pygame.time.get_ticks()
        self.calibrate_audio_played = False
        MediaPlayer.global_player.play_sound_effect(SEID.GAME_PERFECT)  # 播放音效

    def update_calibration(self):
        now = pygame.time.get_ticks()
        # 播放音效后，显示判定线动画
        if not self.calibrate_audio_played and now - self.calibrate_note_time > 500:
            MediaPlayer.global_player.play_sound_effect(SEID.GAME_PERFECT)
            self.calibrate_audio_played = True
        # 检测按键
        keys = pygame.key.get_pressed()
        if any(keys[self.profile.get_key(f'path_{i}')] for i in range(4)):
            hit_time = now - self.calibrate_note_time
            self.calibrate_times.append(hit_time)
            if len(self.calibrate_times) >= 5:
                avg = sum(self.calibrate_times) / len(self.calibrate_times)
                self.profile.latency = int(avg - 500)  # 500为理论判定点
                self.calibrating = False

    def draw_calibration(self):
        # 简单画一个判定线和下落音符
        h = self.main_window.get_height()
        w = self.main_window.get_width()
        pygame.draw.line(self.main_window, (0, 0, 0), (w//2-100, h-100), (w//2+100, h-100), 5)
        # 下落音符动画
        now = pygame.time.get_ticks()
        t = min((now - self.calibrate_note_time) / 500, 1.0)
        y = int((h-500) * t + 100)
        pygame.draw.circle(self.main_window, (0, 128, 255), (w//2, y), 30)
