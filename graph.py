from datetime import timedelta
import hashtable

# Neighbors are neighboring nodes to a location
class Neighbor:

    def __init__(self, location, distance):
        self.location = location
        self.distance = distance

    def get_hours_to(self):
        return timedelta(hours=self.distance / 18)

    def __str__(self):
        return str(self.location)


# Locations are the nodes on the graph
class Location:

    def __init__(self, node):
        self.address = node
        self.distances = hashtable.HashTable()
        self.neighbors_by_location = hashtable.HashTable()
        self.neighbors = []

    # Adds a corresponding location with edge data
    def add_neighbor(self, location, distance=0):
        neighbor = Neighbor(location, distance)
        self.distances.put(location, distance)
        self.neighbors.append(neighbor)
        self.neighbors_by_location.put(location, neighbor)

    # Returns the list of neighbors for the location
    def get_neighbors(self):
        return self.neighbors

    # O(n log n)
    # Sorts the distances to each neighbor, shortest neighbor 1st
    def sort_distances(self):
        self.neighbors.sort(key=lambda n: n.distance)

    # Used for various messaging
    def __str__(self):
        return str(self.address)


# The Graph is the map of all the locations
class Graph:

    def __init__(self):
        self.location_dict = {}
        self.num_locations = 0
        self.previous = 0

    # Add location to the graph
    def add_location(self, node):
        self.num_locations = self.num_locations + 1
        new_location = Location(node)
        self.location_dict[node] = new_location
        return new_location

    # Access a location from the graph
    def get_location(self, n):
        if n in self.location_dict:
            return self.location_dict[n]
        else:
            return None

    # Adds neighbors to each location with edge data
    def add_path(self, frm, to, distance=0):
        if frm not in self.location_dict:
            self.add_location(frm)
        if to not in self.location_dict:
            self.add_location(to)
        self.location_dict[frm].add_neighbor(self.location_dict[to], distance)
        self.location_dict[to].add_neighbor(self.location_dict[frm], distance)

    # O(n)
    # Sorts the neighbors of each location
    def sort_locations(self):
        for address in self.location_dict:
            self.location_dict[address].sort_distances()


# The Location Graph handles the functionality and initialization of the Graph
class LocationGraph(Graph):

    def __init__(self, distance_file, location_file):
        Graph.__init__(self)
        self.locations = self.load_locations(location_file)
        self.load_distances(distance_file)
        self.sort_locations()
        self.hub = self.get_location('HUB')

    # O(n)
    # Loads locations in from data file (CSV) - locations.csv
    def load_locations(self, filename):
        loc_name = []
        with open(filename) as f:
            locations = [line.split(',') for line in f]
            for i, x in enumerate(locations):  # print the list items
                location = x[0].strip()
                self.add_location(location)

                loc_name.append(location)
        return loc_name

    # O(n^2)
    # Loads distances in from data file (CSV) - distances.csv
    def load_distances(self, filename):
        with open(filename) as f:
            distances = [line.split(',') for line in f]
            for i, x in enumerate(distances):  # print the list items
                for l, d in enumerate(x):
                    if d.strip() == '0':
                        break
                    self.add_path(self.locations[i].strip(), self.locations[l].strip(), float(d))

    # Access number of locations from graph
    def get_num_locations(self):
        return len(self.locations)

    # O(n)
    # Find furthest neighbor from location
    def furthest_location(self):
        for neighbor in reversed(self.hub.get_neighbors()):
            if neighbor.location.address in self.locations:
                return neighbor.location

    # O(n)
    # Creates territories based for the number of drivers assigned to warehouse or 'Hub'
    def create_territory(self, furthest_loc, territory_size):
        t = [furthest_loc]
        self.locations.remove(furthest_loc.address)
        for neighbor in furthest_loc.get_neighbors():
            if len(t) < territory_size:
                if neighbor.location.address in self.locations and neighbor.location != self.hub:
                    t.append(neighbor.location)
                    self.locations.remove(neighbor.location.address)
        return t

    # O(n)
    # Assigns territories for each driver
    def assign_territories(self, num, territory_size):
        print('Dividing territories for drivers...')
        territories = list()
        # print('Amount of Territories: ' + str(num))
        for territory in range(num):
            territories.append(self.create_territory(self.furthest_location(), territory_size))
            # print(' Territory {}'.format(territory))
            # print('\n'.join(
            #     '   Adding location {} - {}'.format(*k) for k in enumerate(territories[territory - 1])))
        return territories
