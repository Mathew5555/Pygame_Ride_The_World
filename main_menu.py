import random
from funcs_backend import *
import pygame
from consts import *
from info_window import info
from settings_window import settings
from guide_window import guide
from wardrobe_window import wb
from account_info_window import acc


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
RUNNING = True
SOUND_LEVEL = 0.5
LAST = ''
PLATFORMS = pygame.sprite.Group()


class Hero:
    pass


class Platform(pygame.sprite.Sprite):
    def __init__(self, image, x):
        super().__init__(PLATFORMS)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.update(x, 500, self.rect[2], self.rect[3])
        self.mask = pygame.mask.from_surface(self.image)

        load_image(IMAGES_DIR + 'platform.png')


class Menu:
    def __init__(self, shop='store.png', info='info.png', start1='play1.png', start2='play1.png',
                 check='check.png', sett='setting.png', exit='exit.png', plat='platform.png',
                 guide='user-guide.png', wardrobe='wardrobe.png', acc_im='user.png', logo='logo.png'):
        self.btn_acc = pic(acc_im, (20, 20), add=(70, 70))
        self.btn_shop = pic(shop, (110, 20), add=(70, 70))
        self.btn_wb = pic(wardrobe, (200, 20), add=(70, 70))

        self.btn_sett = pic(sett, (980, 20), add=(70, 70))
        self.btn_guide = pic(guide, (1070, 20), add=(70, 70))
        self.btn_info = pic(info, (1160, 20))
        self.btn_exit = pic(exit, (1330, 20))

        self.logo_image = pic(logo, (600, 150), add=(300, 200))

        self.btn_start1 = pic(start1, (300, 800))
        self.btn_start2 = pic(start2, (1050, 800))
        self.check_mark1 = pic(check, (-400, -400), add=(40, 40))
        self.check_mark2 = pic(check, (-400, -400), add=(40, 40))
        plat_pic = load_image(IMAGES_DIR + plat)
        self.platform1 = Platform(plat_pic, 375 - plat_pic.get_size()[0] // 2)
        self.platform2 = Platform(plat_pic, 1125 - plat_pic.get_size()[0] // 2)

        self.cd = {0: pic('go.png', (600, 425), add=(300, 150)),
                   1: pic('one.png', (650, 400), add=(200, 200)),
                   2: pic('two.png', (650, 400), add=(200, 200)),
                   3: pic('three.png', (650, 400), add=(200, 200)),
                   'bg': pic('num_bg.png', (650, 350), add=(200, 380))}
        self.effects = {j: pic(f'boom/{j}.png', (600, 350), add=(300, 300)) for j in range(1, 13)}

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
        screen.blit(*self.btn_wb)
        screen.blit(*self.btn_acc)
        screen.blit(*self.logo_image)
        PLATFORMS.draw(screen)

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

    def open_wb(self):
        wb()

    def open_guide(self):
        guide()

    def open_acc(self):
        acc()

    def open_settings(self):
        global SOUND_LEVEL
        SOUND_LEVEL = settings(SOUND_LEVEL)


def play():
    global LAST
    tr = random.choice(TRACKS)
    while tr == LAST:
        tr = random.choice(TRACKS)
    LAST = tr
    pygame.mixer.music.load(tr)
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
                    print(1)
                if menu.btn_guide[1].collidepoint(*mouse):
                    menu.open_guide()
                if menu.btn_wb[1].collidepoint(*mouse):
                    menu.open_wb()
                if menu.btn_acc[1].collidepoint(*mouse):
                    menu.open_acc()
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
