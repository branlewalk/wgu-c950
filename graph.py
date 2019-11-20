from datetime import timedelta
import hashtable


class Neighbor:

    def __init__(self, location, distance):
        self.location = location
        self.distance = distance

    def get_hours_to(self):
        return timedelta(hours=self.distance / 18)

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
