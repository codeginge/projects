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


def generate_keys(date, days, book):
	'''
	this function takes a date and a book and generates 26 rotors the words in the book and generates a csv 
	keysheet with rotor ring settings, plug board pairs, and 10 starting positions. This key sheet is for a 
	machine that removes some weaknesses of the enigma machine. the key sheet will use from 10 to 26 rotors
	and the key sheet will be fully dertermined by the book and date variables. If you put in the same book
	and date the key sheet will be the same.

	inputs: 
	date - DDMMYYYY format
	days - number of days after date to be valid for up to 30 days
	book - full text of book enough for generating 26 sets of rotors

	outputs:
	keysheet json
	{
		"plugboard_pairs": [
			"AB CD EF GH IJ KL MN OP QR ST",
			"LA KS JD HF MG NZ BX VC PQ OW",
			... (26 pairs in total)
		],
		"rotors": [
			{
				"rotor_wiring":"PLMOKNIJBUHVYGCTFXRDZESWAQ",
				"rotor_turnover_notches":"AAA", (1 to 8 letters)
				"rotor_ring_setting":"A" (1 letter)
			},
			... (26 rotors in total)
		],
		"reflectors": [
			"AJBLCPDQERFSGTHUIVKWMXNYOZ",
			"EJMZALYXVBWFCRQUONTSPIKHGD",
			... (26 reflectors)
		]
		"key_sheet":[
		{
			"date":"DDMMYYYY", (next x days)
			"rotors":"QPLAMZOWKS" (10 to 15 rotors)
			"ring settings":"AAAAAAAAAA", (same number as the rotors)
			"plugboard pair": "A", (one of the 26)
			"rotor positions":"", (same number as the rotors)
			"reflector":"A" (one of the 26)
		},
		... (number of valid days)
		]
	}

	'''
	# turn book input to only uppercase letters
	book = ''.join(char.upper() for char in book if char.isalpha())

	# create 26 plugboard pairs
	# create 26 rotors
	# create 26 reflectors	


	return key_sheet


def renigma(key_sheet, message):
	'''
	run an upgraded version of the enigma reimagined to be theoretically impossible to break using brute force
	'''

	# get generated rotors, generated reflectors, daily list of rotors, rotor positions, ring settings, plug board settings, reflector_type

	# run through plugboard, rotors, reflector, reverse rotors, plugboard again
	for letter in message:
		rotor_change(r_pos, rotors)
		letter = plug_board_encryption(letter,pb_pairs)
		for r in rotors:
			letter = rotor_encryption(letter, rotor_encryption_set, position, ring_setting)
		letter = reflector_encryption(letter, reflector_encryption)
		for r in rotors[::-1]:
			letter = rotor_encryption(letter,rotor_encryption_set, position, ring_setting)

	return changed_message


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


def plug_board_encryption(letter, pb_pairs_str, delay, debug):
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


def rotor_encryption(letter, pos, rs, type, delay, dir, debug):
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

    # Define rotor wirings for the rotors
    rotors = {
        'I': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
        'II': 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
        'III': 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
        'IV': 'ESOVPZJAYQUIRHXLNFTGKDCMWB',
        'V': 'VZBRGITYUPSDNHLXAWMJQOFECK',
        'VI': 'JPGVOUMFYQBENHZRDKASXLICTW',
        'VII': 'NZJHGRCXMYSWBOUFAIVLPEKQDT',
        'VIII': 'FKQHTLXOCBJSPDZRAMEWNIUYGV'
    }

    # Define the alphabet for mapping (A-Z)
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # If the letter is not in the alphabet (e.g., space or punctuation), return it unchanged
    if letter not in alphabet:
        return letter

    # Ensure the rotor type is valid
    if type not in rotors:
        print("Invalid rotor type.")
        return letter  

    # Get the rotor wiring
    rotor_wiring = rotors[type]

    # Convert rotor position and ring setting to zero-indexed numbers
    rotor_pos = alphabet.index(pos.upper())  # Rotor position (0-25)
    ring_setting = rs - 1  # Ring setting offset (0-25)

    # Find the letter's position in the alphabet
    letter_pos = alphabet.index(letter)

    # Adjust the input index based on rotor position and ring setting
    effective_input = (letter_pos + rotor_pos - ring_setting) % 26  

    if dir == 'forward':
        # Pass through rotor wiring
        changed_letter = rotor_wiring[effective_input]
    elif dir == 'backward':
        # Find the position of the letter in the rotor wiring and map it back
        effective_input = rotor_wiring.index(alphabet[effective_input])
        changed_letter = alphabet[effective_input]
    else:
        print("Invalid direction.")
        return letter  

    # Adjust the output back after rotor processing
    final_pos = (alphabet.index(changed_letter) - rotor_pos + ring_setting) % 26
    changed_letter = alphabet[final_pos]

    # Optional delay for simulating rotor processing
    time.sleep(delay)

    # Debugging output
    if debug:
        print(f"Rotor Type: {type} Rotor Position: {pos} - Ring Setting: {rs} - Input: {letter} - Output: {changed_letter}")
        print(f"Effective Input: {effective_input} - Wiring: {rotor_wiring}")

    # Return the encrypted letter
    return changed_letter


def reflector_encryption(letter, type, delay, debug):
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

    if debug == False: 
    	print(modified_cp_text) 

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

		if not letter.isalpha(): continue

		# rotor change
		r_pos = rotor_change(r_pos, rotors)

		# debug output
		if debug: print(f"Rotors Position: {r_pos} - Rotor Types: {rotors} - Keyboard Input: {letter}")

		# take letter through plugboard
		letter = plug_board_encryption(letter, pb_pairs, delay, debug)
		cp_text = display_process(text, cp_text, r_pos, i, letter, debug)

		# take letter through rotors forward
		for r in range(len(rotors)):
			letter = rotor_encryption(letter, r_pos[::-1][r], int(rs[::-1][r]), rotors[::-1][r], delay, "forward", debug)
			cp_text = display_process(text, cp_text, r_pos, i, letter, debug)

		# take letter through reflector
		letter = reflector_encryption(letter, ref, delay, debug)
		cp_text = display_process(text, cp_text, r_pos, i, letter, debug)

		# take letter through rotors backward
		for r in range(len(rotors)):
			letter = rotor_encryption(letter, r_pos[r], int(rs[r]), rotors[r], delay, "backward", debug)
			cp_text = display_process(text, cp_text, r_pos, i, letter, debug)

		# take letter through plugboard
		letter = plug_board_encryption(letter, pb_pairs, delay, debug)
		cp_text = display_process(text, cp_text, r_pos, i, letter, debug)

		# insert debug line
		if debug: print("--------------------------------")

	return(cp_text)


# run machine
print(run_enigma_sim())