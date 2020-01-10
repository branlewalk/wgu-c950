from datetime import timedelta
import hashtable


# The Manifest holds onto all the information of the packages that
# will be loaded on the trucks once they are sorted and routed
class Manifest:
    def __init__(self, manifest_id):
        self.manifest_id = manifest_id
        self.packages = list()
        self.truck = 0
        self.driver = 0
        self.is_full = False
        self.route = list()
        self.packages_by_location = hashtable.HashTable()

    # Used to print package information when using various messages
    def __str__(self):
        return '\n'.join(str(package) for package in self.packages)

    # Used for debugging purposes
    def __repr__(self):
        return '\n'.join(str(package) for package in self.route)

    # O(n)
    # When adding multiple packages to the manifest
    def add_packages(self, packages):
        for package in packages:
            self.add_package(package)

    # O(n)
    # Adding a package to the manifest
    def add_package(self, package):
        if package not in self.packages:
            if package.delivery_status == 'At Hub':
                if package.delay != timedelta(hours=8) or package.wrong_address == 'W':
                    package.delivery_status = 'Delayed'
                else:
                    # maybe change name
                    package.delivery_status = 'Loading'
                self.packages.append(package)
            elif package.delivery_status == 'Loading':
                print('{}, already loading...'.format(repr(package)))
            if self.packages_by_location.get(package.location) is None:
                self.packages_by_location.put(package.location, list())
            self.packages_by_location.get(package.location).append(package)
            if len(self.packages) == 16:
                self.is_full = True
        else:
            print('Error adding: ' + str(package) + ', already on Manifest')

    # Remove a package from the manifest
    def remove_package(self, package):
        if package in self.packages:
            package.delivery_status = 'At Hub'
            self.packages.remove(package)
            self.packages_by_location.remove(package.location, package)
            if len(self.packages) == 16:
                self.is_full = False
        else:
            print('Error removing: ' + str(package) + ', not on Manifest')


# The Driver holds onto the time to handle when they would leave an depart from the warehouse or 'Hub'
class Driver:
    def __init__(self, driver_id):
        self.driver_id = driver_id
        self.time = timedelta(hours=8)


