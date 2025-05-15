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


class GameManager:
    """
    :ivar gametime: 游戏进程时间，直接控制游戏内各“可视”元素，比如note
    :ivar musictime: 音乐时间，仅用于控制音乐播放，以此达到调整按键延迟
    :ivar note_queue: 按照时间排序的note队列
    :ivar status: GameManager目前的状态
    """
    class Status(Enum):
        INITIALIZED = auto()
        READY = auto()
        STARTED = auto()
        STOPPED = auto()

    def __init__(self, userprofile: gd.user_profile.UserProfile, track_file_name: str):
        self.userprofile = userprofile
        self.track_file_name = track_file_name
        self.gametime = -config.GAP_TIME
        self.musictime = userprofile.latency - config.GAP_TIME
        self.note_queue = None
        self.status = GameManager.Status.INITIALIZED

    def prepare(self):
        """
        在game_start前调用，为开始游戏做好准备：
        1. 读取track file
        2. 读取music file
        """
        self.status = GameManager.Status.READY
        # todo 读取track file
        # todo 读取music file

    def game_start(self):
        self.status = GameManager.Status.STARTED
        event.post(event.Event(en.MUSIC_START, {"start_time": self.musictime, "file": self.trackfile.musicfile}))
        # todo

    def update(self, delta: float):
        """
        :param delta: 单位为ms
        """
        self.gametime += delta
        self.musictime += delta
        # todo
