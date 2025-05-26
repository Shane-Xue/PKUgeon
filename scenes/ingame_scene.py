import game_manager
from gamedata.user_profile import UserProfile
from note import notedata
import scenes
import pygame
import pygame_gui as gui
from pygame_gui.elements.ui_label import UILabel
from config import *
from sprites.notesprite.tap import TapSprite, linear_calc_midbottom
from sprites.path import PathSprite
import event_number as en
from gamedata.score import Score


class GameScene(scenes.Scene):
    def __init__(self, main_window: pygame.Surface, clock: pygame.Clock):
        super().__init__(main_window, clock)

        self.gamemgr = game_manager.GameManager(UserProfile())

        self.pathsprite = [PathSprite(i) for i in range(PATHS)]
        self.pathgroup = pygame.sprite.Group(self.pathsprite)
        self.notesprite: list[dict[int, TapSprite]] = [{} for i in range(PATHS)]
        self.notegroups = [pygame.sprite.Group() for _ in range(PATHS)]
        self.calc_midbottom = linear_calc_midbottom(self.gamemgr.userprofile.flow_speed, DECISION_POS, INIT_POS)

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
            ntap = TapSprite(self.gamemgr.gametime, data.time, self.calc_midbottom, self.pathsprite[data.path])
            self.notesprite[data.path][id_] = ntap
            self.notegroups[data.path].add(ntap)
        else:
            print("error: unsupported note type")

    def on_dispose_note(self, data: notedata.Note, id_):
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
        self.update_side_board()

    def on_key_down(self, key):
        if key == self.gamemgr.userprofile.get_key('path_0'):
            self.gamemgr.decide(0)
        elif key == self.gamemgr.userprofile.get_key('path_1'):
            self.gamemgr.decide(1)
        elif key == self.gamemgr.userprofile.get_key('path_2'):
            self.gamemgr.decide(2)
        elif key == self.gamemgr.userprofile.get_key('path_3'):
            self.gamemgr.decide(3)

    def main_loop(self, *args, **kwargs) -> tuple[scenes.Scene | None, list, dict]:
        self.gamemgr.prepare(kwargs['trackfile_name'])

        going = True
        while going:
            self.main_window.fill((255, 255, 255))
            for event in pygame.event.get():
                self.side_board_guimgr.process_events(event)
                if event.type == pygame.QUIT:
                    return None, [], {}
                elif event.type == en.CREATE_NOTE:
                    self.on_create_note(event.dict['notedata'], event.dict['id'])
                elif event.type == en.DISPOSE_NOTE:
                    self.on_dispose_note(event.dict['notedata'], event.dict['id'])
                elif event.type == pygame.KEYDOWN:
                    self.on_key_down(event.key)
                elif event.type == en.GAME_OVER:
                    return scenes.GameOverScene(self.main_window, self.clock), [], {"score": self.score,
                                                                             "retry_which": self.gamemgr.trackfile_name}
            self.side_board_guimgr.update(self.clock.get_time() / 1000)
            self.pathgroup.update(self.gamemgr.gametime)
            self.side_board_guimgr.draw_ui(self.main_window)
            self.pathgroup.draw(self.main_window)
            for notegroup in self.notegroups:
                notegroup.update(self.gamemgr.gametime)
                notegroup.draw(self.main_window)
            pygame.display.flip()
            self.clock.tick(FPS)
