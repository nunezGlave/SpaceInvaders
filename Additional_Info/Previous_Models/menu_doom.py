import pygame
import sys
import subprocess
import os 

# Path resources
FULL_PATH = os.getcwd()
FONT_PATH = FULL_PATH + '/Assets/Fonts/'
FONT = FONT_PATH + 'knight_warrior.otf'
IMAGE_PATH = FULL_PATH + '/Assets/Images/Doom/'

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Space Invaders Menu')

def x_coordinate(percentage: int):
    return int(SCREEN_WIDTH * percentage / 100)

def y_coordinate(percentage: int):
    return int(SCREEN_HEIGHT * percentage / 100)

def main_menu():
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 10, 140, 32)
    attach_human_box = pygame.Rect(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 90, 20, 20)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    attach_human = False
    text = ''
    clock = pygame.time.Clock()

    while True:
        # Render menu background.
        background = pygame.image.load(IMAGE_PATH + 'difficulty_menu.png')
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background, (0,0))

        # Render space invaders title img.
        title_left_percentage = 3
        title_top_percentage = 30
        title = pygame.image.load(IMAGE_PATH + 'logo.png')
        title = pygame.transform.scale(title, (520, 230))
        screen.blit(title, (x_coordinate(title_left_percentage), y_coordinate(title_top_percentage)))

        # Start button.
        start_button_left_percentage = 62.5
        start_button_top_percentage = 33
        start_button_rect = pygame.Rect(x_coordinate(start_button_left_percentage), y_coordinate(start_button_top_percentage), 225, 50)
        pygame.draw.rect(screen, (208,98,124) if start_button_rect.collidepoint(pygame.mouse.get_pos()) else (193,52,85), start_button_rect, border_radius=40)
        # Start button txt.
        start_button_font = pygame.font.Font(FONT, 30)
        start_button_text = start_button_font.render('Singleplayer', True, WHITE)
        screen.blit(start_button_text, start_button_text.get_rect(center=start_button_rect.center))

        # Multi button.
        multi_button_left_percentage = 62.5
        multi_button_top_percentage = 48
        multi_button_rect = pygame.Rect(x_coordinate(multi_button_left_percentage), y_coordinate(multi_button_top_percentage), 225, 50)
        pygame.draw.rect(screen, (208,98,124) if multi_button_rect.collidepoint(pygame.mouse.get_pos()) else (193,52,85), multi_button_rect, border_radius=40)
        # Multi button txt.
        multi_button_font = pygame.font.Font(FONT, 30)
        multi_button_text = multi_button_font.render('Multiplayer', True, WHITE)
        screen.blit(multi_button_text, multi_button_text.get_rect(center=multi_button_rect.center))

        # Difficulty button.
        dif_bttn_left_percentage = 62.5
        dif_bttn_top_percentage = 63
        dif_bttn_rect = pygame.Rect(x_coordinate(dif_bttn_left_percentage), y_coordinate(dif_bttn_top_percentage), 225, 50)
        pygame.draw.rect(screen, (208,98,124) if dif_bttn_rect.collidepoint(pygame.mouse.get_pos()) else (193,52,85), dif_bttn_rect, border_radius=40)
        # Difficulty button txt.
        dif_bttn_font = pygame.font.Font(FONT, 30)
        dif_bttn_text = dif_bttn_font.render('Easy', True, WHITE)
        screen.blit(dif_bttn_text, dif_bttn_text.get_rect(center=dif_bttn_rect.center))
        

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
                
                if attach_human_box.collidepoint(event.pos):
                    attach_human = not attach_human

                # TO DO => add an arg like "python main.py 4" so it creates the amount of environment specified, in this case 4.
                if start_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    subprocess.Popen(["python", "main.py"]) # these are cmd args ar if they were executed on the terminal. 
                    sys.exit()
                    
                if multi_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    subprocess.Popen(["python", "main.py", "4"])
                    sys.exit()

                if dif_bttn_rect.collidepoint(event.pos):
                    pygame.quit()
                    subprocess.Popen(["python", "doom_menu.py"])
                    sys.exit()

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode


        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main_menu()
