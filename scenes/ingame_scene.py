import game_manager
from gamedata.user_profile import UserProfile
from note import notedata
from scenes.scene import Scene
import pygame
import pygame_gui as gui
from config import *
from sprites.notesprite.tap import TapSprite, linear_calc_midbottom
from sprites.path import PathSprite
import event_number as en


chart_name = 'test'


class GameScene(Scene):
    def __init__(self, main_window: pygame.Surface, clock: pygame.Clock):
        super().__init__(main_window, clock)

        self.gamemgr = game_manager.GameManager(UserProfile(), chart_name)
        self.gamemgr.prepare()

        self.pathsprite = [PathSprite(i) for i in range(PATHS)]
        self.pathgroup = pygame.sprite.Group(self.pathsprite)
        self.notesprite: list[dict[int, TapSprite]] = [{} for i in range(PATHS)]
        self.notegroups = [pygame.sprite.Group() for _ in range(PATHS)]
        self.calc_midbottom = linear_calc_midbottom(self.gamemgr.userprofile.flow_speed, DECISION_POS, INIT_POS)

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
            case notedata.DecisionLevel.PERFECT:
                print("PERFECT")
            case notedata.DecisionLevel.GREAT:
                print("GREAT")
            case notedata.DecisionLevel.GOOD:
                print("GOOD")
        self.notesprite[data.path][id_].kill()

    def on_key_down(self, key):
        if key == self.gamemgr.userprofile.get_key('path_0'):
            self.gamemgr.decide(0)
        elif key == self.gamemgr.userprofile.get_key('path_1'):
            self.gamemgr.decide(1)
        elif key == self.gamemgr.userprofile.get_key('path_2'):
            self.gamemgr.decide(2)
        elif key == self.gamemgr.userprofile.get_key('path_3'):
            self.gamemgr.decide(3)

    def main_loop(self, *args, **kwargs) -> tuple[Scene | None, list, dict]:
        going = True

        while going:
            self.main_window.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None, [], {}
                elif event.type == en.CREATE_NOTE:
                    self.on_create_note(event.dict['notedata'], event.dict['id'])
                elif event.type == en.DISPOSE_NOTE:
                    self.on_dispose_note(event.dict['notedata'], event.dict['id'])
                elif event.type == pygame.KEYDOWN:
                    self.on_key_down(event.key)
                elif event.type == en.GAME_OVER:
                    return None, [], {}
            self.gamemgr.update(self.clock.get_time())
            self.pathgroup.update(self.gamemgr.gametime)
            self.pathgroup.draw(self.main_window)
            for notegroup in self.notegroups:
                notegroup.update(self.gamemgr.gametime)
                notegroup.draw(self.main_window)
            pygame.display.flip()
            self.clock.tick(FPS)

