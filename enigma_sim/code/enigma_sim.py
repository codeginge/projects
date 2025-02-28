'''
this code simulates the engigma machine and its series of encryptions. the code will 
visualize the text as each encryption/decryption takes place. just like the real machine, 
you put in either plain text or cypher text and if the machine is set correctly your 
message will be encoded or decoded just like it was back in WWII. 

the visual will be that of the full plain or cypher text and letter by letter it will cycle through
and encrypt/decrypt until each letter has be put through the enigma.

EXAMPLE USAGE:
# build env
python3 -m venv myenv_enigma
source myenv_enigma/bin/activate 
pip install

# run with variables
python3 ./enigma.py "<input_text>" "<plugboard_pairs>" "<reflector_type>" "<rotor_positions>" 
			"<rotor1_#>" "<rotor2_#>" "<rotor3_#>" "<rotor4_#>" "<encrypt_decrypt_speed>" "<--debug flag>"

# run EXAMPLES
python3 ./enigma_sim.py "decrypt this" "AH JS KL" "A" "SDHJ" "ETW" "IC" "IIC" "IIIC" 10
python3 ./enigma_sim.py "decrypt this" "AH JS KL" "A" "SDHJ" "ETW" "IC" "IIC" "IIIC" 10 --debug


'''

# imports
import argparse, time

# functions
def arg_inputs():
	parser = argparse.ArgumentParser(description="Enigma Machine Command Parser")

	parser.add_argument("input_text", type=str)
	parser.add_argument("plugboard_pairs", type=str)
	parser.add_argument("reflector", type=str)
	parser.add_argument("rotor_positions", type=str)
	parser.add_argument("rotor1", type=str)
	parser.add_argument("rotor2", type=str)
	parser.add_argument("rotor3", type=str)
	parser.add_argument("rotor4", type=str)
	parser.add_argument("delay", type=float)
	parser.add_argument("--debug", action="store_true", help="Enable debug mode")

	return parser.parse_args()

def plug_board(letter, pb_pairs_str, delay):
    '''
    letter: input letter (character to be swapped)
    pb_pairs_str: string of 10 pairs of letters connected on the plugboard, e.g. 'AFBDCEGT'
    delay: time for each tick (not used directly in this example, but could be for simulation)
    
    returns: changed letter (the letter after it has passed through the plugboard)
    '''
    
    # Convert the letter to uppercase (Enigma uses uppercase letters)
    letter = letter.upper()
    
    # Create a dictionary to map the plugboard pairs from the string
    plugboard_map = {}
    for i in range(0, len(pb_pairs_str), 2):
        plugboard_map[pb_pairs_str[i]] = pb_pairs_str[i + 1]
        plugboard_map[pb_pairs_str[i + 1]] = pb_pairs_str[i]
    
    # If the letter is in the plugboard map, swap it with its pair
    if letter in plugboard_map:
        changed_letter = plugboard_map[letter]
    else:
        # If no swap is needed, return the letter as is
        changed_letter = letter

    # Add a small delay for simulation purposes (optional)
    time.sleep(delay)

    return changed_letter


