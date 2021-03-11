from win32api import GetSystemMetrics
import pygame
import config

WIDTH = GetSystemMetrics(0)
HEIGHT = GetSystemMetrics(1)
LETTERS = {32: " ", 45: "_", 49: "1", 50: "2", 51: "3", 52: "4", 53: "5", 54: "6", 55: "7", 56: "8", 57: "9", 96: "~",
           97: "a", 98: "b", 99: "c", 100: "d", 101: "e", 102: "f", 103: "g", 104: "h", 105: "i", 106: "j", 107: "k",
           108: "l", 109: "m", 110: "n", 111: "o", 112: "p", 113: "q", 114: "r", 115: "s", 116: "t", 117: "u", 118: "v",
           119: "w", 120: "x", 121: "y", 122: "z"}
print(WIDTH, HEIGHT)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Back to life (beta 0.1)")
clock = pygame.time.Clock()

running, console, menu, game = True, False, True, False

do_play_anim, do_exit_anim, do_sett_anim, to_admin, to_tester, wrong_password = False, False, False, False, False, False
text = ""

while running:
    while console:
        clock.tick(30)
        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                console = False
            elif event.type == pygame.KEYDOWN:
                print(event.key)
                if event.key in LETTERS.keys():
                    text += LETTERS[event.key]
                elif event.key == 8:
                    text = text[:-1]
                elif event.key == 13:
                    try:
                        if text[0] == "~":
                            if text[1:6] == "login":
                                if text[7:] == "admin":
                                    to_admin = True
                                    text = ""
                                elif text[7:] == "tester":
                                    to_tester = True
                                    text = ""
                            elif text[1:] == "exit":
                                menu = True
                                console = False
                        elif to_admin:
                            if text == "im_stay_a1ong":
                                admin = True
                                console = False
                            else:
                                wrong_password = True
                        elif to_tester:
                            if text == "12345":
                                tester = True
                                console = False
                            else:
                                wrong_password = True
                    except IndexError:
                        pass

        if wrong_password:
            config.draw_text(screen, "Password wrong!", 30, WIDTH // 2, 60, (255, 0, 0))
        config.draw_text(screen, text, 30, WIDTH//2, HEIGHT//2)
        pygame.display.flip()

    while menu:
        clock.tick(30)
        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen.blit(config.backgrounds.menu_bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu = False
            if event.type == pygame.MOUSEMOTION:
                position = event.pos
                if config.sprites.play_btn.rect.x <= position[0] <=\
                        config.sprites.play_btn.rect.x + config.sprites.play_btn.w and\
                        config.sprites.play_btn.rect.y <= position[1] <=\
                        config.sprites.play_btn.rect.y + config.sprites.play_btn.h:
                    do_play_anim = True
                else:
                    do_play_anim = False
                    config.sprites.play_btn.frame = 0
                    config.sprites.play_btn.mouse_in()

                if config.sprites.exit_btn.rect.x <= position[0] <=\
                        config.sprites.exit_btn.rect.x + config.sprites.exit_btn.w and\
                        config.sprites.exit_btn.rect.y <= position[1] <=\
                        config.sprites.exit_btn.rect.y + config.sprites.exit_btn.h:
                    do_exit_anim = True
                else:
                    do_exit_anim = False
                    config.sprites.exit_btn.frame = 0
                    config.sprites.exit_btn.mouse_in()

                if config.sprites.settings_btn.rect.x <= position[0] <=\
                        config.sprites.settings_btn.rect.x + config.sprites.settings_btn.w and\
                        config.sprites.settings_btn.rect.y <= position[1] <=\
                        config.sprites.settings_btn.rect.y + config.sprites.settings_btn.h:
                    do_sett_anim = True
                else:
                    do_sett_anim = False
                    config.sprites.settings_btn.frame = 0
                    config.sprites.settings_btn.mouse_in()
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = event.pos
                print(position)
                if config.sprites.play_btn.rect.x <= position[0] <= \
                        config.sprites.play_btn.rect.x + config.sprites.play_btn.w and \
                        config.sprites.play_btn.rect.y <= position[1] <= \
                        config.sprites.play_btn.rect.y + config.sprites.play_btn.h:
                    game = True
                    menu = False
                if config.sprites.exit_btn.rect.x <= position[0] <= \
                        config.sprites.exit_btn.rect.x + config.sprites.exit_btn.w and \
                        config.sprites.exit_btn.rect.y <= position[1] <= \
                        config.sprites.exit_btn.rect.y + config.sprites.exit_btn.h:
                    running = False
                    menu = False
                if WIDTH * 0.83 - 10 <= position[0] <= WIDTH * 0.83 + 10 and\
                        HEIGHT * 0.14 - 10 <= position[1] <= HEIGHT * 0.14 + 10:
                    console = True
                    menu = False

        if do_play_anim:
            config.sprites.play_btn.mouse_in()
        if do_exit_anim:
            config.sprites.exit_btn.mouse_in()
        if do_sett_anim:
            config.sprites.settings_btn.mouse_in()

        config.sprites.menu_buttons.draw(screen)

        pygame.display.flip()

    while game:
        clock.tick(30)
        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    config.sprites.player.walk("left")
                if event.key == pygame.K_d:
                    config.sprites.player.walk("right")

        config.sprites.gg.draw(screen)
        # config.sprites.sleepland_mobs.draw(screen)
        pygame.display.flip()

pygame.quit()
