'''
    Created by Alexander
'''

# Import libraries
from pygame import *
from Models.game import SpaceInvaders
from pygame import *

if __name__ == '__main__':
    # Variables to control the game
    optionMenu = 1
    gameControl = True

    # Start the video game
    init()
    clock = time.Clock()
    display.set_caption('Space Invaders')
    screenWidth = display.Info().current_w
    screenHeight = display.Info().current_h

    # Set main screen dimensions
    screen = display.set_mode((screenWidth, screenHeight))  # 800 600

    # Determine half screen width and height
    halfScreenWidth = screenWidth / 2
    halfScreenHeight = screenHeight / 2

    print('Display Mode:')
    print('{} - {}'.format(screenWidth, screenHeight))

    # Initialize games depending on the type of game (single player or multiplayer)
    match optionMenu:
        case 1:

            fullScreen = SpaceInvaders(
                optionMenu, screen, screenWidth, screenHeight)
        case 2:
            leftScreen = SpaceInvaders(
                optionMenu, screen, halfScreenWidth, screenHeight)
            rightScreen = SpaceInvaders(
                optionMenu, screen, halfScreenWidth, screenHeight, halfScreenWidth)
        case 3:
            leftTop = SpaceInvaders(
                optionMenu, screen, halfScreenWidth, halfScreenHeight)
            leftBottom = SpaceInvaders(
                optionMenu, screen, halfScreenWidth, halfScreenHeight, 0, halfScreenHeight)
            rightTop = SpaceInvaders(
                optionMenu, screen, halfScreenWidth, halfScreenHeight, halfScreenWidth)
            rightBottom = SpaceInvaders(
                optionMenu, screen, halfScreenWidth, halfScreenHeight, halfScreenWidth, halfScreenHeight)
        case _:
            gameControl = False
            print("Incorrect Menu Option")

    # Render games
    while gameControl:
        match optionMenu:
            case 1:
                fullScreen.main()
            case 2:
                leftScreen.main()
                rightScreen.main()
            case 3:
                leftTop.main()
                leftBottom.main()
                rightTop.main()
                rightBottom.main()
            case _:
                gameControl = False

        display.update()
        clock.tick(60)
