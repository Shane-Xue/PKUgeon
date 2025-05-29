import pygame
from enum import IntEnum, auto
from note.notedata import DecisionLevel


class SEID(IntEnum):
    ENTRY = auto()
    SHOW_INFO = auto()
    GAME_PERFECT = auto()
    GAME_GREAT = auto()
    GAME_GOOD = auto()
    GAME_MISS = auto()

    @staticmethod
    def from_decision(decision: DecisionLevel):
        match decision:
            case decision.PERFECT:
                return SEID.GAME_PERFECT
            case decision.GREAT:
                return SEID.GAME_GREAT
            case decision.GOOD:
                return SEID.GAME_GOOD
            case decision.MISS:
                return SEID.GAME_MISS


class MediaPlayer:
    """
    媒体播放器类，负责加载和播放音频文件
    """
    global_player = None

    @staticmethod
    def init():
        MediaPlayer.global_player = MediaPlayer()

    def __init__(self):
        pygame.mixer.init()
        MediaPlayer.global_player = self
        self.sound_effects: dict[SEID, pygame.mixer.Sound] = {}
        for seid in SEID:
            self.sound_effects[seid] = pygame.Sound(f'res/se/{seid.name}.wav')
        self.current_music = None

    def load_music(self, music_file):
        """
        加载音乐文件
        :param music_file: 音乐文件路径
        """
        pygame.mixer.music.load(music_file)
        self.current_music = music_file

    def unload_music(self):
        if self.current_music is not None:
            self.current_music = None
            pygame.mixer.music.unload()

    def play_music(self, loops=0):
        """
        播放音乐
        :param loops: 循环次数等于loop+1
        """
        if self.current_music:
            pygame.mixer.music.play(loops)

    def pause(self):
        """暂停音乐"""
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def jump(self, time_ms):
        """音乐跳转到特定时间点"""
        # todo

    def play_sound_effect(self, seid: SEID):
        self.sound_effects[seid].play()
