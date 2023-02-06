import pygame
import pytmx
import os
import sys
import random

MAPS_DIR = "maps/"
MUSIC_DIR = "music/"
IMAGES_DIR = "images/"
FPS = 60
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1600, 960
MAP_SIZE = MAP_WIDTH, MAP_HEIGHT = 1600, 960
all_sprites = pygame.sprite.Group()
player1_sprite = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()


def get_tile_properties(tmxdata, x, y, layer):
    tile_x = x // 32
    tile_y = y // 32
    try:
        properties = tmxdata.get_tile_properties(tile_x, tile_y, layer)
    except ValueError:
        properties = {"solid": 0, "climb": 0, "kill": 0, "fire": 0, "up_solid": 0}
    if properties is None:
        properties = {"solid": 0, "climb": 0, "kill": 0, "fire": 0, "up_solid": 0}
    return properties


class Map:
    def __init__(self, filename, free_tiles):
        self.map = pytmx.load_pygame(f"{MAPS_DIR}{filename}")
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        self.free_tiles = free_tiles

    def render(self, screen, *args):
        for el in args:
            for y in range(self.height):
                for x in range(self.width):
                    image = self.map.get_tile_image(x, y, el - 1)
                    if image is None:
                        continue
                    screen.blit(image, (x * self.tile_size, y * self.tile_size))

    # def get_tile_id(self, position):
    #     return self.map.tiledgidmap[self.map.get_tile_gid(*position, 0)]
    #
    # def is_free(self, position):
    #     return self.get_tile_id(position) in self.free_tiles


