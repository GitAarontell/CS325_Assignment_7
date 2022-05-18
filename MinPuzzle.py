import heapq


class Graph:
    # constructor
    def __init__(self):
        # create a dictionary
        self.graph = {}

    def addEdge(self, node, newVertex, weight):
        # if the node is already in graph then just update the current dictionary there
        if node in self.graph:
            self.graph[node].update({newVertex: weight})
        # if the node is not in the graph
        # then add the dictionary with the key value pair
        else:
            self.graph[node] = {newVertex: weight}

    # print the graph
    def printData(self):
        print(self.graph)

    # lets you iterate through graph
    def __iter__(self):
        return iter(self.graph)

    # lets you use items on object
    def items(self):
        return self.graph.items()

    # returns value of graph at graph[x] which returns a dictionary
    def getValAtKey(self, x):
        return self.graph[x]


# creates a matrix of letters by the width and length of the matrix in parameter and returns it
def createNodeNameTable(matrix):
    # create matrix by width and height of matrix in parameter
    letters = [[] for j in range(len(matrix))]
    # start letter is the ascii value 65 which corresponds to letter A
    startLetter = 65
    # represents the number of times we add a letter
    # Ex: 1 = 'A', 2 = 'AA'
    # if the matrix is larger than 26 cells, then we go back to the letter A
    # but this time we add 2 A's so we get 'AA'
    numLetters = 1

    # for each row of the matrix
    for i in range(len(matrix)):

        # for every element in row i
        for j in range(len(matrix[i])):
            # since there is only 26 letters if we reach the ascii value
            # above Z which is 91, then increase to number of letters by 1 and reset
            # back to letter A
            if startLetter % 91 == 0:
                numLetters += 1
                startLetter = 65

            # add chr(startLetter) numLetters times to letters[i][j]
            for l in range(numLetters):
                letters[i].append('')
                letters[i][j] += chr(startLetter)
            # increment startLetter ascii value by 1
            startLetter += 1

    return letters


# creates a dictionary of dictionaries and returns several values
def puzzleToGraph(matrix):
    # letters equals a matrix of letters by matrix width and height
    letters = createNodeNameTable(matrix)
    # create a graph object
    G = Graph()

    # for each row of the matrix
    for i in range(len(matrix)):
        # for every element in row i
        for j in range(len(letters[i])):

            # we can add an edge on the left
            if j != 0:
                G.addEdge(letters[i][j], letters[i][j - 1], matrix[i][j - 1])

            # we can add an edge below
            if i != len(letters) - 1 and j < len(letters[i + 1]):
                G.addEdge(letters[i][j], letters[i + 1][j], matrix[i + 1][j])

            # we can add an edge above
            if i != 0 and j < len(letters[i-1]):
                G.addEdge(letters[i][j], letters[i - 1][j], matrix[i - 1][j])

            # we can add an edge on the right
            if j != len(letters[i]) - 1:
                G.addEdge(letters[i][j], letters[i][j + 1], matrix[i][j + 1])
    # returns the graph, the starting vertex name at letters[0][0], the weight at that vertex at matrix[0][0],
    # and the name of the vertex we are looking for at n-1 m-1 in letters.
    # returns the graph, the starting vertex name at letters[0][0], the weight at that vertex at matrix[0][0],
    # and the name of the vertex we are looking for at n-1 m-1 in letters.
    return G, letters[0][0], matrix[0][0], letters[len(letters) - 1][len(letters[0]) - 1]


def minEffort(puzzle):
    # gets starting values from puzzleToGraph method
    graph, startVertex, startVal, endVertex = puzzleToGraph(puzzle)

    # creates a dictionary of each vertex in graph and an infinity value as the value of those keys
    distances = {vertex: float('infinity') for vertex in graph}
    route = {vertex: '' for vertex in graph}
    maxEffort = -1

    # creates a queue with starting tuple of starting nodes weight and name,
    # used to represent node that is waiting to be looked at
    priorityQueue = [(startVal, startVertex)]

    # while there are nodes waiting to be looked at continue loop
    while len(priorityQueue) > 0:
        # takes the lowest value by weight from the priority queue
        # puts the tuple values into current distance and current vertex
        current_distance, current_vertex = heapq.heappop(priorityQueue)

        # sometimes while calculating nodes, a lower weight to another node, previously calculated
        # and added to the pq will be found, and so since the pq is ordered everytime heapq is used on it
        # we will instead calculate that shorter distance path first, so when we do come across that other
        # the same node but with a higher weighted path, we just don't do the calculation since we already
        # know that there is a shorter path and it has already been calculated
        if current_distance > distances[current_vertex]:
            continue

        # loops through each neighbor of current node
        for neighbor, weight in graph.getValAtKey(current_vertex).items():

            if neighbor == 'A':
                continue

            distance = current_distance + abs(graph.getValAtKey(neighbor)[current_vertex] - weight)

            # if the distance to the neighbor node is less than what has been calculated
            if distance < distances[neighbor]:
                # add array of

                # then set the distances array at node neighbor to the new distance
                distances[neighbor] = distance

                # when there is a shortest distance, will store the node that it came from
                # that provided that shortest distance
                # if route[neighbor] != 'A':
                route[neighbor] = current_vertex

                # push the node with this distance onto pq, since we know need to calculate
                # new values for the distances to this node, or that we have just not calculated
                # any values for this node yet
                heapq.heappush(priorityQueue, (distance, neighbor))

        # after the while loop ends store the lowest distance nodes
    print(route)
    while endVertex != 'A':

        endVertexWeight = graph.getValAtKey(route[endVertex])[endVertex]
        parentNodeWeight = graph.getValAtKey(endVertex)[route[endVertex]]
        effort = abs(endVertexWeight - parentNodeWeight)
        if maxEffort < effort:
            maxEffort = effort
        endVertex = route[endVertex]

    # calculate all paths by absolute distance to get the smallest value
    graph.printData()
    print(route)
    return maxEffort


if __name__ == '__main__':
    puzzle = [[3, 5, 2],
              [2, 8, 3],
              [3, 9, 7]]
    print(minEffort(puzzle))
