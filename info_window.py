from funcs_backend import *
import pygame
from consts import *


pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
RUNNING = True


class Info:
    def __init__(self, back='back.png'):
        self.btn_back = pic(back, (20, 20))

    def render_text(self, screen, text1, otst, i, titles, plus):
        size = 30
        curr = 80 + (i - titles) * 30 + titles * 50 + plus
        line = text1[i]
        clr = (255, 255, 255)
        if type(text1[i]) == tuple:
            size = 50
            curr = 80 + (i - titles) * 30 + titles * 50 + plus + 20
            line = line[0]
            titles += 1
            plus += 20
            clr = (255, 80, 255)
        font = pygame.font.Font(FONT, size)
        line = font.render(line, True, clr)
        screen.blit(line, (otst, curr))
        return titles, plus

    def render(self, screen):
        bottom = pygame.Surface((700, 800))
        bottom.set_alpha(100)
        bottom.fill((0, 0, 0))
        screen.blit(bottom, (30, 100))
        screen.blit(bottom, (770, 100))

        text1 = [('О проекте', 'title'),
                 'Данная игра основана на игре PS',
                 '"Duck Game". В ней двое игроков,',
                 'играющих за уток, воюют друг',
                 'против друга, взаимодействуют с',
                 'картой.',
                 'Мы постарались реализовать эту идею',
                 'и представляем игру "Ride The ',
                 'World"!',
                 ('Команда', 'title'),
                 'Тимлид, дизайнер и вообще крутой',
                 'человек: Муляр Никита',
                 'Разработчик боя: Давидян Матвей',
                 'Дизайнер, разработчик магазина:',
                 'Московских Лена']
        text2 = [('Музыка', 'title'),
                 'В игре использованы музыкальные',
                 'произвдения композитора Yu Peng Chen',
                 'и команды HoYoMix.',
                 ('Ресурсы', 'title'),
                 'Источники: интернет, itch.io,',
                 'flaticon.com, pinterest.com',
                 ('Описание игры', 'title'),
                 'В нашей игре мы берём разных героев',
                 'и проходим с ними различные карты,',
                 'тем самым исследуя новые окрестности.',
                 'В то же время наш персонаж выступает',
                 'как посредник между нами и игрой,',
                 'который позволяет нам, не отходя от',
                 'компьютера, взглянуть на чудесные',
                 'земли, стилизованные в тематике',
                 'Genshin Impact!']
        titles = 0
        plus = 0
        for i in range(len(text1)):
            titles, plus = self.render_text(screen, text1, 50, i, titles, plus)
        titles = 0
        plus = 0
        for i in range(len(text2)):
            titles, plus = self.render_text(screen, text2, 790, i, titles, plus)
        screen.blit(*self.btn_back)

    def back(self):
        global RUNNING
        RUNNING = False


def info():
    global RUNNING
    info = Info()
    FON = split_animated_gif(IMAGES_DIR + 'fon_info.gif')[:]
    ind = 0
    RUNNING = True
    clock.tick(FPS)
    while RUNNING:
        screen.blit(FON[ind], (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if info.btn_back[1].collidepoint(*mouse):
                    info.back()
                    break
        info.render(screen)
        pygame.display.flip()
        ind = (ind + 1) % len(FON)
        clock.tick(FPS)


if __name__ == '__main__':
    info()
