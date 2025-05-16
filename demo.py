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
                data: notedata.Note = event.dict['notedata']
                match data.decision:
                    case notedata.DecisionLevel.MISS: print("MISS")
                    case notedata.DecisionLevel.PERFECT: print("PERFECT")
                    case notedata.DecisionLevel.GREAT: print("GREAT")
                    case notedata.DecisionLevel.GOOD: print("GOOD")
                notesprite[event.dict['path']][event.dict['id']].kill()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    gamemgr.decide(0)
                elif event.key == pygame.K_f:
                    gamemgr.decide(1)
                elif event.key == pygame.K_j:
                    gamemgr.decide(2)
                elif event.key == pygame.K_k:
                    gamemgr.decide(3)
            elif event.type == en.GAME_OVER:
                going = False
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