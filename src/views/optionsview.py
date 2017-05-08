import tkinter
import tkinter.filedialog

from os import path

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

        graph_button = tkinter.Button(self, text='Edge list', command=self.openGraphFile).grid(row=0, column=0, **self.button_opts)    
        vertices_button = tkinter.Button(self, text='Electricity needs for each vertex', command=self.openElectricityNeedsFile).grid(row=1, column=0, **self.button_opts)
        edges_button = tkinter.Button(self, text='Build cost for each edge', command=self.openCostFiles).grid(row=2, column=0, **self.button_opts)

    def openGraphFile(self):
        pass
        # filename = tkinter.filedialog.askopenfilename(**self.file_opts)
        # # TODO: validate graph
        # self.Graph = nx.read_edgelist(path=filename, delimiter=":")
        # pos = nx.spring_layout(self.Graph)
        # nx.draw(self.Graph, pos, ax=self.subplot)
        # self.canvas.draw()

    def openElectricityNeedsFile(self):
        pass
        # TODO: implement
        # filename = tkinter.filedialog.askopenfilename(**self.file_opts)

    def openCostFiles(self):
        pass
        # TODO: implement
        # filename = tkinter.filedialog.askopenfilename(**self.file_opts)