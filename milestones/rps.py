import random


# Will randomly pick an option between "Rock", "Paper", and "Scissors" and return the choice.
def get_computer_choice():
	return ['R', 'P', 'S'][random.randint(0,2)];


# Will ask the user for an input and return it
def get_user_choice():
	# getting user input
	choice = input("Input your choice [R:Rock P:Paper S:Scissors] >")

	# Exception handling
	if choice not in ['R', 'P', 'S']:
		print("Sorry! Not an option.")
		return get_user_choice();
	
	return choice


# choose a winner based on the classic rules of Rock-Paper-Scissors
def get_winner(computer_choice, user_choice):
	if computer_choice == user_choice: 
		return 'Draw';
	if (computer_choice == 'R' and user_choice == 'S') or (computer_choice == 'P' and user_choice == 'R') or (computer_choice == 'S' and user_choice == 'P'):
		return 'Computer';
	return 'User';


# running the Rock-Paper-Scissors game
def play(preset_user_choice=None):
	user_options = { 'R':'Rock', 'P':'Paper', 'S':'Scissors' };
	if preset_user_choice == None:
		user_choice = get_user_choice()
	else:
		user_choice = preset_user_choice
	computer_choice = get_computer_choice()

	print(f"User is {user_options[user_choice]}.");
	print(f"Computer is {user_options[computer_choice]}.");
	print(f"Winner is {get_winner(computer_choice, user_choice)}.")
	print()