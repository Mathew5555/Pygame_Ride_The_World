import pygame
import pytmx
import os
import sys
import sqlite3
import sys
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.QtWidgets import *


id = 1 #сюда передается айди игрока

FONT = 'data/font.ttf'

def back_door():
    global running
    running = False

def renew_db(players_money, tovar, flag, id):
    global cur, con
    con = sqlite3.connect('account_info.db')
    cur = con.cursor()
    if flag:
        bought_s1 = cur.execute(
            f'''SELECT skins FROM info where id = "{id}"''').fetchall()
        str1 = ''
        for el in bought_s1:
            l = el
        for el in l:
            str1 = str1 + el
        str1 = str1 + f'images/{tovar};'
        cur.execute(f"""UPDATE info
            SET skins = '{str1}'
            WHERE id = '{id}'""")
    else:
        bought_s1 = cur.execute(
            f'''SELECT boosts FROM info where id = "{id}"''').fetchall()
        str1 = ''
        for el in bought_s1:
            print(el)
            l = el
        for el in l:
            print(el)
            str1 = str1 + el
        str1 = str1 + f'images/{tovar};'
        cur.execute(f"""UPDATE info
                    SET boosts = '{str1}'
                    WHERE id = '{id}'""")
    cur.execute(f"""UPDATE info
    SET coins = '{str(players_money)}'
    WHERE id = '{id}'""")
    con.commit()

def id_new(id):
    global cost_boosts, cost_skins, sold_skins, sold_boosts, players_money
    # подключение бд
    con = sqlite3.connect('account_info.db')
    cur = con.cursor()

    # цена товаров
    cost_b = cur.execute(
        '''SELECT cost FROM boosts''').fetchall()
    cost_s = cur.execute(
        '''SELECT cost FROM skins''').fetchall()
    cost_boosts = []
    cost_skins = []
    players_money = ''
    for el in cost_b:
        if el[0]:
            cost_boosts.append(el[0])
    for el in cost_s:
        if el[0]:
            cost_skins.append(el[0])

    # купленные скины
    bought_s = cur.execute(
        f'''SELECT skins FROM info where id = "{id}"''').fetchall()
    bought_skins = ''
    for el in bought_s:
        bought_skins = el[0]
    bought_skin = str(bought_skins)[:-1].replace('(', '').replace(')', '').split(';')
    for i in range(len(bought_skin)):
        bought_skin[i] = bought_skin[i].split('/')[-1]

    sold_skins = [0, 0, 0, 0]
    for i in range(len(skins_photo)):
        if skins_photo[i] in bought_skin:
            sold_skins[i] = 1
    sold_boosts = [0, 0, 0, 0, 0, 0]

    # деньги игрока
    players_m = cur.execute(
        f'''SELECT coins FROM info where id = "{id}"''').fetchall()
    for el in players_m:
        if int(el[0]) >= 0:
            players_money = int(el[0])
    print(players_money)


