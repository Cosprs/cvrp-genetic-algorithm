import random

# This function generates a random coordinates array, number wide and with values between minimum and maximum
def get_coordinates(number, minimum, maximum):
	coordinates = [[None for i in range(2)] for i in range(number)]
	for i in range(0, number):
		coordinates[i][0] = random.randint(minimum, maximum)
		coordinates[i][1] = random.randint(minimum, maximum)
	return coordinates

# This function generates a random distances matrix, number wide and with values between minimum and maximum
def get_distances(number, minimum, maximum):
	distances = [[None for i in range(number)] for i in range(number)]
	for i in range(number):
		for j in range(i + 1, number):
			distances[i][j] = random.randint(minimum, maximum)
			distances[j][i] = random.randint(minimum, maximum)
	return distances

# This function returns a distances matric from a coordinates array parameter
def coordinates_to_distances(coordinates):
	length = len(coordinates)
	distances = [[None for i in range(length)] for i in range(length)]
	for i in range(length):
		for j in range(i + 1, length):
			distance = ((coordinates[i][0] - coordinates[j][0])**2 + (coordinates[i][1] - coordinates[j][1])**2)**(1/2)
			distances[i][j] = distance
			distances[j][i] = distance
	return distances
