import random
import networkx as nx
from structures import Plant, Network, Solution, Config


def calculate_demand(graph):
    """Calculate and return the demand for power in a connected graph."""
    return sum((data["demand"] for node, data in graph.nodes(data=True)))


def network_from_graph(graph, config):
    """Create and return a valid network from a connected graph."""
    demand = calculate_demand(graph)
    plant = Plant(random.choice(graph.nodes()), demand, config.cost_of_power(demand))

    return Network(graph, plant)


def generate_random_solution(base_solution, config):
    network_list = []

    for base_network in base_solution.network_list:
        g = nx.Graph(base_network.graph)
        for i in range(0, random.randint(1, len(g.edges()))):
            g.remove_edges_from([random.choice(g.edges())])

        network_list.extend(
            network_from_graph(component, config) for component in nx.connected_component_subgraphs(g)
        )

    return Solution(network_list)


def prepare_initial_solution_set(base_solution, n, config):
    return {generate_random_solution(base_solution, config) for x in range(n)}


class NetworkChangeImpossibleError(Exception):
    pass


class NetworkDivisionImpossibleError(Exception):
    pass


class UnableToGenerateNeighbourError(Exception):
    pass


class SwitchOperation:
    def __init__(self, edge, from_net, to_net):
        self.edge = edge
        self.from_net = from_net
        self.to_net = to_net

    def perform(self, solution, config):
        to_g = nx.Graph(self.to_net.graph)
        from_g = nx.Graph(self.from_net.graph)

        to_g.add_edges_from([self.edge])
        if self.edge[0] in from_g:
            to_g.add_node(self.edge[0], from_g.node[self.edge[0]])
        else:
            to_g.add_node(self.edge[1], from_g.node[self.edge[1]])

        from_g.remove_node(self.edge[0] if self.edge[0] in from_g else self.edge[1])

        network_list = solution.network_list.copy()
        network_list.remove(self.from_net)
        network_list.remove(self.to_net)
        network_list.append(network_from_graph(to_g, config))
        if len(from_g):
            network_list.append(network_from_graph(from_g, config))

        return Solution(network_list)


def change_network(solution, base_solution, config):
    if len(solution.network_list) < 2:
        raise NetworkChangeImpossibleError

    possible_switches = [
        SwitchOperation(
            edge,
            from_net,
            to_net
        )

        for base_network in base_solution.network_list
        for from_net in solution.network_list
        for to_net in solution.network_list
        for edge in base_network.graph.edges_iter(data=True)

        if (from_net != to_net) and
        ((edge[0] in from_net.graph and edge[1] in to_net.graph) or
            (edge[0] in to_net.graph and edge[1] in from_net.graph))
    ]

    return random.choice(possible_switches).perform(solution, config)


def divide_network(solution, config):
    if all(len(network.graph) < 2 for network in solution.network_list):
        raise NetworkDivisionImpossibleError

    network = random.choice(solution.network_list)
    g = network.graph
    node_count = len(g.nodes())
    start_node = random.choice(g.nodes())
    partition = random.randint(0, node_count - 2)

    bfs_ordered_nodes = [e[1] for e in nx.bfs_edges(g, start_node)]

    g1 = g.subgraph([start_node] + bfs_ordered_nodes[:partition])
    network1 = network_from_graph(g1, config)

    g2 = g.subgraph(bfs_ordered_nodes[partition:])
    network2 = network_from_graph(g2, config)

    network_list = solution.network_list.copy()
    network_list.remove(network)
    network_list.extend([network1, network2])

    return Solution(network_list)


def generate_neighbour(solution, base_solution, config):
    if random.random() < config.change_network_chance:
        try:
            return change_network(solution, base_solution, config)
        except NetworkChangeImpossibleError:
            try:
                return divide_network(solution, config)
            except NetworkDivisionImpossibleError:
                raise UnableToGenerateNeighbourError
    else:
        try:
            return divide_network(solution, config)
        except NetworkDivisionImpossibleError:
            try:
                return change_network(solution, base_solution, config)
            except NetworkChangeImpossibleError:
                raise UnableToGenerateNeighbourError


def generate_neighbourhood(solution, base_solution, config):
    new_solution_set = set()

    while len(new_solution_set) < config.number_of_neighbours:
        try:
            new_solution_set.add(generate_neighbour(solution, base_solution, config))
        except UnableToGenerateNeighbourError:
            break

    return new_solution_set


def find_best_solution_in_neighbourhood(solution, base_solution, config):
    return choose_best_solution({solution} | generate_neighbourhood(solution, base_solution, config))


def stop_condition(best_solution, iterations, config):
    return iterations > config.number_of_max_iterations or best_solution.cost < config.minimal_cost


def choose_solutions_for_next_iteration(new_solution_set, config):
    prepared_solution_set = [x for x in new_solution_set if config.max_times_used > x.times_used]
    output_solution_set = set(sorted(prepared_solution_set, key=lambda solution: solution.cost)[:config.number_of_solutions])
    for x in output_solution_set:
        x.times_used += 1
    return output_solution_set


def prepare_next_iteration_solution_set(new_solution_set, base_solution, number_of_bees, config):
    selected_solution_set = choose_solutions_for_next_iteration(new_solution_set, config)
    while len(selected_solution_set) < number_of_bees:
        selected_solution_set.add(generate_random_solution(base_solution, config))
    return selected_solution_set, choose_best_solution(selected_solution_set)


def choose_best_solution(solution_set):
    return min(solution_set, key=lambda solution: solution.cost)


def generate_base_solution(initial_graph, config):
    network_list = [
        network_from_graph(component, config)
        for component in nx.connected_component_subgraphs(initial_graph)
    ]

    return Solution(network_list)


def algorithm(initial_graph, number_of_bees, config):
    base_solution = generate_base_solution(initial_graph, config)
    solution_set = prepare_initial_solution_set(base_solution, number_of_bees, config)
    best_solution = choose_best_solution(solution_set)
    iterations = 0
    while not stop_condition(best_solution, iterations, config):
        new_solution_set = {find_best_solution_in_neighbourhood(solution, base_solution, config) for solution in solution_set}
        solution_set, current_best_solution = prepare_next_iteration_solution_set(
                new_solution_set, base_solution, number_of_bees, config)
        best_solution = choose_best_solution({best_solution, current_best_solution})
        iterations += 1
    return best_solution


def algorithm_wrapper(graph, build_cost, config_dict):
    """Prepare arguments for the algorithm, run the algorithm and return the results."""
    def const_spline_interp(key_val_dict):
        def interpolant(x):
            min_gteq_key = min((k for k in key_val_dict if k >= x), default=None)
            return key_val_dict.get(min_gteq_key, None)
        return interpolant

    config_dict['cost_of_power'] = const_spline_interp(build_cost)

    config = Config(**config_dict)
    number_of_bees = config_dict['number_of_bees']

    return algorithm(graph, number_of_bees, config)
