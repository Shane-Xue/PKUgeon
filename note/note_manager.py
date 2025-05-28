import copy

from . import notedata
from config import *
import pygame
from pygame import event
import event_number as en


class NoteManager:
    """
    管理游戏进程中创建的notes
    :ivar disposed: 表示notes列表中下标[0, disposed)的对象都被创建过并且已经被销毁
    :ivar created: 表示notes列表中下标[0, created)的对象都被创建过
    :ivar pre_creation_offset: note对象的创建比被判定时间提前的时间
    """
    def __init__(self, notes: list[list[notedata.Note]], gametime: float, pre_creation_offset: float):
        self.notes = copy.deepcopy(notes)
        self.disposed: list[int] = [0 for _ in range(PATHS)]
        self.created: list[int] = [0 for _ in range(PATHS)]
        self.gametime = gametime
        self.pre_creation_offset = pre_creation_offset

    def update(self, delta: float):
        self.gametime += delta
        for p in range(PATHS):
            # dispose some notes and set self.disposed
            for i in range(self.disposed[p], self.created[p]):
                one: notedata.Note = self.notes[p][i]
                match one.type:
                    case notedata.NoteType.TAP:
                        if one.decision != notedata.DecisionLevel.NONE:
                            self.disposed[p] += 1
                        elif one.time <= self.gametime - GOOD_INTERVAL:
                            one.decision = notedata.DecisionLevel.MISS
                            event.post(event.Event(en.DISPOSE_NOTE,
                                                   {"path": p, "id": i, "notedata": one}))
                            self.disposed[p] += 1
                        else:
                            break
                    case notedata.NoteType.HOLD:
                        one: notedata.Hold = one
                        if one.time + one.interval <= self.gametime:
                            if (one.decision == notedata.DecisionLevel.NONE or
                                    one.decision == notedata.DecisionLevel.MISS):
                                one.decision = notedata.DecisionLevel.MISS
                                one.tail_decision = notedata.DecisionLevel.MISS
                            elif one.tail_decision == notedata.DecisionLevel.NONE:
                                one.tail_decision = notedata.DecisionLevel.PERFECT
                            event.post(event.Event(en.DISPOSE_NOTE,
                                                   {"path": p, "id": i, "notedata": one}))
                            self.disposed[p] += 1
                        else:
                            break

            # create some notes and set self.created
            for i in range(self.created[p], len(self.notes[p])):
                if self.notes[p][i].time <= self.gametime + self.pre_creation_offset:
                    event.post(event.Event(en.CREATE_NOTE, {"path": p, "id": i, "notedata": self.notes[p][i]}))
                    self.created[p] += 1
                else:
                    break

    def down(self, path: int):
        """
        path轨道被按下，判定tap和hold的头判
        """
        i = self.disposed[path]
        if i >= self.created[path]: return
        while self.notes[path][i].decision != notedata.DecisionLevel.NONE and i < self.created[path] - 1:
            i += 1
        delta = self.notes[path][i].time - self.gametime
        if delta > MISS_INTERVAL:
            return
        if abs(delta) < PERFECT_INTERVAL:
            self.notes[path][i].decision = notedata.DecisionLevel.PERFECT
        elif abs(delta) < GREAT_INTERVAL:
            self.notes[path][i].decision = notedata.DecisionLevel.GREAT
        elif abs(delta) < GOOD_INTERVAL:
            self.notes[path][i].decision = notedata.DecisionLevel.GOOD
        else:
            self.notes[path][i].decision = notedata.DecisionLevel.MISS
        if self.notes[path][i].type == notedata.NoteType.TAP:
            event.post(event.Event(en.DISPOSE_NOTE, {"path": path, "id": i, "notedata": self.notes[path][i]}))

    def up(self, path: int):
        """
        path轨道被松开，判定hold的尾判
        """
        i = self.disposed[path]
        if i >= self.created[path]: return
        one: notedata.Hold = self.notes[path][i]
        if (one.type == notedata.NoteType.HOLD and one.decision != notedata.DecisionLevel.NONE
                and one.tail_decision == notedata.DecisionLevel.NONE):
            delta = one.time + one.interval
            if one.time + one.interval - self.gametime < GOOD_INTERVAL:
                one.tail_decision = notedata.DecisionLevel.PERFECT
            else:
                one.tail_decision = notedata.DecisionLevel.MISS
                event.post(event.Event(en.HOLD_EARLY_RELEASE, {"path": path, "id": i}))
            # event.post(event.Event(en.DISPOSE_NOTE, {"path": path, "id": i, "notedata": self.notes[path][i]}))
