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
    except:
        properties = {"solid": 0, "climb": 0, "kill": 0, "fire": 0, "up_solid": 0, "hill": 0}
    if properties is None:
        properties = {"solid": 0, "climb": 0, "kill": 0, "fire": 0, "up_solid": 0, "hill": 0}
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
                    if el == 2:
                        screen.blit(image, (x * self.tile_size, y * self.tile_size + 16))
                    else:
                        screen.blit(image, (x * self.tile_size, y * self.tile_size))
                    Tile(x, y, self.tile_size, image)


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, tile_size, image):
        super().__init__(tiles_group, all_sprites)
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(tile_size * pos_x, tile_size * pos_y)


class Hero(pygame.sprite.Sprite):
    def __init__(self, player_id, x, y, joy, speed_coeff=1.0, health=250, gun_coeff=1.0, joystick=None):
        super().__init__(player_group, all_sprites)
        self.player_id = player_id
        self.joy = joy
        self.joystick = joystick

        self.gravity = 1
        self.speed_x = 3 * speed_coeff
        self.speed_y = 6 * speed_coeff
        self.fly = 0
        self.climb = False

        self.cur_frame = 0
        self.jump_frame = 0

        self.rect = pygame.Rect(x, y, 28, 40)

        self.climb_flag = 0
        self.health = health
        self.shoot_cooldown = 0
        self.fire_flag = 0
        self.fire = 20
        self.die_flag = 0
        self.gun_coeff = gun_coeff

        self.sheet()
        if self.player_id == 1:
            self.direction = "right"
            self.image = self.stand_r
            self.health_bar = HealthBar(0, 2, self.health, self.health)
            self.gun = Gun(self.rect.centerx, self.rect.centery, self.direction, self.rect.width, gun_coeff)
        else:
            self.direction = "left"
            self.image = self.stand_l
            self.health_bar = HealthBar(1450, 2, self.health, self.health)
            self.gun = Gun(self.rect.centerx, self.rect.centery, self.direction, self.rect.width,
                           gun_coeff)

        health_group.add(self.health_bar)
        gun_group.add(self.gun)

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

    def move(self, keys, game_map):
        flag = 0
        if self.button(keys, "left"):
            left_tile = get_tile_properties(game_map.map, self.rect.midleft[0] - self.speed_x,
                                            self.rect.bottomleft[1] - 5, 0)
            if left_tile['solid'] == 0:
                self.rect.x -= self.speed_x
                if self.direction == "right":
                    self.gun.update(-self.speed_x, 0, flag=1)
                else:
                    self.gun.update(-self.speed_x, 0)
                self.cur_frame = (self.cur_frame + 1) % len(self.left)
                self.image = self.left[self.cur_frame]
                flag = 1
            elif self.direction == "right":
                self.gun.update(0, 0, flag=1)
            self.direction = "left"
        if self.button(keys, "right"):
            right_tile = get_tile_properties(game_map.map, self.rect.midright[0] + self.speed_x,
                                             self.rect.bottomright[1] - 5, 0)
            if right_tile['solid'] == 0:
                self.rect.x += self.speed_x
                if self.direction == "left":
                    self.gun.update(self.speed_x, 0, flag=-1)
                else:
                    self.gun.update(self.speed_x, 0)
                self.cur_frame = (self.cur_frame + 1) % len(self.right)
                self.image = self.right[self.cur_frame]
                flag = 1
            elif self.direction == "left":
                self.gun.update(0, 0, flag=-1)
            self.direction = "right"
        if self.direction == "right":
            standing_on = get_tile_properties(game_map.map, self.rect.bottomleft[0], self.rect.bottomleft[1] + 3, 0)
            standing_on2 = get_tile_properties(game_map.map, self.rect.bottomright[0], self.rect.bottomright[1], 0)
        else:
            standing_on = get_tile_properties(game_map.map, self.rect.bottomright[0], self.rect.bottomright[1] + 3, 0)
            standing_on2 = get_tile_properties(game_map.map, self.rect.bottomleft[0], self.rect.bottomleft[1] + 3, 0)
        ladder_check = get_tile_properties(game_map.map, self.rect.midbottom[0], self.rect.midbottom[1] - 3, 2)
        if self.button(keys, "up"):
            if ladder_check["climb"] + ladder_check["climb"] >= 1:
                self.climb = True
            if standing_on['solid'] + standing_on2['solid'] >= 1:
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
                    self.rect.y -= self.speed_y
                    self.gun.update(0, -self.speed_y)
                    self.jump_frame -= 1
                else:
                    self.jump_frame = 0
            else:
                if standing_on2['solid'] + standing_on['solid'] == 0:
                    self.rect.y += self.speed_y
                    self.gun.update(0, self.speed_y)

    def update(self, keys, game_map):
        if self.health > 0:
            if self.shoot_cooldown > 0:
                self.shoot_cooldown -= 1
            if self.button(keys, "shoot"):
                self.shoot()
            self.move(keys, game_map)
            self.kill_and_damage(game_map)
            self.hill(game_map)
            if self.rect.right < 0:
                self.rect.x = 0
                self.die()
            elif self.rect.left > WINDOW_WIDTH:
                self.rect.x = WINDOW_WIDTH - self.rect.width
                self.die()
            elif self.rect.bottom > WINDOW_HEIGHT:
                self.die()
        else:
            self.die()

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 30
            if self.direction == "left":
                bullet = Bullet(self.rect.x - self.rect.width // 2, self.rect.y + self.rect.height // 2, self.direction,
                                self.gun_coeff)
            else:
                bullet = Bullet(self.rect.x + self.rect.width // 4, self.rect.y + self.rect.height // 2, self.direction,
                                self.gun_coeff)
            bullet_group.add(bullet)

    def die(self):
        self.gun.kill()
        self.health = 0
        self.image = self.dead_image
        self.rect.y -= self.speed_y // 2
        self.die_flag = 1

    def kill_and_damage(self, game_map):
        damage_check = get_tile_properties(game_map.map, self.rect.midbottom[0], self.rect.midbottom[1] - 16, 1)
        if damage_check["kill"] == 1:
            self.health = 0
            self.die()
            self.gun.kill()
        elif not self.fire_flag and damage_check["fire"] == 1:
            self.health -= self.fire
            self.fire_flag = 15
        elif self.fire_flag:
            self.fire_flag -= 1

    def hill(self, game_map):
        hill_check = get_tile_properties(game_map.map, self.rect.midbottom[0], self.rect.centery, 1)
        if hill_check["hill"] == 1 and self.health < self.health_bar.max_health:
            self.health += 0.3


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, gun_coeff):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 30
        self.image = pygame.transform.scale(load_image("images/bullet1.png"), (40, 10))
        self.rect = self.image.get_rect().move(x, y)
        self.direction = direction
        self.damage = 20 * gun_coeff

    def render(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, map):
        if self.direction == "left":
            left_tile = get_tile_properties(map.map, self.rect.midleft[0] - 3, self.rect.bottomleft[1], 0)
            if left_tile["solid"]:
                self.kill()
            self.rect.x -= self.speed
        else:
            right_tile = get_tile_properties(map.map, self.rect.midright[0] + 3, self.rect.bottomright[1], 0)
            if right_tile["solid"]:
                self.kill()
            self.rect.x += self.speed
        if self.rect.left < 0 or self.rect.right > WINDOW_WIDTH:
            self.kill()
        for player in player_group:
            if pygame.sprite.collide_mask(self, player):
                player.health -= self.damage
                self.kill()


