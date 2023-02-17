import pygame
import pytmx
import random
import sqlite3
from funcs_backend import pic, load_image
from consts import *

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
gun_group = pygame.sprite.Group()
health_group = pygame.sprite.Group()
UPDATED = False
MAP_NAME = ""


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
                    if MAP_NAME == "map2.tmx" and el == 2:
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
    def __init__(self, player_id, x, y, joy, color, speed_coeff=1.0, health=250, gun_coeff=1.0, joystick=None):
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

        self.color = color
        self.sheet()
        if self.player_id == 1:
            self.direction = "right"
            self.image = self.images_dict["stand_r"]
            self.health_bar = HealthBar(2, 2, self.health, self.health, color)
            self.gun = Gun(self.rect.centerx, self.rect.centery, self.direction, self.rect.width, gun_coeff)
        else:
            self.direction = "left"
            self.image = self.images_dict["stand_l"]
            self.health_bar = HealthBar(1420, 2, self.health, self.health, color)
            self.gun = Gun(self.rect.centerx, self.rect.centery, self.direction, self.rect.width, gun_coeff)

        health_group.add(self.health_bar)
        gun_group.add(self.gun)

    def sheet(self):
        images_path = {"dead_image": "ghost.png", "stand_r": f"{self.color}/stand.png",
                       "jump_r": f"{self.color}/jump.png", "land_r": f"{self.color}/hit.png"}
        self.images_dict = dict()
        for key, val in images_path.items():
            self.images_dict[key] = pygame.transform.scale(load_image(f"{IMAGES_DIR}" + val),
                                                           (self.rect.width, self.rect.height))
            if key != "dead_image":
                self.images_dict[key[:-1] + "l"] = pygame.transform.flip(self.images_dict[key], True, False)
        self.images_dict["right"] = [pygame.transform.scale(load_image(f"{IMAGES_DIR}{self.color}/walk{i + 1}.png"),
                                                            (self.rect.width, self.rect.height)) for i in range(2)]
        self.images_dict["left"] = [pygame.transform.flip(image, True, False) for image in self.images_dict["right"]]

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
                    return self.joystick.get_button(0)
                elif direction == "down":
                    return self.joystick.get_button(12)
                elif direction == "shoot":
                    return self.joystick.get_button(1)
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
                return self.joystick.get_button(0)
            elif direction == "down":
                return self.joystick.get_button(12)
            elif direction == "shoot":
                return self.joystick.get_button(1)

    def move(self, keys, game_map):
        flag = 0
        if self.button(keys, "left"):
            left_tile = get_tile_properties(game_map.map, self.rect.midleft[0] - self.speed_x,
                                            self.rect.bottomleft[1] - self.speed_y + 1, MAPS_FLAGS[MAP_NAME][2])
            if left_tile['solid'] == 0 and not self.rect.left < 0:
                self.rect.x -= self.speed_x
                if self.direction == "right":
                    self.gun.update(-self.speed_x, 0, flag=1)
                else:
                    self.gun.update(-self.speed_x, 0)
                self.cur_frame = (self.cur_frame + 1) % len(self.images_dict["left"])
                self.image = self.images_dict["left"][self.cur_frame]
                flag = 1
            elif self.direction == "right":
                self.gun.update(0, 0, flag=1)
            self.direction = "left"
        if self.button(keys, "right"):
            right_tile = get_tile_properties(game_map.map, self.rect.midright[0] + self.speed_x,
                                             self.rect.bottomright[1] - self.speed_y + 1, MAPS_FLAGS[MAP_NAME][2])
            if right_tile['solid'] == 0 and not self.rect.right > WINDOW_WIDTH2:
                self.rect.x += self.speed_x
                if self.direction == "left":
                    self.gun.update(self.speed_x, 0, flag=-1)
                else:
                    self.gun.update(self.speed_x, 0)
                self.cur_frame = (self.cur_frame + 1) % len(self.images_dict["right"])
                self.image = self.images_dict["right"][self.cur_frame]
                flag = 1
            elif self.direction == "left":
                self.gun.update(0, 0, flag=-1)
            self.direction = "right"
        if self.direction == "right":
            standing_on = get_tile_properties(game_map.map, self.rect.bottomleft[0], self.rect.bottomleft[1] + 3,
                                              MAPS_FLAGS[MAP_NAME][2])
            standing_on2 = get_tile_properties(game_map.map, self.rect.bottomright[0], self.rect.bottomright[1],
                                               MAPS_FLAGS[MAP_NAME][2])
        else:
            standing_on = get_tile_properties(game_map.map, self.rect.bottomright[0],
                                              self.rect.bottomright[1] + self.speed_y / 2, MAPS_FLAGS[MAP_NAME][2])
            standing_on2 = get_tile_properties(game_map.map, self.rect.bottomleft[0],
                                               self.rect.bottomleft[1] + self.speed_y / 2, MAPS_FLAGS[MAP_NAME][2])
        ladder_check = get_tile_properties(game_map.map, self.rect.midbottom[0],
                                           self.rect.midbottom[1] - self.speed_y / 2, MAPS_FLAGS[MAP_NAME][2] + 2)
        if self.button(keys, "up"):
            if ladder_check["climb"] + ladder_check["climb"] >= 1:
                self.climb = True
            if standing_on['solid'] + standing_on2['solid'] >= 1:
                self.jump_frame = 20
                flag = 1
                if self.direction == "left":
                    self.image = self.images_dict["jump_l"]
                else:
                    self.image = self.images_dict["jump_r"]
        if self.button(keys, "down"):
            self.jump_frame = 0
        if not flag and not self.jump_frame:
            if self.direction == "left":
                self.image = self.images_dict["stand_l"]
            else:
                self.image = self.images_dict["stand_r"]
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
                above_tile = get_tile_properties(game_map.map, self.rect.topleft[0], self.rect.topleft[1],
                                                 MAPS_FLAGS[MAP_NAME][2])
                above_tile2 = get_tile_properties(game_map.map, self.rect.topright[0], self.rect.topright[1],
                                                  MAPS_FLAGS[MAP_NAME][2])
                if above_tile['up_solid'] + above_tile2['up_solid'] == 0:
                    self.rect.y -= self.speed_y
                    self.gun.update(0, -self.speed_y)
                    self.jump_frame -= 1
                else:
                    self.jump_frame = 0
            else:
                if standing_on2['solid'] + standing_on['solid'] == 0:
                    self.rect.y += self.speed_y
                    if self.direction == "left":
                        self.image = self.images_dict["land_l"]
                    else:
                        self.image = self.images_dict["land_r"]
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
            if self.rect.bottom > WINDOW_HEIGHT2:
                self.die()
        else:
            self.die()

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 30
            if self.direction == "left":
                bullet = Bullet(self.rect.left - 10, self.rect.y + self.rect.height // 2, self.direction,
                                self.gun_coeff, self.speed_x)
            else:
                bullet = Bullet(self.rect.right + 10, self.rect.y + self.rect.height // 2, self.direction,
                                self.gun_coeff, self.speed_x)
            bullet_group.add(bullet)

    def die(self):
        self.gun.kill()
        self.health = 0
        self.image = self.images_dict["dead_image"]
        self.rect.y -= self.speed_y // 2
        self.die_flag = 1

    def kill_and_damage(self, game_map):
        if MAP_NAME == "map2.tmx":
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
        if not MAP_NAME == "map_2.tmx":
            hill_check = get_tile_properties(game_map.map, self.rect.midbottom[0],
                                             self.rect.centery, MAPS_FLAGS[MAP_NAME][1] - 1)
            if hill_check["hill"] == 1 and self.health < self.health_bar.max_health:
                self.health += 0.3


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, gun_coeff, speed_player):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 45 * (speed_player / 3)
        self.image = pygame.transform.scale(load_image(f"{IMAGES_DIR}bullet.png"), (40, 10))
        self.rect = self.image.get_rect().move(x, y)
        self.direction = direction
        self.damage = 20 * gun_coeff

    def render(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, map):
        if self.direction == "left":
            left_tile = get_tile_properties(map.map, self.rect.left - 3, self.rect.bottomleft[1],
                                            MAPS_FLAGS[MAP_NAME][2])
            if left_tile["solid"]:
                self.kill()
            self.rect.x -= self.speed
        else:
            right_tile = get_tile_properties(map.map, self.rect.right + 3, self.rect.bottomright[1],
                                             MAPS_FLAGS[MAP_NAME][2])
            if right_tile["solid"]:
                self.kill()
            self.rect.x += self.speed
        if self.rect.left < 0 or self.rect.right > WINDOW_WIDTH2:
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
        guns = {1: [f"{IMAGES_DIR}guns/gun1.png", (35, 20)], 1.25: [f"{IMAGES_DIR}guns/gun2.png", (35, 20)],
                1.5: [f"{IMAGES_DIR}guns/gun3.png", (40, 25)], 1.75: [f"{IMAGES_DIR}guns/gun4.png", (45, 20)],
                2.0: [f"{IMAGES_DIR}guns/gun5.png", (35, 25)], 2.5: [f"{IMAGES_DIR}guns/gun6.png", (35, 25)]}
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
    def __init__(self, x, y, health, max_health, color):
        super().__init__()
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
        self.color = color
        self.image = pygame.transform.scale(load_image(f"{IMAGES_DIR}skins/{color}.png"), (50, 50))

    def draw(self, health, screen):
        self.health = health
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, pygame.Color("black"), (self.x - 2, self.y - 2, 180, 30))
        pygame.draw.rect(screen, pygame.Color("red"), (self.x, self.y, 176, 26))
        pygame.draw.rect(screen, pygame.Color("green"), (self.x, self.y, 176 * ratio, 26))

        font = pygame.font.Font(FONT, 28)
        text = font.render(str(round(self.health)), True, (255, 255, 255))
        if self.x == 2:
            text_x = 200
            image_x = 250
        else:
            text_x = 1350
            image_x = 1280
        if self.health == 0:
            self.image = pygame.transform.scale(load_image(f"{IMAGES_DIR}skins/{self.color}_kill.png"), (50, 50))
        text_y = 0
        screen.blit(text, (text_x, text_y))
        screen.blit(self.image, (image_x, text_y))


