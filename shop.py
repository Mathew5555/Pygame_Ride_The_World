from funcs_backend import *
import pygame
from consts import *
import sqlite3


pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
RUNNING = True


class Shop:
    def __init__(self, back='back.png', bottom='wb_bg.png', left='previous.png', right='next.png',
                 ok='check.png'):
        self.con = sqlite3.connect('data/account_info.db')
        self.cur = self.con.cursor()
        self.btn_back = pic(back, (20, 20))
        self.bottom1 = pic(bottom, (1280, 20), add=(200, 50))
        self.bottom2 = pic(bottom, (1280, 80), add=(200, 50))
        self.boosts = self.cur.execute("SELECT boost_dir, description FROM boosts").fetchall()
        self.maxx1 = len(self.boosts) * 5
        self.ind = 0
        self.curr_pl = 1

        self.btn_left = pic(left, (300, 875), add=(100, 100))
        self.btn_right = pic(right, (1100, 875), add=(100, 100))
        self.btn_pick = pic(ok, (700, 875), add=(100, 100))

    def render(self, screen):
        create_and_blit_surface(screen, -50, 250, (1600, 500), (0, 200, 200), 50)
        create_and_blit_surface(screen, 40, 90, (1200, 150), (0, 0, 0), 150)

        render_and_blit_text(screen, 45, 'Примечание:', 50, 90, (255, 0, 0))
        render_and_blit_text(screen, 25, 'Это не магазин, который был запланирован. Это "сырая" версия его.', 50, 140, (255, 255, 255))
        render_and_blit_text(screen, 25, 'Член команды не доделал магазин к сроку сдачи, поэтому пришлось делать', 50, 160, (255, 255, 255))
        render_and_blit_text(screen, 25, 'наспех то, что должно было быть для работы игры. Из-за этого все скины', 50, 180, (255, 255, 255))
        render_and_blit_text(screen, 25, 'доступны сразу, а буст на игру можно выбрать бесплатно. См. ветку feature/store', 50, 200, (255, 255, 255))

        if self.curr_pl == 1:
            x, y = 1275, 15
        else:
            x, y = 1275, 75
        size = 210, 60
        create_and_blit_surface(screen, x, y, size, (0, 255, 0), 100)

        screen.blit(*self.bottom1)
        screen.blit(*self.bottom2)
        render_and_blit_text(screen, 45, 'Игрок 1', 1292, 17, (255, 255, 255))
        render_and_blit_text(screen, 45, 'Игрок 2', 1292, 77, (255, 255, 255))
        screen.blit(*self.btn_back)
        screen.blit(*self.btn_right)
        screen.blit(*self.btn_left)
        screen.blit(*self.btn_pick)

    def render_boosts(self):
        cnt = 0
        for i in range(self.ind, self.ind + 5):
            try:
                screen.blit(*pic(self.boosts[i % len(self.boosts)][0], (50 + cnt * 300, 350), add=(200, 200)))
                render_and_blit_text(screen, 35, self.boosts[i % len(self.boosts)][1], 50 + cnt * 300, 600, (255, 255, 255))
            except Exception:
                cnt += 1
                continue
            cnt += 1

    def next(self):
        self.ind += 1
        if self.ind == len(self.boosts):
            self.ind = 0

    def previous(self):
        self.ind -= 1
        if self.ind < 0:
            self.ind = len(self.boosts) - 1

    def pick(self):
        self.cur.execute(
            f"UPDATE info SET boosts = '{self.boosts[self.ind + 2][0]}' WHERE id = {self.curr_pl}")
        self.con.commit()

    def back(self):
        global RUNNING
        RUNNING = False
        self.con.close()


def shop():
    global RUNNING
    shop_list = Shop()
    FON = split_animated_gif(IMAGES_DIR + 'shop.gif')[:]
    ind = 0
    RUNNING = True
    clock.tick(FPS2)
    while RUNNING:
        screen.blit(FON[ind], (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                sound.play(0)
                mouse = pygame.mouse.get_pos()
                if shop_list.btn_back[1].collidepoint(*mouse):
                    shop_list.back()
                    break
                if shop_list.bottom1[1].collidepoint(*mouse):
                    shop_list.curr_pl = 1
                if shop_list.bottom2[1].collidepoint(*mouse):
                    shop_list.curr_pl = 2
                if shop_list.btn_right[1].collidepoint(*mouse):
                    shop_list.next()
                if shop_list.btn_pick[1].collidepoint(*mouse):
                    shop_list.pick()
                if shop_list.btn_left[1].collidepoint(*mouse):
                    shop_list.previous()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    shop_list.next()
                if event.key == pygame.K_LEFT:
                    shop_list.previous()
                if event.key == pygame.K_RETURN:
                    shop_list.pick()
                if event.key == pygame.K_1:
                    shop_list.curr_pl = 1
                if event.key == pygame.K_2:
                    shop_list.curr_pl = 2
                if event.key == pygame.K_ESCAPE:
                    shop_list.back()
                    break
        shop_list.render(screen)
        shop_list.render_boosts()
        sound_level = float(
            open('data/sound.txt', mode='r', encoding='utf-8').readlines()[0].strip('\n'))
        check_busy(sound_level)
        pygame.display.flip()
        ind = (ind + 1) % len(FON)
        clock.tick(FPS2)


if __name__ == '__main__':
    shop()
