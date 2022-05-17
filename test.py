'''
source: https://bradfieldcs.com/algos/graphs/dijkstras-algorithm/
'''
import heapq


def calculate_distances(graph, starting_vertex):
    # creates a dictionary of floats with the value infinity for each vertex in graph
    # distances = {'U': inf, 'V': inf, 'W': inf, 'X': inf, 'Y': inf, 'Z': inf}
    distances = {vertex: float('infinity') for vertex in graph}
    # sets the X key value pair to 0 in distances dictionary
    # will set distances to {'U': inf, 'V': inf, 'W': inf, 'X': 0, 'Y': inf, 'Z': inf}
    distances[starting_vertex] = 0

    # creates an array with one tuple pq = [(0, 'X')]
    pq = [(0, starting_vertex)]
    # print(len(pq)) = 1

    # loops while there is a tuple in pq once the length goes to 0 then loop will stop
    while len(pq) > 0:

        # this seems to take a tuple from an array, pop it off and return the two values
        # in the tuple in order
        # hence for the first pop:
        # current distance = 0
        # current vertex = X
        current_distance, current_vertex = heapq.heappop(pq)

        # Nodes can get added to the priority queue multiple times. We only
        # process a vertex the first time we remove it from the priority queue.
        # when we first set the distance of a neighbor node in the distances array from X, then
        # current distance, when we pop this vertex off the pq, and distances[current_vertex] will be equal
        # Ex: U is 1 distance from X so in the distances array we would have [('U': 1)] and during the first
        # run this would be pushed onto pq. Later when we revisit this node the current_distance will be 1 again,
        # so this if statement will not true, however the same node can be re-added with a smaller distance during
        # our search, we have this case with node 'W', when we first run through this our node 'W' gets the a value of
        # 3 in our distances array, and is pushed onto our as pq[('W', 3)], but when we push off node 'Y' from our pq
        # we again calculate the distance to node 'W' since the distance is smaller in this path to 'W' than what was
        # previously calculated we add that onto the priority q, and the pq is such that the smaller value get added
        # closer to the front of the line than the higher value nodes, so when we add ('W', 2) to pq, it goes in front
        # of ('W', 3) so we know that we will pop off the value with the shorter distance and skip the distance to the
        # node with the larger distance since that will not provide the shortest distance to that node, and hence we
        # will always be going the shortest path to that node from now on before we calculate things. As a result this
        # skips that second calculation that could occur since for example if we pop ('W',2) off of pq and then
        # we calculate its value to node V, we would always get a distance from X that is larger than if we would have
        # had the starting value of 2 with the shorter distance. So with (W,2) we get a distance to V from W of 5,
        # where with (W, 3) we get a distance of 6. The heapq pop also keeps the pq in order by distances, so we always
        # are popping off the node that has the smallest distance from x, hence we will always do the lowest amount of
        # calculations needed. So before example pq = [(U,1)(Y,1),(V,2),(W,3)] we start with (U,1), later when (Y,1)
        # get popped off we add (W,2), now pq = [(V,2)(W,2)(W,3)]. So always popping off from the front of the queue,
        # which is guaranteeing the lowest distances.
        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            # runs through each dictionary item starting at current_vertex which is X, the items function means
            # return the key value pair, so it returns multiple values, also arrays the dictionary to do this
            # so for graph[X] we would normally get {'U': 1, 'V': 2, 'W': 3, 'Y': 1}, but with
            # graph[x].items() we get dict_items([('U': 1), ('V': 2), ('W': 3), ('Y': 1)]) which is an array of tuples
            # neighbor will equal the name of the node so in dictionary 'X': {'U': 1, 'V': 2, 'W': 3, 'Y': 1}
            # neighbor = U
            # weight = 1 for the 1st iteration
            # print(graph[current_vertex].items())
            # print(neighbor)
            # print(weight)
            distance = current_distance + weight

            # Only consider this new path if it's better than any path we've
            # already found.
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances


example_graph = {
    'U': {'V': 2, 'W': 5, 'X': 1},
    'V': {'U': 2, 'X': 2, 'W': 3},
    'W': {'V': 3, 'U': 5, 'X': 3, 'Y': 1, 'Z': 5},
    'X': {'U': 1, 'V': 2, 'W': 3, 'Y': 1},
    'Y': {'X': 1, 'W': 1, 'Z': 1},
    'Z': {'W': 5, 'Y': 1},
}
print(calculate_distances(example_graph, 'X'))
# => {'U': 1, 'W': 2, 'V': 2, 'Y': 1, 'X': 0, 'Z': 2}
