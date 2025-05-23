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
        self.notes = notes
        self.disposed: list[int] = [0 for _ in range(PATHS)]
        self.created: list[int] = [0 for _ in range(PATHS)]
        self.gametime = gametime
        self.pre_creation_offset = pre_creation_offset

    def update(self, delta: float):
        self.gametime += delta
        for p in range(PATHS):
            # dispose some notes and set self.disposed
            for i in range(self.disposed[p], self.created[p]):
                if self.notes[p][i].decision != notedata.DecisionLevel.NONE:
                    self.disposed[p] += 1
                elif self.notes[p][i].time <= self.gametime - GOOD_INTERVAL:
                    self.notes[p][i].decision = notedata.DecisionLevel.MISS
                    event.post(event.Event(en.DISPOSE_NOTE, {"path": p, "id": i, "notedata": self.notes[p][i]}))
                    # print(f"emit dispose {p} {i}")
                    self.disposed[p] += 1
                else:
                    break
            # create some notes and set self.created
            for i in range(self.created[p], len(self.notes[p])):
                if self.notes[p][i].time <= self.gametime + self.pre_creation_offset:
                    event.post(event.Event(en.CREATE_NOTE, {"path": p, "id": i, "notedata": self.notes[p][i]}))
                    # print(f"emit create note {p} {i}")
                    self.created[p] += 1
                else:
                    break

    def decide(self, path: int):
        """
        判定path轨道上的note
        """
        i = self.disposed[path]
        while self.notes[path][i].decision != notedata.DecisionLevel.NONE:
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
        event.post(event.Event(en.DISPOSE_NOTE, {"path": path, "id": i, "notedata": self.notes[path][i]}))
