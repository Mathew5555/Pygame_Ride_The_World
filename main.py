import pygame

size = width, height = 1500, 1000
FPS = 60


class Hero(pygame.sprite.Sprite):
    def __init__(self, id):
        super().__init__(all_sprites)
        self.id = id
        self.direction = "right"
        self.cur_frame = 0
        self.sheet()
        self.image = self.stand_r
        self.rect = pygame.Rect(0, 0, 50, 70)

    def sheet(self):
        self.stand_r = pygame.transform.scale(
            pygame.image.load(f"Base pack/Player/p{self.id}_stand.png").convert_alpha(), (50, 70))
        self.stand_l = pygame.transform.flip(self.stand_r, True, False)
        self.jump_r = pygame.transform.scale(pygame.image.load(f"Base pack/Player/p{self.id}_jump.png").convert_alpha(),
                                             (50, 70))
        self.jump_l = pygame.transform.flip(self.jump_r, True, False)
        self.land_r = pygame.transform.scale(pygame.image.load(f"Base pack/Player/p{self.id}_hurt.png").convert_alpha(),
                                             (50, 70))
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
        self.right = [pygame.transform.scale(image, (50, 70)) for image in right]
        self.left = [pygame.transform.flip(image, True, False) for image in self.right]

    # def update_check(self):
    #     if self.rect.topleft[0] < 0:
    #         self.rect.x = 0
    #     if self.rect.bottomright[0] > width:
    #         self.rect.x = width - self.rect.w - 1
    #     if self.rect.topleft[1] < 0:
    #         self.rect.y = 0
    #     if self.rect.bottomright[1] > height:
    #         self.rect.y = height - self.rect.h - 1

    def update(self, keys):
        flag = 0
        if keys[pygame.K_a]:
            self.direction = "left"
            self.rect.x -= 5
            self.cur_frame = (self.cur_frame + 1) % len(self.left)
            self.image = self.left[self.cur_frame]
            flag = 1
        if keys[pygame.K_d]:
            self.direction = "right"
            self.rect.x += 5
            self.cur_frame = (self.cur_frame + 1) % len(self.right)
            self.image = self.right[self.cur_frame]
            flag = 1
        if keys[pygame.K_w]:
            self.rect.y -= 5
            flag = 1
            if self.direction == "left":
                self.image = self.jump_l
            else:
                self.image = self.jump_r
        if keys[pygame.K_s]:
            self.rect.y += 5
            flag = 1
            if self.direction == "left":
                self.image = self.land_l
            else:
                self.image = self.land_r
        if not flag:
            if self.direction == "left":
                self.image = self.stand_l
            else:
                self.image = self.stand_r


# class Map:
#     def __init__(self, filename, free_tiles):
#         self.map = pytmx.load_pygame(f"{MAPS_DIR}{filename}")
#         self.height = self.map.height
#         self.width = self.map.width
#         self.tile_size = self.map.tilewidth
#         self.free_tiles = free_tiles
#
#     def render(self, screen):
#         for y in range(self.height):
#             for x in range(self.width):
#                 image = self.map.get_tile_image(x, y, 0)
#                 if image is None:
#                     continue
#
#                 screen.blit(image, (x * self.tile_size - (MAP_WIDTH - WINDOW_WIDTH * 1.5) // 2,
#                                     y * self.tile_size - (MAP_HEIGHT - WINDOW_HEIGHT * 1.5) // 2))
#
#     def get_tile_id(self, position):
#         return self.map.tiledgidmap[self.map.get_tile_gid(*position, 0)]
#
#     def is_free(self, position):
#         return self.get_tile_id(position) in self.free_tiles

class Game:
    def __init__(self, hero1):
        # self.map = map
        self.hero1 = hero1
        # self.hero2 = hero2

    def render(self, screen):
        # self.map.render(screen)
        self.hero1.render(screen)
        # self.hero2.render(screen)

    def update_hero(self, args):
        all_sprites.draw(screen)
        self.hero1.update(args)
        # all_sprites.update(keys)

    def check_win(self):
        pass

    def check_lose(self):
        pass


# class Platform(pygame.sprite.Sprite):
#     def __init__(self, pos):
#         super().__init__(all_sprites)
#         self.add(platforms)
#         self.image = pygame.Surface((50, 10))
#         self.rect = pygame.Rect(0, 0, 50, 10)
#         self.rect.topleft = pos
#         pygame.draw.rect(self.image, pygame.Color("grey"), (0, 0, 50, 10), 0)


screen = pygame.display.set_mode(size)
pygame.display.set_caption("Game")

clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player1_sprite = pygame.sprite.Sprite()
# platforms = pygame.sprite.Group()

hero1 = Hero(1)
game = Game(hero1)
running = True
while running:
    screen.fill((0, 0, 0))
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    game.update_hero(keys)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