def rotor(letter, num, pos, type, delay, dir, bypass):
    '''
    letter: input letter (e.g., 'A')
    num: rotor number (1 for rotor 1, 2 for rotor 2, etc.)
    pos: rotor positions (e.g., 'ADFG' for rotor positions A=0, D=3, F=5, G=6)
    type: rotor type (e.g., 'I', 'II', etc.)
    delay: time for each tick (simulation delay)
    dir: direction for the rotor ('forward' or 'backward')
    bypass: whether to bypass rotor processing
    returns: changed letter after passing through the rotor wiring
    '''
    
    # If bypass is True, return the letter without processing
    if bypass:
        return letter

    # Define rotor wirings for the 4 rotors as string-to-string connections
    rotors = {
        'I': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',  # Rotor I
        'II': 'AJDKSIRUXBLHWTMCQGZNPYFVOE',  # Rotor II
        'III': 'BDFHJLCPRTXVZNYEIWGAKMUSQO',  # Rotor III
        'IV': 'ESOVPZJAYQUIRHXLNFTGKDCMWB',  # Rotor IV
    }
    
    # Define the alphabet for mapping (0-25 = A-Z)
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    # If the letter is not in the alphabet (e.g., a space or punctuation), return it unchanged
    if letter not in alphabet:
        return letter
    
    # Convert the position letter (e.g., 'A', 'D', 'F', 'G') to its corresponding index (0-25)
    rotor_positions = [alphabet.index(c) for c in pos]  # Convert 'A' -> 0, 'D' -> 3, etc.
    
    # Ensure the rotor type is valid (either 'I', 'II', 'III', or 'IV')
    if type not in rotors:
        print("Invalid rotor type.")
        return letter  # Return the original letter if the rotor type is invalid
    
    # Get the rotor wiring for the specified rotor type (I, II, III, IV)
    rotor_wiring = rotors[type]
    
    # Find the letter's position in the alphabet
    letter_pos = alphabet.index(letter)
    
    # Adjust the letter's position based on the rotor's current position
    rotor_pos = rotor_positions[num - 1]  # Get the position of the specified rotor
    letter_pos = (letter_pos - rotor_pos) % 26  # Shift the letter by the rotor's position
    
    if dir == 'forward':
        # In forward direction, use the rotor wiring to map the letter
        changed_letter = rotor_wiring[letter_pos]
    elif dir == 'backward':
        # In backward direction, we need to reverse the rotor mapping
        # Find the position of the letter in the rotor wiring and map it back
        changed_letter = alphabet[rotor_wiring.index(alphabet[letter_pos])]
    else:
        print("Invalid direction.")
        return letter  # Return the original letter if direction is invalid
    
    # Optional: Add a delay for each tick (simulating time between operations)
    import time
    time.sleep(delay)

    # Return the changed letter after passing through the rotor
    return changed_letter


def reflector(letter, type, delay):
    '''
    letter: input letter (A-Z)
    type: reflector type (either 'A' or 'B' in the Enigma machine)
    delay: time for each tick (simulated delay)
    returns: changed letter after passing through the reflector
    '''
    
    # Define the reflector mappings for 'A' and 'B'
    reflectors = {
        'A': 'EJMZALYXVBWFCRQUONTSPIKHGD',  # Reflector Type A
        'B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',  # Reflector Type B
    }

    # Check if the letter is valid (i.e., A-Z)
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    if letter not in alphabet:
        return letter  # Return the letter unchanged if it's not in the alphabet
    
    # Check if the reflector type is valid
    if type not in reflectors:
        print("Invalid reflector type.")
        return letter  # Return the original letter if the reflector type is invalid
    
    # Get the reflector wiring for the specified type
    reflector_wiring = reflectors[type]
    
    # Find the letter's position in the alphabet
    letter_pos = alphabet.index(letter)
    
    # Reflect the letter using the reflector wiring
    changed_letter = reflector_wiring[letter_pos]
    
    # Optional: Simulate a delay (e.g., for processing time)
    import time
    time.sleep(delay)

    # Return the changed letter after passing through the reflector
    return changed_letter


def rotor_change(r_pos, r1, r2, r3, r4):
    '''
    r_pos: rotor position (string, e.g., 'A', 'B', 'C')
    r1: rotor1 type (type of the first rotor, e.g., 'I', 'II', 'III', etc.)
    r2: rotor2 type (type of the second rotor)
    r3: rotor3 type (type of the third rotor)
    r4: rotor4 type (type of the fourth rotor)
    
    Returns: updated rotor positions after change.
    '''

    # Rotor movement rules (rotors move when a key is pressed)
    # The first rotor always moves one step forward on every key press.
    # The second rotor moves every time the first rotor completes a full cycle (26 steps).
    # The third rotor moves every time the second rotor completes a full cycle (26 steps).
    # The fourth rotor, if used, would follow similar rules.
    
    # Define rotor alphabets for shifting
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    # Convert current rotor positions to a list for easier modification
    rotor_positions = list(r_pos)

    # Move the first rotor by one step
    rotor_positions[0] = alphabet[(alphabet.index(rotor_positions[0]) + 1) % 26]
    
    # If the first rotor has completed one full cycle, move the second rotor
    if rotor_positions[0] == 'A':  # When the first rotor completes a cycle (from Z to A)
        rotor_positions[1] = alphabet[(alphabet.index(rotor_positions[1]) + 1) % 26]
    
    # If the second rotor has completed one full cycle, move the third rotor
    if rotor_positions[1] == 'A':  # When the second rotor completes a cycle
        rotor_positions[2] = alphabet[(alphabet.index(rotor_positions[2]) + 1) % 26]
    
    # If the third rotor has completed one full cycle, move the fourth rotor (if applicable)
    if rotor_positions[2] == 'A' and len(rotor_positions) > 3:  # For four rotors
        rotor_positions[3] = alphabet[(alphabet.index(rotor_positions[3]) + 1) % 26]
    
    # Convert rotor positions back to string format
    changed_r_pos = ''.join(rotor_positions)
    
    return changed_r_pos


