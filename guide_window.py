from funcs_backend import *
import pygame
from consts import *


pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
RUNNING = True


class Guide:
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

        text1 = [('Управление', 'title'),
                 '-Для управления используйте стрелки и',
                 'клавиши WASD',
                 ('Награды', 'title'),
                 '-За каждую игру начисляются монеты:',
                 '  - поражение: -5',
                 '  - победа: +30',
                 '  - за игру: время в сек * 2',
                 ('О магазине', 'title'),
                 'Со временем в магазине можно будет',
                 'купить новые карты и новые скины.',
                 'Используйте монеты, чтобы купить',
                 'костюмы или полезные бусты!',
                 ('Начать игру', 'title'),
                 'Чтобы начать игру, нажмите левый и',
                 'правый shift, либо нажмите на кнопки',
                 'мышью. У вас будет 3 секунды, чтобы',
                 'приготовиться к игре!']
        text2 = [('Геймлей', 'title'),
                 '-В игре встроен PvP режим, в котором',
                 'двое игроков могут друг с другом',
                 'бороться.',
                 '-В бой можно взять только 1 буст.',
                 'После окончания боя буст пропадает.',
                 '-Чтобы победить, нужно понизить ХП',
                 'врага до 0. Изначально у каждого',
                 'игрока есть по 10 ед. ХП.']
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


def guide():
    global RUNNING
    guide_w = Guide()
    FON = split_animated_gif(IMAGES_DIR + 'fon_guide.gif')[:]
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
                if guide_w.btn_back[1].collidepoint(*mouse):
                    guide_w.back()
                    break
        guide_w.render(screen)
        sound_level = float(
            open('data/sound.txt', mode='r', encoding='utf-8').readlines()[0].strip('\n'))
        check_busy(sound_level)
        pygame.display.flip()
        ind = (ind + 1) % len(FON)
        clock.tick(FPS)


if __name__ == '__main__':
    guide()
