import tkinter
import tkinter.filedialog
import tkinter.messagebox

from os import path

from networkx import read_weighted_edgelist
from networkx import set_node_attributes



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

        self.graph_button = tkinter.Button(
            self, text='Edges list with cost', command=self.openGraphFile)
        self.graph_label = tkinter.Label(self, text='No file selected')
        self.vertices_button = tkinter.Button(
            self, text='Electricity needs for each vertex', command=self.openElectricityNeedsFile, state=tkinter.DISABLED)
        self.vertices_label = tkinter.Label(self, text='Select edges list first')

        self.run_button = tkinter.Button(
            self, text='Run algorithm', command=self.runAlgorithm)

        self.graph_button.grid(row=0, column=0, **self.button_opts)
        self.graph_label.grid(row=0, column=1, **self.button_opts)
        self.vertices_button.grid(row=1, column=0, **self.button_opts)
        self.vertices_label.grid(row=1, column=1, **self.button_opts)

        self.run_button.grid(row=2, column=0, columnspan=2, padx=20, pady=40, sticky='S')

        self.graph = None
        self.graph_loaded = False
        self.electricity_needs_loaded = False

    def openGraphFile(self):
        filename = tkinter.filedialog.askopenfilename(**self.file_opts)
        self.graph = read_weighted_edgelist(path=filename, delimiter=self.separator)
        self.graph_label.config({'text': path.split(filename)[-1]})
        self.vertices_button['state'] = tkinter.NORMAL
        self.vertices_label['text'] = "No file selected"
        self.root.graphview.updateGraph(self.graph)


    def openElectricityNeedsFile(self):
        filename = tkinter.filedialog.askopenfilename(**self.file_opts)
        lines = [line.strip() for line in open(filename)]
        vertices = []
        values = []
        idx = 1
        for line in lines:
            a,b = line.split(self.separator)
            try:
                b = int(b)
                vertices.append(a.strip())
                values.append(b)
                idx += 1
            except:
                tkinter.messagebox.showerror(title="Expected numeric value", message="Expected integer values describing electricity needs for each vertex in line " + str(idx))
                break
        if set(vertices) <= set(self.graph.nodes()):
            for idx in range(1, len(vertices)):
                self.graph.node[str(vertices[idx])]['cost'] = values[idx]

            self.vertices_label.config({'text': path.split(filename)[-1]})
            self.root.graphview.addVertexLabels(self.graph)
            
        else:
            tkinter.messagebox.showerror(title="Node values mismatch", message="The selected file specifies nodes that were not present in previous file\n")

    def runAlgorithm(self):
        pass
