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
import argparse

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

def plug_board(letter, pb_pairs, delay, dir):
	'''
	letter: input letter
	pb_pairs: pairs of letters connected on the plugboard
	delay: time for each tick
	dir: dirrection for the rotor
	returns: changed letter
	'''

	changed_letter = letter
	return changed_letter


def rotor(letter, num, pos, type, delay, dir):
	'''
	letter: input letter
	num: rotor number
	pos: rotor positions
	type: rotor type
	delay: time for each tick
	dir: dirrection for the rotor
	returns: changed letter
	'''

	changed_letter = letter
	return changed_letter


def reflector(letter, type, delay):
	'''
	letter: input letter
	type: reflector type
	delay: time for each tick
	returns: changed letter
	'''

	changed_letter = letter
	return changed_letter


def rotor_change(r_pos, r1, r2, r3, r4):
	'''
	r_pos: rotor position
	r1: rotor1 type
	r2: rotor2 type
	r3: rotor3 type
	r4: rotor4 type
	'''
	changed_r_pos = r_pos
	return(changed_r_pos)


def display_process(cp_text, pos, letter, debug):
	'''
	cp_text: cypher/plain text to modify
	pos: position of letter to modify
	letter: letter to change to
	'''
	if debug == True: print(letter)
	return (cp_text)


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

	# loop through each letter in text
	for i in range(len(cp_text)):
		letter = cp_text[i]
		# rotor change
		r_pos = rotor_change(r_pos, r1, r2, r3, r4)
		# take letter through plugboard
		letter = plug_board(letter, pb_pairs, delay, "forward")
		cp_text = display_process(cp_text, i, letter, debug)
		# take take letter through rotor 1
		letter = rotor(letter, 1, r_pos, r1, delay, "forward")
		cp_text = display_process(cp_text, i, letter, debug)
		# take take letter through rotor 2
		letter = rotor(letter, 2, r_pos, r2, delay, "forward")
		cp_text = display_process(cp_text, i, letter, debug)
		# take take letter through rotor 3
		letter = rotor(letter, 3, r_pos, r3, delay, "forward")
		cp_text = display_process(cp_text, i, letter, debug)
		# take take letter through rotor 4
		letter = rotor(letter, 4, r_pos, r4, delay, "forward")
		cp_text = display_process(cp_text, i, letter, debug)
		# take letter through reflector
		letter = reflector(letter, ref, delay)
		cp_text = display_process(cp_text, i, letter, debug)
		# take take letter through rotor 4
		letter = rotor(letter, 4, r_pos, r4, delay, "backward")
		cp_text = display_process(cp_text, i, letter, debug)
		# take take letter through rotor 3
		letter = rotor(letter, 3, r_pos, r3, delay, "backward")
		cp_text = display_process(cp_text, i, letter, debug)
		# take take letter through rotor 2
		letter = rotor(letter, 2, r_pos, r2, delay, "backward")
		cp_text = display_process(cp_text, i, letter, debug)
		# take take letter through rotor 1
		letter = rotor(letter, 1, r_pos, r1, delay, "backward")
		cp_text = display_process(cp_text, i, letter, debug)
		# take letter through plugboard
		letter = plug_board(letter, pb_pairs, delay, "backward")
		cp_text = display_process(cp_text, i, letter, debug)

	return(cp_text)


# run machine
print(run_enigma_sim())