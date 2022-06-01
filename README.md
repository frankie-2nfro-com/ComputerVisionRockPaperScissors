# ComputerVisionRockPaperScissors
Computer Vision Rock Paper Scissors

## Milestone 1
Train a vision classifier in the Teachable-Machine website with three set of images captured by the webcam namely Rock, Paper and Scissors. The generated model from the website has been downloaded and import to the code repository. And it will be loaded by the program and run to classify any Rock, Paper or Scissors are in the screen to trigger the program to react.

## Milestone 2
Environment setup for python to run with conda. Also create the requirements.txt to record all packages needed in the project. To generate the file by:

```python
pip list > requirements.txt
```

However, the environment setup in my MacBookPro which is using M1 CPU is failure to run the program. The keras and tensorflow library cannot be configured normally. I need to search in google to see if there is any way to solve the problem. 

## Milestone 3
Add code to implement the game by manual input. And for future camera playing, the play() function will have a parameter to set the user choice. If having that parameter input to the function, it will bypass getting user choice from the standard input. 

```python
play() #get user choice from standard input

play('R') #directly pass user choice to play the game
```

Details you can check manual_rps.py

## Milestone 4
Integrate the visual classifier to the game and make the game playable with webcam. It is quite straight forward to make everything work. However, to make the game more funny and improve the user experience, I need to change the base structure of the program to be similar with an game engine. So I create the GameEngine, Scene as the base class. 

### GameEngine ###
GameEngine is the heart of the structure. The make loop of the program is here and it dispatch all Video capture, Timeout event and Keyboard event to all other scenes. Scene is the screen of the game. Like this project, I create IntroScene, OpponentScene, PlayingScene, WinScene and LoseScene. 

### GameScene ###
GameScene will have a update() function which will be call for every heart beat of GameEngine. And for keyboard detected and timeout events will also be called when GameEngine triggered. 

### Classes of the RockPaperScissors ###
I create following classes for this project:

#### RockPaperScissorsGame ####
```python
class RockPaperScissorsGame(GameraGameEngine):
	def setup(self):
		self.registerScene("INTRO", IntroductionScene(self))
		self.registerScene("OPPONENT", OpponentScene(self))
		self.registerScene("PLAYING", PlayingScene(self))
		self.registerScene("WIN", WinScene(self))
		self.registerScene("LOSE", LoseScene(self))
		self.initScene("INTRO")
```

#### IntroScene ####
This scene is the cover of the game and just with a background and a continue message. User press 'c' button to jump to OpponentScene

#### OpponentScene ####
This scene is for player to select one opponent by the visual classifier. User press 'c' button to jump to PlayingScene with the selected opponent

#### PlayingScene ####
This scene is base on the game requirement to play rock-paper-scissors until either player or computer win three games firstly. If player win, it will jump to WinScene. Otherwise, it will jump to LoseScene

#### WinScene ####
This scene show winning background. User can press 'c' button to jump back to IntroScene.

#### LoseScene
This scene show lose background. User can press 'c' button to jump back to IntroScene.

## Conclusions
As the visual classifier is generated from Teachable-Machine. The accuracy is not good actually. So to improve the project, I think I should have a better classifier. Also, instead of the whole screen classifying rock, paper or scissors, it will be better to know where is coordinates in the captured picture. It will make more possibility of the game development 
