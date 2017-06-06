import tkinter
from tkinter import Grid

class SolutionView(tkinter.PanedWindow):

    label_opts = {
        'padx': 20,
        'pady': 5,
        'sticky': tkinter.NSEW
    }

    def __init__(self, root):
        self.root = root
        tkinter.PanedWindow.__init__(self, root, {'orient': tkinter.VERTICAL})

        self.main_label = tkinter.Label(self, text="Solution: ", justify=tkinter.CENTER, anchor=tkinter.CENTER, font = "Verdana 12 bold")
        self.iter_num_label = tkinter.Label(self, text="Number of iterations: ")
        self.end_condition = tkinter.Label(self, text="End condition triggered: ")
        self.total_cost = tkinter.Label(self, text="Total cost: ")

        self.main_label.grid(row=0, column=0, columnspan=2, **self.label_opts)
        self.iter_num_label.grid(row=1, column=0, **self.label_opts)
        self.end_condition.grid(row=2, column=0, **self.label_opts)
        self.total_cost.grid(row=3, column=0, **self.label_opts)

        for row_index in range(4):
            Grid.rowconfigure(self, row_index, weight=1)

        for col_index in range(2):
            Grid.columnconfigure(self, col_index, weight=1)    


    def setSolution(self, solution, iter_count):
        self.iter_num_label['text'] += str(iter_count)
        self.end_condition['text'] += " Max iterations reached" if iter_count == self.root.optionsview.requested_iter_num else " Min cost reached"
        self.total_cost['text'] += str(solution.cost)
        self.root.graphview.setSolutionView(solution.network_list)
        self.root.optionsview.unlockRunButton()


