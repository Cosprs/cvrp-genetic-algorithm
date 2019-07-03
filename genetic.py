import copy
import random

import utilities

cities = 20
capacity = 10
sample = 50
generations = 10000

class Environment:

	def __init__(self, distances, capacity):
		self.quantity = len(distances)
		self.capacity = capacity
		self.distances = distances
		self.individuals = []
		for i in range(sample):
			path = []
			points = list(range(1, self.quantity))
			while len(points) != 0:
				tour = []
				for i in range(min(random.randint(1, self.capacity), len(points))):
					j = random.randint(0, len(points) - 1)
					tour.append(points[j])
					del points[j]
				path.append(tour)
			self.individuals.append(Individual(self, path))
		for i in range(generations):
			for j, old in enumerate(self.individuals):
				new = Individual(self, copy.deepcopy(old.path))
				new.mutate()
				a = new.evaluate()
				b = old.evaluate()
				if (a < b):
					print('Generation: ' + str(i) + ' Individual: ' + str(j) + ' Improvement: ' + str(b) + ' -> ' + str(a))
					self.individuals[j] = new

class Individual:

	def __init__(self, environment, path):
		self.environment = environment
		self.path = path

	def evaluate(self):
		score = 0
		for tour in self.path:
			score += self.environment.distances[0][tour[0]]
			i = 0
			for i in range(1, len(tour)):
				score += self.environment.distances[tour[i - 1]][tour[i]]
			a = tour[i]
			score += self.environment.distances[tour[i]][0]
		return score

	def mutate(self):
		j = random.randint(0, self.environment.quantity - 2)
		for i in range(len(self.path)):
			j -= len(self.path[i])
			if j < 0:
				break
		j = len(self.path[i]) + j
		m = random.randint(-1, len(self.path) - 1)
		if m == -1:
			self.path.append([self.path[i][j]])
			del self.path[i][j]
			if len(self.path[i]) == 0:
				del self.path[i]
		else:
			n = random.randint(0, self.environment.capacity - 1)
			if n < len(self.path[m]):
				self.path[m][n], self.path[i][j] = self.path[i][j], self.path[m][n]
			else:
				if m != i:
					n = random.randint(0, len(self.path[m]))
					self.path[m].insert(n, self.path[i][j])
					del self.path[i][j]
					if len(self.path[i]) == 0:
						del self.path[i]
				else:
					n = random.randint(0, len(self.path[m]) - 1)
					self.path[m][n], self.path[i][j] = self.path[i][j], self.path[m][n]

coordinates = utilities.get_coordinates(cities, -1000, 1000)

environment = Environment(utilities.coordinates_to_distances(coordinates), capacity)

for individual in environment.individuals:
	print(str(individual.evaluate()) + ': ' + str(individual.path))
