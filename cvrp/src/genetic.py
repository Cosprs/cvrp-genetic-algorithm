import functools
import copy
import json
import math
import random
import time

from utilities import get_coordinates, coordinates_to_distances

# The environment is our algorithm
class Environment:

    # We execute the genetic algorithm in the constructor
    def __init__(self, distances, capacity, individuals, replace, generations):

        #We setup our variables
        self.quantity = len(distances)
        self.capacity = capacity
        self.distances = distances
        self.individuals = []
        
        # We check if the replacement parameter is not too large compared to the individuals number
        self.replace = min(math.floor(individuals / 2), replace)

        # We create the algorithm individuals
        for i in range(individuals):

            # The random path of the algorithm
            path = []
            points = list(range(1, self.quantity))

            # We fill the empty path with every points put in tours
            while len(points) != 0:

                # One tour of the path
                tour = []

                # We create a tour making sure it is not longer than the capacity and fill it with points
                for i in range(min(random.randint(1, self.capacity), len(points))):
                    j = random.randint(0, len(points) - 1)
                    tour.append(points[j])
                    del points[j]
                path.append(tour)

            #We create and add the new individual to our individuals list
            self.individuals.append(Individual(self, path))

        # For each generation we execute the algorithm
        for j in range(generations):

            # For each individual
            for i, old in enumerate(self.individuals):
                # We create a clone of the old individual
                new = Individual(self, copy.deepcopy(old.path))
                # We mutate the clone
                new.mutate()

                # We get the score of the old and new individuals
                a = new.evaluate()
                b = old.evaluate()

                # We keep only the best individual
                if (a < b):
                    self.individuals[i] = new

            # We get rid of our worst individuals to replace them with clones of our best ones
            # This showed to be the fastest way to converge, better than mixing individuals
            self.individuals = sorted(self.individuals, key=lambda individual: individual.evaluate())
            for i in range(0, self.replace):
                del self.individuals[len(self.individuals) - i - 1]
            for i in range(0, self.replace):
                self.individuals.append(Individual(self, copy.deepcopy(self.individuals[i].path)))


# An individual is a path competiting and mutating to become the best
class Individual:

    def __init__(self, environment, path):

        # We setup our variables
        self.environment = environment
        self.path = path

        # We store the score in order to not calculate it if not needed
        self.score = None
        self.muted = True


    # This is the fitness function
    def evaluate(self):

        # We calculate a new value only if needed
        if self.muted:

            # The score we calculate is the lengths of all the edges our path passes on
            self.score = 0
            
            # For each tour we add the lengths of the edges
            for tour in self.path:
                
                # We add the distance from the origin point to the first of our path
                self.score += self.environment.distances[0][tour[0]]

                # We initiate i in case there is only one point in our path
                i = 0

                # We add the lengths of the edges we pass on
                for i in range(1, len(tour)):
                    self.score += self.environment.distances[tour[i - 1]][tour[i]]

                # We add the distance between our last point and the origin one
                self.score += self.environment.distances[tour[i]][0]

            # We tell the algorithm the individual has not been muted since the last fitness calcul
            self.muted = False

        return self.score


    # THe mutation function
    def mutate(self):

        # We tell the algorithm the individual has been muted
        self.muted = True

        # We select a random point in our path
        j = random.randint(0, self.environment.quantity - 2)
        for i, tour in enumerate(self.path):
            j -= len(tour)
            if j < 0:
                break
        j = len(self.path[i]) + j

        # 1/8 chance of the mutation being popping one point out to create its own tour
        if random.randint(0, 7) == 0:
            self.append(i, j)
            self.pop(i, j)

        # Else 1/2 chance of popping one part of a path to add it to another
        elif random.randint(0, 7) < 4:

            # We select random tours
            i = random.randint(0, len(self.path) - 1)
            m = random.randint(0, len(self.path) - 2)
            if i <= m:
                m += 1

            # We exchange portions of tour between two tours, making sure to keep them smaller than the capacity
            qj = random.randint(1, len(self.path[i]))
            j = random.randint(0, len(self.path[i]) - qj)
            qn = random.randint(max(1, len(self.path[m]) - self.environment.capacity + qj), min(len(self.path[m]), self.environment.capacity - len(self.path[i]) + qj))
            n = random.randint(0, len(self.path[m]) - qn)
            self.swap2(i, j, qj, m, n, qn)

        # Else we take one point and either exchange it with another or add it to another tour
        else:

            # We select another random point
            m = random.randint(0, len(self.path) - 1)
            n = random.randint(0, self.environment.capacity - 1)

            # If we can swap two points
            if n < len(self.path[m]):
                self.swap(i, j, m, n)
            else:

                # Insert the first point side another
                if m != i:
                    n = random.randint(0, len(self.path[m]))
                    self.insert(i, j, m, n)
                    self.pop(i, j)

                # We swap two points
                else:
                    n = random.randint(0, len(self.path[m]) - 1)
                    self.swap(i, j, m, n)


    # This function adds the tour of another individual to this one, making sure to not pass multiple times to any point
    def inject(self, other):
        self.muted = True
        m = random.randint(0, len(other.path) - 1)
        for value in other.path[m]:
            self.remove(value)
        self.path.append(copy.deepcopy(other.path[m]))


    # This function adds a point to the path with its own path
    def append(self, i, j):
        self.path.append([self.path[i][j]])


    # This function removes a point from the path
    def pop(self, i, j):
        del self.path[i][j]
        if len(self.path[i]) == 0:
            del self.path[i]


    # This function inserts a point to a position
    def insert(self, i, j, m, n):
        self.path[m].insert(n, self.path[i][j])


    # This function swaps two points
    def swap(self, i, j, m, n):
        self.path[m][n], self.path[i][j] = self.path[i][j], self.path[m][n]


    # This function swaps parts of tours
    def swap2(self, i, j, qj, m, n, qn):
        tour1 = []
        tour2 = []
        for q in range(qj):
            tour1.append(self.path[i][j])
            del self.path[i][j]
        for q in range(qn):
            tour2.append(self.path[m][n])
            del self.path[m][n]
        for q in range(qj):
            self.path[m].insert(n + q, tour1[q])
        for q in range(qn):
            self.path[i].insert(j + q, tour2[q])


    # This function removes a point from the path
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

    print('Score: ' + str(round(environment.individuals[0].evaluate(), 3)))
    print('Path: ' + str(environment.individuals[0].path))
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

cli()
