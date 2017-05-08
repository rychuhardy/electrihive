import tkinter
import tkinter.filedialog

from os import path

from networkx import read_weighted_edgelist

class OptionsView(tkinter.PanedWindow):
    
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

    def openGraphFile(self):
        filename = tkinter.filedialog.askopenfilename(**self.file_opts)
        Graph = read_weighted_edgelist(path=filename, delimiter=":")
        self.graph_label.config({'text': path.split(filename)[-1]})
        self.root.graphview.updateGraph(Graph)


    def openElectricityNeedsFile(self):
        pass
        # TODO: implement
        # filename = tkinter.filedialog.askopenfilename(**self.file_opts)