class Game:
    def __init__(self, map, hero1, hero2, back_btn='back.png'):
        self.map = map
        self.hero1 = hero1
        self.hero2 = hero2
        self.flag = 0
        self.winner = None
        self.loser = None
        self.back_btn = pic(back_btn, (725, 600))

    def render(self, screen, args, game_over=False):
        if self.hero1.die_flag + self.hero2.die_flag == 1:
            self.flag += 1
            self.hero1.gun.kill()
            self.hero2.gun.kill()
            if not self.winner and not self.loser:
                self.winner = self.win()
                self.loser = self.lose()
        self.map.render(screen, *MAPS_FLAGS[MAP_NAME][0])
        if not game_over:
            self.update_screen(args)
        self.hero1.render(screen)
        self.hero2.render(screen)
        for gun in gun_group:
            gun.render(screen)
        if MAPS_FLAGS[MAP_NAME][1] != -1:
            self.map.render(screen, MAPS_FLAGS[MAP_NAME][1])
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

    def render_end_screen(self, screen, winner_id):
        global UPDATED
        bottom = pygame.Surface((1200, 700))
        bottom.set_alpha(100)
        bottom.fill((0, 0, 0))
        screen.blit(bottom, (200, 150))

        title = 'Бой завершен!'
        winner = f'Победитель: Игрок {winner_id}'
        prize = (30, 10)
        loser_id = 2 if winner_id == 1 else 1
        text = (f'Получено монет у игрока {winner_id}: {prize[0]}', f'Получено монет у игрока {loser_id}: '
                                                                    f'{prize[1]}')

        if not UPDATED:
            con = sqlite3.connect('data/account_info.db')
            cur = con.cursor()
            curr_blncs = cur.execute("""SELECT coins FROM info""").fetchall()
            # winner updating
            cur.execute("""UPDATE info SET coins = ? WHERE id = ?""",
                        (prize[0] + curr_blncs[0][0], winner_id,))
            cur.execute("""UPDATE info SET coins = ? WHERE id = ?""",
                        (prize[1] + curr_blncs[1][0], loser_id,))
            con.commit()
            con.close()
            UPDATED = True

        font_title_main = pygame.font.Font(FONT, 80)
        font_title = pygame.font.Font(FONT, 60)
        font_text = pygame.font.Font(FONT, 40)
        line = font_title_main.render(title, True, (255, 100, 100))
        screen.blit(line, (480, 240))
        line = font_title.render(winner, True, (255, 200, 200))
        screen.blit(line, (480, 360))
        line2 = font_text.render(text[0], True, (255, 255, 255))
        screen.blit(line2, (480, 420))
        line2 = font_text.render(text[1], True, (255, 255, 255))
        screen.blit(line2, (480, 460))
        screen.blit(*self.back_btn)

    def game_over(self):
        return not self.flag == 60


