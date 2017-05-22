import tkinter
import tkinter.filedialog
import tkinter.messagebox

from os import path
import _thread

from networkx import read_weighted_edgelist
from networkx import set_node_attributes

from algorithm import start_background_thread


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

        self.files_labels = tkinter.Label(self, text='Description for Each vertex, edge or build cost should be in separate line.\nIntegers in each line should be separated with colon.')

        self.graph_button = tkinter.Button(
            self, text='Edges list with cost', command=self.openGraphFile)
        self.graph_label = tkinter.Label(self, text='No file selected')
        self.vertices_button = tkinter.Button(
            self, text='Electricity needs for each vertex', command=self.openElectricityNeedsFile, state=tkinter.DISABLED)
        self.vertices_label = tkinter.Label(self, text='Select edges list first')
        self.build_cost_button = tkinter.Button(
            self, text='Build cost', command=self.openBuildCostFile)
        self.build_cost_label = tkinter.Label(self, text='No file selected')    

        
        self.neighbour_number_label = tkinter.Label(self, text='Number of neighbours in neighbourhood')
        self.neighbour_number_entry = tkinter.Entry(self, validate="focusout", validatecommand=self.validateNeighbourNumber)
        self.solution_liveness_label = tkinter.Label(self, text='Liveness of the solution')
        self.solution_liveness_entry = tkinter.Entry(self, validate="focusout", validatecommand=self.validateSolutionLiveness)
        self.bees_number_label = tkinter.Label(self, text='Number of bees')
        self.bees_number_entry = tkinter.Entry(self, validate="focusout", validatecommand=self.validateNumberOfBees)
        self.previous_solutions_label = tkinter.Label(self, text='Number of previous solutions in iteration')
        self.previous_solutions_entry = tkinter.Entry(self, validate="focusout", validatecommand=self.validatePreviousSolutionsNumber)
        self.max_iters_cond_label = tkinter.Label(self, text='Max number of iterations')
        self.max_iters_cond_entry = tkinter.Entry(self, validate="focusout", validatecommand=self.validateMaxIterationsNumber)
        self.min_cost_cond_label = tkinter.Label(self, text='Min cost of the solution')
        self.min_cost_cond_entry = tkinter.Entry(self, validate="focusout", validatecommand=self.validateMinSolutionCost)
        self.network_change_probability_label = tkinter.Label(self, text='Probability of network change/break')
        self.network_change_probability_entry = tkinter.Entry(self, validate="focusout", validatecommand=self.validateNetworkChangeProbability)


        self.run_button = tkinter.Button(
            self, text='Run algorithm', command=self.runAlgorithm)
        
        self.files_labels.grid(row=0, column=0, columnspan=2, pady=40)
        self.graph_button.grid(row=1, column=0, **self.button_opts)
        self.graph_label.grid(row=1, column=1, **self.button_opts)
        self.vertices_button.grid(row=2, column=0, **self.button_opts)
        self.vertices_label.grid(row=2, column=1, **self.button_opts)
        self.build_cost_button.grid(row=3, column=0, **self.button_opts)
        self.build_cost_label.grid(row=3, column=1, **self.button_opts)     

        self.neighbour_number_label.grid(row=4, column=0, **self.button_opts)
        self.neighbour_number_entry.grid(row=4, column=1, **self.button_opts)   
        self.solution_liveness_label.grid(row=5, column=0, **self.button_opts)
        self.solution_liveness_entry.grid(row=5, column=1, **self.button_opts)   
        self.bees_number_label.grid(row=6, column=0, **self.button_opts)
        self.bees_number_entry.grid(row=6, column=1, **self.button_opts)  
        self.previous_solutions_label.grid(row=7, column=0, **self.button_opts)
        self.previous_solutions_entry.grid(row=7, column=1, **self.button_opts)
        self.max_iters_cond_label.grid(row=8, column=0, **self.button_opts)
        self.max_iters_cond_entry.grid(row=8, column=1, **self.button_opts)
        self.min_cost_cond_label.grid(row=9, column=0, **self.button_opts)
        self.min_cost_cond_entry.grid(row=9, column=1, **self.button_opts)
        self.network_change_probability_label.grid(row=9, column=0, **self.button_opts)
        self.network_change_probability_entry.grid(row=9, column=1, **self.button_opts)

        self.run_button.grid(row=11, column=0, columnspan=2, padx=20, pady=40, sticky='S')

        self.graph = None
        self.buildCostDict = {}
        self.files_chosen = 0
    
    
    def validatePositiveNumber(self, field):
        text = field.get()
        try:
            result = int(text)
            if result < 1:
                raise 1 #dummy exception

            field.config(fg='black')
            return True
        except:
            field.config(fg='red')
            return False


    def validateNeighbourNumber(self):
        return self.validatePositiveNumber(self.neighbour_number_entry)
    

    def validateSolutionLiveness(self):
        return self.validatePositiveNumber(self.solution_liveness_entry)

    
    def validateNumberOfBees(self):
        return self.validatePositiveNumber(self.bees_number_entry)
    

    def validatePreviousSolutionsNumber(self):
        return self.validatePositiveNumber(self.previous_solutions_entry)
    
    
    def validateMaxIterationsNumber(self):
        return self.validatePositiveNumber(self.max_iters_cond_entry)


    def validateMinSolutionCost(self):
        return self.validatePositiveNumber(self.min_cost_cond_entry)
    

    def validateNetworkChangeProbability(self):
        field = self.network_change_probability_entry
        text = field.get()
        try:
            result = int(text)
            if result < 0 or result > 100:
                raise 1 #dummy exception

            field.config(fg='black')
            return True
        except:
            field.config(fg='red')
            return False

    def openGraphFile(self):
        filename = tkinter.filedialog.askopenfilename(**self.file_opts)
        if len(filename) == 0:
            return
        try:
            self.graph = read_weighted_edgelist(path=filename, delimiter=self.separator)
            self.graph_label.config({'text': path.split(filename)[-1]})
            self.vertices_button['state'] = tkinter.NORMAL
            self.vertices_label['text'] = "No file selected"
            self.root.graphview.updateGraph(self.graph)
            self.files_chosen+=1
        except FileNotFoundError:
            tkinter.messagebox.showerror(title="File not found", message="The selected file was not found or could not be open")


    def openElectricityNeedsFile(self):
        try:
            filename = tkinter.filedialog.askopenfilename(**self.file_opts)
            if len(filename) == 0:
                return
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
        except FileNotFoundError:
            tkinter.messagebox.showerror(title="File not found", message="The selected file was not found or could not be open")
            
        if set(vertices) <= set(self.graph.nodes()):
            for idx in range(1, len(vertices)):
                self.graph.node[str(vertices[idx])]['cost'] = values[idx]
            
            self.files_chosen+=1
            self.vertices_label.config({'text': path.split(filename)[-1]})
            self.root.graphview.addVertexLabels(self.graph)
            
        else:
            tkinter.messagebox.showerror(title="Node values mismatch", message="The selected file specifies nodes that were not present in previous file\n")

    def openBuildCostFile(self):
        filename = tkinter.filedialog.askopenfilename(**self.file_opts)
        if len(filename) == 0:
            return
        try:    
            lines = [line.strip() for line in open(filename)]
            idx = 1
            for line in lines:
                a, b = line.split(self.separator)
                try:
                    a, b = int(a), int(b)
                    self.buildCostDict[a] = b
                except:
                    tkinter.messagebox.showerror(title="Expected numeric value", message="Expected integer values describing build cost in line " + str(idx))    
            self.build_cost_label.config({'text': path.split(filename)[-1]})
            self.files_chosen+=1
        except FileNotFoundError:
            tkinter.messagebox.showerror(title="File not found", message="The selected file was not found or could not be open")     

    def runAlgorithm(self):
        if self.files_chosen < 3:
            tkinter.messagebox.showerror(title="Select all files", message="Please select all three files.")
            return
        
        # Validate all Entry obj
        config = {}
        errMsg = "Please fix the following issues to run the algorithm\n\n"

        if self.validateNeighbourNumber():
            config['neighboursInNeighbourhood'] = int(self.neighbour_number_entry.get())
        else:
            errMsg += "Invalid or missing number of neighbours in neighbourhood\n\n"            

        if self.validateSolutionLiveness():
            config['solutionLiveness'] = int(self.solution_liveness_entry.get())
        else:
            errMsg += "Invalid or missing number of solution liveness\n\n"
    
        if self.validateNumberOfBees():
            config['beesNumber'] = int(self.bees_number_entry.get())
        else:
            errMsg += "Invalid or missing number of bees\n\n"

        if self.validatePreviousSolutionsNumber() and  'beesNumber' in config and int(self.previous_solutions_entry.get()) < config['beesNumber']:
            config['previousSolutionsInIteration'] = int(self.previous_solutions_entry.get())
        else:
            errMsg += "Invalid or missing number of previous solutions in iteration (The number of solutions should be smaller than bees number)\n\n"
        

        hasAnyStopCondition = False
        stopConditionErrMsg = "Should satisfy one of the following:\n\n"
        if self.validateMaxIterationsNumber():
            config['maxIterationsCondition'] = int(self.max_iters_cond_entry.get())
            hasAnyStopCondition = True
        else:
            stopConditionErrMsg += "\t- Invalid or missing max iterations condition\n\n"

        if self.validateMinSolutionCost():
            config['minCostCondition'] = int(self.min_cost_cond_entry.get())
            hasAnyStopCondition = True
        else:
            stopConditionErrMsg += "\t- Invalid or missing number of min cost condition\n\n"
        
        if not hasAnyStopCondition:
            stopConditionErrMsg += "\n"
            errMsg += stopConditionErrMsg


        if self.validateNetworkChangeProbability():
            config['networkChangeProbability'] = int(self.network_change_probability_entry.get())
        else:
            errMsg += "Invalid or missing probability of network change/break (should be between 0 and 100)\n\n"


        if len(errMsg) == 0:
            self.run_button['state'] = tkinter.DISABLED            
            _thread.start_new_thread(start_background_thread, (self.graph, self.buildCostDict, config))
        else:
            tkinter.messagebox.showerror(title="Invalid configuration values", message=errMsg)            