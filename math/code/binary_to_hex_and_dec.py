"""
this python function converts 8-bit binary numbers to hex and decimal.

Example usage: 
binary_to_hex_and_dec --binary_numbers "10001011,00000000,11111111,10101010"
"""

import argparse

def parse_args():
	parser = argparse.ArgumentParser(description="Generate hexidecimal and decimal numbers from the binary numbers provided.")
	parser.add_argument("--binary_numbers", required=True, help="8-bit binary number to convert to hex and decimal")
	
	return parser.parse_args()

def get_hex(binary_numbers):
	nums_hex = []
	for num in binary_numbers:	
		place_values = [8,4,2,1]
		hex_place_values = "0123456789ABCDEF"
		hexs = [str(num[0:4]),str(num[4:8])]
		hex_values = ""
		for h in hexs:
			hex_value_dec = 0
			for i in range(len(h)):
				hex_value_dec += int(h[i])*int(place_values[i])
			hex_value = hex_place_values[hex_value_dec]
			hex_values +=hex_value
		nums_hex.append(hex_values)
	return nums_hex

def get_dec(binary_numbers):
	nums_dec =[]
	for num in binary_numbers:
		place_values = [128,64,32,16,8,4,2,1]
		num_dec = 0
		for bit in range(len(num)):
			num_dec += int(num[bit])*place_values[bit]
		nums_dec.append(num_dec)
	return nums_dec

if __name__ == "__main__":
	args = parse_args()
	binary_numbers = args.binary_numbers.split(",")
	hex_numbers = get_hex(binary_numbers)
	dec_numbers = get_dec(binary_numbers)
	for i in range(len(binary_numbers)):
		print(f"{binary_numbers[i]} | {hex_numbers[i]} | {dec_numbers[i]} \n")
