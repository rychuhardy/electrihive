import tkinter
from views.graphview import GraphView
from views.optionsview import OptionsView
from views.solutionview import SolutionView
from tkinter import Grid
from threading import Lock


class Window(tkinter.Frame):

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.wm_title("Electrihive")
        tkinter.Frame.__init__(self, self.root)

        self.mutex = Lock()
        self.solution = None
        self.iter_count = None

        Grid.rowconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 0, weight=1)
        self.grid(row=0, column=0, sticky=tkinter.NSEW)

        self.optionsview = OptionsView(self)
        self.graphview = GraphView(self)
        self.solutionview = SolutionView(self)

        Grid.rowconfigure(self, 0, weight=1)
        Grid.rowconfigure(self, 2, weight=1)
        Grid.columnconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 1, weight=4)

        self.optionsview.grid(
            row=0, column=0, columnspan=1, sticky=tkinter.NSEW)
        self.graphview.grid(row=0, column=1, columnspan=5,
                            rowspan=2, sticky=tkinter.NSEW)
        self.solutionview.grid(
            row=1, column=0, columnspan=1, sticky=tkinter.NSEW)

    def mainloop(self):
        self.root.after(2000, self.checkIfAlgorithmFinished)
        self.root.mainloop()
    
    def setSolution(self, solution, iter_count):
        try:
            self.mutex.acquire()
            self.solution = solution
            self.iter_count = iter_count
        finally:
            self.mutex.release()

    def checkIfAlgorithmFinished(self):
        try:
            self.mutex.acquire()
            if self.solution is None:
                self.root.after(2000, self.checkIfAlgorithmFinished)
            else:
                self.solutionview.setSolution(self.solution, self.iter_count)
        finally:
            self.mutex.release()