def new(spisok, text_spisok, cost, bought):
    global buy1, buy2, buy3, buy4, screen, bg, players_money
    v = f"money {str(players_money)}"
    text_pm = font.render(v, True, (255, 255, 255))
    screen.blit(text_pm, (970, 60))
    item1 = pygame.sprite.Sprite()
    item1.image = load_image(spisok[0])
    text1 = font.render(text_spisok[0], True, (255, 255, 255))
    item1.image = pygame.transform.scale(item1.image, (250, 250))
    item1.rect = item1.image.get_rect()
    itemsgrp.add(item1)
    item1.rect.x = 180
    item1.rect.y = 270
    if not bought[0]:
        buy1 = pygame.sprite.Sprite()
        buy1.image = load_image("buy.png")
        buy1.image = pygame.transform.scale(buy1.image, (200, 200))
        buy1.rect = buy1.image.get_rect()
        btns.add(buy1)
        buy1.rect.x = 200
        buy1.rect.y = 550
    else:
        buy1 = 0
        sold1 = pygame.sprite.Sprite()
        sold1.image = load_image("sold.png")
        sold1.image = pygame.transform.scale(sold1.image, (200, 200))
        sold1.rect = sold1.image.get_rect()
        btns.add(sold1)
        sold1.rect.x = 200
        sold1.rect.y = 550


    c = str(cost[0])
    text_cost1 = font.render(c, True, (255, 255, 255))
    screen.blit(text_cost1, (345, 215))

    item2 = pygame.sprite.Sprite()
    item2.image = load_image(spisok[1])
    text2 = font.render(text_spisok[1], True, (255, 255, 255))
    item2.image = pygame.transform.scale(item2.image, (250, 250))
    item2.rect = item2.image.get_rect()
    itemsgrp.add(item2)
    item2.rect.x = 480
    item2.rect.y = 270

    if not bought[1]:
        buy2 = pygame.sprite.Sprite()
        buy2.image = load_image("buy.png")
        buy2.image = pygame.transform.scale(buy2.image, (200, 200))
        buy2.rect = buy2.image.get_rect()
        btns.add(buy2)
        buy2.rect.x = 500
        buy2.rect.y = 550
    else:
        buy2 = 0
        sold2 = pygame.sprite.Sprite()
        sold2.image = load_image("sold.png")
        sold2.image = pygame.transform.scale(sold2.image, (200, 200))
        sold2.rect = sold2.image.get_rect()
        btns.add(sold2)
        sold2.rect.x = 500
        sold2.rect.y = 550

    c = str(cost[1])
    text_cost2 = font.render(c, True, (255, 255, 255))
    screen.blit(text_cost2, (645, 215))

    item3 = pygame.sprite.Sprite()
    item3.image = load_image(spisok[2])
    text3 = font.render(text_spisok[2], True, (255, 255, 255))
    item3.image = pygame.transform.scale(item3.image, (250, 250))
    item3.rect = item3.image.get_rect()
    itemsgrp.add(item3)
    item3.rect.x = 780
    item3.rect.y = 270

    if not bought[2]:
        buy3 = pygame.sprite.Sprite()
        buy3.image = load_image("buy.png")
        buy3.image = pygame.transform.scale(buy3.image, (200, 200))
        buy3.rect = buy3.image.get_rect()
        btns.add(buy3)
        buy3.rect.x = 800
        buy3.rect.y = 550
    else:
        buy3 = 0
        sold3 = pygame.sprite.Sprite()
        sold3.image = load_image("sold.png")
        sold3.image = pygame.transform.scale(sold3.image, (200, 200))
        sold3.rect = sold3.image.get_rect()
        btns.add(sold3)
        sold3.rect.x = 800
        sold3.rect.y = 550

    c = str(cost[2])
    text_cost3 = font.render(c, True, (255, 255, 255))
    screen.blit(text_cost3, (945, 215))

    item4 = pygame.sprite.Sprite()
    item4.image = load_image(spisok[3])
    text4 = font.render(text_spisok[3], True, (255, 255, 255))
    item4.image = pygame.transform.scale(item4.image, (250, 250))
    item4.rect = item4.image.get_rect()
    itemsgrp.add(item4)
    item4.rect.x = 1080
    item4.rect.y = 270

    if not bought[3]:
        buy4 = pygame.sprite.Sprite()
        buy4.image = load_image("buy.png")
        buy4.image = pygame.transform.scale(buy4.image, (200, 200))
        buy4.rect = buy4.image.get_rect()
        btns.add(buy4)
        buy4.rect.x = 1100
        buy4.rect.y = 550
    else:
        buy4 = 0
        sold4 = pygame.sprite.Sprite()
        sold4.image = load_image("sold.png")
        sold4.image = pygame.transform.scale(sold4.image, (200, 200))
        sold4.rect = sold4.image.get_rect()
        btns.add(sold4)
        sold4.rect.x = 1100
        sold4.rect.y = 550


    c = str(cost[3])
    text_cost4 = font.render(c, True, (255, 255, 255))
    screen.blit(text_cost4, (1245, 215))

    screen.blit(text1, (180, 570))
    screen.blit(text2, (480, 570))
    screen.blit(text3, (780, 570))
    screen.blit(text4, (1080, 570))


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
font = pygame.font.Font(FONT, 30)
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

