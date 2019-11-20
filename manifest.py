from package import Package


class Manifest:
    def __init__(self, manifest_id):
        self.manifest_id = manifest_id
        self.packages = []
        self.truck = 0
        self.driver = 0
        self.is_full = False
        self.delivery = []

    def __str__(self):
        return '\n'.join(str(package) for package in self.packages)

    def __repr__(self):
        return '\n'.join(str(package) for package in self.delivery)

    def set_driver(self, driver):
        self.driver = driver

    def get_driver(self):
        return self.driver

    def set_truck(self, truck):
        self.truck = truck

    def get_truck(self):
        return self.truck

    def add_package(self, package):
        if package not in self.packages:
            self.packages.append(package)
            if len(self.packages) == 16:
                self.is_full = True
        else:
            print('Error adding: ' + str(package) + ', already on Manifest')

    def remove_package(self, package):
        if package in self.packages:
            self.packages.remove(package)
            if len(self.packages) == 16:
                self.is_full = False
        else:
            print('Error removing: ' + str(package) + ', not on Manifest')

    def get_packages(self):
        return self.packages

