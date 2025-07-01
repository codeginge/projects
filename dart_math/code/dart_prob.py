import math

# the dart numbers as a list starting from 20 going CW 
dart_numbers = [20,1,18,4,13,6,10,15,2,17,3,19,7,16,8,11,14,9,12,5]


def staight_average (wedge_number,left_number,right_number):
	average_s = round((wedge_number + left_number + right_number)/3, 2)
	return average_s
	

def weighted_average (wedge_number,left_number,right_number):
	[wn_weight,wn_weight_tripple,ln_weight,ln_weight_tripple,rn_weight,rn_weight_tripple,] = [0.45, 0.05, 0.2, 0.05, 0.2, 0.05]
	wedge_av = wedge_number*wn_weight + 3*wedge_number*wn_weight_tripple
	left_number_av = left_number*ln_weight + 3*left_number*ln_weight_tripple
	right_number_av = right_number*rn_weight + 3*right_number*rn_weight_tripple
	average_w = round((wedge_av + left_number_av + right_number_av), 2)
	return average_w


# calculate averages and print out information
for wedge_number in range(1, 21):
	left_number = dart_numbers[(dart_numbers.index(wedge_number)-1) % 20]
	right_number = dart_numbers[(dart_numbers.index(wedge_number)+1) % 20]
	average_s = staight_average(wedge_number,left_number,right_number)
	average_w = weighted_average(wedge_number,left_number,right_number)
	print("number: {}	ln: {}	rn: {}	av_s: {}	av_w: {} ".format(wedge_number, left_number, right_number, average_s, average_w))
