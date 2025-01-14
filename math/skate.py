import random
import os
import math

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def roll_dice():
    # Generate a random number between 1 and 6
    dice_result = random.randint(1, 6)
    
    # Display the result and message
    return 7 - dice_result

def draw_cards(card_deck, num_tricks):
    # Draw the specified number of tricks from the deck 
    drawn_cards = []
    trick_cards_pulled = 0
    while (trick_cards_pulled < num_tricks):
        if not card_deck:
            print("Deck is empty!")
            break
        drawn_card = random.choice(card_deck)
        card_deck.remove(drawn_card)  # Remove the drawn card from the deck
        drawn_cards.append(drawn_card)
        if (drawn_card["type"] == "trick"):
            trick_cards_pulled += 1
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


def newline_after_x_words(text, x):
    words = text.split()
    new_text = ""
    for i, word in enumerate(words):
        new_text += word + " "
        if (i + 1) % x == 0:
            new_text += "\n"
    return new_text.strip()  # Remove trailing whitespace

# Define the trick deck with counts and difficulties
stance_deck = {
    "Nollie": {"count": 2, "difficulty": 3, "type" : "modifier",
        "description":"Ride forwards with feet in your non-normal stance"},
    "Fakie": {"count": 3, "difficulty": 1, "type" : "modifier",
        "description":"Ride backwards with feet in a normal stance"},
    "Switch": {"count": 2, "difficulty": 3, "type" : "modifier",
        "description":"Ride backwards with feet in your non-normal stance"},
}

manual_deck = {
    "Manual": {"count": 2, "difficulty": 1, "type" : "trick",
        "description":"Lift up the front truck and balance on the back truck"},
    "Nose Manual": {"count": 2, "difficulty": 1, "type" : "trick",
        "description":"Lift up the back truck and balance on the front truck"},
    "Casper": {"count": 1, "difficulty": 2, "type" : "trick",
        "description":"Flip the board upside down and ballanceon the nose or tail."},
}

flat_deck = {
    "Boneless": {"count": 2, "difficulty": 1, "type" : "trick",
        "description":"Remove the front foot from the skateboard, grab the skateboard with your hand, jump, and replace your foot before landing."},
    "Ollie": {"count": 3, "difficulty": 1, "type" : "trick",
        "description":"Leap into the air without using your hands."},
    "Pop Shove-it": {"count": 2, "difficulty": 1, "type" : "trick",
        "description":"Pop the tail of the skateboard down and simultaneously shove the board around 180 degrees along its axis."},
    "Shove-it": {"count": 2, "difficulty": 1, "type" : "trick",
        "description":"Shove the skateboard around 180 degrees along its axis without popping the tail."},
    "Old School Kickflip": {"count": 1, "difficulty": 1, "type" : "trick",
        "description":"Switch your feet to a ski stance and use them to flip the board while jumping"},
    "Rail Stall": {"count": 1, "difficulty": 1, "type" : "trick",
        "description":"Flip the board up so that you stand on the wheels (primo)."},
    "Rail Flip": {"count": 1, "difficulty": 1, "type" : "trick",
        "description":"Stand on the side of the board (primo) and use the back foot to flip the board with pressure"},

    "360 Pop Shove-it": {"count": 2, "difficulty": 2, "type" : "trick",
        "description":"A variation of the pop shove-it where the board completes a 360-degree rotation along its axis."},
    "360 Shove-it": {"count": 3, "difficulty": 2, "type" : "trick",
        "description":"A variation of the shove-it where the board completes a 360-degree rotation along its axis."},

    "Kickflip": {"count": 4, "difficulty": 2, "type" : "trick",
        "description":"Kick your toe off the skateboard deck with the front foot during ollie, causing the board to flip one full rotation."},
    "Variable flip": {"count": 3, "difficulty": 2, "type" : "trick",
        "description":"A kickflip with a backside pop shove-it."},
    "Variable heelflip": {"count": 3, "difficulty": 2, "type" : "trick",
        "description":"A heelflip combined with a frontside pop shuvit"},
    "Heelflip": {"count": 3, "difficulty": 2, "type" : "trick",
        "description":"Kick your heel off the skateboard deck with the front foot during ollie, causing the board to flip one full rotation. The opposite of a kickflip."},

    "360 flip": {"count": 3, "difficulty": 3, "type" : "trick",
        "description":"A combination of a 360-degree backside-pop shuvit and a kickflip"},
    "Hardflip": {"count": 3, "difficulty": 3, "type" : "trick",
        "description":"A hardflip combines a frontside pop shuvit with a kickflip"},
    "Inward Heelflip": {"count": 3, "difficulty": 3, "type" : "trick",
        "description":"A backside-pop shuvit (180 degree) combined with a heelflip"},

    "Laserflip": {"count": 3, "difficulty": 4, "type" : "trick",
        "description":"A frontside 360 shuvit is combined with a heelflip"},
    "Hospital Flip": {"count": 3, "difficulty": 4, "type" : "trick",
        "description":"Perform a kickflip but stalls the rotation of the board at the halfway point; the front foot then executes an upward flick that causes the board to rotate 180 degrees vertically."},
    "Dolphin Flip": {"count": 3, "difficulty": 4, "type" : "trick",
        "description":"Performed by pushing with the front foot directly off the nose of the board after an ollie, causing the board to rotate almost vertically 180 degrees towards the frontfoot between the rider's legs while flipping the board 180 degrees so it lands wheels down"},
    "Impossible": {"count": 3, "difficulty": 4, "type" : "trick",
        "description":"The board completes one rotation by rolling around the skater’s back foot. The board flip should be as vertical as possible."},
}

