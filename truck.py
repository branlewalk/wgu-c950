from datetime import timedelta


# Truck class handles all package and route calculations
class Truck:
    def __init__(self, manifest, hub):
        self.truck_id = manifest.truck
        self.driver = manifest.driver
        self.route = manifest.route
        self.hub = hub
        self.miles_to_travel = self.set_miles_to_travel(self.route)
        self.time_to_travel = self.set_time_to_travel(self.route)
        self.total_weight = self.set_total_weight(self.route)

    # Calculate total miles for route
    def set_miles_to_travel(self, route):
        miles = 0
        for package in route:
            if package is route[-1]:
                neighbor = package.location.neighbors_by_location.get(self.hub)
                miles = miles + package.miles_to + neighbor.distance
            else:
                miles = miles + package.miles_to
        return miles

    # Calculate total time traveled during route
    def set_time_to_travel(self, route):
        total_time = timedelta(hours=0)
        for package in route:
            if package is route[-1]:
                neighbor = package.location.neighbors_by_location.get(self.hub)
                total_time = total_time + package.hours_to + neighbor.get_hours_to()
            else:
                total_time = total_time + package.hours_to
        return total_time

    # Calculate total weight of packages on truck
    def set_total_weight(self, route):
        total_weight = 0
        for package in route:
            total_weight = total_weight + package.package_weight
        return total_weight

    # Checks to see if all packages were delivered before their deadline
    def verify_on_time_delivery(self):
        late_package = 0
        for package in self.route:
            if package.estimated_delivery_time > package.deadline:
                print('Package {} did not meet deadline'.format(str(package)))
        if late_package == 0:
            print('All packages on Truck {} were delivered on time.'.format(self.truck_id))

