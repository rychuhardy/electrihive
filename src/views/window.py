import tkinter
from views.graphview import GraphView
from views.optionsview import OptionsView
from tkinter import Grid

class Window(tkinter.Frame):

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.wm_title("Electrihive")
        tkinter.Frame.__init__(self, self.root)

        Grid.rowconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 0, weight=1)
        self.grid(row=0, column=0, sticky=tkinter.NSEW)

        self.optionsview = OptionsView(self)
        self.graphview = GraphView(self)

        Grid.rowconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 1, weight=4)
        
        self.optionsview.grid(row=0, column=0, columnspan=1, sticky=tkinter.NSEW)
        self.graphview.grid(row=0, column=1, columnspan=5, sticky=tkinter.NSEW)       


    def mainloop(self):
        self.root.mainloop()
