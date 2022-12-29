from helpers import *
from RouteManager import RouteManager
from selection_methods import *
from crossover_methods import *
from mutation_methods import *


def new_generation(population: list, pool_size: int, selection_method, crossover_method, mutation_method) -> tuple:
    avg_wtt_start = 0
    avg_fitness_start = 0
    avg_wtt_end = 0
    avg_fitness_end = 0

    #
    # Starting stats
    #
    for r in population:
        avg_wtt_start += r.get_wtt()
        avg_fitness_start += r.get_fitness()

    avg_wtt_start /= len(population)
    avg_fitness_start /= len(population)

    print(f"\tStarting: avg_wtt={avg_wtt_start}, avg_fitness={avg_fitness_start}")

    #
    # Creating a mating pool by using a provided selection_method
    #
    mating_pool = selection_method(population, pool_size)

    #
    # Printing out the number of times each chromosome occurs in a mating pool
    #
    #mating_frequencies = {}
    #for r in mating_pool:
    #    if r.id not in mating_frequencies:
    #        mating_frequencies[r.id] = 0
    #    mating_frequencies[r.id] += 1
    #for w in sorted(mating_frequencies, key=mating_frequencies.get, reverse=True):
    #    print(w, mating_frequencies[w])

    #
    # Creating offspring from current generation by using a provided crossover_method
    #
    offspring = crossover_method(mating_pool)

    #
    # Apply mutation to the offspring by using a provided mutation_method
    #
    new_population = mutation_method(offspring)

    #
    # Ending stats
    #
    for r in new_population:
        avg_wtt_end += r.get_wtt()
        avg_fitness_end += r.get_fitness()

    avg_wtt_end /= len(population)
    avg_fitness_end /= len(population)

    print(f"\tEnding: avg_wtt={avg_wtt_end}, avg_fitness={avg_fitness_end}")

    # Returning the population of the new generation
    return new_population


def ga(generations: int, population_size: int, rm: RouteManager, selection_name: str, crossover_name: str, mutation_name: str, tournament_size:int, pool_size:int):
    population = [ rm.get_fixed_length_route() for i in range(population_size) ]

    # Initial population could take more than a day
    #print('Total random routes:', population_size)
    #print(population[0].get_wtt(), 'minutes')
    #return

    # Determine the correct selection method
    if selection_name == "tournament":
        selection_method = get_tournament_selection(tournament_size)
    elif selection_name == "random":
        selection_method = get_random_selection()
    elif selection_name == "truncation":
        selection_method = get_truncation_selection()
    elif selection_name == "proportion":
        selection_method = get_proportion_selection()
    else:
        raise Exception("Selection method not implemented")

    # Determine the correct crossover method
    if crossover_name == "ordered":
        crossover_method = get_ordered_crossover()
    elif crossover_name == "cycle":
        crossover_method = get_cycle_crossover()
    else:
        raise Exception("Crossover method not implemented")

    # Determine the correct mutation method
    if mutation_name == "inversion":
        mutation_method = get_inversion_mutation()
    elif mutation_name == "swap":
        mutation_method = get_swap_mutation()
    elif mutation_name == "simple_inversion":
        mutation_method = get_simple_inversion_mutation()
    elif mutation_name == "scramble":
        mutation_method = get_scramble_mutation()
    else:
        raise Exception("Mutation method not implemented")

    best_route = population[0]

    for i in range(generations):
        print(f"\nGeneration #{i+1}")
        population = new_generation(population, pool_size=pool_size, selection_method=selection_method, crossover_method=crossover_method, mutation_method=mutation_method)

        # Sort routes in the population by their fitness, higher fitness at the top
        ranked_population = sorted(population, key=lambda x: x.get_wtt())

        if ranked_population[0].get_wtt() < best_route.get_wtt():
            best_route = ranked_population[0]
            print(f"\t\t\t\t\t\t\t\t\t\t\tNew best: wtt={best_route.get_wtt()}, fitness={best_route.get_fitness()}")

    print(f"Final best wtt={best_route.get_wtt()}, fitness={best_route.get_fitness()}")
    for s in best_route.route_stops:
        print(s.flat_str())

    print([s.id for s in best_route.route_stops])


if __name__ == "__main__":
    stations = load_stations_from_file()
    rm = RouteManager(stations)

    ga(
        generations=150,
        population_size=1000,
        selection_name="tournament",
        crossover_name="ordered",
        mutation_name="simple_inversion",
        pool_size=1000, # How many chromosomes to select for the mating pool
        tournament_size=50, # Used ONLY in tournament selection method
        rm=rm,
    )