class Hero(pygame.sprite.Sprite):
    def __init__(self, id):
        super().__init__(all_sprites)
        self.id = id
        self.direction = "right"
        self.cur_frame = 0
        self.sheet()
        self.image = self.stand_r
        self.rect = pygame.Rect(0, 0, 28, 40)
        self.jump_frame = 0
        self.fly = 0
        self.climb = False
        self.flag2 = 0

    def sheet(self):
        self.stand_r = pygame.transform.scale(
            pygame.image.load(f"Base pack/Player/p{self.id}_stand.png").convert_alpha(), (28, 40))
        self.stand_l = pygame.transform.flip(self.stand_r, True, False)
        self.jump_r = pygame.transform.scale(pygame.image.load(f"Base pack/Player/p{self.id}_jump.png").convert_alpha(),
                                             (28, 40))
        self.jump_l = pygame.transform.flip(self.jump_r, True, False)
        self.land_r = pygame.transform.scale(pygame.image.load(f"Base pack/Player/p{self.id}_hurt.png").convert_alpha(),
                                             (28, 40))
        self.land_l = pygame.transform.flip(self.land_r, True, False)
        right = [
            pygame.image.load(f"Base pack/Player/p{self.id}_walk/PNG/p{self.id}_walk01.png").convert_alpha(),
            pygame.image.load(f"Base pack/Player/p{self.id}_walk/PNG/p{self.id}_walk02.png").convert_alpha(),
            pygame.image.load(f"Base pack/Player/p{self.id}_walk/PNG/p{self.id}_walk03.png").convert_alpha(),
            pygame.image.load(f"Base pack/Player/p{self.id}_walk/PNG/p{self.id}_walk04.png").convert_alpha(),
            pygame.image.load(f"Base pack/Player/p{self.id}_walk/PNG/p{self.id}_walk05.png").convert_alpha(),
            pygame.image.load(f"Base pack/Player/p{self.id}_walk/PNG/p{self.id}_walk06.png").convert_alpha(),
            pygame.image.load(f"Base pack/Player/p{self.id}_walk/PNG/p{self.id}_walk07.png").convert_alpha(),
            pygame.image.load(f"Base pack/Player/p{self.id}_walk/PNG/p{self.id}_walk08.png").convert_alpha(),
            pygame.image.load(f"Base pack/Player/p{self.id}_walk/PNG/p{self.id}_walk09.png").convert_alpha(),
            pygame.image.load(f"Base pack/Player/p{self.id}_walk/PNG/p{self.id}_walk10.png").convert_alpha(),
            pygame.image.load(f"Base pack/Player/p{self.id}_walk/PNG/p{self.id}_walk11.png").convert_alpha(),
        ]
        self.right = [pygame.transform.scale(image, (28, 40)) for image in right]
        self.left = [pygame.transform.flip(image, True, False) for image in self.right]


    def render(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, keys, map):
        flag = 0
        if keys[pygame.K_a]:
            left_tile = get_tile_properties(map.map, self.rect.midleft[0] - 3, self.rect.bottomleft[1] - 5, 0)
            if left_tile['solid'] == 0:
                self.rect.x -= 3
                self.cur_frame = (self.cur_frame + 1) % len(self.left)
                self.image = self.left[self.cur_frame]
                flag = 1
            self.direction = "left"
        if keys[pygame.K_d]:
            right_tile = get_tile_properties(map.map, self.rect.midright[0] + 3, self.rect.bottomright[1] - 5, 0)
            if right_tile['solid'] == 0:
                self.rect.x += 3
                self.cur_frame = (self.cur_frame + 1) % len(self.right)
                self.image = self.right[self.cur_frame]
                flag = 1
            self.direction = "right"
        if self.direction == "right":
            standing_on = get_tile_properties(map.map, self.rect.bottomleft[0], self.rect.bottomleft[1], 0)
            standing_on2 = get_tile_properties(map.map, self.rect.bottomright[0], self.rect.bottomright[1], 0)
        else:
            standing_on = get_tile_properties(map.map, self.rect.bottomright[0], self.rect.bottomright[1], 0)
            standing_on2 = get_tile_properties(map.map, self.rect.bottomleft[0], self.rect.bottomleft[1], 0)
        ladder_check = get_tile_properties(map.map, self.rect.midbottom[0], self.rect.midbottom[1] - 3, 2)
        if keys[pygame.K_w]:
            if ladder_check["climb"] + ladder_check["climb"] >= 1:
                self.climb = True
            if standing_on['solid'] + standing_on2['solid'] >= 1:
                self.jump_frame = 20
                flag = 1
                if self.direction == "left":
                    self.image = self.jump_l
                else:
                    self.image = self.jump_r
        if not flag:
            if self.direction == "left":
                self.image = self.stand_l
            else:
                self.image = self.stand_r
        if self.climb:
            self.jump_frame = 0
            self.rect.y -= 6
            self.flag2 = 10
            self.climb = False
        else:
            if self.flag2:
                self.jump_frame = 0
                self.flag2 -= 1
            if self.jump_frame > 0:
                above_tile = get_tile_properties(map.map, self.rect.topleft[0], self.rect.topleft[1], 0)
                above_tile2 = get_tile_properties(map.map, self.rect.topright[0], self.rect.topright[1], 0)
                if above_tile['up_solid'] + above_tile2['up_solid'] == 0:
                    self.rect.y = self.rect.y - 6
                    self.jump_frame -= 1
                else:
                    self.jump_frame = 0
            else:
                if standing_on2['solid'] + standing_on['solid'] == 0:
                    self.rect.y = self.rect.y + 6


class Game:
    def __init__(self, map, hero1):
        self.map = map
        # self.screen = screen
        self.hero1 = hero1
        # self.hero2 = hero2

    def render(self, screen, args):
        self.map.render(screen, 1, 3)
        self.update_hero(args)
        self.hero1.render(screen)
        self.map.render(screen, 2)
        # self.hero2.render(screen)

    def update_hero(self, args):
        # all_sprites.draw(self.screen)
        self.hero1.update(args, self.map)
        # all_sprites.update(keys)

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
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.init()

    map = Map("map2.tmx", [])
    hero1 = Hero(1)
    game = Game(map, hero1)
    # hero2 = Hero("red")
    # game = Game(map, hero1, hero2)

    clock = pygame.time.Clock()

    running = True
    game_over = False
    fon = pygame.transform.scale(load_image(IMAGES_DIR + 'back1.jpeg'),
                                 (MAP_WIDTH, MAP_HEIGHT))
    pygame.mixer.init()
    pygame.mixer.music.load(random.choice([MUSIC_DIR + 'inazuma' + f'{i}.mp3' for i in range(1, 6)]))
    pygame.mixer.music.play(999)
    pygame.mixer.music.set_volume(0.5)
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(fon, (0, 0))
        game.render(screen, keys)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
