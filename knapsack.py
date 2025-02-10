import random
import timeit

import random
import sys
import operator


class Knapsack(object):

    # initialize variables and lists
    def __init__(self):

        self.C = 0
        self.weights = []
        self.profits = []
        self.opt = []
        self.parents = []
        self.newparents = []
        self.bests = []
        self.best_p = []
        self.iterated = 1
        self.population = 0
        self.total_value = 0
        self.counter = 0

        # increase max recursion for long stack
        # iMaxStackSize = 15000
        # sys.setrecursionlimit(iMaxStackSize)

    # create the initial population
    def initialize(self):

        self.parents = [[random.choice([0,1]) for _ in self.weights] for _ in range(self.population)]
        # print(self.parents)
        # for i in range(self.population):
        #     parent = []
        #     for k in range(0, 5):
        #         k = random.randint(0, 1)
        #         parent.append(k)
        #     self.parents.append(parent)

    # set the details of this problem
    def properties(self, C, num_items, population):  # Add `num_items`
        for i in range(num_items):  # Use `num_items` to define weights and profits
            self.weights.append(i + 1)  # Item weights
            self.profits.append(pow(i + 1, 2))  # Item profits
        self.C = C
        self.population = population
        self.initialize()

    # calculate the fitness function of each list (sack)
    def fitness(self, parent):

        sum_w = 0
        sum_p = 0
        print(parent)
        # get weights and profits
        for index, i in enumerate(parent):
            if i == 0:
                continue
            else:
                sum_w += self.weights[index]
                sum_p += self.profits[index]

        # if greater than the optimal return -1 or the number otherwise
        if sum_w > self.C:
            return 0
        else:
            return sum_p

    # run generations of GA
    def evaluation(self):

        # loop through parents and calculate fitness
        best_pop = self.population // 2
        for i in range(len(self.parents)):
            parent = self.parents[i]
            ft = self.fitness(parent)
            self.bests.append((ft, parent))
            # print("parent: ", parent, "fitness: ", ft)
        # sort the fitness list by fitness
        self.bests.sort(key=operator.itemgetter(0), reverse=True)
        self.best_p = self.bests[:best_pop]
        self.best_p = [x[1] for x in self.best_p]



    # mutate children after certain condition
    def mutation(self, ch):

        for i in range(len(ch)):
            k = random.uniform(0, 1)
            if k > 0.90:
                # if random float number greater that 0.5 flip 0 with 1 and vice versa
                if ch[i] == 1:
                    ch[i] = 0
                else:
                    ch[i] = 1
        return ch

    # crossover two parents to produce two children by miixing them under random ration each time
    def crossover(self, ch1, ch2):

        threshold = random.randint(1, len(ch1) - 1 )
        tmp1 = ch1[threshold:]
        tmp2 = ch2[threshold:]
        ch1 = ch1[:threshold]
        ch2 = ch2[:threshold]
        ch1.extend(tmp2)
        ch2.extend(tmp1)

        return ch1, ch2




    def run(self, max_generations=1000, fitness_threshold=None, elite_percentage=0.1):
        best_fitness = 0
        best_chromosome = None
        best_generation = -1

        for generation in range(max_generations):
            print(f"Generation: {generation + 1}")

            # Evaluate the population
            self.evaluation()

            # Prepare new parents for the next generation
            newparents = []
            pop = len(self.best_p)

            # Elitism: Retain top individuals
            elite_count = max(1, int(elite_percentage * pop))
            newparents.extend(self.best_p[:elite_count])  # Add elite individuals

            # Generate offspring through crossover and mutation
            for i in range(0, pop - 1):
                r1 = self.best_p[i]
                r2 = self.best_p[i + 1]
                nchild1, nchild2 = self.crossover(r1, r2)
                newparents.append(nchild1)
                newparents.append(nchild2)

            # Handle circular crossover for the last parent
            r1 = self.best_p[-1]
            r2 = self.best_p[0]
            nchild1, nchild2 = self.crossover(r1, r2)
            newparents.append(nchild1)
            newparents.append(nchild2)

            # Apply mutation to new children
            for i in range(len(newparents)):
                newparents[i] = self.mutation(newparents[i])

            # Check for optimal solution
            for child in newparents:
                if fitness_threshold and self.fitness(child) >= fitness_threshold:
                    print(f"Optimal solution found in generation {generation + 1}: {child}")
                    return

            # Track the best fitness
            current_best_fitness = max([self.fitness(parent) for parent in newparents])
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_chromosome = newparents[
                    [self.fitness(parent) for parent in newparents].index(current_best_fitness)]
                best_generation = generation + 1

            # Update population for the next generation
            self.parents = newparents
            self.bests = []
            self.best_p = []

        # If no optimal solution was found, report the best solution
        print(f"\nOptimal solution not found. Best fitness: {best_fitness}")
        print(f"Best chromosome: {best_chromosome}")
        print(f"Found in generation: {best_generation}")



# properties for this particular problem
# weights = [12, 7, 11, 8, 9]
# profits = [24, 13, 23, 15, 16]
# opt = [0, 1, 1, 1, 0]
C = 30
population = 50
num_items = 20

k = Knapsack()
k.properties( C,num_items, population) #weights, profits, opt,
k.run() #max_generations=100000

if __name__ == '__main__':
    start_time = timeit.default_timer()
    Knapsack()
    elapsed_time = timeit.default_timer() - start_time
    print(f"\nElapsed Time: {elapsed_time:.2f} seconds")
