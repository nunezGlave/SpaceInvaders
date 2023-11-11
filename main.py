''' Created by Alexander '''

# Import libraries
from Logical_Layer.Viewport.space_invader import SpaceInvaders
from Logical_Layer.Viewport.screen_surface import Screen
from pygame import *

if __name__ == '__main__':
    # Variables to control the game
    optionMenu = 4
    gameControl = True

    # Start the video game
    init()
    clock = time.Clock()
    display.set_caption('Space Invaders')

    # Set main screen dimensions
    window = display.set_mode((display.Info().current_w , display.Info().current_h))
    screen = Screen(window)
    scaleImage = optionMenu
    
    print('Display Mode:')
    print('{} - {}'.format(screen.width, screen.height))

    # Initialize games depending on the type of game (single player or multiplayer)
    match optionMenu:
        case 1:
            fullScreen = SpaceInvaders(scaleImage, 0, screen, screen.width, screen.height)
        case 2:
            leftScreen = SpaceInvaders(scaleImage, 0, screen, screen.halfWidth, screen.height)
            rightScreen = SpaceInvaders(scaleImage, 1, screen, screen.halfWidth, screen.height, screen.halfWidth)
        case 3:
            leftTop = SpaceInvaders(scaleImage, 0, screen, screen.halfWidth, screen.halfHeight)
            leftBottom = SpaceInvaders(scaleImage, 0, screen, screen.halfWidth, screen.halfHeight, 0, screen.halfHeight)
            rightTop = SpaceInvaders(scaleImage, 1, screen, screen.halfWidth, screen.halfHeight, screen.halfWidth)
            rightBottom = SpaceInvaders(scaleImage, 1, screen, screen.halfWidth, screen.halfHeight, screen.halfWidth, screen.halfHeight)
        case 4:
            leftTop = SpaceInvaders(3, 2, screen, screen.halfWidth, screen.halfHeight)
            leftBottom = SpaceInvaders(3, 2, screen, screen.halfWidth, screen.halfHeight, 0, screen.halfHeight)
            rightTop = SpaceInvaders(3, 2, screen, screen.halfWidth, screen.halfHeight, screen.halfWidth)
            rightBottom = SpaceInvaders(3, 2, screen, screen.halfWidth, screen.halfHeight, screen.halfWidth,
                                screen.halfHeight)
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
            case 4:
                leftTop.main()
                leftBottom.main()
                rightTop.main()
                rightBottom.main()
            case _:
                gameControl = False

        display.update()
        clock.tick(60)

