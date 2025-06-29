import pygame
import json
import scenes
from config import *
from gamedata.mediaplayer import MediaPlayer, SEID


def main():
    pygame.init()
    MediaPlayer.init()
    MediaPlayer.global_player.play_sound_effect(SEID.ENTRY)
    screen = pygame.display.set_mode((WD_WID, WD_HEI), pygame.FULLSCREEN | pygame.SCALED)
    clock = pygame.time.Clock()

    current_scn = scenes.MainScene(screen, clock)
    args = []
    kwargs = {}
    while current_scn is not None:
        current_scn, args, kwargs = current_scn.main_loop(*args, **kwargs)


if __name__ == '__main__':
    main()
