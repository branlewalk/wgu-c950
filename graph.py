import sys
import heapq


class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])


class DijkstraVertex:
    def __init__(self, vertex):
        self.vertex = vertex
        # Set distance to infinity for all nodes
        self.distance = sys.maxint
        # Mark all nodes unvisited
        self.visited = False
        # Predecessor
        self.previous = None

    def get_adjacent(self):
        return self.vertex.adjacent

    def get_id(self):
        return self.vertex.get_id()

    def get_weight(self, neighbor):
        return self.vertex.get_weight(neighbor)

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return str(self.vertex)


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0
        self.previous = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost=0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self):
        return self.previous


class Stop:
    def __init__(self, vertex, total_distance):
        self.vertex = vertex
        self.total_distance = total_distance

    def get_total_time(self):
        return self.total_distance / 18

    def get_total_distance(self):
        return self.total_distance

    def __str__(self):
        return str(self.vertex.get_id()) + ', ' + str(self.total_distance) + ', ' + str(self.get_total_time())

    def set_total_distance(self, total_distance):
        self.total_distance = total_distance


def shortest(v, path):
    ''' make shortest path from v.previous'''
    total = 0
    short(v, path, total)


def short(v, path, total):
    if v.previous:
        total = total + v.distance
        path.append(Stop(v.previous, v.distance))
        short(v.previous, path, total)
    return total


def dijkstra(aGraph, start):

    dijkstra_dict = dict((v.get_id(), DijkstraVertex(v)) for v in aGraph)

    # Set the distance for the start node to zero
    dijkstra_dict[start.get_id()].set_distance(0)
    # Put tuple pair into the priority queue
    unvisited_queue = [(v.get_distance(), v) for v in dijkstra_dict.values()]

    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        # Pops a vertex with the smallest distance
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()

        # for next in v.adjacent:
        for next in current.get_adjacent():
            if next.get_id() in dijkstra_dict:
                dijkstra_next = dijkstra_dict[next.get_id()]
                # if visited, skip
                if dijkstra_next.visited:
                    continue
                new_dist = current.get_distance() + current.get_weight(next)

                if new_dist < dijkstra_next.get_distance():
                    dijkstra_next.set_distance(new_dist)
                    dijkstra_next.set_previous(current)

        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(v.get_distance(), v) for v in dijkstra_dict.values() if not v.visited]
        heapq.heapify(unvisited_queue)
    return dijkstra_dict
