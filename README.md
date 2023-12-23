# Product Description
Taking inspiration from Space Invaders, this game's main objectives include crafting a gaming atmosphere suitable for both human and Artificial Intelligence engagement. The project incorporated two reinforcement learning methods, A3C and DQN, to fulfill these goals.

# Build
To run the code, simply use the command "py main.py."
If you want to generate the executable file, execute "build.bat" in the console.

Note:
All the files necessary to run the game are in the Game folder, which is generated through build.bat

# Architecture
### player.py
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
