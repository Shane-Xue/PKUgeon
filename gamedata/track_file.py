"""
定义了与谱面文件有关的一系列数据结构和函数
"""

import json
from .. import notes


class TrackFile:
    def __init__(self):
        self.notes = []
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
                ret.notes.append(notes.Note(notes.NoteType.TAP,
                                            float(note['time']),
                                            int(note['path'])))
            elif note['type'] == 'hold':
                ret.notes.append(notes.Hold(notes.NoteType.HOLD,
                                            float(note['time']),
                                            int(note['path']),
                                            float(note['interval'])))
    return ret