grind_stance_deck = {
    "Frontside": {"count": 2, "difficulty": 2, "type" : "modifier",
        "description":"A grinding stance where the rider approaches the rail or ledge with their front side facing it."},
    "Backside": {"count": 2, "difficulty": 2, "type" : "modifier",
        "description":"A grinding stance where the rider approaches the rail or ledge with their back side facing it."},
}

grind_deck = {
    "Boardslide": {"count": 3, "difficulty": 1, "type" : "trick",
        "description":"The skateboard front trucks clear the rail and the board slides along a rail with the underside of the skateboard."},
    "Nosegrind": {"count": 3, "difficulty": 1, "type" : "trick",
        "description":"Grind along a rail or ledge with the front truck of the skateboard."},
    "5-0 Grind": {"count": 3, "difficulty": 1, "type" : "trick",
        "description":"Grind along a rail or ledge with only the back truck of the skateboard."},
    "50-50 Grind": {"count": 3, "difficulty": 1, "type" : "trick",
        "description":"Grind along a rail or ledge with both trucks of the skateboard."},
    "Axle Stall": {"count": 2, "difficulty": 1, "type" : "trick",
        "description":"The board balances on the rail with the axle of the skateboard."},

    "Lipslide": {"count": 3, "difficulty": 2, "type" : "trick",
        "description":"A skateboarding trick where the rider slides along the edge of a rail or ledge with the underside of the skateboard facing upward."},
    "Tailslide": {"count": 3, "difficulty": 2, "type" : "trick",
        "description":"A skateboarding trick where the rider slides along the edge of a rail or ledge with the tail of the skateboard."},
    "Noseslide": {"count": 3, "difficulty": 2, "type" : "trick",
        "description":"A skateboarding trick where the rider slides along the edge of a rail or ledge with the nose of the skateboard."},

    "Bluntslide": {"count": 3, "difficulty": 3, "type" : "trick",
        "description":"A skateboarding trick where the rider slides along the edge of a rail or ledge with the tail of the skateboard."},
    "Nose Bluntslide": {"count": 3, "difficulty": 3, "type" : "trick",
        "description":"A skateboarding trick where the rider slides along the edge of a rail or ledge with the nose of the skateboard."},

    "Smith Grind": {"count": 3, "difficulty": 3, "type" : "trick",
        "description":"A skateboarding trick where the rider grinds along the edge of a rail or ledge with the underside of the skateboard facing upward and the front truck locked on the obstacle."},
    "Feeble Grind": {"count": 3, "difficulty": 3, "type" : "trick",
        "description":"A skateboarding trick where the rider grinds along the edge of a rail or ledge with the underside of the skateboard facing upward and the back truck locked on the obstacle."},
    "Crooked Grind": {"count": 3, "difficulty": 3, "type" : "trick",
        "description":"A skateboarding trick where the rider grinds along the edge of a rail or ledge with the underside of the skateboard facing upward and the middle of the board locked on the obstacle."},
    "Salad Grind": {"count": 3, "difficulty": 3, "type" : "trick",
        "description":"A skateboarding trick where the rider grinds along the edge of a rail or ledge with the underside of the skateboard facing upward and the front foot hanging off the nose of the board."},

}

