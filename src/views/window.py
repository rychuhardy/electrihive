import tkinter
from views.graphview import GraphView
from views.optionsview import OptionsView

class Window(tkinter.Frame):

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.wm_title("Electrihive")
        tkinter.Frame.__init__(self, self.root)

        self.optionsview = OptionsView(self)
        self.graphview = GraphView(self)

        self.optionsview.grid(row=0, column=0, rowspan=3, columnspan=1)
        self.graphview.grid(row=0, column=1, rowspan=3, columnspan=2)    

        self.grid()   


    def mainloop(self):
        self.root.mainloop()
