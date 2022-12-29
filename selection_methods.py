import random

# TODO: Elitism? Where strongest chromosomes are kept through generations

def get_tournament_selection(tournament_size : int):
    def tournament_selection(population : list, pool_size: int) -> list:
        mating_pool = []
        for i in range(pool_size):
            tournament = random.sample(population, tournament_size)
            
            best_chromosome = tournament[0]
            for chromosome in tournament:
                if chromosome.get_fitness() > best_chromosome.get_fitness():
                    best_chromosome = chromosome

            mating_pool.append(best_chromosome)

        return mating_pool
        
    return tournament_selection


def get_random_selection():
    def random_selection(population: list, pool_size: int) -> list: # This is pretty much useless, since there is no "pressure" factor
        mating_pool = []

        for i in range(pool_size):
            mating_pool.append(random.choice(population))

        return mating_pool

    return random_selection


def get_truncation_selection():
    # THIS IS BROKEN!!!!
    # I just realized it does nothing - it returns the same population it gets as an input, just
    # ordered differently. God I am stupid.
    def truncation_selection(population: list, pool_size: int) -> list:
        mating_pool = []

        # Sort routes in the population by their fitness, higher fitness at the top
        ranked_population = sorted(population, key=lambda x: x.get_wtt())

        for i in range(pool_size):
            mating_pool.append(ranked_population[i])

        return mating_pool

    return truncation_selection


def get_proportion_selection():
    def proportion_selection(population: list, pool_size: int) -> list:
        mating_pool = []

        # Sort routes in the population by their fitness, higher fitness at the bottom
        ranked_population = sorted(population, key=lambda x: x.get_fitness())

        fitness_sum = 0
        for r in ranked_population:
            fitness_sum += r.get_fitness()

        cumilative_probability = 0
        cumilative_probabilities = []

        for r in ranked_population:
            cumilative_probability += (r.get_fitness() / fitness_sum)
            cumilative_probabilities.append(cumilative_probability)

        for i in range(pool_size):
            val = random.random()

            for j in range(len(cumilative_probabilities)):
                if val <= cumilative_probabilities[j]:
                    mating_pool.append(ranked_population[j])
                    break

        return mating_pool

    return proportion_selection
