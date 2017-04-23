import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import tkinter
import tkinter.filedialog
import networkx as nx
import sys


class MainWindow(tkinter.Frame):

    def __init__(self, root):

        tkinter.Frame.__init__(self, root)
        self.root = root

        # options for buttons
        button_opt = {'fill': tkinter.constants.BOTH, 'padx': 5, 'pady': 5}

        # define buttons
        tkinter.Button(self, text='Load graph from file',
                       command=self.openGraph).pack(**button_opt)
        tkinter.Button(self.root, text = 'root quit', command=self.quit)

        # define options for opening a file
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('.txt', '.gz', '.bz2')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'graph.txt'
        options['parent'] = root
        options['title'] = 'Select file containing graph'

        # Canvas
        figure = Figure(figsize=(5,4), dpi=100)
        self.subplot = figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(figure, master=root)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        self.toolbar = NavigationToolbar2TkAgg(self.canvas, root)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        self.Graph = nx.path_graph(0)
        # Display empty graph
        pos=nx.spring_layout(self.Graph)
        nx.draw(self.Graph, pos, ax=self.subplot)
        self.canvas.draw()
        

    def openGraph(self):
        filename = tkinter.filedialog.askopenfilename(**self.file_opt)

        self.Graph = nx.read_edgelist(path=filename, delimiter=":")
        pos=nx.spring_layout(self.Graph)
        nx.draw(self.Graph, pos, ax=self.subplot)
        self.canvas.draw()

    def quit(self):
        self.root.destroy()        


if __name__ == '__main__':
    root = tkinter.Tk()
    root.wm_title("Electrihive")
    MainWindow(root).pack()
    root.mainloop()
