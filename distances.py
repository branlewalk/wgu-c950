from graph import Graph, Destination, vantage, shortest
import package
import hashtable


def load_locations(filename, g):
    loc_name = []
    with open(filename) as f:
        locations = [line.split(',') for line in f]
        for i, x in enumerate(locations):  # print the list items
            location = x[0].strip()
            g.add_location(location)
            # print "Location - {0} = {1}".format(i, location)
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
                # print "Distance - {0} = From {1} to {2}".format(d, locations[i], locations[l])


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

    del_map = Graph()
    locations = load_locations('locations.csv', del_map)
    load_distances('distance.csv', del_map, locations)

    warehouse = package.PackageWarehouse(del_map)

    # distribute packages by truck -> deliver with -> deadlines -> wrong address
    packages_for_truck = warehouse.get_packages_by_truck('2')
    packages_deliver_together = warehouse.get_packages_deliver_together()
    packages_by_deadline = warehouse.get_packages_with_deadline()
    packages_by_delay = warehouse.get_packages_with_delay()

    print('Package by Truck: ')
    for p in packages_for_truck:
        print('  {0}'.format(p))

    print('Package(s) to be Delivered Together: ')
    for p in packages_deliver_together:
        print(' New together list: ')
        for d in p:
            print('  {0}'.format(d))

    print('Packages by Deadline:')
    for k in packages_by_deadline:
        print(' {0}'.format(k))
        for p in packages_by_deadline[k]:
            print('  {0}'.format(p))

    print('Packages by Delay:')
    for k in packages_by_delay:
        print(' {0}'.format(k))
        for p in packages_by_delay[k]:
            print('  {0}'.format(p))

    # print('Graph data:')
    # for floc in del_map:
    #     for tloc in floc.get_connections():
    #         floc_id = floc.get_address()
    #         tloc_id = tloc.get_address()
    #         print('( %s , %s, %3d)' % (floc_id, tloc_id, floc.get_weight(tloc)))

    hub = del_map.get_location('HUB')
    truck = [warehouse.packages[0].location, warehouse.packages[1].location, warehouse.packages[2].location, hub]

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

    #manifest - the packages on one truck