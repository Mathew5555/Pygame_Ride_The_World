from funcs_backend import *
import pygame
from consts import *


pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
RUNNING = True


class Settings:
    def __init__(self, back='back.png'):
        self.btn_back = pic(back, (20, 20))

    def render(self, screen):
        screen.blit(*self.btn_back)

    def back(self):
        global RUNNING
        RUNNING = False


def settings():
    global RUNNING
    info = Settings()
    FON = split_animated_gif(IMAGES_DIR + 'fon_sett.gif')[:]
    ind = 0
    RUNNING = True
    clock.tick(FPS2)
    while RUNNING:
        screen.blit(FON[ind], (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if info.btn_back[1].colliderect(pygame.rect.Rect(*mouse, 10, 10)):
                    info.back()
                    break
        info.render(screen)
        pygame.display.flip()
        ind = (ind + 1) % len(FON)
        clock.tick(FPS2)


if __name__ == '__main__':
    settings()
