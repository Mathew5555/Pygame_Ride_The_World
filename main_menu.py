import random
from funcs_backend import *
import pygame
from consts import *
from info_window import info
from settings_window import settings
from guide_window import guide


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
RUNNING = True
SOUND_LEVEL = 0.5


class Hero:
    pass


class Menu:
    def __init__(self, shop='shop.png', info='info.png', start1='play1.png', start2='play1.png',
                 check='check.png', platform='platform.png', sett='setting.png', exit='exit.png',
                 guide='user-guide.png'):
        self.btn_shop = pic(shop, (20, 20))
        self.btn_info = pic(info, (190, 20))
        self.btn_sett = pic(sett, (360, 20), add=(60, 60))
        self.btn_guide = pic(guide, (440, 20), add=(60, 60))
        self.btn_exit = pic(exit, (1330, 20))
        self.btn_start1 = pic(start1, (300, 800))
        self.btn_start2 = pic(start2, (1050, 800))
        self.check_mark1 = pic(check, (-400, -400), add=(40, 40))
        self.check_mark2 = pic(check, (-400, -400), add=(40, 40))
        self.platform = load_image(IMAGES_DIR + platform)
        self.cd = {0: pic('go.png', (650, 450), add=(200, 100)),
                   1: pic('one.png', (700, 450), add=(100, 100)),
                   2: pic('two.png', (700, 450), add=(100, 100)),
                   3: pic('three.png', (700, 450), add=(100, 100)),
                   'bg': pic('num_bg.png', (700, 425), add=(100, 190))}
        self.effects = {j: pic(f'boom/{j}.png', (675, 425), add=(150, 150)) for j in range(1, 13)}

    def render(self, screen):
        screen.blit(*self.btn_start1)
        screen.blit(*self.btn_start2)
        screen.blit(*self.check_mark1)
        screen.blit(*self.check_mark2)
        screen.blit(*self.btn_shop)
        screen.blit(*self.btn_info)
        screen.blit(*self.btn_sett)
        screen.blit(*self.btn_exit)
        screen.blit(*self.btn_guide)
        screen.blit(self.platform, (375 - self.platform.get_size()[0] // 2, 500))
        screen.blit(self.platform, (1125 - self.platform.get_size()[0] // 2, 500))

    def update(self, btn):
        if btn == self.btn_start1:
            x, y = self.check_mark1[1][0], self.check_mark1[1][1]
            if (x, y) == (-400, -400):
                x, y = 460, 770
                self.btn_start1 = pic('play2.png', (300, 800))
            else:
                x, y = -400, -400
                self.btn_start1 = pic('play1.png', (300, 800))
            self.check_mark1 = self.check_mark1[0], (x, y, 40, 40)
        elif btn == self.btn_start2:
            x, y = self.check_mark2[1][0], self.check_mark2[1][1]
            if (x, y) == (-400, -400):
                x, y = 1210, 770
                self.btn_start2 = pic('play2.png', (1050, 800))
            else:
                x, y = -400, -400
                self.btn_start2 = pic('play1.png', (1050, 800))
            self.check_mark2 = self.check_mark2[0], (x, y, 40, 40)

    def both_checked(self):
        return self.check_mark1[1] != (-400, -400, 40, 40) and \
               self.check_mark2[1] != (-400, -400, 40, 40)

    def open_info(self):
        info()

    def open_shop(self):
        pass

    def open_guide(self):
        guide()

    def open_settings(self):
        global SOUND_LEVEL
        SOUND_LEVEL = settings(SOUND_LEVEL)


def play():
    pygame.mixer.music.load(random.choice([MUSIC_DIR + 'chasm' + f'{i}.mp3' for i in range(1, 8)]))
    pygame.mixer.music.play(1)
    pygame.mixer.music.set_volume(SOUND_LEVEL)


def time_to_game(menu, timer):
    if menu.both_checked():
        timer += clock.tick(FPS)
        if timer < 3000:
            screen.blit(*menu.cd['bg'])
        screen.blit(*menu.cd[max(3 - int(timer / 1000), 0)])
        if timer < 3000:
            screen.blit(*menu.effects[max((timer % 1000) // 83, 1)])
    else:
        timer = 0
        clock.tick(FPS)
    return timer


def main():
    global RUNNING
    menu = Menu()
    play()
    FON = split_animated_gif(IMAGES_DIR + 'fon.gif')[:]
    ind = 0
    timer = 0
    clock.tick(FPS)
    while RUNNING:
        screen.blit(FON[ind], (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if menu.btn_start1[1].collidepoint(*mouse):
                    menu.update(menu.btn_start1)
                if menu.btn_start2[1].collidepoint(*mouse):
                    menu.update(menu.btn_start2)
                if menu.btn_info[1].collidepoint(*mouse):
                    menu.open_info()
                if menu.btn_shop[1].collidepoint(*mouse):
                    menu.open_shop()
                if menu.btn_sett[1].collidepoint(*mouse):
                    menu.open_settings()
                if menu.btn_guide[1].collidepoint(*mouse):
                    menu.open_guide()
                if menu.btn_exit[1].collidepoint(*mouse):
                    RUNNING = False
                    break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    menu.update(menu.btn_start1)
                elif event.key == pygame.K_RSHIFT:
                    menu.update(menu.btn_start2)
        if not pygame.mixer.music.get_busy():
            play()
        if pygame.mixer.music.get_volume() != SOUND_LEVEL:
            pygame.mixer.music.set_volume(SOUND_LEVEL)

        timer = time_to_game(menu, timer)
        menu.render(screen)
        pygame.display.flip()
        ind = (ind + 1) % len(FON)


if __name__ == '__main__':
    main()
