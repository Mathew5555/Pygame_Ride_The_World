import pygame
import os
import sys
import random
from PIL import Image


MUSIC_DIR = "music/"
IMAGES_DIR = "images/"
FPS = 60
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1500, 1000
FON = []


pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()


class Hero:
    pass


class Menu:
    def __init__(self, shop='shop.png', info='info.jpeg', start1='play1.webp', start2='play2.webp',
                 check='check.png', platform='platform.png'):
        self.btn_shop = pic(shop, (20, 20))
        self.btn_info = pic(info, (190, 20))
        self.btn_start1 = pic(start1, (300, 800))
        self.btn_start2 = pic(start2, (1050, 800))
        self.check_mark1 = pic(check, (-400, -400), add=(40, 40))
        self.check_mark2 = pic(check, (-400, -400), add=(40, 40))
        self.platform = load_image(IMAGES_DIR + platform)

    def update(self, btn):
        if btn == self.btn_start1:
            x, y = self.check_mark1[1][0], self.check_mark1[1][1]
            if (x, y) == (-400, -400):
                x, y = 460, 770
            else:
                x, y = -400, -400
            self.check_mark1 = self.check_mark1[0], (x, y)
        elif btn == self.btn_start2:
            x, y = self.check_mark2[1][0], self.check_mark2[1][1]
            if (x, y) == (-400, -400):
                x, y = 1210, 770
            else:
                x, y = -400, -400
            self.check_mark2 = self.check_mark2[0], (x, y)


def pic(picture, coords, add=(150, 60)):
    image = pygame.transform.scale(load_image(IMAGES_DIR + picture), add)
    imagerect = image.get_rect()
    imagerect.topleft = coords
    return image, imagerect


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

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    FON = split_animated_gif(IMAGES_DIR + 'fon.gif')[:]
    running = True
    play()
    ind = 0
    clock.tick(FPS)
    while running:
        clock.tick(FPS)
        screen.blit(FON[ind], (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if menu.btn_start1[1].colliderect(pygame.rect.Rect(*mouse, 15, 15)):
                    menu.update(menu.btn_start1)
                if menu.btn_start2[1].colliderect(pygame.rect.Rect(*mouse, 15, 15)):
                    menu.update(menu.btn_start2)
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
