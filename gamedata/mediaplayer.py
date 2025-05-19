import pygame

class MediaPlayer:
    """
    媒体播放器类，负责加载和播放音频文件
    """
    def __init__(self):
        pygame.mixer.init()
        self.current_music = None

    def load_music(self, music_file):
        """
        加载音乐文件
        :param music_file: 音乐文件路径
        """
        pygame.mixer.music.load(music_file)
        self.current_music = music_file

    def play_music(self, loops=0):
        """
        播放音乐
        :param loops: 循环次数，0表示无限循环
        """
        if self.current_music:
            pygame.mixer.music.play(loops) 