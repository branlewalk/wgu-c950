from map import Map, Destination, vantage, shortest
import package
import hashtable


def load_locations(filename, g):
    loc_name = []
    with open(filename) as f:
        locations = [line.split(',') for line in f]
        for i, x in enumerate(locations):  # print the list items
            location = x[0].strip()
            g.add_location(location)
            print "Location - {0} = {1}".format(i, location)
            loc_name.append(location)
    return loc_name


def load_distances(filename, g, locations):
    with open(filename) as f:
        distances = [line.split(',') for line in f]
        for i, x in enumerate(distances):  # print the list items
            for l, d in enumerate(x):
                if d.strip() == '0':
                    break
                g.add_trace(locations[i].strip(), locations[l].strip(), float(d))
                print "Distance - {0} = From {1} to {2}".format(d, locations[i], locations[l])


def get_shortest_destination(start, truck):
    shortest_route = None
    vantaged_map = vantage(truck, start)
    for t in truck:
        if t is not start:
            target = vantaged_map[t.get_address()]
            path = [Destination(target, 0)]
            shortest(target, path)
            total = path[-1].get_total_distance()
            if shortest_route is None:
                shortest_route = path[0]
            elif total < shortest_route.total_distance:
                shortest_route = path[0]
            for s in reversed(path):
                s.set_total_distance(total - s.get_total_distance())
    print('Shortest route is: ' + str(shortest_route.total_distance))
    return shortest_route


if __name__ == '__main__':

    del_map = Map()
    locations = load_locations('locations.csv', del_map)
    load_distances('distance.csv', del_map, locations)

    warehouse = package.PackageWarehouse(del_map)

    print('Graph data:')
    for floc in del_map:
        for tloc in floc.get_connections():
            floc_id = floc.get_address()
            tloc_id = tloc.get_address()
            print('( %s , %s, %3d)' % (floc_id, tloc_id, floc.get_weight(tloc)))

    hub = del_map.get_location('HUB')
    truck = [warehouse.packages[0].vertex, warehouse.packages[1].vertex, warehouse.packages[2].vertex, hub]

    route = []
    start = hub
    total_distance = 0
    while len(truck):
        if len(truck) > 1:
            shortest_stop = get_shortest_destination(start, truck)
            total_distance += shortest_stop.total_distance
            truck.remove(start)
            route.append(shortest_stop)
            start = shortest_stop.location.location
        else:
            truck = []
            last_stop = get_shortest_destination(start, [start, hub])
            total_distance += last_stop.total_distance
            route.append(last_stop)

    print('Total distance for route:', total_distance)
