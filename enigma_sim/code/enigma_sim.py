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
python3 ./enigma.py "<rotors>" "<ring_setting>" "<plugboard_pairs>" "<reflector>" "<delay>" --debug "<rotor_positions>" "<input_text>"

# run example
python3 ./enigma_sim.py "I VII IV" "01 10 24" "AY BF CD EG HI JK LM NO PQ RS" "B" 0.01 --debug "ABC" "decrypt this"

'''

# imports
import argparse, time

# functions
def arg_inputs():
	parser = argparse.ArgumentParser(description="Enigma Machine Command Parser")

	parser.add_argument("rotors", type=str)
	parser.add_argument("ring_setting", type=str)
	parser.add_argument("plugboard_pairs", type=str)
	parser.add_argument("reflector", type=str)
	parser.add_argument("delay", type=float)
	parser.add_argument("--debug", action="store_true", help="Enable debug mode")
	parser.add_argument("rotor_positions", type=str)
	parser.add_argument("input_text", type=str)

	return parser.parse_args()


def plug_board(letter, pb_pairs_str, delay, debug):
    """
    letter: input letter (character to be swapped)
    pb_pairs_str: string of space-separated pairs of letters connected on the plugboard, e.g. 'AF BD CE GT'
    delay: time for each tick (not used directly in this example, but could be for simulation)
    
    returns: changed letter (the letter after it has passed through the plugboard)
    """
    
    # Convert the letter to uppercase (Enigma uses uppercase letters)
    letter = letter.upper()
    
    # Create a dictionary to map the plugboard pairs from the string
    plugboard_map = {}
    pairs = pb_pairs_str.split()  # Split the string by spaces to get pairs
    
    for pair in pairs:
        if len(pair) == 2:  # Ensure valid pairs
            plugboard_map[pair[0]] = pair[1]
            plugboard_map[pair[1]] = pair[0]
    
    # If the letter is in the plugboard map, swap it with its pair
    changed_letter = plugboard_map.get(letter, letter)

    # Add a small delay for simulation purposes (optional)
    time.sleep(delay)

    if debug: print(f"Plugboard Pairs: {pb_pairs_str} - Input: {letter} - Output: {changed_letter}")

    return changed_letter


def rotor(letter, pos, rs, type, delay, dir, debug):
    """
    letter: input letter (e.g., 'A')
    pos: rotor position (e.g., 'A' for 0, 'B' for 1, ..., 'Z' for 25)
    rs: ring setting number for rotor (e.g., 1, 20, 24)
    type: rotor type (e.g., 'I', 'II', etc.)
    delay: time for each tick (simulation delay)
    dir: direction for the rotor ('forward' or 'backward')
    debug: whether to output debug codes
    returns: changed letter after passing through the rotor wiring
    """

    # Define rotor wirings for the 4 rotors as string-to-string connections
    rotors = {
        'I': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',  # Rotor I
        'II': 'AJDKSIRUXBLHWTMCQGZNPYFVOE',  # Rotor II
        'III': 'BDFHJLCPRTXVZNYEIWGAKMUSQO',  # Rotor III
        'IV': 'ESOVPZJAYQUIRHXLNFTGKDCMWB',  # Rotor IV
        'V': 'VZBRGITYUPSDNHLXAWMJQOFECK',   # Rotor V
        'VI': 'JPGVOUMFYQBENHZRDKASXLICTW',  # Rotor VI
        'VII': 'NZJHGRCXMYSWBOUFAIVLPEKQDT', # Rotor VII
        'VIII': 'FKQHTLXOCBJSPDZRAMEWNIUYGV' # Rotor VIII
    }
    
    # Define the alphabet for mapping (A-Z)
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    # If the letter is not in the alphabet (e.g., a space or punctuation), return it unchanged
    if letter not in alphabet:
        return letter

    # Ensure the rotor type is valid
    if type not in rotors:
        print("Invalid rotor type.")
        return letter  # Return the original letter if the rotor type is invalid

    # Get the rotor wiring for the specified rotor type (I, II, III, IV)
    rotor_wiring = rotors[type]

    # Step wiring back by ring setting
    shift = (rs - 1) % 26
    rotor_wiring = rotor_wiring[-shift:] + rotor_wiring[:-shift]
    
    # Convert rotor position (e.g., 'A' → 0, 'B' → 1, ..., 'Z' → 25)
    rotor_pos = alphabet.index(pos.upper())
    
    # Find the letter's position in the alphabet
    letter_pos = alphabet.index(letter)

    # Adjust the letter's position based on the rotor's current position
    shifted_pos = (letter_pos + rotor_pos) % 26  # Shift forward for rotor offset

    if dir == 'forward':
        # Use rotor wiring to map the letter
        changed_letter = rotor_wiring[shifted_pos]
    elif dir == 'backward':
        # Find the position of the letter in the rotor wiring and map it back
        shifted_pos = rotor_wiring.index(alphabet[shifted_pos])
        changed_letter = alphabet[shifted_pos]
    else:
        print("Invalid direction.")
        return letter  # Return the original letter if direction is invalid

    # Adjust back for the rotor position shift
    final_pos = (alphabet.index(changed_letter) - rotor_pos) % 26
    changed_letter = alphabet[final_pos]

    # Optional: Add a delay for each tick (simulating time between operations)
    time.sleep(delay)

    # debug output
    if debug: 
    	print(f"Rotor Type: {type} Rotor Position: {pos} - Ring Setting: {rs} - Input: {letter} - Output: {changed_letter}")
    	print(f"Shift: {shift} - Wiring: {rotor_wiring}")

    # Return the changed letter after passing through the rotor
    return changed_letter


def reflector(letter, type, delay, debug):
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
        'C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL'
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
    time.sleep(delay)

    # debug output
    if debug: print(f"Reflector Type: {type} - Input: {letter} - Output: {changed_letter}")

    # Return the changed letter after passing through the reflector
    return changed_letter


def rotor_change(r_pos, rotors):
    '''
    r_pos: Current rotor positions (string, e.g., 'AAA', 'BCD')
    rotors: List of rotor types in order (right to left, e.g., ['I', 'II', 'III'])

    Returns: Updated rotor positions after one key press.
    '''

    # Define rotor turnover notches (where the next rotor steps)
    turnover_notches = {
        'I': 'Q',  
        'II': 'E',  
        'III': 'V',  
        'IV': 'J',  
        'V': 'Z',
        'VI': 'ZM',
        'VII': 'ZM',
        'VIII': 'ZM'
    }

    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    # Convert rotor positions to a list for easier modification and reverse rotor positions
    rotor_positions = list(r_pos)
    rotor_positions = rotor_positions[::-1]


    # **Step Rotor 1 (rightmost rotor) always**
    rotor_positions[0] = alphabet[(alphabet.index(rotor_positions[0]) + 1) % 26]

    # **Determine if middle rotor double-steps**
    double_step = False

    # **Check from right to left**
    for i in range(len(rotors) - 1):  # Stop before the last rotor
        current_rotor = rotors[i]
        next_rotor = rotors[i + 1]

        # Get turnover notches for the current rotor
        notches = turnover_notches.get(current_rotor, '')

        # Check if the rotor is at any of its notches
        if rotor_positions[i] in notches:
            # **Step the next rotor**
            rotor_positions[i + 1] = alphabet[(alphabet.index(rotor_positions[i + 1]) + 1) % 26]

            # **Check for double-stepping**
            if i == 1:  # If the middle rotor (2nd from right) steps due to turnover
                double_step = True  

    # **Apply double-stepping if needed**
    if double_step:
        rotor_positions[1] = alphabet[(alphabet.index(rotor_positions[1]) + 1) % 26]

    # reverse rotor positions
    rotor_positions = rotor_positions[::-1]

    return ''.join(rotor_positions)


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

    if debug == False: print(modified_cp_text) 

    return modified_cp_text


def run_enigma_sim():
	'''
	debug: print out error statments if True
	'''
	[rotors, rs, pb_pairs, ref, delay, debug, r_pos, text] = vars(arg_inputs()).values()
	if debug == True: {
		print(f"Input: {text} \nPlugboard: {pb_pairs}\nReflector: {ref}\nRotor Position: {r_pos}\nRotors: {rotors}\nRing Setting: {rs}\nSpeed: {delay}")
	}

	# create plain/cypher text variable
	cp_text = text
	rotors = rotors.split( )
	rs = rs.split( )

	# loop through each letter in text
	for i in range(len(cp_text)):
		letter = cp_text[i]

		if letter == " ": continue

		# rotor change
		r_pos = rotor_change(r_pos, rotors)

		# debug output
		if debug: print(f"Rotors Position: {r_pos} - Rotor Types: {rotors} - Keyboard Input: {letter}")

		# take letter through plugboard
		letter = plug_board(letter, pb_pairs, delay, debug)
		cp_text = display_process(text, cp_text, r_pos, i, letter, debug)

		# take letter through rotors forward
		for r in range(len(rotors)):
			letter = rotor(letter, r_pos[::-1][r], int(rs[::-1][r]), rotors[::-1][r], delay, "forward", debug)
			cp_text = display_process(text, cp_text, r_pos, i, letter, debug)

		# take letter through reflector
		letter = reflector(letter, ref, delay, debug)
		cp_text = display_process(text, cp_text, r_pos, i, letter, debug)

		# take letter through rotors backward
		for r in range(len(rotors)):
			letter = rotor(letter, r_pos[r], int(rs[r]), rotors[r], delay, "backward", debug)
			cp_text = display_process(text, cp_text, r_pos, i, letter, debug)

		# take letter through plugboard
		letter = plug_board(letter, pb_pairs, delay, debug)
		cp_text = display_process(text, cp_text, r_pos, i, letter, debug)

		# insert debug line
		if debug: print("--------------------------------")

	return(cp_text)


# run machine
print(run_enigma_sim())