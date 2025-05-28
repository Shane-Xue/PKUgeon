import pygame
import json
import scenes
from config import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((WD_WID, WD_HEI), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    current_scn = scenes.MainScene(screen, clock)
    args = []
    kwargs = {}
    while current_scn is not None:
        current_scn, args, kwargs = current_scn.main_loop(*args, **kwargs)


def random_generate():
    """为了测试先随机生成个谱面"""
    trkdata = {'duration_ms': 60000, 'bpm': 60, 'title': 'RANDOM', 'artist': 'None',
               'chart_maker': 'Random', 'level': 12, 'notes': []}
    # 全部弄成8分好了
    t = 2000

    class R:
        def __init__(self):
            self.r = 2000

        def __call__(self):
            self.r = self.r * 313 % 997
            return self.r % 4

    r = R()
    while t < 60000:
        if r() % 10 == 0:
            trkdata['notes'].append({'type': 'hold',
                                     'path': r(),
                                     'time': t,
                                     'interval': 1000 / 4})
            t += 3000 / 8
        else:
            trkdata['notes'].append({'type': 'tap',
                                     'path': r(),
                                     'time': t,
                                     })
            t += 1000 / 8
    with open('save/trackfile/demo/demo', 'w') as file:
        json.dump(trkdata, file)


if __name__ == '__main__':
    random_generate()
    main()
