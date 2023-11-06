# Product Description
Product owner description of the product here
# Architecture
### SpaceInvaders.py
At the start of the game will create an instance of either 
- human_observer(0)
- human_observer(1)
- DQN_observer()
- A3C_observer()

Each frame the game will call Update() on the observer
Commands are sent to the game using the Send_Command(command) function

### Observer.py
- Observer_Interface is an interface that will get data from the game and send input commands
- The subclasses of Observer_Interface will implement the Update() function
- human_observer will get input from the keyboard and send the commands to the game
- the AI observers will get game data and choose and send commands using their respective algorithms