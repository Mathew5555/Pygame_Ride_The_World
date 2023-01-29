import os
import pygame
import sys
from PIL import Image
from consts import *
import random


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


def pic(picture, coords, add=(150, 60)):
    image = pygame.transform.scale(load_image(IMAGES_DIR + picture), add)
    imagerect = image.get_rect()
    imagerect.topleft = coords
    return image, imagerect
