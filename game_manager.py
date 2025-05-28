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

from gamedata.track_file import TrackFile
from note.note_manager import NoteManager


class GameManager:
    """
    :ivar gametime: 游戏进程时间，直接控制游戏内各“可视”元素，比如note
    :ivar musictime: 音乐时间，仅用于控制音乐播放，以此达到调整按键延迟
    """
    def __init__(self, userprofile: gd.user_profile.UserProfile, trackfile: TrackFile):
        self.userprofile = userprofile
        self.gametime = -config.GAP_TIME
        self.musictime = userprofile.latency - config.GAP_TIME
        self.trackfile = trackfile
        self.notemgr = NoteManager(self.trackfile.notes, self.gametime, self.userprofile.pre_creation_offset())
        self.duration_ms = self.trackfile.duration_ms

    def update(self, delta: float):
        """
        :param delta: 距上次update经过的时间，单位为ms
        """
        self.gametime += delta
        self.musictime += delta
        self.notemgr.update(delta)
        if self.gametime >= self.duration_ms + config.GAP_TIME:
            event.post(event.Event(en.GAME_OVER))
        # todo

    def down(self, path: int, auto_op: bool = False):
        self.notemgr.down(path, auto_op)

    def up(self, path: int, auto_op: bool = False):
        self.notemgr.up(path, auto_op)
