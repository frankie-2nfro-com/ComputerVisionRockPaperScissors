from camera_game_engine import CameraGameEngine
from playing_scene import PlayingScene
from introduction_scene import IntroductionScene
from opponent_scene import OpponentScene
from win_scene import WinScene
from lose_scene import LoseScene
from sign_scene import SignScene
from prize_scene import PrizeScene

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