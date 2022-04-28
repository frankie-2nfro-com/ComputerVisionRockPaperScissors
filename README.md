# ComputerVisionRockPaperScissors
Computer Vision Rock Paper Scissors

## Milestone 1
Train a vision classifier in the Teachable-Machine website with three set of images captured by the webcam namely Rock, Paper and Scissors. The generated model from the website has been downloaded and import to the code repository. And it will be loaded by the program and run to classify any Rock, Paper or Scissors are in the screen to trigger the program to react.

## Milestone 2
Environment setup for python run with conda. Also create the requirements.txt to record all packages needed in the project. To generate the file by:

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
