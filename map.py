import sys
import heapq


class Location:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_address(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])


class DiLocations:
    def __init__(self, location):
        self.location = location
        # Set distance to infinity for all nodes
        self.distance = sys.maxint
        # Mark all nodes unvisited
        self.visited = False
        # Predecessor
        self.previous = None

    def get_adjacent(self):
        return self.location.adjacent

    def get_id(self):
        return self.location.get_address()

    def get_weight(self, neighbor):
        return self.location.get_weight(neighbor)

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return str(self.location)


class Map:
    def __init__(self):
        self.location_dict = {}
        self.num_locations = 0
        self.previous = 0

    def __iter__(self):
        return iter(self.location_dict.values())

    def add_location(self, node):
        self.num_locations = self.num_locations + 1
        new_location = Location(node)
        self.location_dict[node] = new_location
        return new_location

    def get_location(self, n):
        if n in self.location_dict:
            return self.location_dict[n]
        else:
            return None

    def add_trace(self, frm, to, cost=0):
        if frm not in self.location_dict:
            self.add_location(frm)
        if to not in self.location_dict:
            self.add_location(to)

        self.location_dict[frm].add_neighbor(self.location_dict[to], cost)
        self.location_dict[to].add_neighbor(self.location_dict[frm], cost)

    def get_locations(self):
        return self.location_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self):
        return self.previous


class Destination:
    def __init__(self, location, total_distance):
        self.location = location
        self.total_distance = total_distance

    def get_total_time(self):
        return self.total_distance / 18

    def get_total_distance(self):
        return self.total_distance

    def __str__(self):
        return str(self.location.get_address()) + ', ' + str(self.total_distance) + ', ' + str(self.get_total_time())

    def set_total_distance(self, total_distance):
        self.total_distance = total_distance


def shortest(v, path, total=0):
    if v.previous:
        total = total + v.distance
        path.append(Destination(v.previous, v.distance))
        shortest(v.previous, path, total)
    return total


def vantage(unsorted_map, start):

    vantage_dict = dict((loc.get_address(), DiLocations(loc)) for loc in unsorted_map)

    # Set the distance for the start node to zero
    vantage_dict[start.get_address()].set_distance(0)
    # Put tuple pair into the priority queue
    unvisited_queue = [(loc.get_distance(), loc) for loc in vantage_dict.values()]

    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        # Pops a vertex with the smallest distance
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()

        # for next in loc.adjacent:
        for next in current.get_adjacent():
            if next.get_address() in vantage_dict:
                vantage_next = vantage_dict[next.get_address()]
                # if visited, skip
                if vantage_next.visited:
                    continue
                new_dist = current.get_distance() + current.get_weight(next)

                if new_dist < vantage_next.get_distance():
                    vantage_next.set_distance(new_dist)
                    vantage_next.set_previous(current)

        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(loc.get_distance(), loc) for loc in vantage_dict.values() if not loc.visited]
        heapq.heapify(unvisited_queue)
    return vantage_dict
