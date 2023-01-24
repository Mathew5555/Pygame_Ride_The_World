import pygame
from main_menu import main, load_image


MUSIC_DIR = "music/"
IMAGES_DIR = "images/"
FPS = 60
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1500, 1000
FON = []


pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)


if __name__ == '__main__':
    FON = pygame.transform.scale(load_image(IMAGES_DIR + 'start.jpeg'), WINDOW_SIZE)
    running = True
    while running:
        screen.blit(FON, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                running = False
                main()
        pygame.display.flip()
