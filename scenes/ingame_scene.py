from pygame_gui.elements import UIButton

import game_manager
from gamedata.user_profile import UserProfile
from note import notedata
import scenes
import pygame
from pygame import Rect
import pygame_gui as gui
from pygame_gui.elements.ui_label import UILabel
from config import *
from sprites.abstract import AbstractNoteSprite
from sprites.notesprite.hold import HoldLineSprite
from sprites.notesprite.tap import TapNoteSprite
from sprites.path import PathSprite
import event_number as en
from gamedata.score import Score


class GameScene(scenes.Scene):
    def __init__(self, main_window: pygame.Surface, clock: pygame.Clock):
        super().__init__(main_window, clock)

        self.gamemgr = game_manager.GameManager(UserProfile())
        self.paused = False

        self.pathsprite = [PathSprite(i) for i in range(PATHS)]
        self.pathgroup = pygame.sprite.Group(self.pathsprite)
        self.notesprite: list[dict[int, AbstractNoteSprite | tuple]] = [{} for i in range(PATHS)]
        self.notegroups = [pygame.sprite.Group() for _ in range(PATHS)]
        self.tap_calc_midbottom = TapNoteSprite.gen_default_fn(self.gamemgr.userprofile.flow_speed,
                                                               DECISION_POS, TOP_POS)
        self.holdline_calc_midbottom = HoldLineSprite.gen_default_fn(self.gamemgr.userprofile.flow_speed,
                                                                     DECISION_POS, TOP_POS)

        self.side_board_guimgr = gui.UIManager((WD_WID, WD_HEI), theme_path="./src/theme/ingame.json")
        self.side_board = gui.core.UIContainer((WD_WID / 2, 0, WD_WID / 2, WD_HEI),
                                               manager=self.side_board_guimgr)
        self.badge_label = UILabel(pygame.Rect((100, 100), (WD_WID / 2 - 100, 100)),
                                   "AP FC+ FC",
                                   manager=self.side_board_guimgr,
                                   container=self.side_board)
        self.score_label = UILabel(pygame.Rect((100, 250), (WD_WID / 2 - 100, 100)),
                                   "SCORE:",
                                   manager=self.side_board_guimgr,
                                   container=self.side_board)
        self.score_label.set_text_scale(100)
        self.combo_label = UILabel(pygame.Rect((100, 400), (WD_WID / 2 - 100, 100)),
                                   "COMBO:",
                                   manager=self.side_board_guimgr,
                                   container=self.side_board)
        self.score = Score()
        self.update_side_board()

        self.pause_guimgr = gui.UIManager((WD_WID, WD_HEI), theme_path="./src/theme/pause_menu.json")
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
        # self.side_board.fill((255, 255, 255))
        self.badge_label.set_text(f"{'AP' if self.score.is_ap else '  '} {'FC+' if self.score.is_fcplus else '   '}"
                                  f"{'FC' if self.score.is_fc else '  '}")
        self.score_label.set_text(f"SCORE: {self.score.score:>8}")
        self.combo_label.set_text(f"COMBO: {self.score.combo:>5} (MAX: {self.score.max_combo:>5})")
        # self.side_board_guimgr.draw_ui(self.side_board)
        # self.main_window.blit(self.side_board, (640, 0))

    def on_create_note(self, data: notedata.Note, id_):
        if data.type == notedata.NoteType.TAP:
            ntap = TapNoteSprite(data.time, self.tap_calc_midbottom, self.pathsprite[data.path])
            self.notesprite[data.path][id_] = ntap
            self.notegroups[data.path].add(ntap)
        elif data.type == notedata.NoteType.HOLD:
            nt1 = TapNoteSprite(data.time, self.tap_calc_midbottom, self.pathsprite[data.path])
            nt2 = TapNoteSprite(data.time, self.tap_calc_midbottom, self.pathsprite[data.path])
            nl = HoldLineSprite(data.time, self.holdline_calc_midbottom, self.pathsprite[data.path])
            self.notesprite[data.path][id_] = nt1, nt2, nl
            self.notegroups[data.path].add(nt1, nt2, nl)

    def on_dispose_note(self, data: notedata.Note, id_):
        if data.type == notedata.NoteType.TAP:
            match data.decision:
                case notedata.DecisionLevel.MISS:
                    print("MISS")
                    self.score.misses += 1
                    self.score.combo = 0
                    self.score.is_ap = False
                    self.score.is_fcplus = False
                    self.score.is_fc = False
                case notedata.DecisionLevel.PERFECT:
                    print("PERFECT")
                    self.score.perfects += 1
                    self.score.combo += 1
                    self.score.max_combo = max(self.score.combo, self.score.max_combo)
                    self.score.score += 10
                case notedata.DecisionLevel.GREAT:
                    print("GREAT")
                    self.score.greats += 1
                    self.score.combo += 1
                    self.score.max_combo = max(self.score.combo, self.score.max_combo)
                    self.score.is_ap = False
                    self.score.score += 6
                case notedata.DecisionLevel.GOOD:
                    print("GOOD")
                    self.score.goods += 1
                    self.score.combo += 1
                    self.score.max_combo = max(self.score.combo, self.score.max_combo)
                    self.score.is_ap = False
                    self.score.is_fcplus = False
                    self.score.score += 3
            self.notesprite[data.path][id_].kill()
        elif data.type == notedata.NoteType.HOLD:
            decision = data.decision
            if data.tail_decision == notedata.DecisionLevel.MISS:
                if decision == notedata.DecisionLevel.GREAT: decision = notedata.DecisionLevel.GOOD
                elif decision == notedata.DecisionLevel.PERFECT: decision = notedata.DecisionLevel.GREAT
            else:
                if decision == notedata.DecisionLevel.MISS: decision = notedata.DecisionLevel.GOOD
                elif decision == notedata.DecisionLevel.GOOD: decision = notedata.DecisionLevel.GREAT
            match data.decision:
                case notedata.DecisionLevel.MISS:
                    print("MISS")
                    self.score.misses += 1
                    self.score.combo = 0
                    self.score.is_ap = False
                    self.score.is_fcplus = False
                    self.score.is_fc = False
                case notedata.DecisionLevel.PERFECT:
                    print("PERFECT")
                    self.score.perfects += 1
                    self.score.combo += 1
                    self.score.max_combo = max(self.score.combo, self.score.max_combo)
                    self.score.score += 20
                case notedata.DecisionLevel.GREAT:
                    print("GREAT")
                    self.score.greats += 1
                    self.score.combo += 1
                    self.score.max_combo = max(self.score.combo, self.score.max_combo)
                    self.score.is_ap = False
                    self.score.score += 12
                case notedata.DecisionLevel.GOOD:
                    print("GOOD")
                    self.score.goods += 1
                    self.score.combo += 1
                    self.score.max_combo = max(self.score.combo, self.score.max_combo)
                    self.score.is_ap = False
                    self.score.is_fcplus = False
                    self.score.score += 6
            ss = self.notesprite[data.path][id_]
            for s in ss: s.kill()
        self.update_side_board()

    def on_key_down(self, key):
        if key == self.gamemgr.userprofile.get_key('path_0'):
            if not self.paused: self.gamemgr.down(0)
        elif key == self.gamemgr.userprofile.get_key('path_1'):
            if not self.paused: self.gamemgr.down(1)
        elif key == self.gamemgr.userprofile.get_key('path_2'):
            if not self.paused: self.gamemgr.down(2)
        elif key == self.gamemgr.userprofile.get_key('path_3'):
            if not self.paused: self.gamemgr.down(3)
        elif key == pygame.K_ESCAPE:
            self.switch_pause_state()

    def on_key_up(self, key):
        if key == self.gamemgr.userprofile.get_key('path_0'):
            if not self.paused: self.gamemgr.up(0)
        elif key == self.gamemgr.userprofile.get_key('path_1'):
            if not self.paused: self.gamemgr.up(1)
        elif key == self.gamemgr.userprofile.get_key('path_2'):
            if not self.paused: self.gamemgr.up(2)
        elif key == self.gamemgr.userprofile.get_key('path_3'):
            if not self.paused: self.gamemgr.up(3)

    def switch_pause_state(self):
        if self.paused:
            self.paused = False
            self.pause_menu.hide()
        else:
            self.paused = True
            self.pause_menu.show()

    def main_loop(self, *args, **kwargs) -> tuple[scenes.Scene | None, list, dict]:
        self.gamemgr.prepare(kwargs['trackfile_name'])

        going = True

        while going:
            self.main_window.fill((255, 255, 255))
            for event in pygame.event.get():
                self.side_board_guimgr.process_events(event)
                self.pause_guimgr.process_events(event)
                if event.type == pygame.QUIT:
                    return None, [], {}
                elif event.type == en.CREATE_NOTE:
                    self.on_create_note(event.dict['notedata'], event.dict['id'])
                elif event.type == en.DISPOSE_NOTE:
                    self.on_dispose_note(event.dict['notedata'], event.dict['id'])
                elif event.type == pygame.KEYDOWN:
                    self.on_key_down(event.key)
                elif event.type == pygame.KEYUP:
                    self.on_key_up(event.key)
                elif event.type == en.GAME_OVER:
                    return (scenes.GameOverScene(self.main_window, self.clock), [],
                            {"score": self.score, "retry_which": self.gamemgr.trackfile_name})
                elif event.type == gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.resume_button:
                        self.switch_pause_state()
                    elif event.ui_element == self.retry_button:
                        return scenes.GameScene(self.main_window, self.clock), args, kwargs
                    elif event.ui_element == self.exit_button:
                        return scenes.MainScene(self.main_window, self.clock), [], {}
            if not self.paused:
                self.gamemgr.update(self.clock.get_time())
            self.side_board_guimgr.update(self.clock.get_time() / 1000)
            self.pause_guimgr.update(self.clock.get_time() / 1000)
            self.pathgroup.update(self.gamemgr.gametime)
            self.side_board_guimgr.draw_ui(self.main_window)
            self.pathgroup.draw(self.main_window)
            for notegroup in self.notegroups:
                notegroup.update(self.gamemgr.gametime)
                notegroup.draw(self.main_window)
            self.pause_guimgr.draw_ui(self.main_window)
            pygame.display.flip()
            self.clock.tick(FPS)
