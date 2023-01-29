from funcs_backend import *
import pygame
from consts import *


pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
RUNNING = True
CURR_VOLUME = 0


class Volume:
    def __init__(self, plus='volume-up.png', minus='volume-down.png'):
        self.colors = [(76, 187, 23), (154, 205, 50), (209, 226, 49), (255, 220, 51), (244, 176, 46),
                       (243, 165, 5), (237, 118, 14), (255, 117, 20), (255, 79, 0), (179, 40, 33)]
        # (241, 58, 19)
        self.btn_plus = pic(plus, (500, 300), add=(50, 50))
        self.btn_minus = pic(minus, (50, 300), add=(50, 50))
        self.lvls = []
        for i in range(10):
            self.lvls.append((pygame.rect.Rect(50 * (i + 1), 260, 50, 30), self.colors[i]))

    def text(self):
        font = pygame.font.Font(FONT, 45)
        text = font.render('Настройка громкости', True, (255, 255, 255))
        screen.blit(text, (50, 190))

    def render(self, screen):
        bottom = pygame.Surface((540, 200))
        bottom.set_alpha(100)
        bottom.fill((255, 255, 255))
        screen.blit(bottom, (30, 180))
        #pygame.draw.rect(screen, pygame.Color(255, 255, 255, 200), (30, 160, 540, 200), border_radius=15)
        for i in range(int(10 * CURR_VOLUME)):
            pygame.draw.rect(screen, self.lvls[i][1], self.lvls[i][0])
        pygame.draw.rect(screen, (0, 0, 0), pygame.rect.Rect(50, 260, 500, 30).inflate(5, 5), 5)
        screen.blit(*self.btn_plus)
        screen.blit(*self.btn_minus)
        self.text()

    def plus(self):
        global CURR_VOLUME
        CURR_VOLUME += 0.1
        CURR_VOLUME = min(round(CURR_VOLUME, 1), 1)

    def minus(self):
        global CURR_VOLUME
        CURR_VOLUME -= 0.1
        CURR_VOLUME = max(round(CURR_VOLUME, 1), 0)


class Settings:
    def __init__(self, back='back.png'):
        self.btn_back = pic(back, (20, 20))
        self.volume_box = Volume()

    def render(self, screen):
        screen.blit(*self.btn_back)
        self.volume_box.render(screen)

    def back(self):
        global RUNNING
        RUNNING = False


def settings(old_volume):
    global RUNNING, CURR_VOLUME
    setting = Settings()
    FON = split_animated_gif(IMAGES_DIR + 'fon_sett.gif')[:]
    ind = 0
    RUNNING = True
    clock.tick(FPS2)
    CURR_VOLUME = old_volume
    while RUNNING:
        screen.blit(FON[ind], (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
            fl = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if setting.btn_back[1].collidepoint(*mouse):
                    setting.back()
                    break
                if setting.volume_box.btn_plus[1].collidepoint(*mouse):
                    setting.volume_box.plus()
                    fl = True
                if setting.volume_box.btn_minus[1].collidepoint(*mouse):
                    setting.volume_box.minus()
                    fl = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_EQUALS:
                    setting.volume_box.plus()
                    fl = True
                elif event.key == pygame.K_MINUS:
                    setting.volume_box.minus()
                    fl = True
            if fl:
                pygame.mixer.music.set_volume(CURR_VOLUME)
        setting.render(screen)
        pygame.display.flip()
        ind = (ind + 1) % len(FON)
        clock.tick(FPS2)
    return CURR_VOLUME


if __name__ == '__main__':
    settings(1)