score = []
clear_terminal()

# Ask user for input
players = integer_input("How many players: ")
for player in range(players):
        score.append(0)
game_type = integer_input("Do you want to skate (1) flat ground, (2) rail, or (3) both? ")
if game_type == 1: 
    flat_tricks = True
    rail_tricks = False
if game_type == 2: 
    flat_tricks = False
    rail_tricks = True
if game_type == 3: 
    flat_tricks = True
    rail_tricks = True
set_difficulty = integer_input("Set Difficulty (1 - 4): ")
#lines = integer_input("How many lines? (5 - 10): ")
lines = 5
#tricks_per_line = integer_input("How many tricks per line? (1 - 3): ")

lines_left = lines

# Create the master deck
master_deck = []
if flat_tricks:
    for trick, data in stance_deck.items():
        add_trick_to_deck(master_deck, {"trick": trick, "difficulty": data["difficulty"],"type":data["type"],"description":data["description"]}, data["count"],set_difficulty)
    for trick, data in manual_deck.items():
        add_trick_to_deck(master_deck, {"trick": trick, "difficulty": data["difficulty"],"type":data["type"],"description":data["description"]}, data["count"],set_difficulty)
    for trick, data in flat_deck.items():
        add_trick_to_deck(master_deck, {"trick": trick, "difficulty": data["difficulty"],"type":data["type"],"description":data["description"]}, data["count"],set_difficulty)
if rail_tricks:
    for trick, data in grind_stance_deck.items():
        add_trick_to_deck(master_deck, {"trick": trick, "difficulty": data["difficulty"],"type":data["type"],"description":data["description"]}, data["count"],set_difficulty)
    for trick, data in grind_deck.items():
        add_trick_to_deck(master_deck, {"trick": trick, "difficulty": data["difficulty"],"type":data["type"],"description":data["description"]}, data["count"],set_difficulty)

while (lines_left>0):

    tricks_per_line = random.randint(1, 3)
    
    # Create Trick

    reshuffle = True
    while reshuffle:
        drawn_cards = []
        for trick in range(4):        
            if trick == 0:
                drawn_cards.extend(draw_cards(master_deck, 1))
            if trick >0 and trick <3:
                drawcard = yes_no_input("Add a trick? ")
                if drawcard == True:
                    drawn_cards.extend(draw_cards(master_deck, 1))
                if drawcard == False:
                    reshuffle = False
                    break
            if trick == 3:
                reshuffle = yes_no_input("Re-Draw? ")
                if reshuffle == False:
                    break
            clear_terminal()
            for player in range(players):
                print("Player {}: {}".format(player+1, score[player]))
            trick_line = ""
            for card in drawn_cards:
                trick_line += card["trick"] + " "
            print("\nCurrent Trick: {}".format(trick_line))

            # Print trick description
            for card in drawn_cards:
                print("\n{} Description: \n{}".format(card["trick"],newline_after_x_words(card["description"],math.floor(os.get_terminal_size().columns/8))))
            # Calculate total difficulty
            total_difficulty = sum(card["difficulty"] for card in drawn_cards) 
            max_points = total_difficulty*100 - 1*10
            print("\nPoints Avaliable: {}".format(max_points)) 
            print("Trick Lines Left: {}".format(lines_left-1))

        if reshuffle:
            for trick in drawn_cards:
                add_trick_to_deck(master_deck, {"trick": trick["trick"], "difficulty": trick["difficulty"],"type": trick["type"],"description": trick["description"]}, 1,set_difficulty)

    for player in range(players):
        tries = integer_input("Player {} How many tries to land?: ".format(player+1))
        points = total_difficulty*100 - tries*10
        score[player] += points
    lines_left -= 1
print("\nFINAL SCORE:")
for player in range(players):
    print("Player {}: {}".format(player+1, score[player]))
