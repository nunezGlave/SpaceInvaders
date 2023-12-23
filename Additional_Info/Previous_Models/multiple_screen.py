''' Created by Alexander '''

# Allow individual execution file [Remove this when finished]
import os, sys
FULL_PATH = os.getcwd()
sys.path.append(FULL_PATH)

# Import libraries
from Presentation_Layer.game import SpaceInvaders as SP1
from Logical_Layer.Viewport.screen_surface import Screen
from Logical_Layer.Viewport.space_invaders import SpaceInvaders as SP2
from pygame import *

if __name__ == '__main__':
    # Variables to control the game
    optionMenu = 0
    gameControl = True
    difficulty = False
    
    # Start the video game
    init()
    clock = time.Clock()
    display.set_caption('Space Invaders')

    # Set main screen dimensions
    window = display.set_mode((display.Info().current_w , display.Info().current_h))
    screen = Screen(window)
    modeGame = optionMenu
    
    print('Display Mode:')
    print('{} - {}'.format(screen.width, screen.height))

    # Initialize games depending on the type of game (single player or multiplayer)
    match optionMenu:
        case -1:
            player1 = [{'typePlayer': 0, 'name': 'Player-1', 'id': 1},{'typePlayer': 1, 'name': 'Player-2', 'id': 2}]
            gameScreen3 = SP1(1, player1, difficulty, screen.width, screen.height)    
        case 0:
            player = [{'typePlayer': 0, 'name': 'Player-1', 'id': 1}]
            gameScreen = SP1(1, player, difficulty, screen.width, screen.height)
        case 1: 
            fullScreen = SP2(modeGame, 2, screen, screen.width, screen.height)            
        case 2:
            leftScreen = SP2(modeGame, 0, screen, screen.halfWidth, screen.height)
            rightScreen = SP2(modeGame, 1, screen, screen.halfWidth, screen.height, screen.halfWidth)
        case 3:
            leftTop = SP2(modeGame, 0, screen, screen.halfWidth, screen.halfHeight)
            leftBottom = SP2(modeGame, 0, screen, screen.halfWidth, screen.halfHeight, 0, screen.halfHeight)
            rightTop = SP2(modeGame, 1, screen, screen.halfWidth, screen.halfHeight, screen.halfWidth)
            rightBottom = SP2(modeGame, 1, screen, screen.halfWidth, screen.halfHeight, screen.halfWidth, screen.halfHeight)
        case 4:
            leftTop = SP2(3, 2, screen, screen.halfWidth, screen.halfHeight)
            leftBottom = SP2(3, 2, screen, screen.halfWidth, screen.halfHeight, 0, screen.halfHeight)
            rightTop = SP2(3, 2, screen, screen.halfWidth, screen.halfHeight, screen.halfWidth)
            rightBottom = SP2(3, 2, screen, screen.halfWidth, screen.halfHeight, screen.halfWidth, screen.halfHeight)
        case _:
            gameControl = False
            print("Incorrect Menu Option")

    # Render games 
    while gameControl:
        match optionMenu:
            case -1:
                gameScreen3.run()
            case 0:
                gameScreen.run()
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

