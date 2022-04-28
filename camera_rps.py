import rps

try:
	while True:
		# for calling when getting user input from camera
		rps.play('R') 
		break
except KeyboardInterrupt:
	print("\n\nThank you for playing. See you soon!")
