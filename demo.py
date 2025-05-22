import pygame
import json
import game_manager
from gamedata.user_profile import UserProfile
import event_number as en
from scenes.main_scene import MainScene
from sprites.path import PathSprite
from sprites.notesprite.tap import TapSprite, linear_calc_midbottom
from config import *
from note import notedata


def main():
    pygame.init()
    screen = pygame.display.set_mode((WD_WID, WD_HEI))
    clock = pygame.time.Clock()

    current_scn = MainScene(screen, clock)
    args = []
    kwargs = {}
    while current_scn is not None:
        current_scn, args, kwargs = current_scn.main_loop(*args, **kwargs)


def random_generate():
    """为了测试先随机生成个谱面"""
    trkdata = {'duration_ms': 60000, 'bpm': 60, 'notes': []}
    # 全部弄成8分好了
    t = 2000
    r = t
    while t < 60000:
        r = r * 313 % 997
        trkdata['notes'].append({'type': 'tap',
                                 'path': int(r % 4),
                                 'time': t,
                                 })
        t += 1000 / 8
    with open('demo.trk', 'w') as file:
        json.dump(trkdata, file)


if __name__ == '__main__':
    main()