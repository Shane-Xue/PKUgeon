"""定义了场景的基类Scene

"""
import pygame


class Scene:
    """场景
    直接控制一个窗口的显示，各对象的加载、更新等等。
    场景应当有一个主循环main_loop，main_loop被调用代表进入场景，退出main_loop代表场景关闭。
    """
    def __init__(self, main_window: pygame.Surface, clock: pygame.Clock):
        self.main_window = main_window
        self.clock = clock
        pass

    def main_loop(self, *args, **kwargs):
        """
        main_loop被调用代表进入场景，main_loop退出代表场景关闭。
        :return: tuple(下一个被调用的场景，参数...);如果是最后一个场景（即该场景退出后程序结束），tuple(None, [], {})
        """
        pass

