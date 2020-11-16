from Route import Route
from RouteManager import RouteManager
import random

# TODO: Elitism? Where strongest chromosomes are kept through generations

def get_ordered_crossover():
    def ordered_crossover(mating_pool : list) -> list:
        offspring = []

        for i in range(0, len(mating_pool), 2):
            parent_1 = mating_pool[i]
            parent_2 = mating_pool[i + 1]

            #print("\nParents:")
            #print([s.id for s in parent_1.route_stops])
            #print([s.id for s in parent_2.route_stops])

            route_len = len(parent_1.route_stops)

            offspring_1 = Route(RouteManager.INSTANCE)
            offspring_2 = Route(RouteManager.INSTANCE)
            
            offspring_1.route_stops = [ None for s in parent_1.route_stops ]
            offspring_2.route_stops = [ None for s in parent_1.route_stops ]

            cutoff_1 = random.randrange(route_len + 1)
            cutoff_2 = random.randrange(route_len + 1)

            cut_start = min(cutoff_1, cutoff_2)
            cut_end = max(cutoff_1, cutoff_2)

            #print("Cuts:")
            #print(cut_start, cut_end)

            # Exchange the cutodd point
            for i in range(cut_start, cut_end):
                offspring_1.route_stops[i] = parent_1.route_stops[i]
                offspring_2.route_stops[i] = parent_2.route_stops[i]

            j_1 = cut_end % route_len
            j_2 = cut_end % route_len

            for i in range(route_len):
                i_conv = (cut_end + i) % route_len

                route_stop_1 = parent_1.route_stops[i_conv]
                route_stop_2 = parent_2.route_stops[i_conv]

                if not offspring_2.has_station(route_stop_1):
                    offspring_2.route_stops[j_2] = route_stop_1
                    j_2 = (j_2 + 1) % route_len

                if not offspring_1.has_station(route_stop_2):
                    offspring_1.route_stops[j_1] = route_stop_2
                    j_1 = (j_1 + 1) % route_len

            offspring_1.build_spf()
            offspring_2.build_spf()

            #print("Offspring:")
            #print([s.id for s in offspring_1.route_stops])
            #print([s.id for s in offspring_2.route_stops])

            offspring.append(offspring_1)
            offspring.append(offspring_2)

        return offspring
        
    return ordered_crossover
