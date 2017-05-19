import random
from collections import Set


def generate_random_solution(base_solution):
    pass


def prepare_initial_solution_set(base_solution, n):
    return {generate_random_solution(base_solution) for x in range(n)}


def change_network(solution):
    pass


def divide_network(solution):
    pass


def generate_neighbour(solution, config):
    if random.random() < config.change_network_chance:
        return change_network(solution)
    else:
        return divide_network(solution)


def generate_neighbourhood(solution, config):
    new_solution_set = Set()
    for x in range(config.number_of_neighbours):
        new_solution_set.add(generate_neighbour(solution))
    return new_solution_set


def find_best_solution_in_neighbourhood(solution, config):
    return choose_best_solution({solution} | generate_neighbourhood(solution, config))


def stop_condition(best_solution, iterations, config):
    return iterations > config.number_of_max_iterations or best_solution.cost < config.minimal_cost


def choose_solutions_for_next_iteration(new_solution_set, config):
    prepared_solution_set = [x for x in new_solution_set if config.max_times_used > x.times_used]
    output_solution_set = sorted(prepared_solution_set, key=lambda x:count_solution_cost(x))[:config.number_of_solutions]
    for x in output_solution_set:
        x.times_used += 1
    return output_solution_set


def prepare_next_iteration_solution_set(new_solution_set, base_solution, number_of_bees, config):
    selected_solution_set = choose_solutions_for_next_iteration(new_solution_set, config)
    while len(selected_solution_set) < number_of_bees:
        selected_solution_set.add(generate_random_solution(base_solution))
    return selected_solution_set


def count_solution_cost(solution):
    if solution.cost is None:
        cost = 0
        for network in solution.network_list:
            cost += network.plant.cost
            for node in network.graph:
                cost += node['cost']
        solution.cost = cost
    return solution.cost


def choose_best_solution(solution_set):
    return max(solution_set, key=lambda x: count_solution_cost(x))


def generate_base_solution(initial_graph):
    pass


def algorithm(initial_graph, number_of_bees, config):
    base_solution = generate_base_solution(initial_graph)
    solution_set = prepare_initial_solution_set(base_solution, number_of_bees)
    best_solution = None
    iterations=0
    while not stop_condition(best_solution, iterations, config):
        new_solution_set = {find_best_solution_in_neighbourhood(solution, config) for solution in solution_set}
        solution_set, current_best_solution = prepare_next_iteration_solution_set(new_solution_set, base_solution,
                                                                               number_of_bees, config)
        best_solution = choose_best_solution({best_solution, current_best_solution})
        iterations += 1
    return best_solution


def start_background_thread(Graph, BuildCost):
    pass