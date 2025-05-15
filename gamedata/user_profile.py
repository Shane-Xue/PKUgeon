"""
定义了user_profile数据结构
"""


class UserProfile:
    """
    游戏玩家的一系列偏好设置，包括流速，延迟。
    """
    def __init__(self):
        self.latency = 0
        self.flow_speed = 5

