import hashtable


class Package:
    def __init__(self, package_id, location, deadline, constraint):
        self.package_id = package_id
        self.location = location
        self.deadline = deadline
        self.constraint = constraint

    def get_address(self):
        return self.location.get_address()

    def get_package_id(self):
        return self.package_id

    def get_deadline(self):
        return self.deadline

    def get_city(self):
        return

    def get_zip_code(self):
        return

    def get_package_weight(self):
        return

    def get_delivery_status(self):
        return


def load_packages(filename, map):
    with open(filename) as f:
        pac_list = []
        packages = [line.split(',') for line in f]
        for i, x in enumerate(packages):  # print the list items
            address = x[1].strip()
            package = Package(x[0].strip(), map.get_location(address), x[5].strip(), x[7].strip())
            pac_list.append(package)
            print "Package - {0} = Delivers to {1} by {2} with note {3}".format(package.package_id, package.vertex.get_address(),
                                                                                package.time, package.constraint)
        return pac_list


if __name__ == '__main__':
    locations = load_packages('package.csv')


class PackageWarehouse:

    def __init__(self, g):
        self.g = g
        self.packages = load_packages('package.csv', g)

        self.package_by_address = hashtable.HashTable()
        for p in self.packages:
            self.package_by_address.put(p.location.get_address(), p)