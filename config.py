from win32api import GetSystemMetrics
import pygame
import os

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
WIDTH = GetSystemMetrics(0)
HEIGHT = GetSystemMetrics(1)
WAY = os.path.abspath(__file__)[:-10]


pygame.init()
screen = pygame.display.set_mode((300, 400))
pygame.display.set_caption("Back to life (beta 0.1)")


def draw_text(surf, text, size, x, y, color=WHITE, font_name=pygame.font.match_font('Arial')):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Backgrounds:
    img = pygame.image.load(WAY + '\\images\\backgrounds\\menu_background.png')
    menu_bg = pygame.transform.scale(img, (WIDTH, HEIGHT))


class Sprites:
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)

            player_img = pygame.image.load('images/player/0.png').convert()
            img = pygame.transform.scale(player_img, (128, 128))
            self.image = img
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect()
            self.rect.center = (200, 200)
            self.frame = 0

        def walk(self, direction):
            if direction == "right":
                player_img = pygame.image.load(f'images/player/walk/{str(int(self.frame))}.png').convert()
                self.rect.x += 7
            elif direction == "left":
                player_img = pygame.image.load(f'images/player/walk/{str(int(self.frame + 6))}.png').convert()
                self.rect.x -= 7
            else:
                player_img = None
            img = pygame.transform.scale(player_img, (128, 128))
            self.image = img
            self.image.set_colorkey(WHITE)
            self.frame += 0.8
            if self.frame > 5:
                self.frame = 0

        def take(self, direction):
            if direction == "right":
                player_img = pygame.image.load(f'images/player/walk/{str(self.frame)}.png').convert()
            elif direction == "left":
                player_img = pygame.image.load(f'images/player/walk/{str(self.frame + 15)}.png').convert()
            else:
                player_img = None
            img = pygame.transform.scale(player_img, (128, 128))
            self.image = img
            self.image.set_colorkey(BLACK)
            self.frame += 1
            if self.frame > 15:
                self.frame = 0

    class Nightmare(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)

            player_img = pygame.image.load('images/nightmare/0.png').convert()
            img = pygame.transform.scale(player_img, (128, 128))
            self.image = img
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect()
            self.rect.x = 200
            self.rect.y = 200
            self.frame = 0

        def walk(self, direction):
            if direction == "right":
                player_img = pygame.image.load(f'images/nightmare/walk/{str(int(self.frame + 4))}.png').convert()
                self.rect.x += 5
            elif direction == "left":
                player_img = pygame.image.load(f'images/nightmare/walk/{str(int(self.frame))}.png').convert()
                self.rect.x -= 5
            else:
                player_img = None
            img = pygame.transform.scale(player_img, (128, 128))
            self.image = img
            self.image.set_colorkey(WHITE)
            self.frame += 0.5
            if self.frame > 3:
                self.frame = 0

    class Button(pygame.sprite.Sprite):
        def __init__(self, image, w, h, x, y, frames):
            pygame.sprite.Sprite.__init__(self)

            btn_img = pygame.image.load(image + '0.png').convert()
            img = pygame.transform.scale(btn_img, (w, h))
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

            self.image_way = image
            self.frame = 0
            self.frames = frames
            self.w = w
            self.h = h

        def mouse_in(self):
            btn_img = pygame.image.load(f'{self.image_way}mouse_in/{str(int(self.frame))}.png').convert()
            img = pygame.transform.scale(btn_img, (self.w, self.h))
            self.image = img
            self.image.set_colorkey(BLACK)
            self.frame -= 1
            if self.frame < 0:
                self.frame = self.frames

    menu_buttons = pygame.sprite.Group()
    play_btn = Button('images/buttons/play_btn/',
                      int(WIDTH * 0.3), int(HEIGHT * 0.1),
                      WIDTH // 2, int(HEIGHT * 0.55),
                      14)
    exit_btn = Button('images/buttons/exit_btn/',
                      int(play_btn.w * 0.715), int(HEIGHT * 0.1),
                      WIDTH // 2 - play_btn.w // 2 + int(play_btn.w * 0.715) // 2, int(HEIGHT * 0.67),
                      11)
    settings_btn = Button('images/buttons/settings_btn/',
                          int(HEIGHT * 0.1), int(HEIGHT * 0.1),
                          WIDTH // 2 + play_btn.w // 2 - int(HEIGHT * 0.1) // 2, int(HEIGHT * 0.67),
                          10)
    menu_buttons.add(play_btn, exit_btn, settings_btn)

    gg = pygame.sprite.Group()
    player = Player()
    gg.add(player)

    sleepland_mobs = pygame.sprite.Group()
    nightmare = Nightmare()
    sleepland_mobs.add(nightmare)


class MenuBg(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        player_img = pygame.image.load('images/backgrounds/loading_background/0.png').convert()
        img = pygame.transform.scale(player_img, (128, 128))
        self.image = img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (150, 200)
        self.frame = 0
        self.end = False

    def update(self):
        bg = pygame.image.load(f'images/backgrounds/loading_background/{str(int(self.frame))}.png').convert()
        self.image = bg
        self.frame += 1
        if self.frame > 22:
            self.end = True


mbg = MenuBg()
bg = pygame.sprite.Group()
bg.add(mbg)

while True:
    pygame.time.Clock().tick(20)
    bg.draw(screen)
    mbg.update()
    pygame.display.flip()
    if mbg.end:
        break

draw_text(screen, "Loading sprites...", 20, 150, 200)
sprites = Sprites
screen.fill(BLACK)
draw_text(screen, "Loading backgrounds...", 20, 150, 200)
backgrounds = Backgrounds
pygame.quit()
