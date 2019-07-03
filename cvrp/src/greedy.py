import sys
import time

import utilities

def greedy(distances):

	# We extract the number of points from the matric dimension
	length = len(distances)

	results = '0\n'
	
	# List of points we have not visited yet
	points = list(range(0, length))
	
	# Point we are currently on
	current = 0
	
	# For each point
	for i in range(1, length):

		# We remove the current point from the remaining points list
		points.remove(current)

		# We look for the closest point
		bestv = sys.maxsize
		
		# We search the value and index of the closest remaining point
		for j in points:
			if distances[current][j] < bestv:
				bestj = j
				bestv = distances[current][j]

		results += str(bestj) + ': ' + str(bestv) + '\n'
		
		# We set the current point to the closest one
		current = bestj

	results += '0: ' + str(distances[current][0]) + '\n'

	# We print our path
	print(results)

#We ask for the number of cities
print('Number of cities ?')
number = eval(input())

# We generated random distances matrix (we prefer it to coordinates because it is faster, but less realistic)
distances = utilities.get_distances(number, 0, 1000)


t1 = time.time_ns()

# We execute the function
greedy(distances)

t2 = time.time_ns()

# We print the elapsed time of the function
print('Time: ' + str((t2 - t1) / 1000000) + 'ms')
