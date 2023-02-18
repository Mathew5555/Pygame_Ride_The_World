MUSIC_DIR = "music/"
IMAGES_DIR = "images/"
FPS = 45
FPS2 = 30
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1500, 1000
WINDOW_SIZE2 = WINDOW_WIDTH2, WINDOW_HEIGHT2 = 1600, 960
FONT = 'data/font.ttf'
TRACKS = [MUSIC_DIR + 'chasm' + f'{i}.mp3' for i in range(1, 16)]
MAPS_DIR = 'maps/'
for_game = {'speed/1.png': 1.1, 'speed/2.png': 1.2, 'speed/3.png': 1.3, 'speed/4.png': 1.4, 'speed/5.png': 1.5,
            'gun/1.png': 1.25, 'gun/2.png': 1.5, 'gun/3.png': 1.75, 'gun/4.png': 2, 'gun/5.png': 2.5,
            'health/1.png': 100, 'health/2.png': 150, 'health/3.png': 200, 'health/4.png': 300, 'health/5.png': 400}
MAPS_FLAGS = {"map2.tmx": [(1, 3), 2, 0], "map_2.tmx": [(1, 2, 3, 4, 5, 6), -1, 2], "map3.tmx": [(1, 2, 4, 5, 6), 3, 1],
              "map_tartaglia.tmx": [(1, 2, 3, 4), -1, 0]}
