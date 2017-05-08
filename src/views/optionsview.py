import tkinter
import tkinter.filedialog
import tkinter.messagebox

from os import path

from networkx import read_weighted_edgelist

class OptionsView(tkinter.PanedWindow):
    
    separator = ":"

    file_opts = {
        'defaultextension': '.txt',
        'filetypes': [('all files', '.*'), ('.txt', '.gz', '.bz2')],
        'initialdir': path.abspath(__file__),
        'title': 'Select file describing graph'
    }

    button_opts = {
        'padx': 20,
        'pady': 5,
        'sticky': 'W'
    }

    def __init__(self, root):
        self.root = root
        tkinter.PanedWindow.__init__(self, root, {'orient': tkinter.VERTICAL})

        self.graph_button = tkinter.Button(self, text='Edge list with cost', command=self.openGraphFile)
        self.graph_label = tkinter.Label(self, text='No file selected')
        self.vertices_button = tkinter.Button(self, text='Electricity needs for each vertex', command=self.openElectricityNeedsFile)
        self.vertices_label = tkinter.Label(self, text='No file selected')

        self.graph_button.grid(row=0, column=0, **self.button_opts)
        self.graph_label.grid(row=0, column=1, **self.button_opts)    
        self.vertices_button.grid(row=1, column=0, **self.button_opts)
        self.vertices_label.grid(row=1, column=1, **self.button_opts)

        self.nodes = None


    def openGraphFile(self):
        filename = tkinter.filedialog.askopenfilename(**self.file_opts)
        Graph = read_weighted_edgelist(path=filename, delimiter=self.separator)
        graphnodes = Graph.nodes()
        graphnodes.sort()
        if self.nodes == None:
            self.nodes = graphnodes
        elif self.nodes == graphnodes:    
            self.graph_label.config({'text': path.split(filename)[-1]})
            self.root.graphview.updateGraph(Graph)
        else:
            tkinter.messagebox.showerror(title="Node values mismatch", message="Either the number of vertices or the names of vertices differ in selected files")              


    def openElectricityNeedsFile(self):
        filename = tkinter.filedialog.askopenfilename(**self.file_opts)
        lines = [line.strip() for line in open(filename)]
        vertices = []
        for line in lines:
            a,b = line.split(self.separator)
            try:
                b = int(b)
            except:
                tkinter.messagebox.showerror(title="Expected numeric value", message="Expected integer values describing electricity needs for each vertex")
                break
            vertices.append(a.strip())    
        vertices.sort()    
        if self.nodes == None:    
            self.nodes = vertices
        elif self.nodes == vertices:   
            self.vertices_label.config({'text': path.split(filename)[-1]})
            # TODO: pass it somewhere accessible
        else:
            tkinter.messagebox.showerror(title="Node values mismatch", message="Either the number of vertices or the names of vertices differ in selected files\n")   
        
