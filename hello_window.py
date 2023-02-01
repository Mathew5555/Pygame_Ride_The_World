import pygame
from main_menu import main
from funcs_backend import *
from consts import *


MUSIC_DIR = "music/"
IMAGES_DIR = "images/"
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1535, 864
FON = []


pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
pygame.mixer.music.load('music/hello.mp3')
pygame.mixer.music.play(999)
pygame.mixer.music.set_volume(0.5)


if __name__ == '__main__':
    FON = split_animated_gif('klee', screen=screen)
    running = True
    ind = 0
    while running:
        if ind >= len(FON):
            ind = 0
        screen.blit(FON[ind], (0, 0))
        font = pygame.font.Font(FONT, 50)
        text = font.render('Нажмите любую клавишу, чтобы продолжить', True, (255, 255, 255))
        text_x = 100
        text_y = 800
        screen.blit(text, (text_x, text_y))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                running = False
                """font = pygame.font.Font(FONT, 80)
                text = font.render('Загрузка...', True, (255, 255, 255))
                text_x = 600
                text_y = 700
                screen.blit(text, (text_x, text_y))
                pygame.display.flip()"""
                pygame.mixer.music.unload()
                main()
                break
        clock.tick(FPS2)
        ind += 1
        pygame.display.flip()
