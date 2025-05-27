"""
game_manager.py
实现一系列控制游戏进程的核心逻辑
"""

import pygame
from pygame import event
import event_number as en
import gamedata as gd
import config
from enum import Enum, auto
from collections import deque
from note.note_manager import NoteManager


class GameManager:
    """
    :ivar gametime: 游戏进程时间，直接控制游戏内各“可视”元素，比如note
    :ivar musictime: 音乐时间，仅用于控制音乐播放，以此达到调整按键延迟
    :ivar status: GameManager目前的状态
    """
    class Status(Enum):
        INITIALIZED = auto()
        READY = auto()
        STARTED = auto()
        STOPPED = auto()

    def __init__(self, userprofile: gd.user_profile.UserProfile):
        self.userprofile = userprofile
        self.gametime = -config.GAP_TIME
        self.musictime = userprofile.latency - config.GAP_TIME
        self.trackfile_name = None
        self.bpm = None
        self.duration_ms = None
        self.status = GameManager.Status.INITIALIZED
        self.notemgr = None

    def prepare(self, trackfile_name: str):
        """
        在game_start前调用，为开始游戏做好准备：
        1. 读取track file
        2. 读取music file
        """
        self.status = GameManager.Status.READY
        self.trackfile_name = trackfile_name
        # 读取track file
        trackfile = gd.track_file.read_track_file(trackfile_name)
        self.bpm = trackfile.bpm
        self.duration_ms = trackfile.duration_ms
        self.notemgr = NoteManager(trackfile.notes, self.gametime, self.userprofile.pre_creation_offset())

        # todo 读取music file

    def game_start(self):
        self.status = GameManager.Status.STARTED
        # todo

    def update(self, delta: float):
        """
        :param delta: 距上次update经过的时间，单位为ms
        """
        self.gametime += delta
        self.musictime += delta
        self.notemgr.update(delta)
        if self.gametime >= self.duration_ms + config.GAP_TIME:
            event.post(event.Event(en.GAME_OVER))
            self.status = GameManager.Status.STOPPED
        # todo

    def down(self, path: int):
        self.notemgr.down(path)

    def up(self, path: int):
        self.notemgr.up(path)