first = pygame.sprite.Sprite()
first.image = load_image("first.png")
first.image = pygame.transform.scale(first.image, (150, 150))
first.rect = first.image.get_rect()
btns.add(first)
first.rect.x = 600
first.rect.y = 10

second = pygame.sprite.Sprite()
second.image = load_image("second.png")
second.image = pygame.transform.scale(second.image, (150, 150))
second.rect = second.image.get_rect()
btns.add(second)
second.rect.x = 760
second.rect.y = 10

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

for i in range(4):
    money = pygame.sprite.Sprite()
    money.image = load_image("money.png")
    money.image = pygame.transform.scale(money.image, (40, 40))
    money.rect = money.image.get_rect()
    btns.add(money)
    money.rect.x = 380 + 300*i
    money.rect.y = 220


back = pygame.sprite.Sprite()
back.image = load_image("back.png")
back.image = pygame.transform.scale(back.image, (200, 100))
back.rect = back.image.get_rect()
btns.add(back)
back.rect.x = 1200
back.rect.y = 25

skins_photo = ['hudPlayer_beige.png', 'hudPlayer_blue.png', 'hudPlayer_green.png', 'hudPlayer_pink.png']
boosts_photo = ['fight.png', 'speed.png', 'hp.png', '2x.png', '3x.png', '4x.png']
skins_items = ['beige skin', 'blue skin', 'green skin', 'pink skin']
boosts_items = ['fight', 'speed', 'hp', '2x', '3x', '4x']
text_boosts = ['+1 урон', '+5% speed', '+2 ХП', '2x очки', '3x очки', '4x очки']
text_skins = ['beige skin', 'blue skin', 'green skin', 'pink skin']
flag = 1

id_new(1)

itemsgrp = pygame.sprite.Group()

