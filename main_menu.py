import pygame
import os
import sys
import random
from PIL import Image


MUSIC_DIR = "music/"
IMAGES_DIR = "images/"
FPS = 45
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1500, 1000
FON = []


pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()


class Hero:
    pass


class Menu:
    def __init__(self, shop='shop.png', info='info.png', start1='play1.png', start2='play1.png',
                 check='check.png', platform='platform.png'):
        self.btn_shop = pic(shop, (20, 20))
        self.btn_info = pic(info, (190, 20))
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


def pic(picture, coords, add=(150, 60)):
    image = pygame.transform.scale(load_image(IMAGES_DIR + picture), add)
    imagerect = image.get_rect()
    imagerect.topleft = coords
    return image, imagerect


def time_to_game(menu, timer):
    if menu.both_checked():
        timer += clock.tick(FPS)
        if timer < 3000:
            screen.blit(*menu.cd['bg'])
        screen.blit(*menu.cd[max(3 - int(timer / 1000), 0)])
    else:
        timer = 0
        clock.tick(FPS)


def split_animated_gif(gif_file_path):
    ret = []
    gif = Image.open(gif_file_path)
    for frame_index in range(gif.n_frames):
        gif.seek(frame_index)
        frame_rgba = gif.convert("RGBA")
        pygame_image = pygame.image.fromstring(frame_rgba.tobytes(), frame_rgba.size,
                                               frame_rgba.mode)
        ret.append(pygame.transform.scale(pygame_image, WINDOW_SIZE))
    return ret


def load_image(name, colorkey=None):
    # если файл не существует, то выходим
    if not os.path.isfile(name):
        print(f"Файл с изображением '{name}' не найден")
        sys.exit()
    image = pygame.image.load(name)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def main():
    menu = Menu()
    FON = split_animated_gif(IMAGES_DIR + 'fon.gif')[:]
    running = True
    ind = 0
    clock.tick(FPS)
    play()
    timer = 0
    clock.tick(FPS)
    while running:
        screen.blit(FON[ind], (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if menu.btn_start1[1].colliderect(pygame.rect.Rect(*mouse, 10, 10)):
                    menu.update(menu.btn_start1)
                if menu.btn_start2[1].colliderect(pygame.rect.Rect(*mouse, 10, 10)):
                    menu.update(menu.btn_start2)
        time_to_game(menu, timer)
        screen.blit(*menu.btn_start1)
        screen.blit(*menu.btn_start2)
        screen.blit(*menu.check_mark1)
        screen.blit(*menu.check_mark2)
        screen.blit(*menu.btn_shop)
        screen.blit(*menu.btn_info)
        screen.blit(menu.platform, (375 - menu.platform.get_size()[0] // 2, 500))
        screen.blit(menu.platform, (1125 - menu.platform.get_size()[0] // 2, 500))
        pygame.display.flip()
        ind = (ind + 1) % len(FON)


def play():
    pygame.mixer.init()
    pygame.mixer.music.load(random.choice([MUSIC_DIR + 'chasm' + f'{i}.mp3' for i in range(1, 4)]))
    pygame.mixer.music.play(999)
    pygame.mixer.music.set_volume(0.5)


if __name__ == '__main__':
    main()
