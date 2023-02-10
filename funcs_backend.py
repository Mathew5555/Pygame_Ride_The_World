import os
import pygame
import sys
from PIL import Image
from consts import *
import random


pygame.mixer.init()
sound = pygame.mixer.Sound('data/mouse.mp3')
sound.set_volume(0.4)


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


def split_animated_gif(gif_file_path, screen=None):
    ret = []
    gifs = []
    if gif_file_path == 'klee':
        for i in range(1, 5):
            gifs.append(Image.open(f'images/klee/{i}.gif'))
        total = 0
        all_len = sum([i.n_frames for i in gifs])
        for gif in gifs:
            for frame_index in range(gif.n_frames):
                gif.seek(frame_index)
                frame_rgba = gif.convert("RGBA")
                pygame_image = pygame.image.fromstring(frame_rgba.tobytes(), frame_rgba.size,
                                                       frame_rgba.mode)
                ret.append(pygame.transform.scale(pygame_image, (1536, 864)))
                screen.fill((0, 0, 0))
                font = pygame.font.Font(FONT, 80)
                s = str(round(total / all_len * 100, 1)) + '%'
                text = font.render(f'Загружено:', True, (255, 255, 255))
                for i in range(len(s)):
                    text1 = font.render(s[i], True, (255, 255, 255))
                    screen.blit(text1, (600 + i * 50, 100))
                screen.blit(text, (100, 100))
                screen.blit(*pic('our_logo.png', (50, 500), add=(300, 300)))
                pygame.display.flip()
                total += 1
    else:
        gif = Image.open(gif_file_path)
        for frame_index in range(gif.n_frames):
            gif.seek(frame_index)
            frame_rgba = gif.convert("RGBA")
            pygame_image = pygame.image.fromstring(frame_rgba.tobytes(), frame_rgba.size,
                                                   frame_rgba.mode)
            ret.append(pygame.transform.scale(pygame_image, WINDOW_SIZE))
    return ret


def pic(picture, coords, add=(150, 60)):
    image = pygame.transform.scale(load_image(IMAGES_DIR + picture), add)
    imagerect = image.get_rect()
    imagerect.topleft = coords
    return image, imagerect


def play():
    data_ = [i.strip('\n') for i in open('data/sound.txt', mode='r', encoding='utf-8').readlines()]
    last, sound_lvl = data_[1], float(data_[0])
    tr = random.choice(TRACKS)
    while tr == last:
        tr = random.choice(TRACKS)
    file = open('data/sound.txt', mode='w', encoding='utf-8')
    file.write(f'{sound_lvl}\n{tr}')
    pygame.mixer.music.load(tr)
    pygame.mixer.music.play(1)
    pygame.mixer.music.set_volume(sound_lvl)


def check_busy(sound_level):
    if not pygame.mixer.music.get_busy():
        play()
    if round(pygame.mixer.music.get_volume(), 1) != sound_level:
        sound_level = round(sound_level, 1)
        file1 = open('data/sound.txt', mode='r', encoding='utf-8')
        data = file1.readlines()
        file1.close()
        file2 = open('data/sound.txt', mode='w', encoding='utf-8')
        pygame.mixer.music.set_volume(sound_level)
        file2.write(f'{sound_level}\n{data[1]}')
        file2.close()
