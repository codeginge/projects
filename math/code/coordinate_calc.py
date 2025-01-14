# Author: Mr. Roberts 
# Date: 230302
# OVERVIEW: Given a specific domain and multiple functions, determine the range and coordinates
# INPUT: domain and function definitions 
# OUTPUT: range and coordinates for each funtion

domain = [-2,-1,0,1,2]

functions_01=[[0,-9, -10],
			[-0,-5,-15],
			[0,-6,-12],
			[0,-11,-13],
			[0,20,-14],
			[0,3,-27],
			[10,0,-4],
			[0,6,24],
			[0,10,10]]

functions_02=[[0,8, -2],
			[0,7,-3],
			[0,2,6],
			[0,45,-25],
			[1,0,2],
			[0,3,2],
			[0,2,-11],
			[0,4,-2],
			[1,0,3]]
print('\n\n\n\n\n* * * * * * 01 ALGP2 * * * * * * ')
for fun in functions_01:
	print('f(x)={}x^2 + {}x + {}'.format(fun[0],fun[1],fun[2]))
	coordinates=[]
	range_y = []
	for x in domain:
		output= fun[0]*(x*x) + fun[1]*x + fun[2]
		range_y.append(output)
		coordinates.append([x,output])
	print('Range = {}\nCoordinates = {}\n'.format(range_y,coordinates))

print('\n\n\n\n\n* * * * * * 02 ALGP2 * * * * * * ')
for fun in functions_02:
	print('f(x)={}x^2 + {}x + {}'.format(fun[0],fun[1],fun[2]))
	coordinates=[]
	range_y = []
	for x in domain:
		output= fun[0]*(x*x) + fun[1]*x + fun[2]
		range_y.append(output)
		coordinates.append([x,output])
	print('Range = {}\nCoordinates = {}\n'.format(range_y,coordinates))