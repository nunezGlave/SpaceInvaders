'''
    Created by Andy
'''
import pygame
import sys
import subprocess

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Space Invaders Menu')

# Font setup
font = pygame.font.Font(None, 36)


def main_menu():
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 70,
                            SCREEN_HEIGHT // 2 - 10, 140, 32)
    attach_human_box = pygame.Rect(
        SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 90, 20, 20)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    attach_human = False
    text = ''
    clock = pygame.time.Clock()
    run_button = pygame.Rect(SCREEN_WIDTH // 2 - 70,
                             SCREEN_HEIGHT // 2 + 40, 140, 40)

    while True:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive

                if attach_human_box.collidepoint(event.pos):
                    attach_human = not attach_human

                if run_button.collidepoint(event.pos):
                    try:
                        num_instances = int(text)
                        for _ in range(num_instances):
                            if _ == 0 and attach_human:  # This is the first instance and human attached
                                subprocess.Popen(
                                    ["python", "SpaceInvaders.py", "--attach-human"])
                            else:
                                subprocess.Popen(
                                    ["python", "SpaceInvaders.py"])
                        pygame.quit()
                        sys.exit()
                    except ValueError:
                        pass

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        # Render number of instances input
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        # Render "Run" button
        run_surface = font.render('Run', True, WHITE)
        pygame.draw.rect(screen, GREEN if run_button.collidepoint(
            pygame.mouse.get_pos()) else BLUE, run_button)
        screen.blit(run_surface, (run_button.x + 45, run_button.y + 5))

        # Render "Attach Human" checkbox
        pygame.draw.rect(
            screen, RED if attach_human else BLUE, attach_human_box)
        attach_human_surface = font.render('Attach Human?', True, (0, 0, 0))
        screen.blit(attach_human_surface,
                    (attach_human_box.x + 30, attach_human_box.y - 5))

        # Render "How many instances" prompt
        prompt_surface = font.render(
            'How many instances do you want to run?', True, (0, 0, 0))
        screen.blit(
            prompt_surface,
            (SCREEN_WIDTH // 2 - prompt_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 60))

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main_menu()
