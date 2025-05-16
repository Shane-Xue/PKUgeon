import pygame
import json
import game_manager
from gamedata.user_profile import UserProfile
import event_number as en
from sprites.path import PathSprite
from sprites.notesprite.tap import TapSprite, linear_calc_midbottom
from config import *
from note import notedata


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))

    random_generate()

    gamemgr = game_manager.GameManager(UserProfile(), 'demo.trk')
    gamemgr.prepare()

    going = True
    time = pygame.time.Clock()

    pathsprite = [PathSprite(i) for i in range(PATHS)]
    pathgroup = pygame.sprite.Group(pathsprite)

    notesprite: list[dict[int, TapSprite]] = [{} for i in range(PATHS)]
    notegroups = [pygame.sprite.Group() for _ in range(PATHS)]

    calc_midbottom = linear_calc_midbottom(gamemgr.userprofile.flow_speed, DECISION_POS, INIT_POS)

    while going:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = False
            elif event.type == en.CREATE_NOTE:
                data: notedata.Note = event.dict['notedata']
                if data.type == notedata.NoteType.TAP:
                    ntap = TapSprite(gamemgr.gametime, data.time, calc_midbottom, pathsprite[data.path])
                    notesprite[data.path][event.dict['id']] = ntap
                    notegroups[data.path].add(ntap)
                else:
                    print("error: unsupported note type")
            elif event.type == en.DISPOSE_NOTE:
                notesprite[event.dict['path']][event.dict['id']].kill()
        gamemgr.update(time.get_time())
        pathgroup.update(gamemgr.gametime)
        pathgroup.draw(screen)
        for notegroup in notegroups:
            notegroup.update(gamemgr.gametime)
            notegroup.draw(screen)
        pygame.display.flip()
        time.tick(FPS)


def random_generate():
    """为了测试先随机生成个谱面"""
    trkdata = {'duration_ms': 60000, 'bpm': 60, 'notes': []}
    # 全部弄成8分好了
    t = 2000
    while t < 60000:
        trkdata['notes'].append({'type': 'tap',
                                 'path': int(t * 997 % 4),
                                 'time': t,
                                 })
        t += 1000 / 8
    with open('demo.trk', 'w') as file:
        json.dump(trkdata, file)


if __name__ == '__main__':
    main()