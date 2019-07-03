import functools
import copy
import json
import math
import random
import time

from .utilities import get_coordinates, coordinates_to_distances

# points = 100
# capacity = 10
# individuals = 50
# replace = 25
# generations = 500


class Environment:

    def __init__(self, distances, capacity, individuals, replace, generations):
        self.quantity = len(distances)
        self.capacity = capacity
        self.distances = distances
        self.individuals = []
        self.replace = min(individuals, math.floor(replace / 2))
        for i in range(individuals):
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
        for j in range(generations):
            for i, old in enumerate(self.individuals):
                new = Individual(self, copy.deepcopy(old.path))
                new.mutate()
                a = new.evaluate()
                b = old.evaluate()
                if (a < b):
                    self.individuals[i] = new
            self.individuals = sorted(self.individuals, key=lambda individual: individual.evaluate())
            for i in range(0, self.replace):
                del self.individuals[len(self.individuals) - i - 1]
            for i in range(0, self.replace):
                self.individuals.append(Individual(self, copy.deepcopy(self.individuals[i].path)))


class Individual:

    def __init__(self, environment, path):
        self.environment = environment
        self.path = path
        self.score = None
        self.muted = True

    def evaluate(self):
        if self.muted:
            self.score = 0
            for tour in self.path:
                self.score += self.environment.distances[0][tour[0]]
                i = 0
                for i in range(1, len(tour)):
                    self.score += self.environment.distances[tour[i - 1]][tour[i]]
                a = tour[i]
                self.score += self.environment.distances[tour[i]][0]
            self.muted = False
        return self.score

    def mutate(self):
        self.muted = True
        j = random.randint(0, self.environment.quantity - 2)
        for i, tour in enumerate(self.path):
            j -= len(tour)
            if j < 0:
                break
        j = len(self.path[i]) + j

        if random.randint(0, 8) == 0:
            self.append(i, j)
            self.pop(i, j)
        else:
            m = random.randint(0, len(self.path) - 1)
            n = random.randint(0, self.environment.capacity - 1)
            if n < len(self.path[m]):
                self.swap(i, j, m, n)
            else:
                if m != i:
                    n = random.randint(0, len(self.path[m]))
                    self.insert(i, j, m, n)
                    self.pop(i, j)
                else:
                    n = random.randint(0, len(self.path[m]) - 1)
                    self.swap(i, j, m, n)

    def inject(self, other):
        self.muted = True
        m = random.randint(0, len(other.path) - 1)
        for value in other.path[m]:
            self.remove(value)
        self.path.append(copy.deepcopy(other.path[m]))

    def append(self, i, j):
        self.path.append([self.path[i][j]])

    def pop(self, i, j):
        del self.path[i][j]
        if len(self.path[i]) == 0:
            del self.path[i]

    def insert(self, i, j, m, n):
        self.path[m].insert(n, self.path[i][j])

    def swap(self, i, j, m, n):
        self.path[m][n], self.path[i][j] = self.path[i][j], self.path[m][n]

    def remove(self, value):
        for i, tour in enumerate(self.path):
            for j, point in enumerate(tour):
                if point == value:
                    self.pop(i, j)
                    return


def cli(points=100,
        capacity=10,
        individuals=50,
        replace=25,
        generations=500):

    coordinates = get_coordinates(points, 0, 2000)

    t1 = time.time_ns()

    environment = Environment(coordinates_to_distances(coordinates), capacity, individuals, replace, generations)

    t2 = time.time_ns()

    print('Best: ' + str(round(environment.individuals[0].evaluate(), 3)))
    print('Time: ' + str(round((t2 - t1) / 1000000000, 3)))


def run(points=100,
        capacity=10,
        individuals=50,
        replace=25,
        generations=500):

    coordinates = get_coordinates(points, 0, 2000)
    environment = Environment(coordinates_to_distances(coordinates), capacity, individuals, replace, generations)
    environment.individuals = sorted(environment.individuals, key=lambda individual: individual.evaluate())
    best = sorted(environment.individuals, key=lambda individual: individual.evaluate())[0]

    return json.dumps({
        "coordinates": coordinates,
        "path": best.path
    })