def display_process(text, cp_text, r_pos, pos, letter, debug):
    '''
    text: original text
    cp_text: cipher/plain text to modify
    pos: position of letter to modify
    letter: letter to change to
    debug: whether to print debug information
    '''
    
    # Check if the position is valid (within the range of the text)
    if pos < 0 or pos >= len(cp_text):
        raise ValueError(f"Position {pos} is out of bounds for the text length.")

    # Convert the cp_text to a list since strings are immutable in Python
    cp_text_list = list(cp_text)
    
    # Modify the letter at the specified position
    cp_text_list[pos] = letter
    
    # Join the list back into a string
    modified_cp_text = ''.join(cp_text_list)
    
    # If debugging is enabled, print the details
    if debug:
        print(f"rotor positions: {r_pos} - modified_cp_text: {modified_cp_text}")

    return modified_cp_text


def run_enigma_sim():
	'''
	debug: print out error statments if True
	'''
	[text, pb_pairs, ref, r_pos, r1, r2, r3, r4, delay, debug] = vars(arg_inputs()).values()
	if debug == True: {
		print(f"Input: {text} \nPlugboard: {pb_pairs}\nReflector: {ref}\nRotors: {r_pos}\nR1: {r1}\nR2: {r2}\nR3: {r3}\nR4: {r4}\nSpeed: {delay}")
	}

	# create plain/cypher text variable
	cp_text = text
	bypass_rotor = True
	# loop through each letter in text
	for i in range(len(cp_text)):
		letter = cp_text[i]
		# rotor change
		r_pos = rotor_change(r_pos, r1, r2, r3, r4)
		# take letter through plugboard
		letter = plug_board(letter, pb_pairs, delay)
		cp_text = display_process(text, cp_text, r_pos, i, letter, debug)
		# take take letter through rotor 1
		letter = rotor(letter, 1, r_pos, r1, delay, "forward", bypass_rotor)
		cp_text = display_process(text, cp_text, r_pos, i, letter, debug)
		# take take letter through rotor 2
		letter = rotor(letter, 2, r_pos, r2, delay, "forward", bypass_rotor)
		cp_text = display_process(text, cp_text, r_pos, i, letter, debug)
		# take take letter through rotor 3
		letter = rotor(letter, 3, r_pos, r3, delay, "forward", bypass_rotor)
		cp_text = display_process(text, cp_text, r_pos, i, letter, debug)
		# take take letter through rotor 4
		letter = rotor(letter, 4, r_pos, r4, delay, "forward", bypass_rotor)
		cp_text = display_process(text, cp_text, r_pos, i, letter, debug)
		# take letter through reflector
		letter = reflector(letter, ref, delay)
		cp_text = display_process(text, cp_text, r_pos, i, letter, debug)
		# take take letter through rotor 4
		letter = rotor(letter, 4, r_pos, r4, delay, "backward", bypass_rotor)
		cp_text = display_process(text, cp_text, r_pos, i, letter, debug)
		# take take letter through rotor 3
		letter = rotor(letter, 3, r_pos, r3, delay, "backward", bypass_rotor)
		cp_text = display_process(text, cp_text, r_pos, i, letter, debug)
		# take take letter through rotor 2
		letter = rotor(letter, 2, r_pos, r2, delay, "backward", bypass_rotor)
		cp_text = display_process(text, cp_text, r_pos, i, letter, debug)
		# take take letter through rotor 1
		letter = rotor(letter, 1, r_pos, r1, delay, "backward", bypass_rotor)
		cp_text = display_process(text, cp_text, r_pos, i, letter, debug)
		# take letter through plugboard
		letter = plug_board(letter, pb_pairs, delay)
		cp_text = display_process(text, cp_text, r_pos, i, letter, debug)

	return(cp_text)


# run machine
print(run_enigma_sim())