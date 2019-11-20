from datetime import datetime, timedelta

import package
from distances import load_locations, load_distances
from graph import Graph
from manifest import Manifest

global hub
global locations
global load_list


def furthest_location():
    for neighbor in reversed(hub.get_neighbors()):
        if neighbor.location.address in locations:
            return neighbor.location


def create_territory(furthest_loc):
    t = [furthest_loc]
    locations.remove(furthest_loc.address)
    for neighbor in furthest_loc.get_neighbors():
        if len(t) < territory_size:
            if neighbor.location.address in locations and neighbor.location != hub:
                t.append(neighbor.location)
                locations.remove(neighbor.location.address)
    return t


def add_package_to_manifest_by_territory(territory, manifest):
    for location in territory:
        packages = warehouse.packages_by_location.get(location)
        for package in packages:
            manifest.add_package(package)


def get_non_constraint_packages(manifest):
    removed_packages = []
    nearest_locations_to_hub = reversed(hub.get_neighbors())
    for neighbor in nearest_locations_to_hub:
        if manifest.is_full:
            for package in manifest.packages:
                if package.location is neighbor.location:
                    non_constraint_packages = warehouse.packages_by_no_constraint.get(package.package_id)
                    if non_constraint_packages is not None:
                        if package in non_constraint_packages:
                            removed_packages.append(package)
                            manifest.remove_package(package)
    return removed_packages


def find_furthest_from_hub(manifest):
    furthest_locations_to_hub = reversed(hub.get_neighbors())
    for neighbor in furthest_locations_to_hub:
        for package in manifest.packages:
            if package not in manifest.delivery:
                return package, neighbor.get_hours_to()


def find_soonest_delivery_time(starting_point, manifest):
    neighbors = starting_point.get_neighbors()
    soonest_hours_to = timedelta(hours=23.99)
    soonest_package = None
    soonest = timedelta(hours=17)
    for neighbor in neighbors:
        for package in manifest.packages:
            if package not in manifest.delivery:
                if package.location == neighbor.location:
                        if package.deadline < soonest:
                            soonest = package.deadline
                            soonest_package = package
                            soonest_hours_to = neighbor.get_hours_to()
    return soonest_package, soonest, soonest_hours_to


def find_closest_from_package(current_location, manifest):
    closest_locations_to_package = current_location.get_neighbors()
    for neighbor in closest_locations_to_package:
        for package in manifest.packages:
            if package not in manifest.delivery:
                return package, neighbor.get_hours_to()


def schedule_package_delivery(package, time, hours_to):
    manifest.delivery.append(package)
    package.estimated_delivery_time = time + hours_to
    print(' Added {}'.format(repr(package)))
    return package


def schedule_best_package(soonest_package, soonest_hours_to, other_package, other_hours_to):
    if soonest_package is not None and total_time > soonest:
        return schedule_package_delivery(soonest_package, time, soonest_hours_to)
    elif other_package is not None:
        return schedule_package_delivery(other_package, time, other_hours_to)


if __name__ == '__main__':
    del_map = Graph()
    locations = load_locations('locations.csv', del_map)
    load_distances('distance.csv', del_map, locations)
    warehouse = package.PackageWarehouse(del_map)
    hub = warehouse.g.get_location('HUB')
    del_map.sort_locations()
    load_list = list(warehouse.packages_by_id.keys)

    drivers = 2
    truck_capacity = 16
    num_locations = len(locations)
    num_packages = len(warehouse.packages)
    num_manifests = int(num_packages / truck_capacity) + (num_packages % truck_capacity > 0)
    num_territories = drivers
    territory_size = (num_locations - 1) / drivers
    manifest_list = []
    territory_list = []
    time = timedelta(hours=8)

    print('Amount of Territories: ' + str(num_territories))
    for territory in range(num_territories):
        territory_list.append(create_territory(furthest_location()))
        print(' Territory {}'.format(len(territory_list)))
        print('\n'.join(
            '   Adding location {} - {}'.format(*k) for k in enumerate(territory_list[len(territory_list) - 1])))

    print('Amount of Manifests: ' + str(num_manifests))
    # Add packages to drivers territory

    # TODO Add Truck and Deliver with Constraint
    #  assign drivers and trucks to manifest
    for m in range(num_manifests):
        manifest = Manifest(len(manifest_list) + 1)
        if m < num_territories:
            add_package_to_manifest_by_territory(territory_list[len(manifest_list)], manifest)
        if m >= num_territories:
            for t_manifest in manifest_list:
                if t_manifest.is_full:
                    packages = get_non_constraint_packages(t_manifest)
                    for package in packages:
                        manifest.add_package(package)
        # manifest.packages.sort()
        manifest_list.append(manifest)
        print(' Manifest {0}:'.format(manifest.manifest_id))
        print(str(manifest))

    cycle = 1
    # Find Furthest package in manifest
    for manifest in manifest_list:
        print(' Manifest {0}:'.format(manifest.manifest_id))
        if cycle < 3:
            time = timedelta(hours=8)
        furthest_package, furthest_hours_to = find_furthest_from_hub(manifest)
        soonest_package, soonest, soonest_hours_to = find_soonest_delivery_time(furthest_package.location, manifest)
        total_time = time + furthest_hours_to + soonest_hours_to
        current_package = schedule_best_package(soonest_package, soonest_hours_to, furthest_package, furthest_hours_to)
        time = current_package.estimated_delivery_time
        while len(manifest.delivery) < len(manifest.packages):
            closest_package, closest_hours_to = find_closest_from_package(current_package.location, manifest)
            soonest_package, soonest, soonest_hours_to = find_soonest_delivery_time(closest_package.location, manifest)
            current_package = schedule_best_package(soonest_package, soonest_hours_to, closest_package, closest_hours_to)
            time = current_package.estimated_delivery_time

        cycle = cycle + 1



    for manifest in manifest_list:
        print('Manifest {0}:'.format(manifest.manifest_id))
        for package in manifest.delivery:
            print(' Delivered: {}'.format(repr(package)))

    # G.  Provide an interface for the insert and look-up functions to view the status of any package at any time.
    # This function should return all information about each package, including delivery status.
    # 1.  Provide screenshots to show package status of all packages at a time between 8:35 a.m. and 9:25 a.m.
    # 2.  Provide screenshots to show package status of all packages at a time between 9:35 a.m. and 10:25 a.m.
    # 3.  Provide screenshots to show package status of all packages at a time between 12:03 p.m. and 1:12 p.m.
