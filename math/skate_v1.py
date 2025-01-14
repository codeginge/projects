import random
import os

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def roll_dice():
    # Generate a random number between 1 and 6
    dice_result = random.randint(1, 6)
    
    # Display the result and message
    return 7 - dice_result

def draw_cards(card_deck, num_cards):
    # Draw the specified number of cards
    drawn_cards = []
    for _ in range(num_cards):
        # Shuffle the deck if needed
        if not card_deck:
            print("Deck is empty!")
            break
        drawn_card = random.choice(card_deck)
        card_deck.remove(drawn_card)  # Remove the drawn card from the deck
        drawn_cards.append(drawn_card)
    return drawn_cards

def add_trick_to_deck(deck, trick, count, desired_difficulty):
    for _ in range(count):
        if trick["difficulty"]<=desired_difficulty:
            deck.append(trick)

def yes_no_input(prompt):
    while True:
        user_input = input(prompt + " (yes/no) ").strip().lower()
        if user_input == "yes" or user_input == "y":
            return True
        elif user_input == "no" or user_input == "n":
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def integer_input(prompt):
    while True:
        try:
            user_input = int(input(prompt))
            return user_input
        except ValueError:
            print("Invalid input. Please enter an integer.")

# Define the trick deck with counts and difficulties
stance_deck = {
    "Nollie": {"count": 2, "difficulty": 3},
    "Fakie": {"count": 3, "difficulty": 1},
    "Switch": {"count": 2, "difficulty": 3},
    "Regular": {"count": 3, "difficulty": 1},
}

flat_deck = {
    "Manual": {"count": 1, "difficulty": 1},
    "Nose Manual": {"count": 1, "difficulty": 2},
    "Ollie": {"count": 1, "difficulty": 1},
    "Boneless": {"count": 1, "difficulty": 0},
    "Kickflip": {"count": 1, "difficulty": 2},
    "Variable flip": {"count": 1, "difficulty": 2},
    "360 flip": {"count": 1, "difficulty": 3},

    "Heelflip": {"count": 1, "difficulty": 2},
    "Hardflip": {"count": 1, "difficulty": 3},
    "Inward Heelflip": {"count": 1, "difficulty": 3},
    "Laserflip": {"count": 1, "difficulty": 4},

    "Hospital Flip": {"count": 1, "difficulty": 4},
    "Dolphin Flip": {"count": 1, "difficulty": 4},
    "Impossible": {"count": 1, "difficulty": 3},

    "Pop Shove-it": {"count": 1, "difficulty": 1},
    "360 Pop Shove-it": {"count": 1, "difficulty": 2},
    "Shove-it": {"count": 1, "difficulty": 1},
    "360 Shove-it": {"count": 1, "difficulty": 2}
}

grind_stance_deck = {
    "": {"count": 5, "difficulty": 1},
    "Frontside": {"count": 5, "difficulty": 3},
    "Backside": {"count": 5, "difficulty": 3},
}

grind_deck = {
    "Boardslide": {"count": 2, "difficulty": 1},
    "Nosegrind": {"count": 1, "difficulty": 1},
    "5-0 Grind": {"count": 1, "difficulty": 1},
    "50-50 Grind": {"count": 2, "difficulty": 1},

    "Lipslide": {"count": 2, "difficulty": 2},
    "Tailslide": {"count": 1, "difficulty": 2},
    "Noseslide": {"count": 1, "difficulty": 2},
    
    "Smith Grind": {"count": 1, "difficulty": 3},
    "Feeble Grind": {"count": 1, "difficulty": 3},
    "Crooked Grind": {"count": 1, "difficulty": 3},
    "Salad Grind": {"count": 1, "difficulty": 3},
    "Bluntslide": {"count": 1, "difficulty": 3},
    "Nose Bluntslide": {"count": 1, "difficulty": 3},
}


score = 0
tricks = 5
tricks_left = tricks
clear_terminal()
flat_tricks = yes_no_input("Do you want to skate flat ground tricks?")
rail_tricks = yes_no_input("Do you want to skate rail ground tricks?")
set_difficulty = integer_input("Set Difficulty (1 - 4): ")

# Create the master deck
master_stance_list = []
for trick, data in stance_deck.items():
    add_trick_to_deck(master_stance_list, {"trick": trick, "difficulty": data["difficulty"]}, data["count"],set_difficulty)
master_flat_trick_list = []
for trick, data in flat_deck.items():
    add_trick_to_deck(master_flat_trick_list, {"trick": trick, "difficulty": data["difficulty"]}, data["count"],set_difficulty)
master_grind_stance_list = []
for trick, data in grind_stance_deck.items():
    add_trick_to_deck(master_grind_stance_list, {"trick": trick, "difficulty": data["difficulty"]}, data["count"],set_difficulty)
master_grind_trick_list = []
for trick, data in grind_deck.items():
    add_trick_to_deck(master_grind_trick_list, {"trick": trick, "difficulty": data["difficulty"]}, data["count"],set_difficulty)

for trick in range(tricks):
    clear_terminal()
    print("Current Score: ", score)
    tries = roll_dice()  # You missed the parentheses to call the function
    tries_left = tries
    drawn_cards = []
    drawn_cards.extend(draw_cards(master_stance_list, flat_tricks))
    drawn_cards.extend(draw_cards(master_flat_trick_list, flat_tricks))
    drawn_cards.extend(draw_cards(master_grind_stance_list, rail_tricks))
    drawn_cards.extend(draw_cards(master_grind_trick_list, rail_tricks))

    # Create trick
    trick_line = ""
    for card in drawn_cards:
        trick_line += card["trick"] + " "  # You are only storing the trick names, not dictionaries
    print("Current Trick: " + trick_line)
    
    # Calculate total difficulty
    total_difficulty = sum(card["difficulty"] for card in drawn_cards) 
    max_points = total_difficulty*100 - tries*10
    print("Points Avaliable: {}".format(max_points)) 
    print("Tricks Left: ", tricks_left)
    tricks_left -= 1
    tries = integer_input("How many tries to land? ")
    points = total_difficulty*100 - tries*10
    score += points
print("FINAL SCORE: {}".format(score))
