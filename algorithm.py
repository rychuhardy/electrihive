def generate_random_solution(base_solution):
    pass


def prepare_initial_solution_set(base_solution, n):
    return {generate_random_solution(base_solution) for x in range(n)}


def generate_neighbourhood(solution):
    pass


def find_best_solution_in_neighbourhood(solution):
    return choose_best_solution(generate_neighbourhood(solution))


def stop_condition():
    pass


def choose_solutions_for_next_iteration(new_solution_set):
    pass


def prepare_next_iteration_solution_set(new_solution_set, base_solution, number_of_bees):
    selected_solution_set = choose_solutions_for_next_iteration(new_solution_set)
    while len(selected_solution_set) < number_of_bees:
        selected_solution_set.add(generate_random_solution(base_solution))
    return selected_solution_set


def count_solution_cost(solution):
    pass


def choose_best_solution(solution_set):
    return max(solution_set, key=lambda x: count_solution_cost(x))


def generate_base_solution(initial_graph):
    pass


def algorithm(initial_graph, number_of_bees):
    base_solution = generate_base_solution(initial_graph)
    solution_set = prepare_initial_solution_set(base_solution, number_of_bees)
    best_solution = None
    while not stop_condition():
        new_solution_set = {find_best_solution_in_neighbourhood(solution) for solution in solution_set}
        solution_set, current_best_solution = prepare_next_iteration_solution_set(new_solution_set, base_solution,
                                                                               number_of_bees)
        best_solution = choose_best_solution({best_solution, current_best_solution})
    return best_solution
