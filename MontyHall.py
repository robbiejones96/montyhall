import random
import pdb

MIN_DOORS = 3
MAX_DOORS = 10

def input_is_valid(user_input, criteria_fn):
	"""Attempts to parse command line input to an integer and evaluate whether 
	it satisfies the given criteria

	Parameters
	----------
	user_input (str): input read from the command line
	critiera_fn (function): takes an integer input and returns a bool based on
							some critiera

	Returns (bool)
	-------
	True if the input was succesfully parsed to in an integer and satisfies the
	given criteria function, False otherwise
	"""
	try:
		numeric_input = int(user_input)
	except ValueError:
		return False
	return criteria_fn(numeric_input)

def get_user_input(init_msg, fail_msg, criteria_fn):
	"""Repeatedly asks the user for an integer input from the command line
	until the user provides one that satisfies the given criteria

	Parameters
	----------
	init_msg (str): initial message to display to the user to ask for input
	fail_msg (str): message to display if the user gives an invalid input. The
					string should have a placeholder for .format() to insert the
					invalid input.
	criteria_fn (function): takes an integer input and returns a bool based on
							some critiera

	Returns (int)
	-------
	integer specified by the user that satisfies the criteria
		
	"""
	user_input = input(init_msg + ": ")
	while not input_is_valid(user_input, criteria_fn):
		print(fail_msg.format(user_input))
		user_input = input(init_msg + ": ")

	return int(user_input)

def get_num_doors():
	"""Asks the user how many doors they want to play the game with.

	Returns (int)
	-------
	the number of doors the user wants to play with
	"""
	init_msg = "How many doors do you want to play with?"
	init_msg += " Must be >= {} and <= {}".format(MIN_DOORS, MAX_DOORS)
	fail_msg = "{} is not a valid number of doors!"
	critera = lambda num : num >= MIN_DOORS and num <= MAX_DOORS
	return get_user_input(init_msg, fail_msg, critera)

def initialize():
	"""Prints the welcome message and asks the user how many doors they want to
	play with.

	Returns (int)
	-------
	the number of doors the user wants to play with

	"""
	print("Welcome to Let's Make a Deal!")
	num_doors = get_num_doors()
	print("Behind exactly one of these doors is a brand new car!")
	print("Behind the other {} doors are smelly goats.".format(num_doors - 1))
	return num_doors

def get_door_choice(init_msg, door_critiera):
	"""Asks the user what door they would like to choose.

	Parameters
	----------
	init_msg (str): initial message to display to the user to ask for input
	door_criteria (function): takes an integer input and returns a bool if it is 
							  a valid door number

	Returns (int)
	-------
	the door number the user has chosen

	"""
	fail_msg = "{} is not a valid door number!"
	return get_user_input(init_msg, fail_msg, door_critiera)

def open_goat_doors(chosen_door, car_door, num_doors):
	"""Opens all but two of the doors, all of which will have goats behind them.
	The door the user has chosen will remain closed.

	Parameters
	----------
	chosen_door (int): the door that is the user's current choice
	car_door (int): the door hiding the car
	num_doors (int): number of doors present in the game

	Returns (int)
	-------
	number of the other door that remains closed (i.e., the one that is not the 
	user's currently chosen door)

	"""

	# host won't open the chosen door or the door with the car behind it
	invalid_doors = {chosen_door, car_door} 
	goat_doors = [i for i in range(1, num_doors + 1) if i not in invalid_doors]

	# if the user chose incorrectly, the car door must be the other closed door
	user_is_incorrect = chosen_door != car_door
	closed_door = car_door if user_is_incorrect else random.choice(goat_doors)

	# reveal the opened doors to the user
	door_output = "X" if closed_door == 1 or chosen_door == 1 else "G"
	for door_num in range(2, num_doors + 1):
		door_is_closed = door_num == closed_door or door_num == chosen_door
		door_output += "\t" + ("X" if door_is_closed else "G")
	print(door_output)

	return closed_door

def get_twist_message(num_doors):
	"""Returns grammatically correct string describing the "twist" of the game
	(namely that the host will reveal doors that have goats behind them).

	Parameters
	----------
	num_doors (int): number of doors present in the game

	Returns (str)
	-------
	string describing that the host will reveal some of the doors to the user

	"""
	message = "To add a twist, let me show you {} {} with {} behind {}."
	if num_doors - 2 == 1:
		return message.format(num_doors - 2, "door", "a goat", "it")
	else:
		return message.format(num_doors - 2, "doors", "goats", "them")
		
def show_final(chosen_door, car_door, num_doors):
	"""Opens all of the doors to the user and says whether they won or lost.

	Parameters
	----------
	chosen_door (int): the door that is the user's final choice
	car_door (int): the door hiding the car
	num_doors (int): the number of doors present in the game

	Returns (bool)
	-------
	True if the user won the car, False otherwise

	"""
	door_output = "C" if car_door == 1 else "G"
	for door_num in range(2, num_doors + 1):
		door_output += "\t" + ("C" if car_door == door_num else "G")
	print(door_output)
	if chosen_door == car_door:
		print("Congrats! This new car is all yours!")
		return True
	else:
		print("Unlucky for you! Have fun with your goat.")
		return False

def play_game(num_doors):
	"""Plays full game with the specified number of doors. The door hiding the
	car is randomly chosen.

	Parameters
	----------
	num_doors (int): number of doors to play with
	"""
	print("\t".join("X" for _ in range(num_doors))) # print closed doors
	car_door = random.randint(1, num_doors)

	# get first door choice from user
	message = "To begin, pick a door between 1 and {}".format(num_doors)
	door_criteria = lambda num : num >= 1 and num <= num_doors
	chosen_door = get_door_choice(message, door_criteria)
	print("Door {} is a great choice!".format(chosen_door))

	# reveal some of the incorrect doors to the user
	print(get_twist_message(num_doors))
	closed_door = open_goat_doors(chosen_door, car_door, num_doors)
	door1, door2 = min(chosen_door, closed_door), max(chosen_door, closed_door)
	print("The remaining doors are {} and {}".format(door1, door2))

	# ask the user to make their final choice
	door_criteria = lambda num : num == chosen_door or num == closed_door
	chosen_door = get_door_choice("Choose either of the doors: ", door_criteria)
	return show_final(chosen_door, car_door, num_doors)

def play_again():
	"""Asks the user if they would like to play again. User must specify "yes"
	or "y" for yes and "no" or "n" for no.

	Returns
	-------
	True if the user would like to play again, False otherwise

	"""
	valid_yes = {"yes", "y"}
	valid_no = {"no", "n"}
	answer = input("Do you want to play again? ").lower()
	while(answer not in valid_yes and answer not in valid_no):
		print("Sorry, didn't understand that.")
		answer = input("Do you want to play again? ").lower()
	return answer in valid_yes

def main():
	"""Repeatedly plays game with the user until requested to stop. Will then
	print out statistics for how well the user did.

	"""
	num_doors = initialize() # gets the number of doors to play with
	num_won = 0
	total_games = 0
	num_won += play_game(num_doors)
	total_games += 1
	while(play_again()):
		num_won += play_game(num_doors)
		total_games += 1
	percent_won = num_won / total_games * 100
	print("You won {} out of {} games ({}%)".format(num_won, total_games, percent_won))

if __name__ == "__main__":
	main()