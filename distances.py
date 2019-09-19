import graph
import package
import hashtable


def load_locations(filename, g):
    loc_name = []
    with open(filename) as f:
        locations = [line.split(',') for line in f]
        for i, x in enumerate(locations):  # print the list items
            location = x[0].strip()
            g.add_vertex(location)
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
                g.add_edge(locations[i].strip(), locations[l].strip(), float(d))
                print "Distance - {0} = From {1} to {2}".format(d, locations[i], locations[l])


def get_shortest_stop(start, truck):
    shortest = None
    dijkstra_graph = graph.dijkstra(truck, start)
    for t in truck:
        if t is not start:
            target = dijkstra_graph[t.get_id()]
            path = [graph.Stop(target, 0)]
            graph.shortest(target, path)
            total = path[-1].get_total_distance()
            if shortest is None:
                shortest = path[0]
            elif total < shortest.total_distance:
                shortest = path[0]
            for s in reversed(path):
                s.set_total_distance(total - s.get_total_distance())
    print('Shortest route is: ' + str(shortest.total_distance))
    return shortest


if __name__ == '__main__':

    g = graph.Graph()
    locations = load_locations('locations.csv', g)
    load_distances('distance.csv', g, locations)

    warehouse = package.PackageWarehouse()

    print('Graph data:')
    for v in g:
        for w in v.get_connections():
            vid = v.get_id()
            wid = w.get_id()
            print('( %s , %s, %3d)' % (vid, wid, v.get_weight(w)))

    hub = g.get_vertex('HUB')
    truck = [warehouse.packages[0].vertex, warehouse.packages[1].vertex, warehouse.packages[2].vertex, hub]

    route = []
    start = hub
    total_distance = 0
    while len(truck):
        if len(truck) > 1:
            shortest_stop = get_shortest_stop(start, truck)
            total_distance += shortest_stop.total_distance
            truck.remove(start)
            route.append(shortest_stop)
            start = shortest_stop.vertex.vertex
        else:
            truck = []
            last_stop = get_shortest_stop(start, [start, hub])
            total_distance += last_stop.total_distance
            route.append(last_stop)

    print('Total distance for route:', total_distance)
