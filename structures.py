import networkx as nx


class Node:
    def __init__(self, node_id, cost=0.0):
        self.node_id = node_id
        self.cost = cost


class Plant:
    def __init__(self, node=None, cost=0.0):
        if node is None:
            node = Node(0)
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
