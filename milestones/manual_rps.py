import milestones.rps as rps

try:
	while True:
		# rps.play('R')  #for calling when getting user input from camera
		rps.play()
except KeyboardInterrupt:
	print("\n\nThank you for playing. See you soon!")