class Gun(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, player_width, gun_coeff):
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        self.x = x
        self.image = self.sheet(gun_coeff)

        self.left_move = pygame.transform.flip(self.image, True, False)
        self.right_move = self.image
        if direction == "left":
            self.image = self.left_move
        self.rect = self.image.get_rect().move(self.x, y)
        self.player_width = player_width

    def sheet(self, gun_coeff):
        guns = {1: ["images/guns/gun1.png", (35, 20)], 1.25: ["images/guns/gun2.png", (35, 20)],
                1.5: ["images/guns/gun3.png", (40, 25)], 1.75: ["images/guns/gun4.png", (45, 20)],
                2.0: ["images/guns/gun5.png", (35, 25)], 2.5: ["images/guns/gun6.png", (35, 25)]}
        if self.direction == "left":
            self.x -= guns[gun_coeff][1][0]
        return pygame.transform.scale(load_image(guns[gun_coeff][0], -1), guns[gun_coeff][1])

    def render(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, x, y, flag=0):
        if flag < 0:
            self.image = self.right_move
            self.rect.x += self.rect.width
        elif flag > 0:
            self.image = self.left_move
            self.rect.x -= self.rect.width
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
    def __init__(self, map, hero1, hero2):
        self.map = map
        self.hero1 = hero1
        self.hero2 = hero2
        self.flag = 0
        self.winner = None
        self.loser = None

    def render(self, screen, args):
        if self.hero1.die_flag + self.hero2.die_flag == 1:
            self.flag += 1
            if not self.winner and not self.loser:
                self.winner = self.win()
                self.loser = self.lose()
        self.map.render(screen, 1, 3)
        self.update_screen(args)
        self.hero1.render(screen)
        self.hero2.render(screen)
        for gun in gun_group:
            gun.render(screen)
        self.map.render(screen, 2)
        for bullet in bullet_group:
            bullet.render(screen)
        self.hero1.health_bar.draw(self.hero1.health, screen)
        self.hero2.health_bar.draw(self.hero2.health, screen)

    def win(self):
        if self.hero1.die_flag == 1:
            return 2
        return 1

    def lose(self):
        return 3 - self.win()

    def update_screen(self, args):
        self.hero1.update(args, self.map)
        self.hero2.update(args, self.map)
        bullet_group.update(self.map)

    def game_over(self):
        return not self.flag == 60


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
    joy = True
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.init()
    if joy:
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for el in joysticks:
            el.init()
        print(joysticks)
        hero1 = Hero(1, 0, 20, joy, joystick=joysticks[0])
        hero2 = Hero(2, 1570, 20, joy, joystick=joysticks[1])
    else:
        hero1 = Hero(1, 0, 20, joy)
        hero2 = Hero(2, 1570, 20, joy)
    map = Map("map2.tmx", [])
    game = Game(map, hero1, hero2)

    clock = pygame.time.Clock()

    running = True
    fon = pygame.transform.scale(load_image(IMAGES_DIR + 'back1.jpeg'), (MAP_WIDTH, MAP_HEIGHT))
    pygame.mixer.init()
    pygame.mixer.music.load(random.choice([MUSIC_DIR + 'inazuma' + f'{i}.mp3' for i in range(1, 6)]))
    pygame.mixer.music.play(999)
    pygame.mixer.music.set_volume(0.5)
    while running:
        running = game.game_over()
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(fon, (0, 0))
        game.render(screen, keys)
        clock.tick(FPS)
        pygame.display.flip()

    """ФИНАЛЬНОЕ ОКНО"""
    pygame.quit()


if __name__ == '__main__':
    main()