# The Manifest List handles all the sorting and routing of each manifest
class ManifestList:

    def __init__(self, num_manifests, warehouse, hub):
        self.num_manifests = num_manifests
        self.manifests = list()
        self.hub = hub
        self.warehouse = warehouse

    # O(n)
    # Adds all packages to manifests from each territory
    # Looks at each manifest to see if it over capacity
    # Removes those packages
    # After manifest are at capacity or 'full', loads remaining packages on to new manifests
    # While adding packages to manifest both the truck and deliver with constraint are handled
    def sort(self, territories):
        print('Sorting packages...')
        num_territories = len(territories)
        # print('Amount of Manifests: ' + str(self.num_manifests))
        for m in range(self.num_manifests):
            manifest = Manifest(m)
            if m < num_territories:
                self.add_packages_to_manifest_from_territory(territories[m], manifest)
            else:
                self.move_non_constraint_packages_to_other_manifest(manifest)
            self.manifests.append(manifest)
            # print(' Manifest {0}:'.format(manifest.manifest_id))
            # print(str(manifest))
        self.assign_truck_ids()

    # O(n)
    # Assigns truck id's to manifest without them
    def assign_truck_ids(self):
        truck_id_list = ['1', '2', '3']
        for manifest in self.manifests:
            if manifest.truck is 0:
                manifest.truck = truck_id_list[0]
                truck_id_list.pop(0)
            else:
                truck_id_list.remove(manifest.truck)

    # O(n^2)
    # Add package to manifest from territory
    def add_packages_to_manifest_from_territory(self, territory, manifest):
        for location in territory:
            packages = self.warehouse.packages_by_location.get(location)
            for package in packages:
                # Handle Truck constraint
                if package.delivery_status == 'At Hub':
                    if manifest.truck == 0 and package.truck != '':
                        manifest.truck = package.truck
                        manifest.add_packages(self.warehouse.packages_by_truck.get(package.truck))
                    # Handle Deliver With constraint
                    elif len(package.deliver_with) > 0:
                        manifest.add_packages(self.warehouse.get_packages_deliver_together(package.deliver_with))
                    # Handle package without constraint
                    else:
                        manifest.add_package(package)

    # O(n^2)
    # Remove packages from manifest over the set truck capacity and add to a new manifest
    def move_non_constraint_packages_to_other_manifest(self, manifest):
        for t_manifest in self.manifests:
            if t_manifest.is_full:
                packages = self.get_non_constraint_packages(t_manifest)
                for package in packages:
                    manifest.add_package(package)

    # O(n^2)
    # Removes packages from an over capacity manifest and adds them to a list
    def get_non_constraint_packages(self, manifest):
        removed_packages = list()
        furthest_locations_from_hub = reversed(self.hub.get_neighbors())
        for package in manifest.packages:
            if manifest.is_full:
                if package.wrong_address is not '':
                    removed_packages.append(package)
                    manifest.remove_package(package)
            else:
                break
        for neighbor in furthest_locations_from_hub:
            if manifest.is_full:
                packages_at_location = manifest.packages_by_location.get(neighbor.location)
                if packages_at_location is not None:
                    for package in packages_at_location:
                        if not package.has_constraint():
                            removed_packages.append(package)
                            manifest.remove_package(package)
        return removed_packages

    # O(n^2)
    # Routes the manifests packages and places them on a new list
    # Looks at three different situations
    # 1) If a package is delayed, 2) has a deadline, or
    # 3) is the closest to the current location
    # It then then look at each candidate to decide where to go to first
    # Once an optimal candidate id chosen it is added to the route
    def route(self):
        print('Routing packages...')
        drivers = [Driver(1), Driver(2)]
        for manifest in self.manifests:
            driver = drivers[0]
            if drivers[0].time > drivers[1].time:
                driver = drivers[1]
            time = driver.time
            # print('Driver is driver {}'.format(driver.driver_id))
            manifest.driver = driver.driver_id
            current_location = self.hub
            # print(' Manifest {0}:'.format(manifest.manifest_id))
            while len(manifest.route) < len(manifest.packages):
                # 'wrong address' scenario
                if time >= timedelta(hours=10, minutes=40):
                    package = self.warehouse.packages_by_id.get(9)
                    package.delivery_status = 'Loaded'
                    package.location = self.warehouse.g.get_location('410 S State St')

                delayed = self.find_soonest_delayed_time(current_location, manifest)
                closest = self.find_closest_from_package(current_location, manifest)
                soonest = self.find_soonest_delivery_time(current_location, manifest)

                package_delivery = self.schedule_best_package(delayed, soonest, closest, time, current_location,
                                                              manifest)

                current_location = package_delivery.package.location
                time = package_delivery.package.estimated_delivery_time
            to_hub = package_delivery.package.location.neighbors_by_location.get(self.hub)
            time = time + timedelta(hours=to_hub.distance/18)
            driver.time = time
            # Switch drivers
            drivers.append(driver)
            if drivers[0]:
                drivers.pop(0)
            elif drivers[1]:
                driver.pop(1)

    # O(n^2)
    # Looks for the package with the soonest deadline and returns it as a candidate
    def find_soonest_delivery_time(self, starting_point, manifest):
        neighbors = starting_point.get_neighbors()
        soonest_hours_to = timedelta(hours=23.99)
        soonest_package = None
        soonest = timedelta(hours=17)
        soonest_miles = 0
        for neighbor in neighbors:
            packages = manifest.packages_by_location.get(neighbor.location)
            if packages is not None:
                for package in packages:
                    if package not in manifest.route:
                        if package.deadline < soonest:
                            soonest_package = package
                            soonest_hours_to = neighbor.get_hours_to()
                            soonest = package.deadline
                            soonest_miles = neighbor.distance
        return PackageDelivery(soonest_package, soonest_hours_to, soonest_miles)

    # O(n^2)
    # Looks for the package that is the closest to the current location and returns it as a candidate
    def find_closest_from_package(self, current_location, manifest):
        current_location_packages = manifest.packages_by_location.get(current_location)
        if current_location_packages is not None:
            for package in current_location_packages:
                if package not in manifest.route and package.delivery_status is not 'Delayed' and package in manifest.packages:
                    return PackageDelivery(package, timedelta(hours=0), 0)
        closest_locations_to_package = current_location.get_neighbors()
        for neighbor in closest_locations_to_package:
            for pac in manifest.packages:
                if pac not in manifest.route and pac.location is neighbor.location:
                    if pac.delivery_status is not 'Delayed':
                        return PackageDelivery(pac, neighbor.get_hours_to(), neighbor.distance)
                    else:
                        continue

    # O(n^2)
    # Looks for a package that is delayed and returns it as a candidate
    def find_soonest_delayed_time(self, starting_point, manifest):
        neighbors = starting_point.get_neighbors()
        delayed_hours_to = timedelta(hours=23.99)
        delayed_package = None
        delayed = timedelta(hours=17)
        delayed_miles = 0
        for neighbor in neighbors:
            packages = manifest.packages_by_location.get(neighbor.location)
            if packages is not None:
                for package in packages:
                    if package not in manifest.route:
                        if package.delay < delayed and package.delay != timedelta(
                                hours=8) and package.delivery_status is 'Delayed':
                            delayed_package = package
                            delayed_hours_to = neighbor.get_hours_to()
                            delayed = package.delay
                            delayed_miles = neighbor.distance
        return PackageDelivery(delayed_package, delayed_hours_to, delayed_miles)

    # O(1) + O(n) + 0(1)
    # Choose which candidate will be delivered by first checking oif the deadline will be met
    # second, if the package has a delay, and third if the the other 2 criteria are not met it will
    # choose the closest package
    def schedule_best_package(self, delayed, soonest, closest, time, current_location, manifest):
        if soonest.package is not None and closest is not None and soonest.package is not closest.package:
            more_time = self.find_time_between(closest.package.location, soonest.package.location)
            total_time = time + closest.hours_to + more_time
            if total_time > soonest.package.deadline:
                return self.schedule_package_delivery(soonest, time, timedelta(0), manifest, 'Soonest')
        if delayed.package is not None and closest is not None:
            time_back = self.find_time_between(self.hub, delayed.package.location)
            if time + closest.hours_to > delayed.package.delay:
                time_to_hub = self.find_time_between(current_location, self.hub)
                for package in manifest.packages:
                    if package.delivery_status is 'Delayed' and package.delay == delayed.package.delay:
                        package.delivery_status = 'Loaded'
                return self.schedule_package_delivery(delayed, time, time_to_hub + time_back, manifest, 'Delayed')
        if closest is not None and closest.package is not None:
            return self.schedule_package_delivery(closest, time, timedelta(0), manifest, 'Closest')

    # O(1)
    # Schedules the package, giving it a delivery time
    def schedule_package_delivery(self, package_delivery, time, additional_time, manifest, type):
        package_delivery.type = type
        manifest.route.append(package_delivery.package)
        package_delivery.package.estimated_delivery_time = time + additional_time + package_delivery.hours_to
        package_delivery.package.hours_to = package_delivery.hours_to + additional_time
        package_delivery.package.miles_to = float(package_delivery.package.hours_to.seconds / 60) / 60 * 18
        # print(' Added {}'.format(repr(package_delivery)))
        return package_delivery

    # O(n)
    # Finds the time it take to travel between locations
    def find_time_between(self, other_location, soonest_location):
        if other_location is soonest_location:
            return timedelta(hours=0)
        neighbors = other_location.get_neighbors()
        for neighbor in neighbors:
            if neighbor.location is soonest_location:
                return neighbor.get_hours_to()


# The Package Delivery acts as a candidate for a package to be delivered.
class PackageDelivery:
    def __init__(self, package, hours_to, miles_to):
        self.package = package
        self.hours_to = hours_to
        self.miles_to = miles_to
        self.type = ''

    def __repr__(self):
        return '   Type {}, {}, Hours to {}'.format(self.type, repr(self.package), self.hours_to)
