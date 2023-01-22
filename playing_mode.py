import pygame
import pytmx
import os
import sys
import random


MAPS_DIR = "maps/"
MUSIC_DIR = "music/"
IMAGES_DIR = "images/"
FPS = 60
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1500, 1000
MAP_SIZE = MAP_WIDTH, MAP_HEIGHT = 3200, 1600


class Map:
    def __init__(self, filename, free_tiles):
        self.map = pytmx.load_pygame(f"{MAPS_DIR}{filename}")
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        self.free_tiles = free_tiles

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                if image is None:
                    continue
                screen.blit(image, (x * self.tile_size - (MAP_WIDTH - WINDOW_WIDTH * 1.5) // 2,
                                    y * self.tile_size - (MAP_HEIGHT - WINDOW_HEIGHT * 1.5) // 2))

    def get_tile_id(self, position):
        return self.map.tiledgidmap[self.map.get_tile_gid(*position, 0)]

    def is_free(self, position):
        return self.get_tile_id(position) in self.free_tiles


class Hero:
    pass


class Game:
    def __init__(self, map, hero1, hero2):
        self.map = map
        self.hero1 = hero1
        self.hero2 = hero2

    def render(self, screen):
        self.map.render(screen)
        # self.hero1.render(screen)
        # self.hero2.render(screen)

    def update_hero(self):
        pass

    def check_win(self):
        pass

    def check_lose(self):
        pass


# Сообщение о победе какого-либо игрока с подсчетом очков
def show_message(screen, message):
    pass


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
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    map = Map("map1.tmx", [])
    hero1 = Hero()
    hero2 = Hero()
    game = Game(map, hero1, hero2)

    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    running = True
    game_over = False
    fon = pygame.transform.scale(load_image(IMAGES_DIR + 'background_inazuma.jpg'),
                                 (MAP_WIDTH, MAP_HEIGHT))
    pygame.mixer.init()
    pygame.mixer.music.load(random.choice([MUSIC_DIR + 'inazuma' + f'{i}.mp3' for i in range(1, 6)]))
    pygame.mixer.music.play(999)
    pygame.mixer.music.set_volume(0.5)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(fon, (0, 0))
        map.render(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
