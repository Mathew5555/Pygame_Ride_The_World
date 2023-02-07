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
player_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
gun_group = pygame.sprite.Group()
health_group = pygame.sprite.Group()


def get_tile_properties(tmx_data, x, y, layer):
    tile_x = x // 32
    tile_y = y // 32
    try:
        properties = tmx_data.get_tile_properties(tile_x, tile_y, layer)
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
                    Tile(x, y, self.tile_size, image)


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, tile_size, image):
        super().__init__(tiles_group, all_sprites)
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(tile_size * pos_x, tile_size * pos_y)


class Hero(pygame.sprite.Sprite):
    def __init__(self, player_id):
        super().__init__(player_group, all_sprites)
        self.player_id = player_id

        self.speed_x = 3
        self.speed_y = 6
        self.direction = "right"
        self.fly = 0
        self.climb = False

        self.cur_frame = 0
        self.jump_frame = 0

        self.rect = pygame.Rect(0, 20, 28, 40)

        self.climb_flag = 0
        self.health = 100
        self.shoot_cooldown = 0

        self.sheet()
        self.image = self.stand_r

        self.gun = Gun(self.rect.centerx, self.rect.centery, self.direction, self.rect.width)
        gun_group.add(self.gun)

        health_bar = HealthBar(0, 2, self.health, self.health)
        health_group.add(health_bar)

    def sheet(self):
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
            load_image(f"man/p{self.player_id}_walk/PNG/p{self.player_id}_walk01.png"),
            load_image(f"man/p{self.player_id}_walk/PNG/p{self.player_id}_walk02.png"),
            load_image(f"man/p{self.player_id}_walk/PNG/p{self.player_id}_walk03.png"),
            load_image(f"man/p{self.player_id}_walk/PNG/p{self.player_id}_walk04.png"),
            load_image(f"man/p{self.player_id}_walk/PNG/p{self.player_id}_walk05.png"),
            load_image(f"man/p{self.player_id}_walk/PNG/p{self.player_id}_walk06.png"),
            load_image(f"man/p{self.player_id}_walk/PNG/p{self.player_id}_walk07.png"),
            load_image(f"man/p{self.player_id}_walk/PNG/p{self.player_id}_walk08.png"),
            load_image(f"man/p{self.player_id}_walk/PNG/p{self.player_id}_walk09.png"),
            load_image(f"man/p{self.player_id}_walk/PNG/p{self.player_id}_walk10.png"),
            load_image(f"man/p{self.player_id}_walk/PNG/p{self.player_id}_walk11.png")
        ]

        self.right = [pygame.transform.scale(image, (self.rect.width, self.rect.height)) for image in right]
        self.left = [pygame.transform.flip(image, True, False) for image in self.right]

    def render(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def move(self, keys, game_map):
        flag = 0
        if keys[pygame.K_a]:
            left_tile = get_tile_properties(game_map.map, self.rect.midleft[0] - 3, self.rect.bottomleft[1] - 5, 0)
            if left_tile['solid'] == 0:
                self.rect.x -= self.speed_x
                if self.direction == "right":
                    self.gun.update(-self.speed_x, 0, flag=1)
                else:
                    self.gun.update(-self.speed_x, 0)
                self.cur_frame = (self.cur_frame + 1) % len(self.left)
                self.image = self.left[self.cur_frame]
                flag = 1
            self.direction = "left"
        if keys[pygame.K_d]:
            right_tile = get_tile_properties(game_map.map, self.rect.midright[0] + 3, self.rect.bottomright[1] - 5, 0)
            if right_tile['solid'] == 0:
                self.rect.x += self.speed_x
                if self.direction == "left":
                    self.gun.update(self.speed_x, 0, flag=-1)
                else:
                    self.gun.update(self.speed_x, 0)
                self.cur_frame = (self.cur_frame + 1) % len(self.right)
                self.image = self.right[self.cur_frame]
                flag = 1
            self.direction = "right"
        if self.direction == "right":
            standing_on = get_tile_properties(game_map.map, self.rect.bottomleft[0], self.rect.bottomleft[1], 0)
            standing_on2 = get_tile_properties(game_map.map, self.rect.bottomright[0], self.rect.bottomright[1], 0)
        else:
            standing_on = get_tile_properties(game_map.map, self.rect.bottomright[0], self.rect.bottomright[1], 0)
            standing_on2 = get_tile_properties(game_map.map, self.rect.bottomleft[0], self.rect.bottomleft[1], 0)
        ladder_check = get_tile_properties(game_map.map, self.rect.midbottom[0], self.rect.midbottom[1] - 3, 2)
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
            self.rect.y -= self.speed_y
            self.gun.update(0, -self.speed_y)
            self.climb_flag = 10
            self.climb = False
        else:
            if self.climb_flag:
                self.jump_frame = 0
                self.climb_flag -= 1
            if self.jump_frame > 0:
                above_tile = get_tile_properties(game_map.map, self.rect.topleft[0], self.rect.topleft[1], 0)
                above_tile2 = get_tile_properties(game_map.map, self.rect.topright[0], self.rect.topright[1], 0)
                if above_tile['up_solid'] + above_tile2['up_solid'] == 0:
                    self.rect.y = self.rect.y - self.speed_y
                    self.gun.update(0, -self.speed_y)
                    self.jump_frame -= 1
                else:
                    self.jump_frame = 0
            else:
                if standing_on2['solid'] + standing_on['solid'] == 0:
                    self.rect.y = self.rect.y + self.speed_y
                    self.gun.update(0, self.speed_y)

    def update(self, keys, game_map):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if keys[pygame.K_e]:
            self.shoot()
        self.move(keys, game_map)
        damage_check = get_tile_properties(game_map.map, self.rect.midbottom[0], self.rect.midbottom[1] - 3, 1)
        if damage_check["kill"] == 1:
            print("die")

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 30
            if self.direction == "left":
                bullet = Bullet(self.rect.x - self.rect.width // 2, self.rect.y + self.rect.height // 2, self.direction)
            else:
                bullet = Bullet(self.rect.x + self.rect.width // 4, self.rect.y + self.rect.height // 2, self.direction)
            bullet_group.add(bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 30
        self.image = pygame.transform.scale(load_image("images/bullet1.png"), (40, 10))
        self.rect = self.image.get_rect().move(x, y)
        self.direction = direction

    def render(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, map):
        if self.direction == "left":
            left_tile = get_tile_properties(map.map, self.rect.midleft[0] - 3, self.rect.bottomleft[1] - 5, 0)
            if left_tile["solid"]:
                self.kill()
            self.rect.x -= self.speed
        else:
            right_tile = get_tile_properties(map.map, self.rect.midright[0] + 3, self.rect.bottomright[1] - 5, 0)
            if right_tile["solid"]:
                self.kill()
            self.rect.x += self.speed
        if self.rect.left < 0 or self.rect.right > WINDOW_WIDTH:
            self.kill()
        for player in player_group:
            if pygame.sprite.collide_mask(self, player):
                self.kill()


class Gun(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, player_width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(load_image("images/gun.png", -1), (30, 20))
        self.left_move = pygame.transform.flip(self.image, True, False)
        self.right_move = self.image
        self.rect = self.image.get_rect().move(x, y)
        self.direction = direction
        self.player_width = player_width

    def render(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, x, y, flag=0):
        if flag < 0:
            self.image = self.right_move
            self.rect.x += self.player_width
        elif flag > 0:
            self.image = self.left_move
            self.rect.x -= self.player_width
        self.rect.x += x
        self.rect.y += y


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, x, y, health, max_health):
        super().__init__()
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health, screen):
        self.health = health
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, pygame.Color("black"), (self.x - 2, self.y - 2, 150, 20))
        pygame.draw.rect(screen, pygame.Color("red"), (self.x, self.y, 146, 16))
        pygame.draw.rect(screen, pygame.Color("green"), (self.x, self.y, 146 * ratio, 16))


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
        for gun in gun_group:
            gun.render(screen)
        self.map.render(screen, 2)
        for bullet in bullet_group:
            bullet.render(screen)
        for health in health_group:
            health.draw(10, screen)
        # self.hero2.render(screen)

    def update_hero(self, args):
        # all_sprites.draw(self.screen)
        self.hero1.update(args, self.map)
        bullet_group.update(self.map)
        # all_sprites.update(keys)

    def check_win(self):
        pass

    def check_lose(self):
        pass


def load_image(name, colorkey=None):
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

    clock = pygame.time.Clock()

    running = True
    game_over = False
    fon = pygame.transform.scale(load_image(IMAGES_DIR + 'back1.jpeg'), (MAP_WIDTH, MAP_HEIGHT))
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
