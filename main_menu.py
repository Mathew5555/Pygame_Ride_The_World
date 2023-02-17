import random
from funcs_backend import *
import pygame
import sqlite3
from consts import *
from info_window import info
from settings_window import settings
from guide_window import guide
from wardrobe_window import wb
from account_info_window import acc
from playing_mode import game
from shop import shop


pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Ride The World - BETA 1.0')
clock = pygame.time.Clock()
RUNNING = True
PLATFORMS = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()


class Hero(pygame.sprite.Sprite):
    def __init__(self, player_id, x, y, color, joy, joystick=None):
        super().__init__(player_group, all_sprites)
        self.player_id = player_id
        self.joy = joy
        self.joystick = joystick

        self.gravity = 1
        self.speed_x = 7
        self.speed_y = 5
        self.fly = 0

        self.cur_frame = 0
        self.jump_frame = 0

        self.rect = pygame.Rect(x, y, 56, 80)

        self.color = color
        self.sheet()
        if self.player_id == 1:
            self.direction = "right"
            self.image = self.images_dict["stand_r"]
        else:
            self.direction = "left"
            self.image = self.images_dict["stand_l"]

    def sheet(self):
        images_path = {"stand_r": f"{self.color}/stand.png",
                       "jump_r": f"{self.color}/jump.png", "land_r": f"{self.color}/hit.png"}
        self.images_dict = dict()
        for key, val in images_path.items():
            self.images_dict[key] = pygame.transform.scale(load_image(f"{IMAGES_DIR}" + val),
                                                           (self.rect.width, self.rect.height))
            if key != "dead_image":
                self.images_dict[key[:-1] + "l"] = pygame.transform.flip(self.images_dict[key],
                                                                         True, False)
        self.images_dict["right"] = [
            pygame.transform.scale(load_image(f"{IMAGES_DIR}{self.color}/walk{i + 1}.png"),
                                   (self.rect.width, self.rect.height)) for i in range(2)]
        self.images_dict["left"] = [pygame.transform.flip(image, True, False) for image in
                                    self.images_dict["right"]]

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
        ups = any([self.rect.bottom <= i.rect.top + 5 and i.rect.left - 3 <= self.rect.centerx <= i.rect.right + 3 for i in PLATFORMS.sprites()])
        flag_collide = pygame.sprite.spritecollideany(self, PLATFORMS) and ups
        if self.button(keys, "left"):
            self.rect.x -= self.speed_x
            if flag_collide:
                self.cur_frame = (self.cur_frame + 1) % len(self.images_dict["left"])
                self.image = self.images_dict["left"][self.cur_frame]
            flag = 1
            self.direction = "left"
        if self.button(keys, "right"):
            self.rect.x += self.speed_x
            if flag_collide:
                self.cur_frame = (self.cur_frame + 1) % len(self.images_dict["right"])
                self.image = self.images_dict["right"][self.cur_frame]
            flag = 1
            self.direction = "right"
        if self.button(keys, "up") and flag_collide:
            self.jump_frame = 20
            flag = 1
            if self.direction == "left":
                self.image = self.images_dict["jump_l"]
            else:
                self.image = self.images_dict["jump_r"]
        if not flag_collide and not self.jump_frame:
            self.rect.y += self.speed_y
            if self.direction == "left":
                self.image = self.images_dict["land_l"]
            else:
                self.image = self.images_dict["land_r"]
        elif not flag and not self.jump_frame:
            if self.direction == "left":
                self.image = self.images_dict["stand_l"]
            else:
                self.image = self.images_dict["stand_r"]
        if self.jump_frame > 0:
            self.rect.y -= 10
            self.jump_frame -= 1


class Platform(pygame.sprite.Sprite):
    def __init__(self, image, x):
        super().__init__(PLATFORMS)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.update(x, 700, self.rect[2], self.rect[3])
        self.mask = pygame.mask.from_surface(self.image)

        load_image(IMAGES_DIR + 'platform.png')


class Menu:
    def __init__(self, hero1, hero2, shop='store.png', info='info.png', start1='play1.png', start2='play1.png',
                 check='check.png', sett='setting.png', exit='exit.png', plat='platform.png',
                 guide='user-guide.png', wardrobe='wardrobe.png', acc_im='user.png', logo='our_logo.png'):
        self.hero1 = hero1
        self.hero2 = hero2
        self.btn_acc = pic(acc_im, (20, 20), add=(70, 70))
        self.btn_shop = pic(shop, (110, 20), add=(70, 70))
        self.btn_wb = pic(wardrobe, (200, 20), add=(70, 70))

        self.btn_sett = pic(sett, (980, 20), add=(70, 70))
        self.btn_guide = pic(guide, (1070, 20), add=(70, 70))
        self.btn_info = pic(info, (1160, 20))
        self.btn_exit = pic(exit, (1330, 20))

        self.logo_image = pic(logo, (600, 50), add=(300, 300))

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
        self.hero1.render(screen)
        self.hero2.render(screen)
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
        shop()

    def open_wb(self):
        wb()

    def open_guide(self):
        guide()

    def open_acc(self):
        acc()

    def open_settings(self):
        settings()

    def start_game(self):
        game(self.hero1.color, self.hero2.color)


def time_to_game(menu, timer):
    if menu.both_checked():
        timer += clock.tick(FPS)
        if timer < 3000:
            screen.blit(*menu.cd['bg'])
        screen.blit(*menu.cd[max(3 - int(timer / 1000), 0)])
        if timer < 3000:
            screen.blit(*menu.effects[max((timer % 1000) // 83, 1)])
        if timer > 4000:
            timer = 0
            menu.update(menu.btn_start1)
            menu.update(menu.btn_start2)
            menu.start_game()
            pygame.display.set_mode(WINDOW_SIZE)
    else:
        timer = 0
        clock.tick(FPS)
    return timer


def main():
    global RUNNING
    joy = False
    con = sqlite3.connect('data/account_info.db')
    cur = con.cursor()
    res = cur.execute("""SELECT curr_skin FROM info""").fetchall()
    if joy:
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for el in joysticks:
            el.init()
        print(joysticks)
        hero1 = Hero(1, 250, 20, res[0][0], joy, joystick=joysticks[0])
        hero2 = Hero(2, 1200, 20, res[1][0], joy, joystick=joysticks[1])
    else:
        hero1 = Hero(1, 250, 20, res[0][0], joy)
        hero2 = Hero(2, 1200, 20, res[1][0], joy)
    menu = Menu(hero1, hero2)
    pygame.display.set_mode(WINDOW_SIZE)
    play()
    FON = split_animated_gif(IMAGES_DIR + 'fon.gif')[:]
    ind = 0
    timer = 0
    clock.tick(FPS)

    while RUNNING:
        screen.blit(FON[ind], (0, 0))
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
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
                    res = cur.execute("""SELECT curr_skin FROM info""").fetchall()
                    hero1.color = res[0][0]
                    hero1.sheet()
                    hero2.color = res[1][0]
                    hero2.sheet()
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
        hero1.move(keys)
        hero2.move(keys)
        if not screen.get_rect().colliderect(hero1.rect):
            hero1.rect.x = 250
            hero1.rect.y = 20
        if not screen.get_rect().colliderect(hero2.rect):
            hero2.rect.x = 1200
            hero2.rect.y = 20
        pygame.display.flip()
        ind = (ind + 1) % len(FON)
    con.close()


if __name__ == '__main__':
    main()
