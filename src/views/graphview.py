import tkinter
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from tkinter import Grid
import numpy as np

# matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import networkx as nx


class GraphView(tkinter.PanedWindow):

    def __init__(self, root):
        self.root = root
        tkinter.PanedWindow.__init__(self, root, {'orient': tkinter.VERTICAL})

        figure = Figure(figsize=(10, 8), dpi=100)
        self.subplot = figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(figure, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=0, rowspan=8, sticky=tkinter.NSEW)

        self.toolbar_helper_frame = tkinter.Frame(self)
        self.toolbar_helper_frame.grid(row=1, sticky=tkinter.NSEW)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.toolbar_helper_frame)
        self.toolbar.update()

        Grid.rowconfigure(self, 0, weight=9)
        Grid.rowconfigure(self, 1, weight=1)
        Grid.columnconfigure(self, 0, weight=1)

        self.Graph = nx.path_graph(0)
        # Display empty graph
        pos = nx.spring_layout(self.Graph)
        nx.draw(self.Graph, pos, ax=self.subplot)
        self.canvas.draw()


    def updateGraph(self, G):
        self.Graph = G
        self.subplot.clear()
        self.pos = nx.spring_layout(self.Graph)
        edge_labels = nx.get_edge_attributes(self.Graph,  'cost')
        nx.draw_networkx_edge_labels(
            self.Graph, self.pos, edge_labels, ax=self.subplot, font_size=10, font_family='sans-serif',)
        nx.draw(self.Graph, self.pos, ax=self.subplot)
        self.canvas.draw()

    def addVertexLabels(self, G):
        self.Graph = G
        val_labels = nx.get_node_attributes(self.Graph, 'demand')
        nx.draw_networkx_labels(self.Graph, self.pos, ax=self.subplot,
                                font_size=10, font_family='sans-serif', labels=val_labels)
        self.canvas.draw()

    def setSolutionView(self, network_list):
        colors_count = len(network_list)
        cmap = plt.get_cmap('gnuplot')
        colors = [cmap(i) for i in np.linspace(0.25, 1, colors_count)]

        # edge_labels = nx.get_edge_attributes(self.Graph,  'cost')
        # vertex_labels = nx.get_node_attributes(self.Graph, 'demand')

        nodes_colors = self.Graph.nodes()[:]
        plant_nodes = []
        plant_nodes_colors = []

        for idx in range(colors_count):
            plant_nodes.append(network_list[idx].plant.node)
            plant_nodes_colors.append(colors[idx])            
            for node in network_list[idx].graph.nodes():
                nodes_colors[nodes_colors.index(node)] = colors[idx]

        nx.draw_networkx_nodes(self.Graph, pos=self.pos, ax=self.subplot, node_color=nodes_colors)
        # nx.draw_networkx_labels(network_list[idx].graph, pos, ax=self.subplot, font_size=10, font_family='sans-serif', labels=vertex_labels)

        
        nx.draw_networkx_nodes(self.Graph, pos=self.pos, ax=self.subplot, nodelist=plant_nodes, node_color=plant_nodes_colors, node_shape='s')


        self.canvas.draw()
