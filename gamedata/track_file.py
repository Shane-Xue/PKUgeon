"""
定义了与谱面文件有关的一系列数据结构和函数
"""

import json
from ..note import notedata
from config import *


class TrackFile:
    def __init__(self):
        self.notes: list[list[notedata.Note]] = [[] for i in range(PATHS)]
        self.bpm = 0
        self.duration_ms = 0


def read_track_file(filename: str) -> TrackFile:
    ret = TrackFile()
    with open(filename, 'r') as f:
        data = json.load(f)
        ret.duration_ms = int(data['duration_ms'])
        ret.bpm = int(data['bpm'])
        for note in data['notes']:
            if note['type'] == 'tap':
                ret.notes[int(note['path'])].append(notedata.Note(notedata.NoteType.TAP,
                                                    float(note['time']),
                                                    int(note['path']),
                                                    notedata.DecisionLevel.NONE))
            elif note['type'] == 'hold':
                ret.notes[int(note['path'])].append(notedata.Hold(notedata.NoteType.HOLD,
                                                    float(note['time']),
                                                    int(note['path']),
                                                    notedata.DecisionLevel.NONE,
                                                    float(note['interval'])))
        for i in range(PATHS):
            ret.notes.sort()
    return ret