def game(clr1, clr2):
    global MAP_NAME
    MAP_NAME = random.choice(["map_tartaglia.tmx", "map_2.tmx", "map2.tmx", "map3.tmx"])
    joy = False
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE2)
    pygame.display.set_caption('Ride The World - BETA 1.0')
    pygame.display.flip()
    if joy:
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for el in joysticks:
            el.init()
        hero1 = Hero(1, 0, 20, joy, clr1, joystick=joysticks[0])
        hero2 = Hero(2, 1570, 20, joy, clr2, joystick=joysticks[1])
    else:
        hero1 = Hero(1, 0, 20, joy, clr1, speed_coeff=1.5)
        hero2 = Hero(2, 1550, 20, joy, clr2)
    map = Map(MAP_NAME, [])
    game = Game(map, hero1, hero2)

    clock = pygame.time.Clock()

    running = True
    fon = pygame.transform.scale(load_image(IMAGES_DIR + 'back.jpg'), (WINDOW_WIDTH2, WINDOW_HEIGHT2))
    pygame.mixer.init()
    pygame.mixer.music.load(random.choice([MUSIC_DIR + 'mond' + f'{i}.mp3' for i in range(1, 3)]))
    pygame.mixer.music.play(999)
    sound_level = float(
        open('data/sound.txt', mode='r', encoding='utf-8').readlines()[0].strip('\n'))
    pygame.mixer.music.set_volume(sound_level)
    flag_closed = False
    while running:
        screen.fill((0, 0, 0))
        running = game.game_over()
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag_closed = True
                running = False
                break
        if hero1.die_flag and hero2.die_flag:
            running = False
        screen.blit(fon, (0, 0))
        game.render(screen, keys)
        clock.tick(FPS)
        pygame.display.flip()

    go_back = False
    pygame.mixer.music.load(MUSIC_DIR + 'victory.mp3')
    pygame.mixer.music.play()
    while not go_back and not running and not flag_closed:
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                go_back = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.back_btn[1].collidepoint(*mouse):
                    go_back = True
        screen.blit(fon, (0, 0))
        game.render(screen, {}, game_over=True)
        game.render_end_screen(screen, game.win())
        clock.tick(FPS2)
        pygame.display.flip()
    pygame.mixer.music.stop()


if __name__ == '__main__':
    game('blue', 'yellow')
