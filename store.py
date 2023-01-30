import pygame
import pytmx
import os
import sys

def new(spisok):
    item1 = pygame.sprite.Sprite()
    item1.image = load_image(spisok[0])
    item1.image = pygame.transform.scale(item1.image, (250, 250))
    item1.rect = item1.image.get_rect()
    itemsgrp.add(item1)
    item1.rect.x = 180
    item1.rect.y = 270

    item2 = pygame.sprite.Sprite()
    item2.image = load_image(spisok[1])
    item2.image = pygame.transform.scale(item2.image, (250, 250))
    item2.rect = item2.image.get_rect()
    itemsgrp.add(item2)
    item2.rect.x = 480
    item2.rect.y = 270

    item3 = pygame.sprite.Sprite()
    item3.image = load_image(spisok[2])
    item3.image = pygame.transform.scale(item3.image, (250, 250))
    item3.rect = item3.image.get_rect()
    itemsgrp.add(item3)
    item3.rect.x = 780
    item3.rect.y = 270

    item4 = pygame.sprite.Sprite()
    item4.image = load_image(spisok[3])
    item4.image = pygame.transform.scale(item4.image, (250, 250))
    item4.rect = item4.image.get_rect()
    itemsgrp.add(item4)
    item4.rect.x = 1080
    item4.rect.y = 270


def clear():
    for el in itemsgrp:
        el.kill()
    itemsgrp.clear(screen, bg)


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image



FPS = 60
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1500, 1000
bg = pygame.image.load("images\store2.png")
pygame.init()
#pygame.mixer.music.load("music\paradise.mp3")
#pygame.mixer.music.play()
screen = pygame.display.set_mode(WINDOW_SIZE)
screen.blit(bg, (0, 0))
pygame.display.set_caption('Game_store')
btns = pygame.sprite.Group()

boosts = pygame.sprite.Sprite()
boosts.image = load_image("boosts.png")
boosts.image = pygame.transform.scale(boosts.image, (250, 125))
boosts.rect = boosts.image.get_rect()
btns.add(boosts)
boosts.rect.x = 10
boosts.rect.y = 10

skins = pygame.sprite.Sprite()
skins.image = load_image("skins.png")
skins.image = pygame.transform.scale(skins.image, (250, 125))
skins.rect = skins.image.get_rect()
btns.add(skins)
skins.rect.x = 240
skins.rect.y = 10

left = pygame.sprite.Sprite()
left.image = load_image("left.png")
left.image = pygame.transform.scale(left.image, (150, 150))
left.rect = left.image.get_rect()
btns.add(left)
left.rect.x = 10
left.rect.y = 470

right = pygame.sprite.Sprite()
right.image = load_image("right.png")
right.image = pygame.transform.scale(right.image, (150, 150))
right.rect = right.image.get_rect()
btns.add(right)
right.rect.x = 1370
right.rect.y = 470

back = pygame.sprite.Sprite()
back.image = load_image("back.png")
back.image = pygame.transform.scale(back.image, (200, 100))
back.rect = back.image.get_rect()
btns.add(back)
back.rect.x = 1200
back.rect.y = 25

skins_photo = ['pig.png', 'sheep.png', 'rainbowsheep.png', 'russiasheep.png']
boosts_photo = ['fight.png', 'speed.png', 'hp.png', '2x.png', '3x.png', '4x.png']
skins_items = ['pig', 'sheep', 'rainbowsheep', 'russiasheep']
boosts_items = ['fight', 'speed', 'hp', '2x', '3x', '4x']
itemsgrp = pygame.sprite.Group()

pygame.display.flip()
running = True
mainlist = []
mainlist1 = []
new(skins_photo)
mainlist = skins_photo
while running:
    btns.draw(screen)
    itemsgrp.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if right.rect.collidepoint(x, y):
                clear()
                mainlist = mainlist[-1:] + mainlist[:-1]
                mainlist1 = mainlist1[-1:] + mainlist1[:-1]
                new(mainlist)
            if left.rect.collidepoint(x, y):
                clear()
                mainlist = mainlist[1:] + mainlist[:1]
                mainlist1 = mainlist1[1:] + mainlist1[:1]
                new(mainlist)
            if boosts.rect.collidepoint(x, y):
                clear()
                new(boosts_photo)
                mainlist = boosts_photo
                mainlist1 = boosts_items
            if skins.rect.collidepoint(x, y):
                clear()
                new(skins_photo)
                mainlist = skins_photo
                mainlist1 = skins_items

    pygame.display.flip()
pygame.quit()
