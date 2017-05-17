def generateRandomSolution(baseSolution):
    pass


def prepareInitialSolutionSet(baseSolution,n):
    return {generateRandomSolution(baseSolution) for x in range(n)}


def generateNeighbourhood(solution):
    pass


def findBestSolutionInNeighbourhood(solution):
    return chooseBestSolution(generateNeighbourhood(solution))


def stopCondition():
    pass


def chooseSolutionsForNextIteration(newSolutionSet):
    pass


def prepareNextIterationSolutionSet(newSolutionSet, baseSolution, number_of_bees):
    selectedSolutionSet = chooseSolutionsForNextIteration(newSolutionSet)
    while(len(selectedSolutionSet)<number_of_bees):
        selectedSolutionSet.add(generateRandomSolution(baseSolution))
    return selectedSolutionSet


def countSolutionCost(solution):
    pass


def chooseBestSolution(solutionSet):
    return max(solutionSet, key = lambda x: countSolutionCost(x))


def generateBaseSolution(initialGraph):
    pass


def algorithm(initialGraph, number_of_bees):
    baseSolution = generateBaseSolution(initialGraph)
    solutionSet = prepareInitialSolutionSet(baseSolution, number_of_bees)
    bestSolution = None
    while not stopCondition():
        newSolutionSet = {findBestSolutionInNeighbourhood(solution) for solution in solutionSet}
        solutionSet, currentBestSolution = prepareNextIterationSolutionSet(newSolutionSet, baseSolution, number_of_bees)
        bestSolution = chooseBestSolution({bestSolution,currentBestSolution})
    return bestSolution


def start_background_thread(Graph, BuildCost):
    pass