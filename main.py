import random
import timeit

# Constants
POPULATION_SIZE = 10000  # Number of individuals in each generation
GENES = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOP QRSTUVWXYZ 1234567890, .-;:_!"#%&/()=?@${[]}'''  # Valid genes
TARGET = "Data Warehouse and Business Intelligence!"  # Target string to be generated


class Individual:
    """Class representing an individual in the population."""

    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = self.calculate_fitness()

    @classmethod
    def mutated_genes(cls):
        """Create random genes for mutation."""
        return random.choice(GENES)

    @classmethod
    def create_gnome(cls):
        """Create a chromosome (string of genes)."""
        return [cls.mutated_genes() for _ in range(len(TARGET))]

    def mate(self, partner):
        """
        Perform mating and produce a new offspring.
        """
        child_chromosome = []

        for gp1, gp2 in zip(self.chromosome, partner.chromosome):
            prob = random.random()
            if prob < 0.45:  # Gene from parent 1
                child_chromosome.append(gp1)
            elif prob < 0.90:  # Gene from parent 2
                child_chromosome.append(gp2)
            else:  # Random mutation for diversity
                child_chromosome.append(self.mutated_genes())

        return Individual(child_chromosome)

    def calculate_fitness(self):
        """
        Calculate fitness score as the number of characters 
        that differ from the target string.
        """
        return sum(1 for gs, gt in zip(self.chromosome, TARGET) if gs != gt)


def main():
    global POPULATION_SIZE

    # Current generation
    generation = 1
    found = False
    population = []

    # Create initial population
    for _ in range(POPULATION_SIZE):
        gnome = Individual.create_gnome()
        population.append(Individual(gnome))

    while not found:
        # Sort the population by fitness score
        population = sorted(population, key=lambda x: x.fitness)

        # Check if the best individual has reached the target
        if population[0].fitness == 0:
            found = True
            break

        # Generate new generation
        new_generation = []

        # Elitism: Retain 10% of the fittest individuals
        s = int(0.1 * POPULATION_SIZE)
        new_generation.extend(population[:s])

        # Crossover: Generate offspring from 50% of the fittest individuals
        s = int(0.9 * POPULATION_SIZE)
        for _ in range(s):
            parent1 = random.choice(population[:50])
            parent2 = random.choice(population[:50])
            child = parent1.mate(parent2)
            new_generation.append(child)

        population = new_generation

        # Print the current generation details
        print("Generation: {}\tString: {}\tFitness: {}".format(
            generation,
            "".join(population[0].chromosome),
            population[0].fitness
        ))

        generation += 1

    # Final result
    print("Generation: {}\tString: {}\tFitness: {}".format(
        generation,
        "".join(population[0].chromosome),
        population[0].fitness
    ))


if __name__ == '__main__':
    start_time = timeit.default_timer()
    main()
    elapsed_time = timeit.default_timer() - start_time
    print(f"Elapsed Time: {elapsed_time:.2f} seconds")