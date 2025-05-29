from config import *
import pygame
import game_manager
from gamedata.track_file import TrackFile
from gamedata.user_profile import UserProfile
from note import notedata
from sprites.abstract import AbstractNoteSprite
from sprites.notesprite.hold import HoldLineSprite
from sprites.notesprite.tap import TapNoteSprite, HoldStartNoteSprite
from sprites.path import PathSprite
import event_number as en


class GameRenderer:
    def __init__(self, userprofile: UserProfile, trackfile: TrackFile):
        self.gamemgr = game_manager.GameManager(userprofile, trackfile)

        self.pathsprite = [PathSprite(i) for i in range(PATHS)]
        self.pathgroup = pygame.sprite.Group(self.pathsprite)
        self.notesprite: list[dict[int, AbstractNoteSprite | tuple]] = [{} for i in range(PATHS)]
        self.notegroups = [pygame.sprite.Group() for _ in range(PATHS)]
        self.tap_calc_midbottom = TapNoteSprite.gen_default_fn(self.gamemgr.userprofile.flow_speed,
                                                               DECISION_POS, TOP_POS)
        self.holdline_calc_midbottom = HoldLineSprite.gen_default_fn(self.gamemgr.userprofile.flow_speed,
                                                                     DECISION_POS, TOP_POS)
        self.holdline_calc_length = HoldLineSprite.gen_calc_length_fn(self.gamemgr.userprofile.flow_speed,
                                                                      DECISION_POS, TOP_POS)

        self.size = WD_WID / 2, WD_HEI

    def render(self) -> pygame.Surface:
        ret = pygame.Surface(self.size)
        ret.fill((255, 255, 255))
        self.pathgroup.draw(ret)
        for notegroup in self.notegroups:
            notegroup.draw(ret)
        return ret

    def update(self, delta_time: float):
        self.gamemgr.update(delta_time)
        self.pathgroup.update(self.gamemgr.gametime)
        for notegroup in self.notegroups:
            notegroup.update(self.gamemgr.gametime)

    def process_events(self, event: pygame.event.Event):
        if event.type == en.CREATE_NOTE:
            self.create_note_sprite(event.dict['notedata'], event.dict['id'])
        elif event.type == en.DISPOSE_NOTE:
            self.dispose_note_sprite(event.dict['notedata'], event.dict['id'])
        elif event.type == en.HOLD_EARLY_RELEASE:
            for s in self.notesprite[event.dict['path']][event.dict['id']]:
                s.image.fill((108, 108, 108))

    def create_note_sprite(self, data: notedata.Note, id_):
        if data.type == notedata.NoteType.TAP:
            ntap = TapNoteSprite(data.time, self.tap_calc_midbottom, self.pathsprite[data.path])
            self.notesprite[data.path][id_] = ntap
            self.notegroups[data.path].add(ntap)
        elif data.type == notedata.NoteType.HOLD:
            nt1 = HoldStartNoteSprite(data.time, DECISION_POS, self.tap_calc_midbottom, self.pathsprite[data.path])
            nt2 = TapNoteSprite(data.time + data.interval, self.tap_calc_midbottom, self.pathsprite[data.path])
            nl = HoldLineSprite(nt1, nt2, data.time, self.holdline_calc_length(data.interval))
            self.notesprite[data.path][id_] = nt1, nt2, nl
            self.notegroups[data.path].add(nt1, nt2, nl)

    def dispose_note_sprite(self, data: notedata.Note, id_) -> tuple[notedata.NoteType, notedata.DecisionLevel]:
        if data.type == notedata.NoteType.TAP:
            self.notesprite[data.path][id_].kill()
            pygame.event.post(pygame.Event(en.DECISION,
                                           {'decision': data.decision, 'type_': data.type, 'path': data.path}))
            print("post ", data.decision, data.type, data.path)
        elif data.type == notedata.NoteType.HOLD:
            decision = data.decision
            if data.tail_decision == notedata.DecisionLevel.MISS:
                if decision == notedata.DecisionLevel.GREAT: decision = notedata.DecisionLevel.GOOD
                elif decision == notedata.DecisionLevel.PERFECT: decision = notedata.DecisionLevel.GREAT
            else:
                if decision == notedata.DecisionLevel.MISS: decision = notedata.DecisionLevel.GOOD
                elif decision == notedata.DecisionLevel.GOOD: decision = notedata.DecisionLevel.GREAT
            ss = self.notesprite[data.path][id_]
            for s in ss: s.kill()
            pygame.event.post(pygame.Event(en.DECISION,
                                           {'decision': decision, 'type_': data.type, 'path': data.path}))
            print("post ", decision, data.type, data.path)

    def key_down(self, path: int, auto_op: bool = False):
        r = self.gamemgr.down(path, auto_op)
        if r == notedata.NoteType.TAP:
            self.pathsprite[path].tap()
        elif r == notedata.NoteType.HOLD:
            self.pathsprite[path].pressed()
        elif not auto_op:
            self.pathsprite[path].pressed()

    def key_up(self, path: int, auto_op: bool = False):
        if self.gamemgr.up(path, auto_op) or not auto_op:
            self.pathsprite[path].released()

