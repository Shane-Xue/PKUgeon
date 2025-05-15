"""
定义了user_profile数据结构
"""


class UserProfile:
    """
    游戏玩家的一系列偏好设置，包括流速，延迟。

    :ivar latency: 延迟，单位为ms，正值代表提前播放音乐（即假设玩家的音乐播放设备有延迟）
    :ivar flow_speed: 流速，note从顶端落到底端需要的时间为5s/flow_speed
    """
    def __init__(self):
        self.flow_speed = 5
        self.latency = 0

    def pre_creation_latency(self):
        return 5000 / self.flow_speed

