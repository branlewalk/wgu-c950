import sys
import heapq

import hashtable


class Neighbor:

    def __init__(self, location, distance):
        self.location = location
        self.distance = distance

    def __str__(self):
        return str(self.location) + ' ' + str(self.distance)


class Location:
    def __init__(self, node):
        self.address = node
        self.distances = hashtable.HashTable()
        self.neighbors = []

    def add_neighbor(self, neighbor, distance=0):
        self.distances.put(neighbor, distance)
        self.neighbors.append(Neighbor(neighbor, distance))

    def get_connections(self):
        return self.distances.keys()

    def get_address(self):
        return self.address

    def get_distance(self, neighbor):
        return self.distances.get(neighbor)

    def get_neighbors(self):
        return self.neighbors

    def sort_distances(self):
        self.neighbors.sort(key=lambda n: n.distance)

    def __str__(self):
        return str(self.address)


# class DiLocations:
#     def __init__(self, location):
#         self.location = location
#         # Set distance to infinity
#         self.distance = sys.maxint
#         # Mark all unvisited
#         self.visited = False
#         # Predecessor
#         self.previous = None
#
#     def get_adjacent(self):
#         return self.location.adjacent
#
#     def get_id(self):
#         return self.location.get_address()
#
#     def get_weight(self, neighbor):
#         return self.location.get_distance(neighbor)
#
#     def set_distance(self, dist):
#         self.distance = dist
#
#     def get_distance(self):
#         return self.distance
#
#     def set_previous(self, prev):
#         self.previous = prev
#
#     def set_visited(self):
#         self.visited = True
#
#     def __str__(self):
#         return str(self.location)


class Graph:
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

    def add_path(self, frm, to, distance=0):
        if frm not in self.location_dict:
            self.add_location(frm)
        if to not in self.location_dict:
            self.add_location(to)

        self.location_dict[frm].add_neighbor(self.location_dict[to], distance)
        self.location_dict[to].add_neighbor(self.location_dict[frm], distance)

    def get_locations(self):
        return self.location_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self):
        return self.previous

    def sort_locations(self):
        for address in self.location_dict:
            self.location_dict[address].sort_distances()


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

# def vantage(unsorted_map, start):
#
#     vantage_dict = dict((loc.get_address(), DiLocations(loc)) for loc in unsorted_map)
#
#     # Set the distance for the start location to zero
#     vantage_dict[start.get_address()].set_distance(0)
#     # Put tuple pair into the priority queue
#     unvisited_queue = [(loc.get_distance(), loc) for loc in vantage_dict.values()]
#
#     heapq.heapify(unvisited_queue)
#
#     while len(unvisited_queue):
#         # Pops a location with the smallest distance
#         uv = heapq.heappop(unvisited_queue)
#         current_loc = uv[1]
#         current_loc.set_visited()
#
#         for next_adj_loc in current_loc.get_adjacent():
#             if next_adj_loc.get_address() in vantage_dict:
#                 vantage_next = vantage_dict[next_adj_loc.get_address()]
#                 # if visited, skip
#                 if vantage_next.visited:
#                     continue
#                 new_dist = current_loc.get_distance() + current_loc.get_distance(next_adj_loc)
#
#                 if new_dist < vantage_next.get_distance():
#                     vantage_next.set_distance(new_dist)
#                     vantage_next.set_previous(current_loc)
#
#         # Rebuild heap
#         # 1. Pop every adj
#         while len(unvisited_queue):
#             heapq.heappop(unvisited_queue)
#         # 2. Put all locations not visited into the queue
#         unvisited_queue = [(loc.get_distance(), loc) for loc in vantage_dict.values() if not loc.visited]
#         heapq.heapify(unvisited_queue)
#     return vantage_dict
