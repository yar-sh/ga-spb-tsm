from Route import Route
from RouteManager import RouteManager
import random


def get_simple_inversion_mutation():
    def simple_inversion_mutation(offspring: list) -> list: # aka SIM
        mutated_offspring = []

        for o in offspring:
            route_len = len(o.route_stops)

            cutoff_1 = random.randrange(route_len + 1)
            cutoff_2 = random.randrange(route_len + 1)

            cut_start = min(cutoff_1, cutoff_2)
            cut_end = max(cutoff_1, cutoff_2)

            mutated_o = Route(RouteManager.INSTANCE)

            for i in range(cut_start):
                mutated_o.route_stops.append(o.route_stops[i])

            for i in range(cut_end - cut_start):
                mutated_o.route_stops.append(o.route_stops[cut_end - i - 1])

            for i in range(cut_end, route_len):
                mutated_o.route_stops.append(o.route_stops[i])

            mutated_o.build_spf()

            mutated_offspring.append(mutated_o)

        return mutated_offspring

    return simple_inversion_mutation


def get_swap_mutation():
    def swap_mutation(offspring: list) -> list: # aka EM
        mutated_offspring = []

        for o in offspring:
            route_len = len(o.route_stops)

            swap_pos_1 = random.randrange(route_len)
            swap_pos_2 = random.randrange(route_len)

            mutated_o = Route(RouteManager.INSTANCE)
            mutated_o.route_stops = [ s for s in o.route_stops]

            temp = mutated_o.route_stops[swap_pos_1]
            mutated_o.route_stops[swap_pos_1] = mutated_o.route_stops[swap_pos_2]
            mutated_o.route_stops[swap_pos_2] = temp 

            mutated_offspring.append(mutated_o)

        return mutated_offspring

    return swap_mutation


def get_inversion_mutation():
    def inversion_mutation(offspring: list) -> list: # aka IVM
        mutated_offspring = []

        for o in offspring:
            route_len = len(o.route_stops)

            cutoff_1 = random.randrange(route_len + 1)
            cutoff_2 = random.randrange(route_len + 1)

            cut_start = min(cutoff_1, cutoff_2)
            cut_end = max(cutoff_1, cutoff_2)

            cut_route = list(reversed(o.route_stops[cut_start:cut_end]))

            leftovers = o.route_stops[:cut_start] + o.route_stops[cut_end:]
            try:
                insert_at = random.randrange(len(leftovers))
            except:
                insert_at = 0

            mutated_o = Route(RouteManager.INSTANCE)
            mutated_o.route_stops = leftovers[:insert_at] + cut_route + leftovers[insert_at:]

            mutated_o.build_spf()

            mutated_offspring.append(mutated_o)

        return mutated_offspring

    return inversion_mutation
