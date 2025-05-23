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


    def pre_creation_latency(self):
        return 5000 / self.flow_speed
    
    def __init__(self):
        proflie = json.load(open('gamedata/user_profile.json', 'r'))
        self.flow_speed = proflie['flow_speed']
        self.latency = proflie['latency']
        self.key_bindings = {}
        for action, key in proflie['key_bindings'].items():
            self.key_bindings[action] = getattr(pygame, key)

    def get_key(self, action: str):
        """
        获取按键绑定
        :param action: 动作名称
        :return: 按键绑定
        """
        return self.key_bindings.get(action)
    
    def update(self):
        """
        更新用户配置文件
        :return: None
        """
        with open('gamedata/user_profile.json', 'w') as f:
            json.dump({
                'flow_speed': self.flow_speed,
                'latency': self.latency,
                'key_bindings': {action: key for action, key in self.key_bindings.items()}
            }, f, indent=4)

