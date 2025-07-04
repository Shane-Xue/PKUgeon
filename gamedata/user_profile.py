"""
定义了UserProfile数据结构
"""
from dataclasses import dataclass
import json
import pygame


@dataclass
class UserProfile:
    """
    游戏玩家的一系列偏好设置，包括流速，延迟。

    :ivar latency: 延迟，单位为ms，正值代表提前播放音乐（即假设玩家的音乐播放设备有延迟）
    :ivar flow_speed: 流速，note从顶端落到底端需要的时间为5s/flow_speed
    """

    def pre_creation_offset(self):
        return 5000 / self.flow_speed
    
    def __init__(self):
        with open('save/user_profile.json', 'r') as file:
            profile: dict = json.load(file)
            self.flow_speed = profile.get('flow_speed', 5)
            self.latency = profile.get('latency', 0)
            self.music_volume = profile.get('music_volume', 100)
            self.sfx_volume = profile.get('sfx_volume', 100)
            self.key_bindings = {}
            for action, key in profile['key_bindings'].items():
                self.key_bindings[action] = [getattr(pygame, key), key]

    def get_key(self, action: str):
        """
        获取按键绑定
        :param action: 动作名称
        :return: 按键绑定
        """
        return self.key_bindings.get(action)[0]
    
    def update(self):
        """
        更新用户配置文件
        :return: None
        """
        with open('save/user_profile.json', 'w') as f:
            json.dump({
                'flow_speed': self.flow_speed,
                'latency': self.latency,
                'music_volume': self.music_volume,
                'sfx_volume': self.sfx_volume,
                'key_bindings': {action: key[1] for action, key in self.key_bindings.items()}
            }, f, indent=4)

