from camera_game_engine import GameraGameEngine
from playing_scene import PlayingScene
from introduction_scene import IntroductionScene
from opponent_scene import OpponentScene
from win_scene import WinScene
from lose_scene import LoseScene

class RockPaperScissorsGame(GameraGameEngine):
	def setup(self):
		self.registerScene("INTRO", IntroductionScene(self))
		self.registerScene("OPPONENT", OpponentScene(self))
		self.registerScene("PLAYING", PlayingScene(self))
		self.registerScene("WIN", WinScene(self))
		self.registerScene("LOSE", LoseScene(self))
		self.initScene("INTRO")


RockPaperScissorsGame(0, 'Computer Vision Rock-Paper-Scissors')