"""
定义了各类型的note
注意这些只是note的数据表示，并不是在屏幕上移动的真正的note对象。
note对象由NoteManager创建和销毁
"""

from dataclasses import dataclass
from enum import Enum, auto


class NoteType(Enum):
    TAP = auto()
    HOLD = auto()


@dataclass
class Note:
    """
    普通note(tap)
    :ivar time: 判定时间
    :ivar path: 所在下落轨道的编号
    """
    type: NoteType
    time: float
    path: int

    def __lt__(self, other):
        return self.time < other.time or (self.time == other.time and self.path < other.path)


@dataclass
class Hold(Note):
    """
    hold音符
    :ivar interval: 持续时间
    """
    interval: float
