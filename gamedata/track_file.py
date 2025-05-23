"""
定义了与谱面文件有关的一系列数据结构和函数
"""

import json
from note import notedata
import os
from note import notedata
from config import *

save_dir = 'gamedata/resources'

class TrackFile:
    def __init__(self):
        self.notes: list[list[notedata.Note]] = [[] for i in range(PATHS)]
        self.bpm = 0
        self.duration_ms = 0
        self.start_time = 0 # 记录谱面开始时间，单位为ms，在此基础上加减latency

    def add(self, note):
        self.notes[note.path].append(note)

    def remove(self, note):
        if note in self.notes:
            self.notes.remove(note)
        else:
            raise ValueError("Note not found in track file")


def read_track_file(filename: str) -> TrackFile:
    full_path = os.path.join(save_dir, filename, filename)
    ret = TrackFile()
    with open(full_path, 'r') as f:
        data = json.load(f)
        ret.duration_ms = float(data['duration_ms'])
        ret.bpm = int(data['bpm'])
        ret.start_time = float(data['start_time'])
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

def write_track_file(filename: str, track_file: TrackFile):
    full_path = os.path.join(save_dir, filename, filename)
    data = {
        'duration_ms': track_file.duration_ms,
        'bpm': track_file.bpm,
        'start_time': track_file.start_time,
        'notes': []
    }
    for path in track_file.notes:
        for note in path:
            if type(note) == notedata.Note:
                data['notes'].append({
                    'type': 'tap',
                    'time': note.time,
                    'path': note.path
                })
            elif type(note) == notedata.Hold:
                data['notes'].append({
                    'type': 'hold',
                    'time': note.time,
                    'path': note.path,
                    'interval': note.interval
                })
    with open(full_path, 'w') as f:
        json.dump(data, f, indent=4)
