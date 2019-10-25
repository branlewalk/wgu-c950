from graph import Graph, Destination, shortest
import package
import hashtable
from manifest import Manifest

global warehouse
global load_list


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
                g.add_path(locations[i].strip(), locations[l].strip(), float(d))
                # print "Distance - {0} = From {1} to {2}".format(d, locations[i], locations[l])


# def get_shortest_destination(start, truck):
#     shortest_route = None
#     vantaged_map = vantage(truck, start)
#     for t in truck:
#         if t is not start:
#             target = vantaged_map[t.get_address()]
#             path = [Destination(target, 0)]
#             shortest(target, path)
#             total = path[-1].get_total_distance()
#             if shortest_route is None:
#                 shortest_route = path[0]
#             elif total < shortest_route.total_distance:
#                 shortest_route = path[0]
#             for s in reversed(path):
#                 s.set_total_distance(total - s.get_total_distance())
#     print('Shortest route is: ' + str(shortest_route.total_distance))
#     return shortest_route


def find_furthest_package(starting_location):
    for neighbor in reversed(starting_location.get_neighbors()):
        package = warehouse.package_by_location.get(neighbor.location)
        if package is not None:
            print('Found furthest package: ' + str(package))

            return package
    return None


# not correct yet
def find_closest_package(starting_location):
    for neighbor in (starting_location.get_neighbors()):
        package = warehouse.package_by_location.get(neighbor.location)
        if package is not None:
            print('Found furthest package: ' + str(package))

            return package
    return None


def add_packages_with_same_truck():
    for package in warehouse.packages:
        if package.get_truck() is furthest.get_truck():
            if package.location in load_list:
                manifest.add_package(package)
                load_list.remove(package.location)


# not correct yet
def add_packages_with_same_address(manifest):
    for package in manifest.get_packages():
        packages = warehouse.package_by_address.get_bucket(package.location)
        for p in packages:
            if p in warehouse.packages:
                if p.location in load_list:
                    manifest.add_package(p)
                    load_list.remove(p.location)
                    add_packages_with_same_address(manifest)


if __name__ == '__main__':

    del_map = Graph()
    locations = load_locations('locations.csv', del_map)
    load_distances('distance.csv', del_map, locations)
    del_map.sort_locations()

    drivers = 2
    truck_capacity = 16
    warehouse = package.PackageWarehouse(del_map)
    load_list = list(warehouse.package_by_location.keys)
    hub = warehouse.g.get_location('HUB')

    # Divide warehouse by truck capacity to discover how many manifests are needed
    manifest_count = len(warehouse.packages)/truck_capacity + (1 if (len(warehouse.packages) % truck_capacity) > 0 else 0)
    print('Amount of Manifest: ' + str(manifest_count))

    # Look for furthest points based on drive quantity
    furthest = find_furthest_package(hub)
    load_list.remove(furthest.location)

    # Build manifest around 1st furthest point
    manifest = Manifest()
    manifest.add_package(furthest)
    if furthest.get_truck() is not None:
        manifest.set_truck(furthest.get_truck())
        add_packages_with_same_truck()
        add_packages_with_same_address(manifest)

    print(str(manifest))
    print('\n'.join(str(p) for p in load_list))
    # - Go through constraints
    #   * Truck constraint

    #   * Deliver with const
    #   * Deadline const
    #   * Delay const
    # - Add locations closest to furthest point until truck capacity is met
    # - If all constraint based packages are spoken for, start adding non const packages
    # - Start new manifest

    # Sort manifests by distance (I think quick sort does this)
    # Load trucks
    # Start Delivering

    # hub = del_map.get_location('HUB')
    # manifest = [warehouse.packages[0].location, warehouse.packages[1].location, warehouse.packages[2].location]
    # for neighbor in reversed(hub.get_neighbors()):
    #     if neighbor.location in manifest:
    #         print('Found furthest: ' + str(neighbor))
    #         break

    # distribute packages by truck -> deliver with -> deadlines -> wrong address
    packages_for_truck = warehouse.get_packages_by_truck('2')
    packages_deliver_together = warehouse.get_packages_deliver_together()
    packages_by_deadline = warehouse.get_packages_with_deadline()
    packages_by_delay = warehouse.get_packages_with_delay()

    # print('Package by Truck: ')
    # for p in packages_for_truck:
    #     print('  {0}'.format(p))
    #
    # print('Package(s) to be Delivered Together: ')
    # for p in packages_deliver_together:
    #     print(' New together list: ')
    #     for d in p:
    #         print('  {0}'.format(d))
    #
    # print('Packages by Deadline:')
    # for k in packages_by_deadline:
    #     print(' {0}'.format(k))
    #     for p in packages_by_deadline[k]:
    #         print('  {0}'.format(p))
    #
    # print('Packages by Delay:')
    # for k in packages_by_delay:
    #     print(' {0}'.format(k))
    #     for p in packages_by_delay[k]:
    #         print('  {0}'.format(p))

    # print('Graph data:')
    # for floc in del_map:
    #     for tloc in floc.get_connections():
    #         floc_id = floc.get_address()
    #         tloc_id = tloc.get_address()
    #         print('( %s , %s, %3d)' % (floc_id, tloc_id, floc.get_weight(tloc)))
    # route = []
    # start = hub
    # total_distance = 0
    # while len(truck):
    #     if len(truck) > 1:
    #         shortest_stop = get_shortest_destination(start, truck)
    #         total_distance += shortest_stop.total_distance
    #         truck.remove(start)
    #         route.append(shortest_stop)
    #         start = shortest_stop.location.location
    #     else:
    #         truck = []
    #         last_stop = get_shortest_destination(start, [start, hub])
    #         total_distance += last_stop.total_distance
    #         route.append(last_stop)
    #
    # print('Total distance for route:', total_distance)
    # manifest - the packages on one truck
