from funcs_backend import *
import pygame
from consts import *
import sqlite3


pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
RUNNING = True


class Wardrobe:
    def __init__(self, back='back.png', bottom='wb_bg.png', left='previous.png', right='next.png',
                 ok='check.png'):
        self.con = sqlite3.connect('data/account_info.db')
        self.cur = self.con.cursor()
        self.btn_back = pic(back, (20, 20))
        self.bottom1 = pic(bottom, (1280, 20), add=(200, 50))
        self.bottom2 = pic(bottom, (1280, 80), add=(200, 50))
        self.player1 = self.cur.execute("SELECT skins FROM info WHERE id = 1").fetchall()[0][0].split(';')
        self.player2 = self.cur.execute("SELECT skins FROM info WHERE id = 2").fetchall()[0][0].split(';')
        self.maxx1 = len(self.player1)
        self.maxx2 = len(self.player2)
        self.ind = 0
        self.curr_pl = 1

        self.btn_left = pic(left, (300, 875), add=(100, 100))
        self.btn_right = pic(right, (1100, 875), add=(100, 100))
        self.btn_pick = pic(ok, (700, 875), add=(100, 100))

        self.font = pygame.font.Font(FONT, 45)

    def render(self, screen):
        bottom = pygame.Surface((1600, 500))
        bottom.set_alpha(50)
        bottom.fill((255, 0, 255))
        screen.blit(bottom, (-50, 250))

        screen.blit(*self.bottom1)
        screen.blit(*self.bottom2)
        line = self.font.render('Игрок 1', True, (255, 255, 255))
        screen.blit(line, (1292, 17))
        line = self.font.render('Игрок 2', True, (255, 255, 255))
        screen.blit(line, (1292, 77))
        screen.blit(*self.btn_back)
        screen.blit(*self.btn_right)
        screen.blit(*self.btn_left)
        screen.blit(*self.btn_pick)

    def render1_wb(self):
        cnt = 0
        for i in range(self.ind - 3, self.ind):
            try:
                screen.blit(*pic(self.player1[i], (200 + cnt * 400, 350), add=(300, 300)))
                k = (i + len(self.player1) + 1) % len(self.player1)
                if k == 0:
                    k = len(self.player1)
                line = self.font.render(f'Костюм {k}', True, (255, 255, 255))
                screen.blit(line, (200 + cnt * 400 + 50, 700))
            except Exception:
                cnt += 1
                continue
            cnt += 1

    def render2_wb(self):
        cnt = 0
        for i in range(self.ind - 3, self.ind):
            try:
                screen.blit(*pic(self.player2[i], (200 + cnt * 400, 350), add=(300, 300)))
                k = (i + len(self.player2) + 1) % len(self.player2)
                if k == 0:
                    k = len(self.player2)
                line = self.font.render(f'Костюм {k}', True, (255, 255, 255))
                screen.blit(line, (200 + cnt * 400 + 50, 700))
            except Exception:
                cnt += 1
                continue
            cnt += 1

    def next(self):
        self.ind += 1
        if self.curr_pl == 1:
            self.ind = self.ind % self.maxx1
        elif self.curr_pl == 2:
            self.ind = self.ind % self.maxx2

    def previous(self):
        self.ind -= 1
        if self.ind < 0:
            if self.curr_pl == 1:
                self.ind = self.maxx1 - 1
            else:
                self.ind = self.maxx2 - 1

    def pick(self):
        if self.curr_pl == 1:
            self.cur.execute(
                f"UPDATE info SET curr_skin = '{self.player1[self.ind - 2]}' WHERE id = {self.curr_pl}")
        else:
            self.cur.execute(
                f"UPDATE info SET curr_skin = '{self.player2[self.ind - 2]}' WHERE id = {self.curr_pl}")
        self.con.commit()

    def back(self):
        global RUNNING
        RUNNING = False
        self.con.close()


def wb():
    global RUNNING
    wardrobe = Wardrobe()
    FON = split_animated_gif(IMAGES_DIR + 'fon_wb.gif')[:]
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
                if wardrobe.btn_back[1].collidepoint(*mouse):
                    wardrobe.back()
                    break
                if wardrobe.bottom1[1].collidepoint(*mouse):
                    wardrobe.curr_pl = 1
                if wardrobe.bottom2[1].collidepoint(*mouse):
                    wardrobe.curr_pl = 2
                if wardrobe.btn_right[1].collidepoint(*mouse):
                    wardrobe.next()
                if wardrobe.btn_pick[1].collidepoint(*mouse):
                    wardrobe.pick()
                if wardrobe.btn_left[1].collidepoint(*mouse):
                    wardrobe.previous()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    wardrobe.next()
                if event.key == pygame.K_LEFT:
                    wardrobe.previous()
                if event.key == pygame.K_BREAK:
                    wardrobe.pick()
        wardrobe.render(screen)
        if wardrobe.curr_pl == 1:
            wardrobe.render1_wb()
        else:
            wardrobe.render2_wb()
        sound_level = float(
            open('data/sound.txt', mode='r', encoding='utf-8').readlines()[0].strip('\n'))
        check_busy(sound_level)
        pygame.display.flip()
        ind = (ind + 1) % len(FON)
        clock.tick(FPS2)


if __name__ == '__main__':
    wb()
