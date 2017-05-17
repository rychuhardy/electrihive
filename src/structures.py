import networkx as nx


class Plant:
    def __init__(self, node, cost=0.0):
        self.node = node
        self.cost = cost


class Network:
    def __init__(self, graph=None, plant=None):
        if graph is None:
            graph = nx.Graph()
        self.graph = graph
        if plant is None:
            plant = Plant()
        self.plant = plant


class Solution:
    def __init__(self, network_list=None):
        if network_list is None:
            network_list = []
        self.network_list = network_list
        self.cost = None
        self.times_used=0
