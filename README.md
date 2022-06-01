# ComputerVisionRockPaperScissors
This github repository is storing the project development files of the Computer Vision Rock Paper Scissors game of AiCore course. And this README is for answering some questions of the project, description and some highlight infomation for the project milestones. 

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

Details you can check [manual_rps.py](https://github.com/frankie-2nfro-com/ComputerVisionRockPaperScissors/blob/main/manual_rps.py)

## Milestone 4
Integrate the visual classifier to the game and make the game playable with webcam. It is quite straight forward to make everything work. However, to make the game more funny and improve the user experience, I need to change the base structure of the program to be similar with an game engine. So I create the GameEngine, Scene as the base class. 

### GameEngine ###
GameEngine is the heart of the structure. The main loop of the program is here and it dispatchs all Video capture, Timeout event and Keyboard event to all other scenes. Scene is the screen of the game. Like this project, I create IntroScene, OpponentScene, PlayingScene, WinScene and LoseScene. 

### GameScene ###
GameScene will have a update() function which will be call for every heart beat of GameEngine. The heart beat just like the execution cycle for every screen captured by the game engine. It includes detecting player's rock, paper and scissors, game logic, screen drawing. And for keyboard detection and timeout events will also be called when GameEngine triggered. 

Game engine update function is called in the main loop after webcam capturing a screen, it will call the update() of the active scene as follows:
```python
def update(self):
	if self.currentScene != None:
		# scene will overload update() for preparing elements 
		self.scene[self.currentScene].update();
```

### Classes of the RockPaperScissors ###
I also create following classes for this project:

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
As the visual classifier is generated from Teachable-Machine. The accuracy is not good actually. So to improve the project, I think I should have a better classifier. Also, instead of the whole screen classifying rock, paper or scissors for each screen captured, it will be better to detect the hand first. Comparing directly call the classifier for every webcam screen. I think detecting hand would be faster a lot. Only with hand detected and pass the picture to the classifier would increase the frame per second rate to the game. Also it will make more possibility for further enhancement. 

This is the my first project in AiCore. I am happy with the process and let me know the missing parts of my previous developments. 

## Add-on
Finally I find a hand detection model in MediaPipe. And it will return the different points of the hand with location. It preforms well. But it is not able to run with Teachable-Machine as the tensorflow version for both model collapsed. So I use MediaPipe instead. Using the points of hand as the data to train a model to identify hand gesture is also easy. So I make this new model to classify hand gesture. 

After improving the hand detection, I added some scenes to make the game more funny.

```python
class RockPaperScissorsGame(CameraGameEngine):
	def setup(self):
		self.registerScene("INTRO", IntroductionScene(self))
		self.registerScene("OPPONENT", OpponentScene(self))
		self.registerScene("PLAYING", PlayingScene(self))
		self.registerScene("WIN", WinScene(self))
		self.registerScene("LOSE", LoseScene(self))
		self.registerScene("SIGN", SignScene(self))
		self.registerScene("PRIZE", PrizeScene(self))
		self.initScene("INTRO")

if __name__ == '__main__':
	RockPaperScissorsGame('Computer Vision Game: Rock-Paper-Scissors')
```