font = pygame.font.Font(FONT, 40)
pygame.display.flip()
running = True
mainlist = []
mainlist1 = []
maincost = cost_skins
main_bought = sold_skins
new(skins_photo, text_skins, cost_skins, main_bought)
mainlist = skins_photo
maintext = text_skins
while running:
    btns.draw(screen)
    itemsgrp.draw(screen)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if right.rect.collidepoint(x, y):
                clear()
                screen.blit(bg, (0, 0))
                mainlist = mainlist[-1:] + mainlist[:-1]
                mainlist1 = mainlist1[-1:] + mainlist1[:-1]
                maintext = maintext[-1:] + maintext[:-1]
                maincost = maincost[-1:] + maincost[:-1]
                main_bought = main_bought[-1:] + main_bought[:-1]
                new(mainlist, maintext, maincost, main_bought)
                print(main_bought)
                pygame.display.flip()
            if left.rect.collidepoint(x, y):
                clear()
                screen.blit(bg, (0, 0))
                mainlist = mainlist[1:] + mainlist[:1]
                mainlist1 = mainlist1[1:] + mainlist1[:1]
                maintext = maintext[1:] + maintext[:1]
                maincost = maincost[1:] + maincost[:1]
                main_bought = main_bought[1:] + main_bought[:1]
                new(mainlist, maintext, maincost, main_bought)
                print(main_bought)
                pygame.display.flip()
            if boosts.rect.collidepoint(x, y):
                clear()
                screen.blit(bg, (0, 0))
                new(boosts_photo, text_boosts, cost_boosts, sold_boosts)
                mainlist = boosts_photo
                mainlist1 = boosts_items
                maintext = text_boosts
                maincost = cost_boosts
                flag = 0
                main_bought = sold_boosts
                pygame.display.flip()
            if skins.rect.collidepoint(x, y):
                clear()
                screen.blit(bg, (0, 0))
                new(skins_photo, text_skins, cost_skins, sold_skins)
                mainlist = skins_photo
                mainlist1 = skins_items
                maintext = text_skins
                maincost = cost_skins
                flag = 1
                main_bought = sold_skins
                pygame.display.flip()
            if back.rect.collidepoint(x, y):
                back_door()
            if buy1!= 0 and buy1.rect.collidepoint(x, y):
                if not main_bought[0]:
                    if players_money >= maincost[0]: #если хватает денег на покупку товара
                        players_money = players_money - maincost[0]
                        if flag: #если покупают скины
                            tovar = skins_photo[0]
                            sold_skins[0] = 1
                            main_bought[0] = 1
                        else: #если покупают бусты
                            tovar = boosts_photo[0]
                            main_bought = sold_boosts
                        renew_db(players_money, tovar, flag, id)
                        new(mainlist, maintext, maincost, main_bought)

            if buy2 != 0 and buy2.rect.collidepoint(x, y):
                if not main_bought[3]:
                    if players_money >= maincost[1]:  # если хватает денег на покупку товара
                        players_money = players_money - maincost[1]
                        if flag:  # если покупают скины
                            tovar = skins_photo[1]
                            sold_skins[1] = 1
                            main_bought = sold_skins
                        else:  # если покупают бусты
                            tovar = boosts_photo[1]
                            main_bought = sold_boosts
                        renew_db(players_money, tovar, flag, id)
                        new(mainlist, maintext, maincost, main_bought)

            if buy3 != 0 and buy3.rect.collidepoint(x, y):
                if not main_bought[2]:  # если товар возможно купить
                    if players_money >= maincost[2]:  # если хватает денег на покупку товара
                        players_money = players_money - maincost[2]
                        if flag:  # если покупают скины
                            tovar = skins_photo[2]
                            sold_skins[2] = 1
                            main_bought = sold_skins
                        else:  # если покупают бусты
                            tovar = boosts_photo[2]
                            main_bought = sold_boosts
                        renew_db(players_money, tovar, flag, id)
                        new(mainlist, maintext, maincost, main_bought)


            if buy4 != 0 and buy4.rect.collidepoint(x, y):
                if not main_bought[3]:  # если товар возможно купить
                    if players_money >= maincost[3]:  # если хватает денег на покупку товара
                        players_money = players_money - maincost[3]
                        if flag:  # если покупают скины
                            tovar = skins_photo[3]
                            sold_skins[3] = 1
                            main_bought = sold_skins
                        else:  # если покупают бусты
                            tovar = boosts_photo[3]
                            main_bought = sold_boosts
                        renew_db(players_money, tovar, flag, id)
                        new(mainlist, maintext, maincost, main_bought)

            if first.rect.collidepoint(x, y):
                id = 1
                id_new(1)
                itemsgrp = pygame.sprite.Group()
                font = pygame.font.Font(FONT, 40)
                pygame.display.flip()
                running = True
                mainlist = []
                mainlist1 = []
                maincost = cost_skins
                main_bought = sold_skins
                new(skins_photo, text_skins, cost_skins, main_bought)
                mainlist = skins_photo
                maintext = text_skins
            if second.rect.collidepoint(x, y):
                screen.blit(bg, (0, 0))
                id = 2
                id_new(2)
                itemsgrp = pygame.sprite.Group()
                font = pygame.font.Font(FONT, 40)
                pygame.display.flip()
                running = True
                mainlist = []
                mainlist1 = []
                maincost = cost_skins
                main_bought = sold_skins
                new(skins_photo, text_skins, cost_skins, main_bought)
                mainlist = skins_photo
                maintext = text_skins






    pygame.display.flip()
pygame.quit()

