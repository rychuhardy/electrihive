import tkinter
import matplotlib

matplotlib.use('TkAgg')
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
        self.canvas.get_tk_widget().grid(row=0, rowspan=8)

        self.toolbar_helper_frame = tkinter.Frame(self)
        self.toolbar_helper_frame.grid(row=8, sticky='W')
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.toolbar_helper_frame)
        self.toolbar.update()

        self.Graph = nx.path_graph(0)
        # Display empty graph
        pos = nx.spring_layout(self.Graph)
        nx.draw(self.Graph, pos, ax=self.subplot)
        self.canvas.draw()


    def updateGraph(self, G):
        self.Graph = G
        pos = nx.spring_layout(self.Graph)
        nx.draw(self.Graph, pos, ax=self.subplot)
        self.canvas.draw()        
