"""
config.py

配置各种无法被用户修改的游戏参数
"""

import os
import sys

WD_HEI = 1080  # 主窗口高度
WD_WID = 1920  # 主窗口宽度

PATHS = 4  # 4k

GAP_TIME = 3000  # 进入游戏后的间隙时间

FPS = 60

DECISION_POS = 960  # 判定线位置
TOP_POS = 80  # note最早出现的位置

HOLD_LINE_WIDTH = 10

PERFECT_INTERVAL = 30  # ms
GREAT_INTERVAL = 60  # ms
GOOD_INTERVAL = 100  # ms
MISS_INTERVAL = 200  # ms

# THEME_COLOR = (0x8e, 0xc7, 0xcc)
THEME_COLOR = (135, 178, 176)


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
