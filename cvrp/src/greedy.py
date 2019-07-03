import sys
import time

import utilities

def greedy(distances):
	length = len(distances)
	results = '0\n'
	points = list(range(0, length))
	current = 0
	for i in range(1, length):
		points.remove(current)
		bestj = 0
		bestv = sys.maxsize
		for j in points:
			if distances[current][j] < bestv:
				bestj = j
				bestv = distances[current][j]
		results += str(bestj) + ': ' + str(bestv) + '\n'
		current = bestj
	results += '0: ' + str(distances[current][0]) + '\n'
	print(results)

number = eval(input())

distances = utilities.get_distances(number, 0, 1000)

print('START')

t1 = time.time_ns()

greedy(distances)

t2 = time.time_ns()

print('END')

print((t2 - t1) / 1000000)
