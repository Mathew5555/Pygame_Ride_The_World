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
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
RUNNING = True
PLATFORMS = pygame.sprite.Group()


class Hero(pygame.sprite.Sprite):
    def __init__(self, player_id, x, y, joy, joystick=None):
        super().__init__(player_group, all_sprites)
        self.player_id = player_id
        self.joy = joy
        self.joystick = joystick

        self.gravity = 1
        self.fly = 0

        self.cur_frame = 0
        self.jump_frame = 0

        self.rect = pygame.Rect(x, y, 28, 40)

        self.sheet()
        if self.player_id == 1:
            self.direction = "right"
            self.image = self.stand_r
        else:
            self.direction = "left"
            self.image = self.stand_l

    def sheet(self):
        self.dead_image = pygame.transform.scale(load_image(f"images/ghost.png"),
                                                 (self.rect.width, self.rect.height))
        self.stand_r = pygame.transform.scale(load_image(f"man/p{self.player_id}_stand.png"),
                                              (self.rect.width, self.rect.height))
        self.stand_l = pygame.transform.flip(self.stand_r, True, False)

        self.jump_r = pygame.transform.scale(load_image(f"man/p{self.player_id}_jump.png"),
                                             (self.rect.width, self.rect.height))
        self.jump_l = pygame.transform.flip(self.jump_r, True, False)

        self.land_r = pygame.transform.scale(load_image(f"man/p{self.player_id}_hurt.png"),
                                             (self.rect.width, self.rect.height))
        self.land_l = pygame.transform.flip(self.land_r, True, False)

        right = [
            load_image(f"man/p{self.player_id}_walk/p{self.player_id}_walk01.png"),
            load_image(f"man/p{self.player_id}_walk/p{self.player_id}_walk02.png"),
            load_image(f"man/p{self.player_id}_walk/p{self.player_id}_walk03.png"),
            load_image(f"man/p{self.player_id}_walk/p{self.player_id}_walk04.png"),
            load_image(f"man/p{self.player_id}_walk/p{self.player_id}_walk05.png"),
            load_image(f"man/p{self.player_id}_walk/p{self.player_id}_walk06.png"),
            load_image(f"man/p{self.player_id}_walk/p{self.player_id}_walk07.png"),
            load_image(f"man/p{self.player_id}_walk/p{self.player_id}_walk08.png"),
            load_image(f"man/p{self.player_id}_walk/p{self.player_id}_walk09.png"),
            load_image(f"man/p{self.player_id}_walk/p{self.player_id}_walk10.png"),
            load_image(f"man/p{self.player_id}_walk/p{self.player_id}_walk11.png")
        ]

        self.right = [pygame.transform.scale(image, (self.rect.width, self.rect.height)) for image in right]
        self.left = [pygame.transform.flip(image, True, False) for image in self.right]

    def render(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def button(self, keys, direction):
        if self.player_id == 1:
            if not self.joy:
                if direction == "left":
                    return keys[pygame.K_a]
                elif direction == "right":
                    return keys[pygame.K_d]
                elif direction == "up":
                    return keys[pygame.K_w]
                elif direction == "down":
                    return keys[pygame.K_s]
                elif direction == "shoot":
                    return keys[pygame.K_e]
            else:
                if direction == "left":
                    return self.joystick.get_button(13)
                elif direction == "right":
                    return self.joystick.get_button(14)
                elif direction == "up":
                    return self.joystick.get_button(11)
                elif direction == "down":
                    return self.joystick.get_button(12)
                elif direction == "shoot":
                    return self.joystick.get_button(0)
        if not self.joy:
            if direction == "left":
                return keys[pygame.K_k]
            elif direction == "right":
                return keys[pygame.K_SEMICOLON]
            elif direction == "up":
                return keys[pygame.K_o]
            elif direction == "down":
                return keys[pygame.K_l]
            elif direction == "shoot":
                return keys[pygame.K_i]
        else:
            if direction == "left":
                return self.joystick.get_button(13)
            elif direction == "right":
                return self.joystick.get_button(14)
            elif direction == "up":
                return self.joystick.get_button(11)
            elif direction == "down":
                return self.joystick.get_button(12)
            elif direction == "shoot":
                return self.joystick.get_button(0)

    def move(self, keys):
        flag = 0
        if self.button(keys, "left"):
            self.rect.x -= 1
            self.cur_frame = (self.cur_frame + 1) % len(self.left)
            self.image = self.left[self.cur_frame]
        if self.button(keys, "right"):
            self.rect.x += 1
            self.cur_frame = (self.cur_frame + 1) % len(self.right)
            self.image = self.right[self.cur_frame]
        if self.button(keys, "up"):
            self.jump_frame = 20
            flag = 1
            if self.direction == "left":
                self.image = self.jump_l
            else:
                self.image = self.jump_r
        if self.button(keys, "down"):
            self.jump_frame = 0
        if not flag:
            if self.direction == "left":
                self.image = self.stand_l
            else:
                self.image = self.stand_r
        if self.jump_frame > 0:
            self.rect.y -= 1
            self.jump_frame -= 1
        else:
            self.rect.y += 1


class Platform(pygame.sprite.Sprite):
    def __init__(self, image, x):
        super().__init__(PLATFORMS)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.update(x, 700, self.rect[2], self.rect[3])
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

        self.btn_start1 = pic(start1, (300, 900))
        self.btn_start2 = pic(start2, (1050, 900))
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
                x, y = 460, 870
                self.btn_start1 = pic('play2.png', (300, 900))
            else:
                x, y = -400, -400
                self.btn_start1 = pic('play1.png', (300, 900))
            self.check_mark1 = self.check_mark1[0], (x, y, 40, 40)
        elif btn == self.btn_start2:
            x, y = self.check_mark2[1][0], self.check_mark2[1][1]
            if (x, y) == (-400, -400):
                x, y = 1210, 870
                self.btn_start2 = pic('play2.png', (1050, 900))
            else:
                x, y = -400, -400
                self.btn_start2 = pic('play1.png', (1050, 900))
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
        settings()


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
    pygame.display.set_mode(WINDOW_SIZE)
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
                sound.play(0)
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
        sound_level = float(
            open('data/sound.txt', mode='r', encoding='utf-8').readlines()[0].strip('\n'))
        check_busy(sound_level)
        timer = time_to_game(menu, timer)
        menu.render(screen)
        pygame.display.flip()
        ind = (ind + 1) % len(FON)


if __name__ == '__main__':
    main()
