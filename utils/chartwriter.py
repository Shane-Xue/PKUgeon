from note import notedata as nd
from gamedata import track_file as tf



class ChartWriter:
    """
    用于写谱面文件的类
    """
    def __init__(self, filename: str, tick: int = 16):
        self.filename = filename
        self.track_file = tf.TrackFile(filename)
        self.tick = (1/tick) # 默认每个十六分音符为 1 tick

    def create_note(self, type: nd.NoteType, start: int, path: int, end: int = None):
        """
        start: note开始时刻，表示为谱面起始的第start个tick
        end: hold音符的结束时刻，表示为谱面起始的第end个tick
        暂时只考虑四分音符为一拍
        """
        time = start * self.tick * 4 * (60 / self.track_file.bpm) * 1000 + self.track_file.start_time
        if type == nd.NoteType.TAP:
            return nd.Note(type, time, path, nd.DecisionLevel.NONE, 0)
        elif type == nd.NoteType.HOLD:
            interval = (end - start) * self.tick * 4 * (60 / self.track_file.bpm) * 1000
            return nd.Hold(type, time, path, nd.DecisionLevel.NONE, 0, interval, nd.DecisionLevel.NONE)
        else:
            raise ValueError("Invalid note type")
        
    def create_note_by_time(self, type: nd.NoteType, time: int, path: int, interval: int = None):
        if type == nd.NoteType.TAP:
            return nd.Note(type, time, path, nd.DecisionLevel.NONE, 0)
        elif type == nd.NoteType.HOLD:
            return nd.Hold(type, time, path, nd.DecisionLevel.NONE, 0, interval, nd.DecisionLevel.NONE)

    def create_chart(self, bpm: int, duration_ms: int, start_time: int = 0, title: str = "Unknown", artist: str = "Unknown", chart_maker: str = "Unknown", level: int = 0):
        self.track_file.bpm = bpm
        self.track_file.duration_ms = duration_ms
        self.track_file.start_time = start_time
        self.track_file.title = title
        self.track_file.artist = artist
        self.track_file.chart_maker = chart_maker
        self.track_file.level = level
    
    def load_chart(self):
        self.track_file = tf.read_track_file(self.filename)

    def add_note(self, type: nd.NoteType, start: int, path: int, end: int = None):
        note = self.create_note(type, start, path, end)
        self.track_file.add(note)

    def add_note_by_time(self, type: nd.NoteType, time: int, path: int, interval: int = None):
        note = self.create_note_by_time(type, time, path, interval)
        self.track_file.add(note)

    def remove_note(self, type: nd.NoteType, start: int, path: int, end: int = None):
        note = self.create_note(type, start, path, end)
        self.track_file.remove(note)

    def save(self):
        for path in self.track_file.notes:
            path.sort()
        tf.write_track_file(self.filename, self.track_file)