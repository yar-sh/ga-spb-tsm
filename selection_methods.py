import random

# TODO: Elitism? Where strongest chromosomes are kept through generations

def get_tournament_selection(tournament_size : int):
    def tournament_selection(population : list) -> list:
        mating_pool = []
        for i in range(len(population)):
            tournament = random.sample(population, tournament_size)
            
            best_chromosome = tournament[0]
            for chromosome in tournament:
                if chromosome.get_fitness() > best_chromosome.get_fitness():
                    best_chromosome = chromosome

            mating_pool.append(best_chromosome)

        random.shuffle(mating_pool)
        return mating_pool
        
    return tournament_selection
