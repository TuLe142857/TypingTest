import pygame
import app

if __name__ == "__main__":
    pygame.init()
    intro = '''
    -----------------------------------------------------
    |               TYPING TEST                         |
    |author: Le Ngoc Tu                                 |
    |for more information:                              |
    |   https://github.com/TuLe142857/TypingTest.git    |
    -----------------------------------------------------
    '''
    print(intro)
    app = app.App()
    app.run()
    input()
    pygame.quit()