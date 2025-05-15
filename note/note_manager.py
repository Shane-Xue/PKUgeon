import notedata
import config


class NoteManager:
    """
    管理游戏进程中创建的notes
    :ivar disposed: 表示notes列表中下标[0, disposed)的对象都被创建过并且已经被销毁
    :ivar created: 表示notes列表中下标[0, created)的对象都被创建过
    """
    def __init__(self, notes: list[notedata.Note], gametime: float, pre_creation_offset: float):
        self.notes = notes
        self.disposed: int = 0
        self.created: int = 0
        self.gametime = gametime
        self.pre_creation_offset = pre_creation_offset

    def update(self, delta: float):
        self.gametime += delta
        # todo dispose some notes and set self.disposed
        # todo create some notes and set self.created
