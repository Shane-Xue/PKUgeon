import os.path

from pygame_gui.elements import UIButton

from game_renderer import GameRenderer
from gamedata.mediaplayer import MediaPlayer, SEID
from gamedata.user_profile import UserProfile
from note import notedata
import scenes
import pygame
from pygame import Rect
import pygame_gui as gui
from pygame_gui.elements.ui_label import UILabel
from config import *
import event_number as en
from gamedata.score import Score
from sprites.delta_bar import DeltaBar, Marker
from sprites.tap_effect import ColoredTextSprite
from sprites.progress_bar import ProgressBar


class GameScene(scenes.Scene):
    def __init__(self, main_window: pygame.Surface, clock: pygame.Clock, autoplay: bool = False):
        super().__init__(main_window, clock)
        self.userprofile = UserProfile()
        self.game_renderer = None

        self.auto_play = autoplay

        self.decision_label_group = pygame.sprite.Group()
        self.decision_label: list[ColoredTextSprite] = [None for _ in range(PATHS)]
        
        self.delta_bar = DeltaBar()
        self.delta_bar.rect.midbottom = WD_WID / 4, WD_HEI - 40
        self.delta_bar_group = pygame.sprite.Group(self.delta_bar)
        
        self.progress_bar = ProgressBar(self.main_window, 5)
        
        self.side_board_guimgr = gui.UIManager((WD_WID, WD_HEI),
                                               theme_path=resource_path('res/theme/ingame.json'))
        self.side_board = gui.core.UIContainer((WD_WID / 2, 0, WD_WID / 2, WD_HEI),
                               manager=self.side_board_guimgr)
        self.badge_label = UILabel(pygame.Rect((WD_WID * 0.052, WD_HEI * 0.093), (WD_WID * 0.396, WD_HEI * 0.093)),
                       "AP FC+ FC",
                       manager=self.side_board_guimgr,
                       container=self.side_board)
        self.score_label = UILabel(pygame.Rect((WD_WID * 0.052, WD_HEI * 0.231), (WD_WID * 0.396, WD_HEI * 0.093)),
                       "SCORE:",
                       manager=self.side_board_guimgr,
                       container=self.side_board)
        self.score_label.set_text_scale(100)
        self.combo_label = UILabel(pygame.Rect((WD_WID * 0.052, WD_HEI * 0.37), (WD_WID * 0.396, WD_HEI * 0.093)),
                       "COMBO:",
                       manager=self.side_board_guimgr,
                       container=self.side_board)
        self.score = Score()
        self.score.max_score = 1
        self.update_side_board()

        self.paused = False

        self.pause_guimgr = gui.UIManager((WD_WID, WD_HEI),
                                          theme_path=resource_path('res/theme/pause_menu.json'))
        self.pause_menu = gui.core.UIContainer((WD_WID * 0.1, WD_HEI * 0.2, WD_WID * 0.3, WD_HEI * 0.6),
                                               manager=self.pause_guimgr)
        self.pause_menu.hide()
        ts = self.pause_menu.rect.size
        self.pause_label = UILabel(Rect(0, 0, ts[0], 50), "PAUSED",
                                   manager=self.pause_guimgr, container=self.pause_menu)
        self.resume_button = UIButton(Rect(ts[0] * 0.2, ts[1] * 0.2, ts[0] * 0.6, 50), "Resume",
                                      manager=self.pause_guimgr, container=self.pause_menu)
        self.retry_button = UIButton(Rect(ts[0] * 0.2, ts[1] * 0.4, ts[0] * 0.6, 50), "Retry",
                                     manager=self.pause_guimgr, container=self.pause_menu)
        self.exit_button = UIButton(Rect(ts[0] * 0.2, ts[1] * 0.6, ts[0] * 0.6, 50), "Exit",
                                    manager=self.pause_guimgr, container=self.pause_menu)

    def update_side_board(self):
        self.badge_label.set_text(f"{'AP' if self.score.is_ap else '  '}  {'FC+' if self.score.is_fcplus else '   '}  "
                                  f"{'FC' if self.score.is_fc else '  '}")
        t = self.score.score / self.score.max_score * 100
        self.score_label.set_text(f"SCORE: {self.score.score:0>8} "
                                  f"({'0' if t < 100 else ''}{'0' if t < 10 else ''}{t:3.6f}%)")
        self.combo_label.set_text(f"COMBO: {self.score.combo:0>5} (MAX: {self.score.max_combo:0>5})")

    def on_decision(self, type_: notedata.NoteType, decision: notedata.DecisionLevel, path: int, delta: float):
        mult = 1 if type_ == type_.TAP else 2
        match decision:
            case notedata.DecisionLevel.MISS:
                self.score.misses += 1
                self.score.combo = 0
                self.score.is_ap = False
                self.score.is_fcplus = False
                self.score.is_fc = False
            case notedata.DecisionLevel.PERFECT:
                self.score.perfects += 1
                self.score.combo += 1
                self.score.max_combo = max(self.score.combo, self.score.max_combo)
                self.score.score += 10 * mult
            case notedata.DecisionLevel.GREAT:
                self.score.greats += 1
                self.score.combo += 1
                self.score.max_combo = max(self.score.combo, self.score.max_combo)
                self.score.is_ap = False
                self.score.score += 8 * mult
            case notedata.DecisionLevel.GOOD:
                self.score.goods += 1
                self.score.combo += 1
                self.score.max_combo = max(self.score.combo, self.score.max_combo)
                self.score.is_ap = False
                self.score.is_fcplus = False
                self.score.score += 5 * mult
        self.update_side_board()
        self.show_tap_effect(path, decision)
        if decision != decision.MISS or delta < -MISS_INTERVAL:
            self.delta_bar.add_marker(Marker(), delta)
        MediaPlayer.global_player.play_sound_effect(SEID.from_decision(decision))

    def on_key_down(self, key):
        if not self.auto_play:
            if key == self.userprofile.get_key('path_0'):
                if not self.paused:
                    self.game_renderer.key_down(0)
            elif key == self.userprofile.get_key('path_1'):
                if not self.paused:
                    self.game_renderer.key_down(1)
            elif key == self.userprofile.get_key('path_2'):
                if not self.paused:
                    self.game_renderer.key_down(2)
            elif key == self.userprofile.get_key('path_3'):
                if not self.paused:
                    self.game_renderer.key_down(3)
        if key == pygame.K_ESCAPE:
            self.switch_pause_state()

    def on_key_up(self, key):
        if not self.auto_play:
            if key == self.userprofile.get_key('path_0'):
                if not self.paused: self.game_renderer.key_up(0)
            elif key == self.userprofile.get_key('path_1'):
                if not self.paused: self.game_renderer.key_up(1)
            elif key == self.userprofile.get_key('path_2'):
                if not self.paused: self.game_renderer.key_up(2)
            elif key == self.userprofile.get_key('path_3'):
                if not self.paused: self.game_renderer.key_up(3)

    def switch_pause_state(self):
        if self.paused:
            self.paused = False
            self.pause_menu.hide()
            MediaPlayer.global_player.unpause()
        else:
            self.paused = True
            self.pause_menu.show()
            MediaPlayer.global_player.pause()

    def show_tap_effect(self, path: int, decision_level: notedata.DecisionLevel):
        if self.decision_label[path] is not None:
            self.decision_label[path].kill()
        center = WD_WID / 2 * (2 * path + 1) / 2 / PATHS, 1000
        if decision_level == notedata.DecisionLevel.PERFECT:
            self.decision_label[path] = ColoredTextSprite.perfect((center[0], center[1]))
        elif decision_level == notedata.DecisionLevel.GREAT:
            self.decision_label[path] = ColoredTextSprite.great((center[0], center[1]))
        elif decision_level == notedata.DecisionLevel.GOOD:
            self.decision_label[path] = ColoredTextSprite.good((center[0], center[1]))
        elif decision_level == notedata.DecisionLevel.MISS:
            self.decision_label[path] = ColoredTextSprite.miss((center[0], center[1]))
        self.decision_label_group.add(self.decision_label[path])
        pygame.time.set_timer(pygame.event.Event(en.HIDE_TAP_EFFECT + path), 500, loops=1)

    def hide_tap_effect(self, path: int):
        if self.decision_label[path] is not None:
            self.decision_label[path].kill()
            self.decision_label[path] = None

    def main_loop(self, *args, **kwargs) -> tuple[scenes.Scene | None, list, dict]:
        trackfile = kwargs['trackfile']
        self.score.max_score = trackfile.max_score
        self.game_renderer = GameRenderer(self.userprofile, trackfile)

        MediaPlayer.global_player.set_music_volume(self.userprofile.music_volume)
        MediaPlayer.global_player.set_sfx_volume(self.userprofile.sfx_volume)

        going = True

        pygame.event.clear()

        while going:
            self.main_window.fill(THEME_COLOR)
            for event in pygame.event.get():
                self.side_board_guimgr.process_events(event)
                self.pause_guimgr.process_events(event)
                self.game_renderer.process_events(event)
                if event.type == pygame.QUIT:
                    return None, [], {}
                elif event.type == pygame.KEYDOWN:
                    self.on_key_down(event.key)
                elif event.type == pygame.KEYUP:
                    self.on_key_up(event.key)
                elif event.type == en.GAME_OVER:
                    MediaPlayer.global_player.unload_music()
                    return (scenes.GameOverScene(self.main_window, self.clock), [],
                            {"score": self.score, "retry_which": kwargs['trackfile']})
                elif event.type == gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.resume_button:
                        self.switch_pause_state()
                    elif event.ui_element == self.retry_button:
                        return scenes.ChartInfoScene(self.main_window, self.clock), args, kwargs
                    elif event.ui_element == self.exit_button:
                        return scenes.MainScene(self.main_window, self.clock), [], {}
                elif en.HIDE_TAP_EFFECT <= event.type < en.HIDE_TAP_EFFECT + PATHS:
                    self.hide_tap_effect(event.type - en.HIDE_TAP_EFFECT)
                elif event.type == en.DECISION:
                    self.on_decision(event.dict['type_'], event.dict['decision'],
                                     event.dict['path'], event.dict['delta'])
                elif event.type == en.PLAY_MUSIC:
                    MediaPlayer.global_player.play_music()
            if self.auto_play:
                for i in range(PATHS):
                    self.game_renderer.key_down(i, True)
                    self.game_renderer.key_up(i, True)
            if not self.paused:
                self.game_renderer.update(self.clock.get_time())
            self.side_board_guimgr.update(self.clock.get_time() / 1000)
            self.pause_guimgr.update(self.clock.get_time() / 1000)
            self.side_board_guimgr.draw_ui(self.main_window)
            self.main_window.blit(self.game_renderer.render(), (0, 0))
            if not self.auto_play:
                self.delta_bar_group.draw(self.main_window)
            self.decision_label_group.draw(self.main_window)
            self.progress_bar.update_bar(self.game_renderer.get_time())
            self.pause_guimgr.draw_ui(self.main_window)
            pygame.display.flip()
            self.clock.tick(FPS)
