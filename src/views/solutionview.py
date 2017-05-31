import tkinter


class SolutionView(tkinter.PanedWindow):

    def __init__(self, root):
        self.root = root
        tkinter.PanedWindow.__init__(self, root, {'orient': tkinter.VERTICAL})

        self.main_label = tkinter.Label(self, text="Solution: ")
        self.iter_num_label = tkinter.Label(self, text="Number of iterations: ")
        self.time_spent = tkinter.Label(self, text="Time spent: ")
        self.end_condition = tkinter.Label(self, text="End condition triggered: ")
        self.total_cost = tkinter.Label(self, text="Total cost: ")

    def setSolution(self, iterNum, endCondition):
        pass    