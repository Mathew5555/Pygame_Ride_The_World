from main_menu import main
from funcs_backend import *
from consts import *


MUSIC_DIR = "music/"
IMAGES_DIR = "images/"
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1536, 864
FON = []


if __name__ == '__main__':
    joy = input('Вы будете играть с джойстиком или без? (Введите "да" или "нет" без кавычек): ')
    while joy not in ['да', 'нет']:
        joy = input('Вы будете играть с джойстиком или без? (Введите "да" или "нет" без кавычек): ')
    if joy == 'да':
        joy = True
    else:
        joy = False

    pygame.init()
    pygame.display.set_caption('Ride The World - ver 1.0')
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()
    pygame.mixer.music.load('music/hello.mp3')
    pygame.mixer.music.play(999)
    pygame.mixer.music.set_volume(0.5)

    FON = split_animated_gif('klee', screen=screen)
    running = True
    ind = 0
    while running:
        if ind >= len(FON):
            ind = 0
        screen.blit(FON[ind], (0, 0))
        render_and_blit_text(screen, 50, 'Нажмите любую клавишу, чтобы продолжить', 100, 800, (255, 255, 255))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                running = False
                pygame.mixer.music.unload()
                main(joy)
                break
        clock.tick(FPS2)
        ind += 1
        pygame.display.flip()
