from funcs_backend import *
import pygame
from consts import *
import sqlite3


pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
RUNNING = True


class Account:
    def __init__(self, back='back.png', none_im='none.png'):
        self.btn_back = pic(back, (20, 20))
        self.con = sqlite3.connect('data/account_info.db')
        self.cur = self.con.cursor()
        self.info = self.cur.execute(f"SELECT * FROM info").fetchall()
        self.im1 = none_im if self.info[0][-1] is None else self.info[0][-1]
        self.im2 = none_im if self.info[1][-1] is None else self.info[1][-1]
        self.info = [[*self.info[0][:5], self.info[0][6]], [*self.info[1][:5], self.info[1][6]]]
        self.clr = (250, 235, 215)

    def render(self, screen):
        x = 750
        screen.blit(*self.btn_back)
        bottom = pygame.Surface((690, 840))
        bottom.set_alpha(150)
        bottom.fill((0, 0, 0))
        screen.blit(bottom, (30, 130))
        screen.blit(bottom, (x + 30, 130))

        screen.blit(*pic(self.im1 + '/stand.png', (50, 150), add=(150, 150)))
        screen.blit(*pic(self.im2 + '/stand.png', (50 + x, 150), add=(150, 150)))
        t = len(self.info[0]) - 1
        text = ['ID', 'Уровень игрока:', 'Баланс монет:', 'Кол-во убийств:', 'Лучший результат:']
        for i in range(t):
            font = pygame.font.Font(FONT, 40)
            line = font.render(text[i], True, (255, 255, 255))
            screen.blit(line, (50, 320 + i * 120))

            font = pygame.font.Font(FONT, 60)
            line = font.render(str(self.info[0][i]), True, self.clr)
            screen.blit(line, (50, 360 + i * 120))
        for i in range(t):
            font = pygame.font.Font(FONT, 40)
            line = font.render(text[i], True, (255, 255, 255))
            screen.blit(line, (50 + x, 320 + i * 120))

            font = pygame.font.Font(FONT, 60)
            line = font.render(str(self.info[1][i]), True, self.clr)
            screen.blit(line, (50 + x, 360 + i * 120))

    def back(self):
        global RUNNING
        RUNNING = False


def acc():
    global RUNNING
    account = Account()
    FON = split_animated_gif(IMAGES_DIR + 'fon_acc_info.gif')[:]
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
                if account.btn_back[1].collidepoint(*mouse):
                    account.back()
                    break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    account.back()
                    break
        account.render(screen)
        sound_level = float(
            open('data/sound.txt', mode='r', encoding='utf-8').readlines()[0].strip('\n'))
        check_busy(sound_level)
        pygame.display.flip()
        ind = (ind + 1) % len(FON)
        clock.tick(FPS2)


if __name__ == '__main__':
    acc()
